# Muon Telescope Electronics Review

**Audience:** A scientist with prior introductory electronics and strong electromagnetism background  
**Purpose:** Explain the electronic design, why each circuit block exists, where signal and power flow, and how noise and loss constrain the PCB  
**Companion design:** `01_design_spec.md`  
**Revision:** 1.0, 2026-08-22

---

## 1. The central idea

A particle crossing the scintillator creates a faint optical signal. That light does not directly power the output pulse. Instead, it triggers avalanche cells in the SiPM, allowing energy stored by the bias supply to appear as an electrical pulse. The optical event carries the information; the power supply provides most of the electrical energy.

The instrument therefore has two overlapping systems:

| System | Path | Purpose |
|---|---|---|
| Information path | muon -> scintillation light -> SiPM charge pulse -> voltage pulse -> comparator edge -> FPGA event | Preserve whether and when a plausible particle crossing occurred |
| Power path | 5 V input -> protected rails -> amplifier, comparator, and 27-29 V SiPM bias | Supply energy while disturbing the information path as little as possible |

The design challenge is not simply to obtain gain. It is to keep switching current, rail noise, electromagnetic pickup, and digital return current from becoming indistinguishable from a real SiPM pulse.

Each detector head implements:

```text
SiPM -> 49.9 ohm current-to-voltage conversion
     -> AC coupling and 50 mV baseline
     -> TPH2502 amplifier, gain about 13.4
     -> TLV3502 threshold comparator
     -> 0-3.3 V digital trigger
```

Two trigger signals go to the Cora Z7 FPGA. The FPGA requires a near-simultaneous event in both scintillators, strongly rejecting dark counts and local disturbances that affect only one sensor.

---

## 2. From light to charge: the SiPM

### 2.1 Physical model

The onsemi MICROFC-60035-SMT-TR is a 6 mm x 6 mm silicon photomultiplier containing 18,980 microcells. Each microcell is an avalanche photodiode operated above breakdown with its own quench resistor.

A photon can initiate a self-sustaining avalanche. The quench resistor reduces current until the junction drops below breakdown, stopping the avalanche and allowing the cell to recharge. One fired cell produces an approximately quantized charge packet. Many fired cells add at the common terminals.

At 2.5 V overvoltage, the datasheet gives a typical gain near 3 million. The electrical pulse is therefore not the original photoelectron current multiplied by a linear resistor network. It is the collective discharge and recharge of many biased avalanche cells.

### 2.2 Breakdown and overvoltage

The device breakdown voltage is approximately 24.2-24.7 V. The meaningful control variable is:

```text
overvoltage = applied bias - breakdown voltage
```

Increasing overvoltage increases avalanche charge, photon-detection efficiency, and pulse amplitude. It also increases dark-count rate, optical crosstalk, afterpulsing, and sensitivity to temperature. The revision A bias range of approximately 27.0-28.9 V covers useful operation without treating 30 V as an automatically desirable target.

Breakdown voltage changes by about 21.5 mV per degree C. A fixed bias therefore produces a temperature-dependent overvoltage. For initial counting experiments this is handled by recording temperature and recalibrating threshold or bias. A later design could compensate bias electronically.

### 2.3 The sensor is also a large capacitor

The standard anode-cathode capacitance is about 3.4 nF. This matters because a fast current pulse must charge and discharge that capacitance through the sensor, sense resistor, traces, and amplifier input.

The dedicated fast output is only about 48 pF, but revision A leaves it floating. The standard output is simpler, produces a useful charge signal, and is adequate for a roughly 100 ns coincidence measurement. Using the fast output would require a more explicitly RF-like front end and does not materially improve the first scientific goal.

The SiPM datasheet lists a microcell recharge time constant near 95 ns. As a crude lumped comparison:

```text
49.9 ohm x 3.4 nF = 170 ns
```

The actual pulse is not a single RC exponential because the microcell quench network, avalanche current, coupling capacitor, and amplifier impedance all participate. The estimate simply explains why the standard output is much slower than the nanosecond fast output.

### 2.4 Intrinsic detector noise

Even in complete darkness, thermally generated carriers trigger avalanches. The 6 mm device has a typical dark-count rate in the megahertz range at 2.5 V overvoltage. Most dark pulses are small, but crosstalk can make one avalanche trigger neighbors, and trapped charge can create afterpulses.

This intrinsic pulse noise is usually more important than ordinary resistor noise. The threshold rejects many small dark events; coincidence rejects the much larger set of dark events that occur in only one detector.

---

## 3. The 49.9 ohm sense resistor

The standard SiPM output is a current pulse. The sense resistor converts it into voltage:

```text
Vraw(t) = Isipm(t) x 49.9 ohm
```

A 200 microamp instantaneous current would produce approximately 10 mV. The pulse is then amplified before thresholding.

The resistor value is a tradeoff:

| Larger resistance | Smaller resistance |
|---|---|
| Larger voltage for a given current | Smaller voltage |
| Easier discrimination | Faster discharge and recovery |
| Larger RC time constant with sensor capacitance | Smaller RC time constant |
| More Johnson voltage noise | Less Johnson voltage noise |

onsemi commonly uses a smaller value when recovery time is the priority. The 49.9 ohm value follows the low-rate CosmicWatch style: cosmic events are rare, so improved voltage amplitude is more valuable than maximizing count-rate capability.

The resistor must be physically beside the SiPM anode. Trace inductance is not merely an abstract parasitic. The voltage across a stray inductance is:

```text
V = L x dI/dt
```

A large current slew through a long loop can therefore create a voltage comparable to the pulse being measured.

---

## 4. Bias generation: the MAX5026 boost converter

### 4.1 Why a boost converter

The system receives 5 V, while the SiPM requires approximately 27-29 V at very low average current. A linear regulator cannot create a voltage above its input. A boost converter transfers energy through an inductor to generate the higher rail.

During the switch-on interval, current and magnetic energy build in the 47 uH inductor:

```text
Einductor = (1/2) L I^2
```

When the internal switch opens, the inductor voltage reverses as required to continue current. That current flows through the Schottky diode into the output capacitors. Repetition at roughly 500 kHz raises the capacitor voltage until the feedback pin reaches its reference.

The MAX5026 is appropriate because it is an adjustable, current-mode boost controller designed for low-current outputs up to 36 V. Its maximum output power is only about 120 mW, but the SiPM bias load is tiny. A high-current converter would be unnecessary and potentially noisier.

### 4.2 Feedback

The output is set by a resistive divider:

```text
Vout = 1.25 V x (1 + Rtop/Rbottom)
```

Revision A uses 147 kohm above 6.65 kohm plus a 500 ohm trimmer, giving a typical adjustment of approximately 27.0-28.9 V.

Feedback is a control measurement, so the FB node is sensitive. If the switching node capacitively couples into FB, the controller reacts to an error it created itself. Keeping FB physically quiet is as important as selecting the right resistor values.

### 4.3 Where converter power is lost

An ideal converter conserves energy. The real converter loses power through:

- Inductor winding resistance and magnetic core loss.
- Internal switch on-resistance and switching transitions.
- Schottky forward voltage and leakage.
- Capacitor ESR and dielectric loss.
- Quiescent current in the controller and feedback divider.

These losses mainly affect efficiency and ripple, not event amplitude directly. They become signal problems when switching ripple reaches the SiPM bias, analog ground, or amplifier supply.

### 4.4 Why several capacitors and resistors appear around the bias rail

The output capacitors store energy over switching cycles. A following 100 ohm resistor and 1 uF capacitor form an approximate low-pass filter:

```text
fc = 1 / (2 pi x 100 ohm x 1 uF) = 1.6 kHz
```

The 10 nF capacitor has less stored charge but lower high-frequency impedance and parasitic inductance. It handles the fast edge content that a large ceramic capacitor may not suppress effectively.

The head repeats local decoupling beside the SiPM. During an avalanche, the nearby capacitor supplies transient current through a small loop. Without it, pulse current must travel through the cable and converter network, temporarily changing the bias. Since SiPM gain depends on overvoltage, bias motion becomes gain modulation.

---

## 5. Input coupling and the 50 mV baseline

The raw node is AC-coupled through 100 nF into an amplifier input biased to VBASE through 499 ohm. This performs two jobs.

First, the capacitor prevents the SiPM's DC bias conditions from setting the amplifier operating point. Second, VBASE places the quiescent signal around 50 mV instead of exactly at the negative supply rail.

The approximate high-pass corner is:

```text
fc approximately 1 / (2 pi x 499 ohm x 100 nF)
   approximately 3.2 kHz
```

The pulse spectrum lies far above this corner, so the useful fast component passes. Slow baseline drift and DC offsets are rejected. The cost is a small undershoot or baseline-recovery tail after a pulse, an unavoidable consequence of AC coupling.

VBASE comes from a 130 kohm / 2.00 kohm divider on 3.3 V:

```text
3.3 V x 2.00 / (130 + 2.00) = 50 mV
```

The second TPH2502 channel buffers this divider. A voltage divider alone has finite Thevenin impedance and would move when loaded by several resistors and dynamic input currents. The voltage follower supplies current while preserving the reference voltage.

This reference should be quiet because noise on VBASE is effectively added to the signal. It is local to each head so one detector cannot modulate the other's analog baseline through a shared high-impedance node.

---

## 6. The TPH2502 amplifier

### 6.1 Negative feedback and gain

Channel A is a non-inverting amplifier referenced to VBASE. Negative feedback drives the inverting input toward the non-inverting input. The closed-loop signal gain is:

```text
gain = 1 + 12.4 kohm / 1.00 kohm = 13.4
```

A 5 mV raw excursion becomes approximately 67 mV above the 50 mV baseline. This gives the comparator a comfortable signal without requiring the amplifier to approach the 5 V rail.

### 6.2 Why this amplifier

The TPH2502 is a dual, rail-to-rail input/output amplifier that operates from 5 V. Its typical gain-bandwidth product is about 120 MHz and its slew rate about 200 V/us. The wide bandwidth preserves pulse shape, and the dual package supplies both the gain stage and VBASE buffer.

For a simple single-pole estimate, the closed-loop bandwidth is:

```text
120 MHz / 13.4 approximately 9 MHz
```

The real response depends on source impedance, sensor capacitance, noise gain, package parasitics, and load. The estimate shows the design intent: preserve a pulse on the scale of tens to hundreds of nanoseconds, not its fastest sub-nanosecond structure.

### 6.3 Stability and parasitic feedback

An op-amp does not distinguish the intended feedback path from capacitance and inductance created by the board. A long output-to-inverting-input loop adds phase shift. Once total loop phase approaches 180 degrees while loop gain remains above unity, negative feedback becomes positive and the amplifier can ring or oscillate.

This is why feedback geometry matters more than ordinary DC trace resistance. The two feedback resistors should form a compact loop at the pins. An optional small C0G capacitor across the 12.4 kohm resistor can reduce high-frequency gain if measurement shows ringing, but it should not be populated blindly.

### 6.4 Amplifier noise

The TPH2502 input-voltage noise is typically about 6.5 nV/sqrt(Hz) at 1 kHz. A deliberately crude white-noise estimate over 9 MHz gives:

```text
6.5 nV/sqrt(Hz) x sqrt(9 MHz) approximately 20 uV RMS input-referred
20 uV x 13.4 approximately 0.27 mV RMS at the output
```

This is not a full noise analysis: the spectrum is not perfectly white, the transfer function is not a brick-wall filter, and the SiPM impedance is frequency dependent. It does show scale. With an initial threshold 50 mV above baseline, ordinary op-amp noise should be much smaller than the decision margin. Real SiPM dark pulses and electromagnetic coupling are more likely false-trigger mechanisms.

---

## 7. The TLV3502 comparator

### 7.1 From analog amplitude to a digital event

The comparator computes a one-bit nonlinear measurement:

```text
TRIG = HIGH if AMP_OUT > VTH
TRIG = LOW  if AMP_OUT < VTH
```

It is not an amplifier used at extreme gain. A comparator is designed to recover quickly from differential overdrive and drive a logic load. The TLV3502 provides a push-pull 3.3 V output, approximately 4.5 ns propagation delay under its specified overdrive conditions, and an input range extending near the supply rails.

Once this comparison occurs, pulse-height information is lost. The FPGA receives event time and approximate time-over-threshold, not a calibrated energy measurement. Revision A is therefore a counter and coincidence detector, not a spectrometer.

### 7.2 Threshold and equivalent raw signal

The trimmer range is limited to approximately 0-0.53 V. With VBASE near 50 mV, gain 13.4, and VTH initially 100 mV:

```text
equivalent raw threshold
  = (100 mV - 50 mV) / 13.4
  = 3.7 mV
```

The correct threshold is empirical. Too low gives dark counts and noise triggers. Too high rejects small real scintillation events and makes the two detectors inefficient.

### 7.3 Hysteresis

The TLV3502 includes about 6 mV of hysteresis. The rising signal must cross one effective threshold and fall below a slightly different threshold before the output returns.

Hysteresis suppresses repeated switching when a noisy or slowly varying input hovers near the decision level. It trades a small threshold uncertainty for a much cleaner digital event.

### 7.4 Timing error: propagation delay, jitter, and time walk

The quoted propagation delay is not the whole timing error.

- **Propagation delay** is the time between threshold crossing and output transition.
- **Jitter** is random variation in that time, driven by input noise and finite signal slope.
- **Time walk** is systematic: a large pulse crosses a fixed threshold earlier than a small pulse of the same underlying arrival time.

For a noisy ramp, a useful local approximation is:

```text
timing jitter approximately voltage noise / signal slope at threshold
```

The 100 ns coincidence window is intentionally much wider than the comparator's few-nanosecond delay. Revision A values robust detection above fine timing resolution.

---

## 8. Protection, regulation, and rail ownership

### 8.1 Input fuse and reverse-polarity diode

The resettable fuse limits sustained fault current. It is slow compared with an electronic current limiter, but it helps prevent a wiring mistake from turning a trace or cable into a heater.

The SS14 Schottky diode blocks reversed input polarity. Its forward drop wastes some voltage and power:

```text
Ploss = Vf x I
```

Schottky chemistry is used because its forward drop is lower than that of a conventional silicon rectifier. The analog rail is therefore slightly below the external 5 V input, which remains acceptable for the TPH2502.

### 8.2 The 3.3 V LDO

The TLV75533 converts the protected 5 V rail to a quiet 3.3 V supply for the comparators and threshold networks. A linear regulator dissipates the voltage difference as heat:

```text
Ploss = (Vin - 3.3 V) x Iload
```

The load is small, so efficiency is secondary to simplicity and low noise. The detector's 3.3 V rail is not connected to the Cora Pmod 3.3 V rail. Connecting two independently regulated outputs can make them source current into one another.

### 8.3 Decoupling capacitors

An IC draws current in short bursts. The power supply and cable cannot respond with zero inductance. A nearby 100 nF capacitor supplies high-frequency transient current locally, while a several-microfarad capacitor supports slower load changes.

At high frequency, a real capacitor behaves as C with ESR and ESL. Above its self-resonant frequency, package and trace inductance dominate and its impedance rises. A capacitor several centimeters away may have the correct printed value but fail as high-frequency decoupling because the loop inductance is too large.

---

## 9. Noise and loss map

Noise is any unwanted variation that overlaps the observable. Loss is energy removed from a desired path. They are related but not identical: a diode drop is a loss, while boost ripple is noise; optical leakage can reduce signal without adding electronic noise.

| Source | Mechanism | What it looks like | Main control |
|---|---|---|---|
| Optical coupling loss | Reflection, gaps, absorption, poor wrapping | Smaller real pulses | Good optical contact and light-tight reflective wrapping |
| SiPM dark counts | Thermal avalanche initiation | Real-looking small pulses in one detector | Threshold, moderate overvoltage, temperature tracking, coincidence |
| Crosstalk and afterpulsing | Secondary avalanches | Larger or delayed dark events | Moderate overvoltage and empirical threshold |
| Johnson noise | Thermal voltage of resistors, `sqrt(4 k T R B)` | Broadband baseline noise | Reasonable resistance and bandwidth |
| Op-amp voltage/current noise | Device noise integrated through noise gain | Amplified baseline noise | Low-noise part, limited bandwidth, compact input loop |
| Boost ripple | 500 kHz switching and harmonics | Periodic structure or false triggers | RC filtering, local decoupling, physical separation |
| Ground bounce | Shared return impedance times transient current | Trigger-correlated analog motion | Continuous plane and controlled return paths |
| Capacitive coupling | Electric field from high `dV/dt` nodes | Narrow injected spikes | Small switching-node area and distance |
| Inductive coupling | Mutual inductance from high `dI/dt` loops | Loop-dependent spikes or ringing | Small loop area and orientation control |
| Power-supply coupling | Finite PSRR and shared rail impedance | Rail activity visible at output | Bypass capacitors, filtering, local rail ownership |
| Probe loading | Probe capacitance and ground-lead inductance | Slower edges or apparent ringing | Short ground spring and low-capacitance probing |

The most important conceptual split is between **intrinsic pulse background** and **avoidable electronic contamination**. Dark avalanches are part of the sensor physics and should be handled statistically. Boost pickup, oscillation, and ground bounce are design errors and should not be accepted as detector background.

---

## 10. The PCB as an electromagnetic structure

### 10.1 Every signal is a loop

A schematic wire represents a complete current path, not a one-way line. At high frequency the return current follows the route of lowest impedance, usually directly beneath the signal trace on a continuous ground plane. This minimizes magnetic field area and inductance.

Cutting the plane forces current around the gap, enlarging the loop and increasing both radiation and susceptibility. The design therefore uses one continuous ground plane rather than separate analog and digital ground islands.

### 10.2 Signal path versus power path

| Region | Desired current behavior | Board implication |
|---|---|---|
| `SIPM_RAW` | Tiny transient loop local to sensor and sense resistor | Short trace, no connector, no plane gap, nearby ground probe point |
| Amplifier feedback | Current circulates between output, resistors, and inverting input | Smallest practical loop, no via if possible |
| Comparator output | Fast 3.3 V edge with more energy than raw signal | Route beside return, use 100 ohm source damping, keep away from raw input |
| Boost LX loop | Large pulsed `dI/dt` current | Tight cluster of IC, inductor, diode, and output capacitor |
| Bias distribution | Nearly DC voltage that must remain quiet | RC filtering, distance from LX and digital edges |
| 5 V and 3.3 V rails | Supply transient current with little voltage movement | Wider copper and local decoupling at each load |

Physical separation matters because fields fall with distance and coupling depends strongly on loop geometry. The boost converter belongs on the power/interface board, while the SiPM and first amplifier remain together on each detector head.

### 10.3 Why the cable alternates conductors with ground

Each head cable pairs bias, 5 V, 3.3 V, and trigger conductors with nearby ground conductors. The grounds are not redundant decorations. They provide short return paths and reduce the loop area that couples electric and magnetic fields.

Only the digital trigger crosses the frame. Sending the raw millivolt pulse over the same cable would expose it to supply ripple, connector capacitance, and external pickup before amplification.

### 10.4 Source damping on the trigger

The 100 ohm series resistor at the comparator output combines with trace and cable capacitance to slow the edge slightly and absorb energy that would otherwise reflect. It is not a precision 50 ohm RF termination. It is a pragmatic source damper for a short, low-rate digital connection.

### 10.5 Clearance and contamination

The 27-29 V bias is not a serious shock hazard, but larger clearance reduces leakage across flux residue, solder bridges, dust, and probe slips. In this design, clearance is more about reliability and measurement access than air breakdown.

### 10.6 Measurement changes the circuit

The raw and amplified nodes are high-bandwidth measurements. A long oscilloscope ground lead adds an inductive loop and can manufacture ringing. A probe also adds capacitance that can slow the pulse or destabilize an amplifier output.

Use a short ground spring, probe pads with adjacent ground, and the 10x high-impedance setting. Treat a waveform that changes dramatically with probe geometry as evidence about the measurement loop, not immediately as evidence that the board is oscillating.

---

## 11. From two triggers to a muon event

The comparator pulses are asynchronous to the FPGA clock. Each input therefore passes through a two-flip-flop synchronizer before edge detection. The first flip-flop may enter a metastable state if an edge arrives near its clock aperture; the second gives that state time to resolve before the logic uses it.

At 125 MHz, the clock period is 8 ns. A 13-cycle coincidence window is 104 ns. This is wide compared with analog propagation differences and narrow compared with the typical time between unrelated cosmic events.

For independent Poisson backgrounds, the accidental coincidence rate scales approximately as:

```text
Raccidental approximately R1 x R2 x W
```

The exact factor depends on whether `W` is defined as a one-sided or symmetric window. The important result is linear scaling with window width and multiplicative scaling with the two singles rates. Lower thresholds increase both singles rates and can therefore increase accidental coincidence much faster than intuition based on either detector alone.

Coincidence is the central statistical filter. The analog circuitry makes each detector sensitive; the two-plane geometry makes the result credible.

---

## 12. Why each major part exists

| Part | Why it is present | What would fail without it |
|---|---|---|
| MICROFC-60035 SiPM | Converts scintillation photons into avalanche charge | No compact optical-to-electrical detection |
| 49.9 ohm resistor | Converts avalanche current into voltage | No defined raw voltage signal |
| 100 nF coupling capacitor | Separates SiPM DC conditions from amplifier bias | Amplifier operating point becomes tied to sensor bias path |
| 130 kohm / 2.00 kohm divider | Creates a small positive baseline | Signal sits too close to the negative rail |
| TPH2502 channel B | Buffers VBASE | Divider voltage moves under load and couples stages |
| TPH2502 channel A | Provides controlled wideband gain | Comparator threshold must operate on a few-millivolt signal |
| 12.4 kohm / 1.00 kohm feedback | Sets gain to 13.4 | Gain is undefined or inappropriate |
| TLV3502 | Converts analog pulse to 3.3 V logic | FPGA sees an unsafe or ambiguous analog signal |
| Threshold trimmer | Selects the minimum accepted pulse | No way to balance noise rejection and efficiency |
| 100 ohm output resistor | Damps the trigger edge | More cable ringing and return-current disturbance |
| MAX5026 | Converts 5 V to adjustable SiPM bias | No appropriate sensor overvoltage |
| 47 uH inductor and Schottky diode | Store and transfer boost energy | Converter cannot raise voltage |
| Bias RC filters | Remove switching ripple and supply local charge | Bias motion appears as gain variation or false signal |
| TLV75533 LDO | Makes a quiet local 3.3 V rail | Comparator rail depends on FPGA power or a noisier source |
| SS14 and resettable fuse | Protect against reversed input and sustained faults | A wiring error can damage traces and ICs |
| Continuous ground plane | Provides low-inductance return paths | Larger loops, coupling, ringing, and ambiguous reference voltages |

---

## 13. The useful mental model

The detector is a cascade of representations:

```text
deposited energy
-> scintillation photons
-> number of fired SiPM cells
-> charge pulse
-> voltage pulse
-> threshold crossing
-> synchronized digital event
-> two-plane coincidence
```

Every stage discards information. Optical loss discards photons. Thresholding discards pulse height. Clock synchronization quantizes time. The design is successful if it preserves the one fact required by revision A: two spatially separated detectors observed compatible crossings within a short interval.

From an electromagnetic perspective, the board succeeds when large, fast power currents remain confined to their intended loops and the small signal current sees a short, quiet return path. Most layout rules are consequences of that sentence.

---

## 14. Primary references

- [onsemi C-Series SiPM datasheet](https://www.onsemi.com/download/data-sheet/pdf/microc-series-d.pdf): device model, gain, capacitance, dark counts, overvoltage, temperature coefficient, and package.
- [onsemi SiPM biasing and readout note](https://www.onsemi.com/download/application-notes/pdf/and9782-d.pdf): standard output, unused fast output, decoupling, recovery, and layout.
- [Analog Devices MAX5025-MAX5028 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/max5025-max5028.pdf): boost topology, feedback, component selection, output power, filtering, and layout.
- [3PEAK TPH2502 product page and datasheet](https://www.3peak.com/high-speed-op-amps/tph2502): supply range, gain-bandwidth, slew rate, rail-to-rail behavior, and voltage noise.
- [Texas Instruments TLV3501/TLV3502 datasheet](https://www.ti.com/lit/gpn/TLV3502): comparator delay, hysteresis, input range, overdrive, and output behavior.
- [Digilent Cora Z7 reference manual](https://digilent.com/reference/programmable-logic/cora-z7/reference-manual): FPGA clock and Pmod electrical interface.
- [CosmicWatch v3X paper](https://arxiv.org/html/2508.12111): reference detector architecture and measured implementation.
