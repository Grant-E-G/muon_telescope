# FPGA Muon Telescope and Crude Transmission Imager

**Board-ready build specification**  
**Version:** 0.2  
**Review date:** 2026-08-20  
**Target FPGA:** Digilent Cora Z7-07S or Cora Z7-10  
**Project goal:** Two-plane plastic-scintillator muon telescope with FPGA singles, coincidence, and timestamp logging  
**Budget goal:** Less than $300 excluding the FPGA and existing bench tools

---

## 0. Decision summary

Build three PCBs:

1. **Detector head PCB, quantity 2.** Each board contains one 6 mm x 6 mm SiPM, one local amplifier channel, one local comparator channel, a threshold trimmer, and test points.
2. **Power/interface PCB, quantity 1.** This board contains the protected 5 V input, local 3.3 V regulator, adjustable SiPM-bias boost converter, two keyed detector-head connectors, and the Cora Z7 Pmod interface.

This is a change from the earlier central two-channel analog board. The local-head architecture is more robust because the raw 10-30 mV SiPM signal does not travel through a long cable. Only the comparator's 3.3 V digital output crosses the detector frame.

The first build uses the **standard SiPM output**. The fast output is left electrically floating, as onsemi recommends when it is unused. The first build counts and timestamps events but does not digitize pulse height.

### Release status

This document is ready for schematic capture and PCB layout, but it is not a claim that the new three-board adaptation has already been measured. Treat the first fabrication as an engineering prototype. Do not order boards until every item in Section 18 is signed off.

---

## 1. Audit findings and corrections

The earlier version had a sound physics scope and a reasonable reference design, but several details were not ready to convert directly into copper.

| Earlier statement or omission | Why it was a problem | Correction in version 0.2 |
|---|---|---|
| A fixed 147 kohm / 6.34 kohm MAX5026 divider was specified while the bring-up procedure required adjustment from 27.2 V to 30 V. | The fixed divider cannot perform that procedure. | Use 147 kohm over 6.65 kohm plus a 500 ohm, 10-turn series trimmer. Approximate adjustment is 27.0-28.9 V. Start at minimum voltage. |
| Operation near 30 V was presented as a normal high-performance setting. | The C-Series datasheet recommends 1.0-5.0 V overvoltage. With a possible 24.2 V breakdown, 30 V can exceed the recommended range. | Limit the first board to about 28.9 V. Characterize near 27.2 V first. Do not exceed measured breakdown plus 5.0 V. |
| The carrier connector mixed raw analog, bias, fast output, and optional temperature signals. | A small raw signal on a mixed cable is vulnerable to pickup, crosstalk, and connector mistakes. | Put amplification and discrimination on each detector head. The cable carries power, bias, grounds, and a 3.3 V digital trigger only. |
| The amplifier input bias path had no exact resistor value. | The AC-coupled input had no defined DC path or high-pass corner. | Use 100 nF coupling and 499 ohm bias to VBASE, for an approximate 3.2 kHz high-pass corner. |
| VBASE was described as 25-100 mV and also as a shared node without a complete circuit. | The schematic could not be captured unambiguously, and a shared high-impedance node could cross-couple channels. | Generate and buffer a local nominal 50 mV VBASE on each detector head. |
| Comparator hysteresis was omitted. | Slow or noisy threshold crossings can chatter. | TLV3502 already provides about 6 mV internal hysteresis. Add a DNP 330 kohm external-feedback footprint only if measured chatter remains. |
| Comparator input clamping was mandatory but unspecified. | The added diode capacitance and exact topology affect timing. | Default to a 1 kohm series resistor, using the TLV3502's documented input protection. Add DNP BAT54S clamp footprints for experiments. |
| The fast SiPM output was routed to a normal test connector even though it was not used. | onsemi says an unused fast output should be left floating; a trace or cable adds parasitic loading and an antenna. | Leave pin 2 floating in revision A. Do not route it away from the package. |
| The SiPM center/mechanical paddle instruction was vague. | The 6 mm package has a specific exception that can be missed when creating the footprint. | Solder pin 4. Do not solder the pin 5 paddle. Follow the current onsemi POD/CAD exactly. |
| A 50 ohm standard-output resistor was presented as universal. | onsemi typically suggests 10 ohm for a 6 mm device to reduce recovery time. | Keep 49.9 ohm for the low-rate CosmicWatch-style detector because it increases pulse voltage and is proven in this use; document 10 ohm as an alternate stuffing value. |
| The first FPGA timing table assumed a 100 MHz Cora Z7 clock. | The board's direct PL oscillator is 125 MHz. | Use the 125 MHz oscillator on H16 and an 8 ns period unless an explicitly generated 100 MHz clock is used. |
| The Pmod description looked like a generic 1x6 connector. | Cora Z7 Pmods are unkeyed 2x6 receptacles. Incorrect physical numbering can connect a signal to power. | Use a standard 2x6 Pmod-compatible male header with unmistakable orientation. Connect trigger A, trigger B, and both grounds. Leave Pmod 3.3 V pins unconnected by default. |
| The AFE could be powered from either an unspecified regulator or the FPGA board. | This invites back-powering and noisy, ambiguous power paths. | Power all detector electronics from a separate protected 5 V input. Share ground with the Cora through the Pmod cable. Do not tie the two 3.3 V rails together. |
| Final high-speed electronics were described as potentially breadboardable. | Solderless breadboards add long loops, uncontrolled capacitance, and poor returns. | Breadboard only slow threshold/reference experiments and FPGA-safe logic. Build the boost, SiPM readout, and 250 MHz op-amp on PCBs. |
| The firmware example used hard-coded cycle counts. | Those values silently change when the clock changes. | Define `CLK_HZ` and derive window and lockout cycles from time parameters. |
| Parts and marketplace prices were treated as durable facts. | Price and listing state are time-dependent. | Treat the earlier prices as historical. Recheck exact MPN, stock, price, and packaging immediately before ordering. |

---

## 2. Honest project scope

### Minimum successful instrument

- Both detector heads produce raw and amplified pulses in darkness.
- Each comparator produces clean 0-3.3 V pulses.
- The FPGA separately counts detector A and detector B.
- Aligned paddles produce a prompt-coincidence excess over delayed coincidence.
- Lateral misalignment reduces the prompt rate.
- The system logs configuration and live time.

### What this is

- A two-plane charged-particle telescope.
- A useful muon coincidence demonstrator.
- A platform for angular scans and long, crude transmission measurements.
- A good mixed-signal PCB, FPGA, instrumentation, statistics, and scientific-control project.

### What this is not

- It is not a position-sensitive tracker.
- It is not 3D scattering tomography.
- It cannot localize a small high-Z object.
- It cannot perform energy spectroscopy in revision A because there is no pulse-height ADC.

True scattering tomography requires position-sensitive X/Y planes above and below the object.

---

## 3. Physical and electrical architecture

```text
5 V protected input
   |
   +--> 3.3 V LDO ------------------------------+
   |                                            |
   +--> adjustable MAX5026 bias, 27.0-28.9 V ---+----> head A
   |                                            +----> head B
   |
   +--> 5 V analog rail ------------------------+----> both heads

head A: scintillator -> SiPM -> gain -> comparator -> 3.3 V trigger A
head B: scintillator -> SiPM -> gain -> comparator -> 3.3 V trigger B

trigger A/B -> oriented 2x6 Pmod -> Cora Z7 -> synchronizers -> coincidence -> log
```

### Cable principle

Each detector-head cable has alternating supply/signal and ground conductors:

| Head connector pin | Net | Purpose |
|---:|---|---|
| 1 | `BIAS_27V` | Filtered SiPM cathode bias |
| 2 | `GND` | Bias return |
| 3 | `+5VA` | TPH2502 supply |
| 4 | `GND` | Analog return |
| 5 | `+3V3_LOCAL` | TLV3502 and threshold supply |
| 6 | `GND` | Logic/reference return |
| 7 | `TRIG_OUT` | 3.3 V comparator output |
| 8 | `GND` | Trigger return |

Use the same keyed connector family and pin numbering on both ends. A JST XH 1x8 through-hole connector is easy to inspect and hand-solder. Use premade or properly crimped housings; do not substitute loose Dupont jumpers in the finished instrument.

---

## 4. Detector-head PCB specification, build two identical boards

### 4.1 Required blocks

- onsemi MICROFC-60035-SMT-TR SiPM.
- Local bias filter and decoupling.
- Standard-output sense resistor.
- AC-coupled non-inverting amplifier.
- Local buffered baseline reference.
- Adjustable comparator threshold.
- 3.3 V high-speed comparator.
- Trigger series termination.
- Raw, amplified, threshold, trigger, bias, rail, and ground test points.
- Test-pulse injection header.

### 4.2 SiPM footprint and pin handling

The custom symbol and footprint are a release-blocking item.

| SiPM pin | Connection in revision A |
|---:|---|
| 1, anode | `SIPM_RAW` |
| 2, fast output | No connect, no routed trace |
| 3, cathode | `BIAS_LOCAL` |
| 4, no connect | Soldered pad; it may be grounded or left floating per onsemi |
| 5, center paddle | No solder pad/paste; follow current onsemi CAD/POD |

Do not infer pad geometry from a photograph. Compare the KiCad footprint printout at 1:1 scale with the manufacturer drawing. Check package orientation using pin 1 in both top and bottom views.

### 4.3 Bias and standard output

```text
BIAS_27V -- 100 ohm --+---- SiPM cathode, pin 3
                      |
                      +---- 10 nF / 100 V to GND, at pin 3
                      |
                      +---- 1 uF / 50 V X7R to GND

SiPM anode, pin 1 ----+---- 49.9 ohm to GND
                      |
                      +---- SIPM_RAW test point
                      |
                      +---- 100 nF coupling capacitor to amplifier
```

Use 49.9 ohm as the default sense resistor. For a future recovery-time comparison, fit a second board with 10.0 ohm. At cosmic-ray event rates, the slower recovery caused by 49.9 ohm is not the rate-limiting effect, and the larger voltage improves a simple threshold detector.

The 10 nF capacitor must be extremely close to the cathode and ground return. The 1 uF capacitor may be slightly farther away. Use at least 50 V rating for the 1 uF part and 100 V for the 10 nF part to reduce DC-bias loss and preserve margin.

### 4.4 Local VBASE

Generate about 50 mV from the local 3.3 V rail:

```text
+3V3_LOCAL -- 130 kohm --+-- 2.00 kohm -- GND
                         |
                         +-- 1 uF || 100 nF to GND
                         |
                         +-- U2B voltage follower --> VBASE
```

The divider gives approximately:

```text
VBASE_DIV = 3.3 V * 2.00 / (130 + 2.00) = 50 mV nominal
```

Use the second half of the TPH2502 as the voltage follower. Do not place a large capacitor directly on the buffered output. The amplifier input-bias and feedback resistors use `VBASE`, not raw ground, so the output quiescent level remains near 50 mV.

### 4.5 Amplifier channel

```text
SIPM_RAW -- 100 nF --+--> U2A non-inverting input
                     |
                     +-- 499 ohm --> VBASE

U2A inverting input -- 1.00 kohm --> VBASE
U2A output ---------- 12.4 kohm --> U2A inverting input
```

Nominal voltage gain:

```text
gain = 1 + 12.4 kohm / 1.00 kohm = 13.4 V/V
```

Nominal AC-coupling high-pass corner:

```text
fc = 1 / (2*pi*499 ohm*100 nF) = 3.19 kHz
```

Add a DNP C0G footprint of 1-5 pF in parallel with 12.4 kohm. It is a tuning option, not a default value. Populate it only in response to measured ringing or stability analysis.

Use the hand-solderable 3PEAK `TPH2502-SR` SOP8 package and power it from `+5VA`. Place 100 nF immediately at the supply pins and 4.7 uF nearby. Keep the feedback loop compact and entirely on the component side if possible.

### 4.6 Comparator and threshold

Use one half of a TI `TLV3502AIDR` SOIC-8 per head:

```text
AMP_OUT -- 1.00 kohm --> comparator A non-inverting input
VTH ------------------> comparator A inverting input
comparator A output -- 100 ohm --> TRIG_OUT connector pin
```

The TLV3502:

- operates from 2.7-5.5 V;
- has push-pull CMOS output;
- has rail-to-rail input common-mode range;
- provides about 6 mV internal hysteresis; and
- permits momentary input overvoltage when current is limited below its specified limit.

The 1 kohm input resistor limits current if the 5 V amplifier saturates above the 3.3 V comparator rail. Add DNP footprints for a BAT54S clamp to 3.3 V and ground. Do not populate the clamp unless bench behavior justifies its capacitance.

Tie the unused TLV3502 channel to a defined state: non-inverting input to ground, inverting input to 3.3 V, and output unconnected.

#### Threshold network

```text
+3V3_LOCAL -- 4.70 kohm --+-- 1.00 kohm -- GND
                           |
                           +-- 1 uF to GND
                           |
                           +-- top of 10 kohm, 10-turn pot
pot bottom ------------------- GND
pot wiper -------------------- VTH
VTH -------------------------- 10 nF to GND
```

The loaded top of the pot is approximately 0.53 V. Start with `VTH = 100 mV`. With a 50 mV baseline and 13.4 gain, that corresponds to roughly 3.7 mV at the raw SiPM node:

```text
raw-equivalent threshold = (100 mV - 50 mV) / 13.4 = 3.7 mV
```

Add a DNP 330 kohm resistor from comparator output back to the non-inverting input. Populate it only if the 6 mV internal hysteresis is insufficient.

### 4.7 Test-pulse injection

Add a two-pin `INJECT` header at the raw node:

```text
INJECT_SIGNAL -- 499 ohm -- SIPM_RAW
INJECT_GND ------------------- GND
```

With the SiPM uninstalled and the board powered, a 100 mV pulse from a 50 ohm generator produces roughly a 9 mV pulse at `SIPM_RAW`, depending on generator amplitude convention. Verify the generator with the oscilloscope before connection.

Do not inject while the SiPM is installed and biased until the polarity and amplitude have been checked.

### 4.8 Head-board test points

Provide labeled test points for:

- `BIAS_27V` at the connector;
- `BIAS_LOCAL` at the cathode filter;
- `+5VA`;
- `+3V3_LOCAL`;
- `VBASE`;
- `SIPM_RAW`;
- `AMP_OUT`;
- `VTH`;
- comparator output before the 100 ohm series resistor;
- `TRIG_OUT` after the series resistor; and
- at least two ground loops, including one adjacent to `SIPM_RAW` and one adjacent to `AMP_OUT`.

These test points are part of the scientific instrument, not decoration. They make the build debuggable and produce much better scope footage for the write-up or video.

---

## 5. Power/interface PCB specification

### 5.1 Power ownership

- The detector electronics have their own 5 V input.
- The detector board creates its own local 3.3 V rail.
- The Cora Z7 and detector share ground through the Pmod connection.
- The Pmod 3.3 V pins are left unconnected on the detector board.
- Never connect local 3.3 V to Cora 3.3 V unless a deliberate single-source power redesign has been reviewed.

### 5.2 Protected 5 V input

Recommended sequence:

```text
5 V input -> 500 mA resettable fuse -> SS14 Schottky -> +5VA
```

Use a JST `B2B-XH-A(LF)(SN)` board header with an `XHP-2` mating housing for the 5 V input. Place 10 uF and 100 nF from `+5VA` to ground at the input section. Add a clearly marked current-measurement jumper or 0 ohm link if board area permits.

### 5.3 Local 3.3 V regulator

Use a TLV75533PDBVR or equivalent low-noise 3.3 V LDO. Follow the selected regulator datasheet for input and output capacitors. The schematic must name the exact part rather than the generic text `3.3 V LDO`.

Budget at least 30 mA, even though the expected load is lower. The output is `+3V3_LOCAL` and supplies both detector heads.

### 5.4 Adjustable SiPM bias

Use MAX5026EUT+T in the manufacturer step-up topology.

| Component | Revision A value or requirement |
|---|---|
| MAX5026 input capacitor | 4.7 uF, 16 V X7R plus 100 nF |
| L1 | 47 uH, shielded ferrite, DCR less than 1 ohm, saturation current at least 350 mA |
| Boost diode | 60 V Schottky, at least 0.5 A pulse capability |
| Raw HV output capacitors | 2 x 1 uF, 50 V X7R, preferably 1206 |
| Feedback top | 147 kohm, 0.1-1% |
| Feedback bottom fixed | 6.65 kohm, 0.1-1% |
| Feedback trim | 500 ohm, 10 turn, used as a rheostat with wiper tied to one end |
| Bias-bus filter | 100 ohm followed by 1 uF / 50 V and 10 nF / 100 V |
| Bleeder | 1 Mohm from filtered bias bus to ground |

Approximate typical adjustment:

```text
Vout = 1.25 V * (1 + 147 kohm / Rbottom)

Rbottom = 7.15 kohm -> about 27.0 V
Rbottom = 6.65 kohm -> about 28.9 V
```

The actual voltage depends on reference and resistor tolerance. Always set it with a meter.

#### Default-off enable

Connect MAX5026 `SHDN` to ground through 100 kohm. A labeled jumper or switch connects `SHDN` to `+5VA` to enable bias. With the jumper absent, the analog and comparator circuits can be tested while high voltage is off.

Test points:

- `HV_RAW`, before the 100 ohm filter;
- `BIAS_27V`, after the filter;
- `SHDN`;
- `FB`; and
- ground next to each HV test point.

Keep the LX loop containing U, L, D, and the output capacitor extremely small. Keep the LX copper area small. Do not route feedback under the inductor or beside LX.

### 5.5 Head connectors

Use two identical JST `B8B-XH-A(LF)(SN)` board headers labeled `HEAD_A` and `HEAD_B`. Use `XHP-8` mating housings and make each cable straight through, pin 1 to pin 1. Continuity-test the completed cables before applying power. Print the voltage next to pins 1, 3, and 5 on silkscreen. Add reverse-side pin-1 markings because connector mistakes are especially destructive here.

### 5.6 Cora Z7 Pmod interface

Use a standard Pmod-compatible 2x6, 2.54 mm right-angle male header so the independently supported power/interface PCB plugs directly into Cora connector JA. The normal Cora Pmod receptacle is not physically keyed, so pin-1 markings and mechanical orientation are release-critical. If a cable is substituted, continuity-map every conductor and add a polarizing arrangement at the detector-board end.

| Pmod physical pin | Detector-board signal | Direction at Cora |
|---:|---|---|
| 1 | `TRIG_A` | Input |
| 2 | `TRIG_B` | Input |
| 3 | NC | - |
| 4 | NC | - |
| 5 | GND | Ground |
| 6 | NC, Cora 3.3 V is not used | - |
| 7-10 | NC | - |
| 11 | GND | Ground |
| 12 | NC, Cora 3.3 V is not used | - |

Place a 10 kohm pulldown on each trigger near the Pmod connector. The detector head has a 100 ohm source-series resistor. Do not add another large series resistor at the FPGA end unless ringing is measured.

---

## 6. PCB stackup and layout rules

### 6.1 Board technology

- Two layers, 1 oz copper.
- 1.6 mm thickness is acceptable.
- ENIG is preferred for the SiPM board because it is flat; lead-free HASL is acceptable only after checking package coplanarity.
- Default fabrication rules may be 0.15 mm / 0.15 mm if the board house supports them, but use larger geometry where practical.
- No controlled-impedance order is required for revision A.
- Use 0805 passives for hand assembly, with 1206 for 50 V 1 uF capacitors when helpful.

### 6.2 Net classes

| Net class | Suggested width | Suggested clearance | Nets |
|---|---:|---:|---|
| `DEFAULT` | 0.25 mm | 0.20 mm | Low-current signals |
| `POWER_5V3V3` | 0.50 mm | 0.25 mm | 5 V and 3.3 V rails |
| `BIAS_30V` | 0.40 mm | 0.50 mm | Raw and filtered SiPM bias |
| `FAST_ANALOG` | 0.25-0.40 mm | 0.20 mm | SiPM raw, amplifier input, feedback, amplifier output |

At 30 V, the enlarged clearance is not required for personal safety. It is useful margin against flux residue, solder bridges, and probing mistakes.

### 6.3 Ground

- Use a continuous bottom ground plane.
- Do not split analog and digital grounds.
- Use placement to control return paths.
- Connect MAX5026 PGND and GND to the same local low-impedance plane region as the input/output capacitors.
- Place the boost converter far from the Pmod connector and far from sensitive test points.
- Add ground stitching vias around board edges and beside connectors without perforating critical return paths.

### 6.4 Detector-head placement order

1. SiPM at the optical edge, using the exact manufacturer orientation.
2. Cathode decoupling immediately beside pin 3.
3. Sense resistor and coupling capacitor beside pin 1.
4. TPH2502 gain half and its feedback components.
5. TPH2502 VBASE half and divider.
6. TLV3502 and threshold network.
7. Trigger output and cable connector.
8. Injection and test headers where probes do not interfere with the scintillator clamp.

### 6.5 Layout stop conditions

Do not release Gerbers if:

- the SiPM footprint was not independently checked;
- the raw node crosses a plane gap;
- the amplifier feedback loop uses a long route or via;
- a boost-switching node appears under the detector-head analog section;
- a 30 V trace is routed through the Pmod area;
- Pmod supply pins are tied to local 3.3 V;
- test points cannot be physically probed after assembly; or
- connector pin 1 is ambiguous.

---

## 7. Exact schematic hierarchy and net names

Use these sheets so a reviewer can navigate the project:

### Detector-head project

- `01_power_and_connector.kicad_sch`
- `02_sipm_and_bias.kicad_sch`
- `03_amplifier_and_reference.kicad_sch`
- `04_threshold_and_trigger.kicad_sch`
- `05_test_points.kicad_sch`

### Power/interface project

- `01_input_and_3v3.kicad_sch`
- `02_bias_boost.kicad_sch`
- `03_head_connectors.kicad_sch`
- `04_pmod_interface.kicad_sch`
- `05_test_points.kicad_sch`

Canonical net names:

```text
+5V_IN
+5VA
+3V3_LOCAL
HV_RAW
BIAS_27V
BIAS_LOCAL
SIPM_RAW
AMP_IN
VBASE_DIV
VBASE
AMP_OUT
VTH_TOP
VTH
CMP_IN
TRIG_INT
TRIG_OUT
TRIG_A
TRIG_B
GND
```

Avoid anonymous long wires. Named nets make review and oscilloscope notes auditable.

---

## 8. Breadboard and pre-PCB experiments

### Reasonable on a solderless breadboard

- The 3.3 V threshold divider and 10-turn potentiometer.
- A slow comparator logic demonstration using a breakout adapter and less than 100 kHz input.
- A 3.3 V logic-pulse source for FPGA synchronizer and coincidence testing.
- The FPGA-side pulldowns and indicator LEDs.

### Do not use a solderless breadboard for final performance

- MICROFC-60035 raw readout.
- TPH2502 gain stage.
- MAX5026 boost loop.
- Fast-output evaluation.
- Nanosecond pulse-width conclusions.

### Better substitute for breadboarding

Order five head PCBs and five power/interface PCBs. Assemble in stages with DNP components and use the injection header. At prototype-board prices, the staged PCB is both cheaper in time and more representative than debugging breadboard parasitics.

If a manufacturer-mounted `MICROFC-SMTPA-60035-GEVB` pin-adapter board is obtainable, it can be used for nonfinal SiPM experiments with sockets or probe clips. onsemi explicitly describes the adapter as a quick evaluation aid with non-optimized timing. Use a current-limited bench bias supply and short connections; do not treat adapter or breadboard waveforms as final front-end performance.

---

## 9. Assembly order

### 9.1 Power/interface board

1. Assemble input protection and 3.3 V LDO only.
2. Verify resistance to ground before power.
3. Current-limit 5 V to 100 mA and verify `+5VA` and `+3V3_LOCAL`.
4. Assemble the MAX5026 stage with `SHDN` held low.
5. Verify feedback resistance and diode orientation.
6. Enable the converter without detector heads.
7. Set the trimmer to maximum resistance first and confirm approximately 27.0 V.
8. Check startup and ripple at `HV_RAW` and `BIAS_27V`.
9. Assemble head connectors and Pmod interface.

### 9.2 Detector head, no SiPM

1. Assemble all passives, TPH2502, TLV3502, and connector, but leave SiPM uninstalled.
2. Power with HV disabled.
3. Verify 5 V, 3.3 V, VBASE near 50 mV, and threshold range 0-0.53 V.
4. Set threshold near 100 mV.
5. Inject a positive pulse at the injection header.
6. Observe `AMP_OUT` and verify about 13.4 gain before saturation.
7. Verify comparator output is 0-3.3 V and pulse polarity is correct.
8. Repeat for the second head.

### 9.3 SiPM installation

1. Bake or handle according to the onsemi MSL and soldering guidance if the packaging history requires it.
2. Apply lead-free paste with a stencil or controlled manual deposition.
3. Align pin 1 under magnification.
4. Reflow using the sensor handling guidance, not an improvised excessive hot-air dwell.
5. Inspect pins 1-4. Confirm the pin 5 paddle was not soldered.
6. Clean only with materials compatible with the clear molded package.
7. Install one head first and keep it dark.

---

## 10. Electrical bring-up

### 10.1 Bias procedure

1. Cover the SiPM completely.
2. Set threshold high enough to avoid constant triggering.
3. Enable bias at about 27.0-27.3 V.
4. Check power-supply current.
5. Observe the raw node with a 10x high-impedance probe and a short spring ground.
6. Increase bias only after light-tightness and stability are established.
7. Never exceed `measured Vbr + 5.0 V`.

The datasheet gives a nominal breakdown range around 24.2-24.7 V and a recommended overvoltage of 1.0-5.0 V. Fixed voltage is therefore not the same thing as fixed gain across temperature or devices.

### 10.2 Scope expectations

The CosmicWatch v3X measurement reported a most-probable raw SiPM pulse near 21 mV for through-going muons, with detector-to-detector variation. After 13.4 gain, a representative pulse is a few hundred millivolts above VBASE.

Do not treat one amplitude as a pass/fail specification. Optical coupling, threshold, bias, and sensor variation matter.

### 10.3 Digital interface check

Before plugging into the Cora:

- comparator low is near 0 V;
- comparator high is no more than local 3.3 V;
- no 5 V or bias voltage appears on any Pmod signal;
- detector and Cora grounds are continuous through pins 5 and 11; and
- local 3.3 V is not continuous to Pmod pins 6 or 12.

---

## 11. FPGA implementation

### 11.1 Clock correction

The direct Cora Z7 PL oscillator is 125 MHz on package pin H16. Use:

```tcl
set_property -dict { PACKAGE_PIN H16 IOSTANDARD LVCMOS33 } [get_ports { clk }]
create_clock -add -name sys_clk_pin -period 8.000 -waveform {0 4.000} [get_ports { clk }]
```

If the design instead uses a 100 MHz Zynq PS fabric clock, state that explicitly and regenerate every cycle count.

For Cora Z7-07S, the official master XDC maps JA[0] to Y18 and JA[1] to Y19. Verify the exact board variant rather than copying these blindly.

```tcl
set_property -dict { PACKAGE_PIN Y18 IOSTANDARD LVCMOS33 } [get_ports { pulse_a_async }]
set_property -dict { PACKAGE_PIN Y19 IOSTANDARD LVCMOS33 } [get_ports { pulse_b_async }]
```

### 11.2 Initial timing at 125 MHz

| Parameter | Cycles | Actual time |
|---|---:|---:|
| Clock | 1 | 8 ns |
| Normal starting window | 13 | 104 ns |
| Wide bring-up window | 63 | 504 ns |
| Event lockout | 125 | 1.000 us |
| Minimum accepted comparator pulse target | 3 | 24 ns |

Measure pulse width. A two-flop synchronizer does not guarantee capture of a pulse shorter than one destination-clock period.

### 11.3 Minimum RTL functions

- Two two-flop asynchronous input synchronizers marked `ASYNC_REG`.
- Rising-edge detection.
- Per-channel 32- or 64-bit singles counters.
- Configurable coincidence window.
- Accepted-event lockout.
- 64-bit free-running timestamp.
- Prompt coincidence counter.
- Delayed coincidence in a separate test mode.
- Snapshot registers so software does not read multiword counters inconsistently.
- Counter clear and run-enable controls.

### 11.4 Parameterized timing pattern

Do not hard-code `10 cycles means 100 ns`.

```systemverilog
parameter int unsigned CLK_HZ      = 125_000_000;
parameter int unsigned WINDOW_NS   = 100;
parameter int unsigned LOCKOUT_NS  = 1_000;

localparam int unsigned WINDOW_CYCLES =
    (CLK_HZ / 1_000_000) * WINDOW_NS / 1_000;

localparam int unsigned LOCKOUT_CYCLES =
    (CLK_HZ / 1_000_000) * LOCKOUT_NS / 1_000;
```

For a reusable core, use a rounding-up integer function and assert that calculated cycle counts are at least one. Simulation must test the exact boundary cycle.

### 11.5 Required simulation cases

- A only increments A singles.
- B only increments B singles.
- Simultaneous A/B creates one coincidence.
- B on the last legal A-window cycle is accepted.
- B one cycle outside the window is rejected.
- Lockout prevents double-counting but does not corrupt singles counters.
- Counter clear works while inputs are low and while an input is high.
- A long comparator pulse produces one rising-edge event.
- Reset release does not create a false edge.
- Counter snapshots are coherent.

### 11.6 Hardware test before detector connection

Use a scope-verified 0-3.3 V pulse source. Never connect a 5 V logic generator directly to the Pmod. At first:

1. Drive A only.
2. Drive B only.
3. Split one safe pulse source to A and B.
4. Add a controlled delay.
5. Compare FPGA counts to generator frequency.

---

## 12. Detector mechanical and optical assembly

### 12.1 Optical coupling

- Couple the 6 mm x 6 mm active area to the polished 10 mm x 50 mm scintillator edge.
- Use a very thin optical-gel layer or a clean approximately 0.3 mm silicone pad.
- More gel is not better; eliminate the air gap without creating a thick compliant lens.
- Use a compliant clamp. Do not bend the PCB or concentrate screw load into the scintillator.

### 12.2 Reflective and opaque wrapping

1. Leave the optical interface accessible.
2. Wrap the remaining scintillator faces in reflective foil or PTFE.
3. Electrically insulate foil from every PCB pad and connector.
4. Add three to four orthogonal opaque layers.
5. Seal cable exits.
6. Keep any visible power LED outside the detector enclosure or omit it.

### 12.3 Frame

- Parallel detector trays.
- 5-25 cm adjustable separation.
- Lateral offset scale.
- Tilt axis and readable angle scale.
- Cable strain relief.
- No clamp force through the SiPM package.

Begin at 5 cm separation. Increase distance only after stable coincidence is measured.

---

## 13. Validation experiments

### 13.1 Light-leak test

At fixed threshold and bias:

1. Count for five minutes in darkness.
2. Turn room lights on.
3. Move a flashlight around seams without directly illuminating an exposed powered SiPM.
4. Flex cable exits.
5. Repair any rate-correlated leak.

### 13.2 Threshold scan

At fixed bias and temperature, record singles A, singles B, prompt coincidence, and delayed coincidence versus threshold. Start above VBASE. Do not compare absolute pot rotations; measure `VTH` with a meter.

### 13.3 Bias scan

Recommended first scan:

- 27.2 V;
- 27.7 V;
- 28.2 V; and
- 28.7 V, only if within `Vbr + 5.0 V`.

Retune or at least record thresholds at every bias.

### 13.4 Prompt and delayed coincidence

Use the same coincidence-window width for prompt and delayed measurements. Delay one channel by much longer than any physical correlation, for example 1 ms, and verify that implementation does not overlap the prompt sample.

Under a symmetric convention, an accidental estimate is often written:

```text
Racc approximately 2 * RA * RB * tau
```

where `tau` is the one-sided window. Under a full-width convention the factor is absorbed into `W`. Record the convention. Prefer the empirical delayed measurement.

### 13.5 Alignment control

- centered;
- 10 mm offset;
- 25 mm offset;
- more than 50 mm offset.

The alignment scan is the fastest convincing first physics plot.

### 13.6 Angular scan

The atmospheric muon angular distribution is often approximated by a cosine-squared dependence near sea level, but detector acceptance must also be modeled. Use long equal-live-time runs and report Poisson uncertainty.

---

## 14. Data format

### One-second summary

```text
utc_time,fpga_ticks,singles_a,singles_b,prompt_coinc,delayed_coinc,
live_ticks,window_ns,lockout_ns,threshold_a_mv,threshold_b_mv,
bias_v,temp_a_c,temp_b_c,angle_deg,separation_mm,run_id
```

### Event mode

```text
fpga_timestamp,channel_mask,run_id
```

### Run metadata

```yaml
run_id: 2026-08-xx_vertical_001
board_revision: muon-head-a1_and_power-a1
fpga_board: Cora-Z7-07S
clock_hz: 125000000
window_cycles: 13
window_ns_actual: 104
lockout_cycles: 125
bias_v: 27.2
threshold_a_mv: 100
threshold_b_mv: 100
paddle_size_mm: [50, 50, 10]
separation_mm: 50
angle_deg: 0
location_label: indoor_lab
notes: first aligned run
```

Record actual, not nominal, window duration and voltages.

---

## 15. Expected rates and statistics

A commonly used incident-flux scale is about one muon per square centimeter per minute through a horizontal surface, integrated over direction. A 25 square centimeter paddle therefore has an incident scale near 25 per minute, but two-plane coincidence is lower because of geometry, threshold, efficiency, and overburden.

The CosmicWatch v3X paper reported a close-geometry coincidence measurement near 0.315 Hz, about 19 per minute, in its high-acceptance configuration. Do not treat that as a guaranteed rate for this mechanical geometry.

For count `N` in live time `T`:

```text
rate = N / T
sigma_count approximately sqrt(N)
sigma_rate approximately sqrt(N) / T
fractional statistical uncertainty approximately 1 / sqrt(N)
```

| Counts | Approximate fractional uncertainty |
|---:|---:|
| 100 | 10% |
| 400 | 5% |
| 2,500 | 2% |
| 10,000 | 1% |

Transmission measurements are slow. Measure an open reference before and after the obstructed run so drift is visible.

---

## 16. Troubleshooting matrix

| Symptom | First measurements | Likely cause |
|---|---|---|
| No bias | 5 V at MAX5026, SHDN, LX, diode orientation, FB | Disabled converter, wrong pinout, open feedback, diode reversed |
| Bias above 29 V | Power off, measure bottom feedback resistance | Trimmer set wrong, wiper wiring error, wrong resistor |
| Large 500 kHz component on bias | Compare `HV_RAW`, `BIAS_27V`, and `BIAS_LOCAL` | Bad filter placement, capacitor DC-bias loss, long return loop |
| VBASE wrong | 3.3 V, divider midpoint, U2B input/output | Wrong divider, op-amp orientation, follower instability |
| No amplifier response with injection | Raw node, coupling capacitor, U2A pins | Missing 499 ohm bias, bad feedback, wrong pulse polarity |
| Amplifier oscillation | Use spring ground, disconnect test cable, inspect supply | Long feedback loop, poor decoupling, capacitive probe load |
| Comparator always high | Measure AMP_OUT baseline and VTH | Threshold below baseline, wrong comparator polarity |
| Comparator chatter | Observe AMP_OUT and trigger together | Noise near threshold; improve layout or populate external hysteresis |
| FPGA counts disconnected input | Pmod pin voltage and 10 kohm pulldown | Floating/wrong Pmod pin, EMI, missing common ground |
| Singles but no coincidence | Inject simultaneous test pulses first | Geometry, threshold, window, logic, or cable mapping |
| Prompt equals delayed | Raise threshold and narrow window | Mostly accidentals, light leak, or delayed logic error |
| Rate follows room light | Light-leak flashlight test | Incomplete opaque wrap |
| Channel mismatch | Swap complete head cables at power board | Determines whether fault follows head or FPGA channel |

---

## 17. Safety and handling

- The bias is low-current but can damage the SiPM, FPGA, and probes.
- Enable bias only after verifying the trimmer at minimum output.
- Never connect or disconnect a head with bias enabled.
- Wait for the 1 Mohm bleeder and confirm voltage before handling.
- Keep a powered SiPM covered. Do not expose it to direct sun or an intense lamp.
- Follow ESD practice.
- Keep reflective foil away from every conductor.
- Use eye protection when cutting or drilling plastic.
- Wet-sand scintillator if finishing is needed and avoid inhaling dust.
- This detector is educational instrumentation, not certified radiation-safety equipment.

---

## 18. Gerber release checklist

### Schematic

- [ ] Exact manufacturer part numbers are in symbol fields.
- [ ] Every IC pin number matches its current datasheet.
- [ ] SiPM pin 2 has a no-connect marker and no routed trace.
- [ ] SiPM pin 5 is not given a solderable pad.
- [ ] Unused comparator inputs are tied to defined rails.
- [ ] MAX5026 SHDN defaults low.
- [ ] Feedback trimmer wiper is tied for open-wiper safety.
- [ ] Local 3.3 V is not tied to Pmod 3.3 V.
- [ ] Both Pmod grounds are connected.
- [ ] All connector pin numbers match the physical mating view.
- [ ] Test points appear on every required net.
- [ ] ERC has zero unexplained errors; every waiver is documented.

### Footprints

- [ ] SiPM footprint independently checked against current onsemi POD/CAD.
- [ ] SOIC, SOT-23, diode, inductor, trimmer, and connector orientations checked.
- [ ] 50 V capacitor package and voltage rating recorded in BOM.
- [ ] 1:1 footprint printout checked with physical parts where available.
- [ ] Mating connectors and cable housings are in the BOM.

### Layout

- [ ] Continuous ground plane.
- [ ] Compact MAX5026 switching loop.
- [ ] Small LX copper area.
- [ ] Feedback kept away from LX and inductor.
- [ ] Cathode 10 nF capacitor is at the SiPM.
- [ ] Amplifier feedback loop is short.
- [ ] Raw and amplified test points have adjacent grounds.
- [ ] Pin-1 markings visible after assembly.
- [ ] DRC clean with documented waivers only.
- [ ] Board outline, holes, clamp clearance, and connector access checked in 3D viewer.

### Manufacturing outputs

- [ ] Gerbers viewed in an independent viewer.
- [ ] Drill files present.
- [ ] Copper and solder-mask layers aligned.
- [ ] No paste on SiPM pin 5 paddle.
- [ ] BOM and placement files exported.
- [ ] Assembly drawing identifies DNP parts.
- [ ] Five head boards and five power/interface boards ordered for prototype insurance.

---

## 19. Weekend plan after boards arrive

### Friday

- Bring up 5 V and 3.3 V.
- Bring up adjustable bias with heads disconnected.
- Verify FPGA counting with safe synthetic pulses.

### Saturday morning

- Bring up head A without SiPM using injected pulses.
- Bring up head B without SiPM using injected pulses.
- Compare gain, threshold range, and trigger width.

### Saturday afternoon

- Install and power one covered SiPM.
- Couple one scintillator and make it light-tight.
- Repeat for the second head.

### Sunday

- Count singles separately.
- Begin with 504 ns coincidence, then reduce toward 104 ns.
- Run aligned, misaligned, and delayed controls.
- Start an overnight aligned run.

Do not schedule useful cosmic-ray data before synthetic-pulse and light-leak tests pass.

---

## 20. Write-up and video evidence plan

Capture:

1. A schematic block explanation.
2. Footprint verification, including the unusual SiPM pin 5 rule.
3. MAX5026 startup at minimum bias.
4. Injected raw, amplified, and comparator traces.
5. A real dark detector pulse.
6. FPGA ILA traces for A, B, and coincidence.
7. Prompt versus delayed counts.
8. Aligned versus misaligned rate.
9. The first long-run plot with Poisson bars.

Do not label LED injection as a muon. Do not label singles as pure muons. Do not label a rate deficit as a tomographic reconstruction.

---

## 21. Expansion path

1. Add a peak detector and ADC for pulse-height distribution.
2. Add per-head temperature sensors and bias compensation.
3. Build four detector heads for redundant coincidence.
4. Replace paddles with narrow bars for one-dimensional position.
5. Use orthogonal X/Y layers above and below the object.
6. Add event building, calibrated timing, and track reconstruction.

The revision A connector and modular head concept are chosen so later heads can be added without redesigning the FPGA interface principle.

---

## 22. Primary references

1. onsemi, **C-Series SiPM datasheet**, including overvoltage, capacitance, temperature coefficient, pin assignment, pin-adapter guidance, and pin 5 soldering guidance:  
   https://www.onsemi.com/download/data-sheet/pdf/microc-series-d.pdf

2. onsemi, **AND9782/D: Biasing and Readout of SiPM Sensors**, including positive-bias standard readout, unused fast-output guidance, decoupling, sense-resistor tradeoffs, and layout guidance:  
   https://www.onsemi.com/download/application-notes/pdf/and9782-d.pdf

3. Analog Devices, **MAX5025-MAX5028 datasheet**, including the 30 V circuit, 47 uH inductor, feedback equation, current limit, shutdown, and layout guidance:  
   https://www.analog.com/media/en/technical-documentation/data-sheets/max5025-max5028.pdf

4. Texas Instruments, **TLV3501/TLV3502 datasheet**, including 2.7-5.5 V operation, push-pull output, rail-to-rail input, 6 mV internal hysteresis, overvoltage-current limiting, and layout:  
   https://www.ti.com/lit/gpn/TLV3502

5. 3PEAK, **TPH2502 product page and datasheet**, including rail-to-rail I/O, supply range, and current production packages:  
   https://www.3peak.com/high-speed-op-amps/tph2502

6. Texas Instruments, **TLV755P 500 mA LDO datasheet**, including pinout and capacitor requirements for TLV75533PDBVR:  
   https://www.ti.com/lit/gpn/TLV755P

7. Axani et al., **CosmicWatch: The Desktop Muon Detector (v3X)**, component-level architecture and measured performance:  
   https://arxiv.org/html/2508.12111

8. University of Delaware, **CosmicWatch v3X repository**, schematics, build files, and license:  
   https://github.com/spenceraxani/CosmicWatch-Desktop-Muon-Detector-v3X

9. Digilent, **Cora Z7 reference manual**, including 125 MHz PL clock and 2x6 Pmod electrical interface:  
   https://digilent.com/reference/programmable-logic/cora-z7/reference-manual

10. Digilent, **Cora Z7-07S master XDC**, including H16 clock and Pmod package pins:  
   https://github.com/Digilent/digilent-xdc/blob/master/Cora-Z7-07S-Master.xdc

11. KiCad, **Getting Started in KiCad 10**, footprint assignment, ERC, net classes, board update, and DRC workflow:  
   https://docs.kicad.org/10.0/en/getting_started_in_kicad/getting_started_in_kicad.html

### Attribution and use

The detector concept and several analog values are derived from CosmicWatch v3X. Preserve attribution in published files and videos. The repository states a CC BY-NC 4.0 license. Personal and educational use is compatible with that license; obtain permission before commercial use.

---

## 23. Final recommendation

Proceed with KiCad this weekend, but design **two identical local detector heads and one shared power/interface board**, not a long-cable raw-analog system.

The highest-value weekend output is a reviewed schematic, verified custom SiPM footprint, clean PCB placement, and a release checklist - not rushed Gerbers. If the two of you complete the schematic and placement but are uncertain about the boost loop or SiPM footprint, stop before routing or ordering and review those two areas again.
