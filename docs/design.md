# Revision A design specification

Status: **engineering prototype; not released for fabrication**. This document
is the reviewed design intent. Values are defaults for the first PCB unless a
measured result and review change them here and in KiCad together.

## Scope and architecture

Revision A answers a narrow question: can two small scintillators produce stable
single-channel counts and a statistically significant excess of aligned prompt
coincidences over misaligned and delayed controls?

```text
protected 5 V input
  +-- local 3.3 V regulator ------------------------+-- both heads
  +-- adjustable 27-29 V nominal SiPM bias --------+-- both heads
  +-- diode-protected analog supply ----------------+-- both heads

head A: scintillator -> SiPM -> gain -> comparator -> 3.3 V trigger A
head B: scintillator -> SiPM -> gain -> comparator -> 3.3 V trigger B
triggers -> Cora Z7 JA -> synchronization -> coincidence -> PS/USB log
```

Use two identical `detector_head` assemblies and one `power_interface`
assembly. Keep amplification and thresholding at each detector; do not send raw
SiPM pulses over the head cable. The Cora and detector share ground, but the
Cora Pmod 3.3 V pins are intentionally not connected to local 3.3 V.

Revision A has no pulse-height ADC or position measurement. It cannot provide
energy spectra, tracks, scattering tomography, or a spatial image. A
"transmission" result is limited to long-duration count-rate comparisons
through a broad geometric aperture.

## Detector-head circuit

Build two copies around an onsemi `MICROFC-60035-SMT-TR`, one dual
`TPH2502-SR`, and one dual `TLV3502AIDR`.

### SiPM footprint and bias

The custom SiPM footprint blocks release until two people have checked the
current manufacturer package drawing and a 1:1 print against the physical part.

| SiPM pin | Revision A connection |
|---:|---|
| 1, anode | `SIPM_RAW` |
| 2, fast output | No connect and no routed trace |
| 3, cathode | `BIAS_LOCAL` |
| 4, no connect | Soldered pad; ground or leave floating consistently |
| 5, center paddle | Mechanical clearance only; no copper, paste, or solder |

The standard-output network is:

```text
BIAS_27V -- 100 ohm --+-- pin 3
                      +-- 10 nF / 100 V to GND, at pin 3
                      +-- 1 uF / 50 V X7R to GND

pin 1 -- SIPM_RAW -- 49.9 ohm -- GND
                  +-- 100 nF -- amplifier input
```

The 49.9 ohm sense resistor favors pulse amplitude in this low-rate instrument.
onsemi typically shows 10 ohm for the 6 mm device to improve recovery; preserve
a documented 10.0 ohm stuffing option. Leave the unused fast output physically
short and floating. Put the 10 nF cathode capacitor and its return immediately
beside the sensor.

### Baseline and amplifier

Create a local nominal 50 mV divider and buffer it with TPH2502 channel B:

```text
+3V3_LOCAL -- 130 kohm --+-- 2.00 kohm -- GND
                         +-- 1 uF || 100 nF -- GND
                         +-- U2B voltage follower -- VBASE
```

Do not put a large capacitive load on buffered `VBASE`. Channel A is an
AC-coupled non-inverting stage:

```text
SIPM_RAW -- 100 nF --+-- U2A non-inverting input
                     +-- 499 ohm -- VBASE
U2A inverting input -- 1.00 kohm -- VBASE
U2A output ---------- 12.4 kohm -- U2A inverting input
```

Nominal gain is 13.4 V/V and the input high-pass corner is about 3.2 kHz. Add a
DNP 2.2 pF C0G footprint across the 12.4 kohm resistor only as a measured
stability option. Power the TPH2502 from `+5VA`, which is the protected input
after a Schottky diode and will normally be below 5.0 V. Place 100 nF at the IC
and 4.7 uF nearby. The feedback loop must be compact.

### Threshold and trigger

Power the TLV3502 from `+3V3_LOCAL`:

```text
AMP_OUT -- 1.00 kohm -- comparator A non-inverting input
VTH ------------------ comparator A inverting input
comparator A output -- 100 ohm -- TRIG_OUT
```

The 1 kohm input resistor limits current when the amplifier exceeds the
comparator rail. Include DNP `BAT54S` clamp footprints; do not populate them
unless testing justifies their added capacitance. The TLV3502 already provides
about 6 mV internal hysteresis. Include a DNP 330 kohm positive-feedback
footprint only for measured chatter. Hold the unused comparator in a defined
state: non-inverting input to ground, inverting input to 3.3 V, output open.

Generate an adjustable threshold of approximately 0-0.53 V:

```text
+3V3_LOCAL -- 4.70 kohm --+-- 1.00 kohm -- GND
                           +-- 1 uF -- GND
                           +-- top of 10 kohm 10-turn pot
pot bottom -- GND; pot wiper -- VTH; VTH -- 10 nF -- GND
```

Begin at a measured `VTH = 100 mV`. With a 50 mV baseline, this is about
3.7 mV referred to `SIPM_RAW`; the real operating point comes from a threshold
scan, not pot rotation.

Provide a two-pin injection header: generator signal through 499 ohm to
`SIPM_RAW`, plus ground. Use it without an installed SiPM first. Verify generator
level and polarity on a scope before connecting it to a biased sensor.

Provide labeled probe points for `BIAS_27V`, `BIAS_LOCAL`, `+5VA`,
`+3V3_LOCAL`, `VBASE`, `SIPM_RAW`, `AMP_OUT`, `VTH`, comparator output,
`TRIG_OUT`, and close ground loops at both analog nodes.

## Power/interface circuit

### Power rails

Use a separate, current-limited 5 V source through:

```text
5 V input -> 500 mA resettable fuse -> SS14 Schottky -> +5VA
```

Use `B2B-XH-A`/`XHP-2` for input power. Put 10 uF and 100 nF at `+5VA`; include
a clearly marked current link if space permits. A `TLV75533PDBVR`, with its
datasheet capacitors, generates `+3V3_LOCAL`. Expected total load is comfortably
below its 500 mA rating, but verify temperature and quiescent current on the
assembled system.

Do not allow either board to back-power the other through the Pmod. Test with
the Cora off and detector on, then detector off and Cora on.

### SiPM bias supply

Use `MAX5026EUT+T` in the manufacturer's adjustable step-up topology.

| Function | Revision A value |
|---|---|
| Input bypass | 4.7 uF / 16 V X7R plus 100 nF |
| Inductor | 47 uH shielded, DCR <1 ohm, saturation current >=350 mA |
| Boost diode | 60 V Schottky, >=0.5 A pulse capability |
| Raw output | 2 x 1 uF / 50 V X7R, preferably 1206 |
| Feedback top | 147 kohm, 0.1% |
| Feedback bottom | 6.65 kohm, 0.1%, plus 500 ohm 10-turn rheostat |
| Distribution filter | 100 ohm, then 1 uF / 50 V and 10 nF / 100 V |
| Discharge | 1 Mohm from filtered bias to ground |

Tie the trimmer wiper to one end so a lost wiper does not open the feedback path.
At the typical 1.25 V reference, the nominal span is about 27.0 V at 7.15 kohm
and 28.9 V at 6.65 kohm. This is **not a hardware voltage clamp**: IC reference,
resistor, and trimmer tolerances can move both endpoints. Start at maximum bottom
resistance and set the output using a high-impedance meter. Never exceed the
part's measured breakdown voltage plus 5.0 V.

Pull `SHDN` low with 100 kohm and use a labeled jumper or switch to connect it
to `+5VA`. Shutdown stops switching but does not isolate the output; the
inductor and diode can leave the output near the input voltage. Always measure
the rail and wait for the bleeder before handling it.

Expose `HV_RAW`, `BIAS_27V`, `FB`, `SHDN`, and adjacent grounds. Keep the IC,
inductor, diode, and first output capacitor in a very small switching loop. Keep
LX copper small and route feedback away from LX and the inductor.

### Head cables

Use identical keyed JST XH, 8-position, straight-through cables and verify every
conductor before power. `HEAD_A` and `HEAD_B` use the same pinout at both ends:

| Pin | Net | Purpose |
|---:|---|---|
| 1 | `BIAS_27V` | Filtered SiPM bias |
| 2 | `GND` | Bias return |
| 3 | `+5VA` | Amplifier supply |
| 4 | `GND` | Analog return |
| 5 | `+3V3_LOCAL` | Comparator/reference supply |
| 6 | `GND` | Logic/reference return |
| 7 | `TRIG_OUT` | 3.3 V trigger |
| 8 | `GND` | Trigger return |

Use `B8B-XH-A` headers and `XHP-8` housings. Mark pin 1 on both PCB faces and
print the voltages at pins 1, 3, and 5. Do not use loose Dupont leads in the
finished instrument.

### Cora Z7 interface

Connect to JA with an independently supported 2x6, 2.54 mm Pmod-compatible
right-angle male header or a fully continuity-mapped cable. JA is unkeyed, so
the mating view and pin-1 marking are release-critical.

| Pmod pin | Connection |
|---:|---|
| 1 | `TRIG_A`, input to Cora |
| 2 | `TRIG_B`, input to Cora |
| 3-4, 7-10 | No connect |
| 5, 11 | Ground |
| 6, 12 | No connect; Cora 3.3 V is not used |

Place 10 kohm pulldowns at the two FPGA inputs. The heads already provide 100
ohm source damping. Before mating boards, verify ground continuity and verify
that local 3.3 V is open-circuit to Pmod pins 6 and 12.

## PCB and mechanical rules

- Use two-layer, 1.6 mm FR-4, 1 oz copper and hand-assembly-friendly 0805
  passives; use 1206 where high-voltage capacitor performance benefits.
- Use one root schematic per board until complexity makes a hierarchy useful.
- Prefer a mostly unbroken ground plane. Do not create a split that forces
  return current around a gap.
- On the head, place sensor, cathode decoupling, sense/coupling parts, amplifier,
  comparator, and connector in signal order. Keep raw and feedback traces short.
- Separate `SIPM_RAW` and `AMP_OUT` from LX copper and trigger edges. Provide
  clearance around the bias rail and keep flux residue out of its feedback path.
- Stop layout review for an ambiguous connector view, crossed ground return,
  long amplifier feedback path, large switch node, or unverified footprint.
- Couple the 6 mm active area near the center of one polished 10 mm x 50 mm edge
  of a 50 mm x 50 mm x 10 mm plastic scintillator. Use a thin, bubble-free
  optical-grease layer and gentle compliant pressure. Wrap the other surfaces
  first in reflective material, then in a fully opaque layer; electrically
  insulate conductive foil from the PCB. Do not rely on tape tension to load
  the package.
- Start with 50 mm paddle separation in a rigid, repeatable frame; preserve an
  adjustment range of roughly 50-250 mm and a repeatable angle reference.

## FPGA and data path

The direct Cora Z7 PL clock is 125 MHz on H16. For Cora Z7-07S and 10, official
constraints map JA[0] to Y18 and JA[1] to Y19; nevertheless confirm the exact
board variant and connector before synthesis.

```tcl
set_property -dict { PACKAGE_PIN H16 IOSTANDARD LVCMOS33 } [get_ports { clk }]
create_clock -add -name sys_clk_pin -period 8.000 -waveform {0 4.000} [get_ports { clk }]
set_property -dict { PACKAGE_PIN Y18 IOSTANDARD LVCMOS33 } [get_ports { pulse_a_async }]
set_property -dict { PACKAGE_PIN Y19 IOSTANDARD LVCMOS33 } [get_ports { pulse_b_async }]
```

Each input needs a two-flop `ASYNC_REG` synchronizer followed by rising-edge
detection. Count 64-bit A singles, B singles, prompt coincidences, and live
ticks. A first edge opens a one-sided window in which the other edge is accepted;
simultaneous edges count once. A 13-cycle starting window is 104 ns at 125 MHz.
Use 63 cycles (504 ns) for first hardware tests, then shorten it after measuring
the comparator pulse and relative latency. An accepted coincidence starts a
125-cycle (1 us) lockout; singles continue counting.

Compute timing without 32-bit overflow or truncation:

```systemverilog
parameter longint unsigned CLK_HZ = 125_000_000;
parameter longint unsigned WINDOW_NS = 100;

function automatic longint unsigned ns_to_cycles(input longint unsigned ns);
    return ((longint'(CLK_HZ) * ns) + 999_999_999) / 1_000_000_000;
endfunction

localparam longint unsigned WINDOW_CYCLES = ns_to_cycles(WINDOW_NS);
```

Assert that derived counts are nonzero. Simulate A-only, B-only, simultaneous,
both window boundaries, lockout, long pulses, counter clear, reset release, and
counter rollover/snapshot behavior. A two-flop synchronizer does not guarantee
capture of a pulse shorter than one destination clock; measure the comparator
pulse and require at least 24 ns for comfortable bring-up. If it is shorter,
stretch it in hardware or use a reviewed asynchronous capture scheme.

The minimum useful data path is not just RTL counters:

1. Validate counters and timing with synthetic pulses, simulation, and an ILA.
2. Expose coherent snapshots and controls through AXI-Lite to the Zynq PS.
3. Emit a one-second CSV summary over the existing USB/UART connection.
4. Add an event FIFO only if timestamp-level analysis is later justified.

One-second records contain `utc_time`, `fpga_ticks`, `singles_a`, `singles_b`,
`prompt_coinc`, `delayed_coinc`, and `live_ticks`. Leave `delayed_coinc` empty—not
zero—until a validated offset mode exists. That mode may use a timestamp queue in
PL or an event stream analyzed by software; it must not overlap the prompt
sample. Run metadata records board and firmware revisions, actual
clock/window/lockout, measured bias and thresholds, temperature, paddle
separation and angle, location label, and notes. Bias, threshold, temperature,
angle, and separation are manually measured in revision A; do not present them
as FPGA telemetry.

For asynchronous singles rates `R_A` and `R_B`, the initial accidental estimate
for a one-sided window `tau` is `R_acc ~= 2 R_A R_B tau`; prefer a delayed-window
measurement made with the same window width.

## Feasibility and remaining design gates

The local analog front end, 3.3 V push-pull triggers, and 125 MHz coincidence
logic form a feasible low-rate prototype. Expected current is far below the
500 mA input protection and LDO rating. A close-geometry CosmicWatch v3X system
measured roughly 0.315 coincidences/s, but geometry, threshold, optical coupling,
and overburden make that a comparison—not a guaranteed rate. Begin at 50 mm
separation and plan hours, not minutes, for controlled comparisons.

The design is not ready to order until all of these are resolved in KiCad and
bench/review evidence:

- exact SiPM footprint and orientation;
- boost switch-loop and feedback layout;
- connector mating views, cable map, and Pmod mechanical support;
- detector/Cora off-state and back-power behavior;
- comparator pulse width and FPGA capture margin; and
- a working PS-to-host summary logger with coherent counter snapshots.

Solderless breadboard tests are appropriate for the threshold divider,
references, and safe 0-3.3 V FPGA pulses. Use a compact PCB or manufacturer
adapter for the boost supply, SiPM node, and high-speed amplifier; breadboard
waveforms are not representative there.

## Primary sources

- [onsemi C-Series SiPM datasheet](https://www.onsemi.com/pdf/datasheet/microc-series-d.pdf)
  and [bias/readout note AND9782/D](https://www.onsemi.com/download/application-notes/pdf/and9782-d.pdf)
- [Analog Devices MAX5025-MAX5028 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/max5025-max5028.pdf)
- [3PEAK TPH2502 product page](https://www.3peak.com/high-speed-op-amps/tph2502)
  and [datasheet](https://static.3peak.com/res/doc/ds/Datasheet_TPH2501-TPH2502-TPH2503-TPH2504.pdf)
- [TI TLV3502 datasheet](https://www.ti.com/lit/gpn/TLV3502) and
  [TLV755P datasheet](https://www.ti.com/lit/gpn/TLV755P)
- [Digilent Cora Z7-07S constraints](https://github.com/Digilent/digilent-xdc/blob/master/Cora-Z7-07S-Master.xdc),
  [Cora Z7-10 constraints](https://github.com/Digilent/digilent-xdc/blob/master/Cora-Z7-10-Master.xdc),
  and [Pmod interface specification](https://digilent.com/reference/_media/reference/pmod/pmod-interface-specification-1_3_0.pdf)
- [CosmicWatch v3X paper](https://arxiv.org/html/2508.12111) and
  [reference repository](https://github.com/spenceraxani/CosmicWatch-Desktop-Muon-Detector-v3X)
- [KiCad 10.0 CLI documentation](https://docs.kicad.org/10.0/en/cli/cli.html)
