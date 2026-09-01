# Revision A design specification

Status: **engineering prototype; not released for fabrication**. This document
is the reviewed design intent. Values are defaults for the first PCB unless a
measured result and review change them here and in KiCad together.

## Pre-KiCad decision checklist

These decisions affect connectivity, footprints, or board geometry. Resolve
them here before schematic capture; do not leave them as annotations to fix
during layout.

**Revision A has no open pre-KiCad design decisions.** The unchecked work in
`docs/build-and-debug.md` is verification or implementation work, not authority
to choose a different interface during capture or layout. A physical mismatch
must be recorded and reviewed before changing the frozen values below.

The allowed `R_CHG`/`C_HOLD` stuffing matrix is the one intentional exception
to frozen first-build values, but not to connectivity or footprint selection:
each is one 0805 site with a provisional population. Fabrication release still
requires measured values to be frozen here, in KiCad, and in the BOM.

Power and bias:

- [x] Use `MAX5026`, not `MAX5028`: both accept 3-11 V, but the MAX5026 has an
  externally adjustable output while the MAX5028 has an internal divider for a
  fixed nominal 30 V output. Device-specific SiPM bias must be adjustable.
- [x] `BIAS_ENABLE = off` may leave the bias rail near the 5 V input while
  detector power remains on; this is safely below SiPM breakdown. Before
  handling a head, remove detector 5 V, wait for the bleeder, and verify the
  rail with a meter. True 0 V with the analog rails powered is out of scope.
- [x] Use 147 kohm over 6.98 kohm plus a 500 ohm trim. With the specified
  reference, feedback-current, resistor-tolerance, and 0-40 deg C temperature
  cases, an intact divider holds the normal upper bound below 28.55 V. Set and
  verify 27.2 V with a meter; this bound is not single-fault protection.
- [x] Power the detector from a regulated, floating/Class II, center-positive
  5 V adapter rated at least 0.5 A through a board-mounted barrel jack. Revision
  A selects `PSAC05A-050L6-R` and `PJ-102AH`; retain the on-board 500 mA PTC.
- [x] Solder SiPM pin 4 to the shared ground plane through a short thermal-relief
  connection. This is the same ground net used by the sense resistor and head
  connector, not a separate analog-ground island. Keep switching and digital
  return currents away from the sensor by placement.

Interface and firmware:

- [x] Target the purchased Cora Z7-07S (`XC7Z007S-1CLG400C`) and use the archived
  Cora Z7-07S master XDC as the constraint source.
- [x] Use the Digilent `240-109` 2x6 Pmod cable and included gender changer so
  the Cora remains reusable. Continuity-map it, mark pin 1 and both mating
  orientations, provide strain relief, and leave Pmod 3.3 V pins 6/12 open.
- [x] Populate a `SN74LVC1G123DCTR` one-shot after each comparator, nominally
  stretching every trigger to about 200 ns. Provide mutually exclusive 0 ohm
  selection links for stretched (default) or direct comparator output. This
  removes the need for a pre-PCB equivalent-front-end characterization.
- [x] Use the register map and logger sequence specified below. Implement the
  delayed coincidence in PL by delaying channel B exactly 125,000 clocks (1 ms) in
  a one-bit circular memory and applying the same coincidence algorithm and
  independent lockout used for prompt events.
- [x] Add a buffered precision peak detector to each head and a shared
  `MCP3202-BI/SN` dual 12-bit SPI ADC to the power/interface board. Preserve the
  comparator, one-shot, and trigger path. Use the two previously unused JA data
  pins plus four more unused JA pins for SPI and a common active-high peak reset.
- [x] Replace each eight-position head connection with a ten-position JST XH
  connection. Pins 1-8 retain their revision-A assignments; pins 9 and 10 add
  `PEAK_OUT` and `PEAK_RESET`. This preserves every existing power and signal
  return rather than repurposing a ground conductor.
- [x] Use a second `TPH2502-SR` on each head. The existing dual amplifier has no
  spare channel: channel A is the signal gain stage and channel B buffers
  `VBASE`. The added dual provides the peak-charging amplifier and cable/ADC
  buffer without altering either existing function.
- [x] Provide mutually exclusive reset footprints for cost-optimized
  `BSS138P,215` and precision `TMUX1101DCKR` assembly variants. The MOSFET is the
  default prototype population; the TMUX1101 is the characterized low-leakage
  option. Never fit both.
- [x] Make only the peak charging resistor and C0G hold capacitor stuffing values
  bench-selectable. Start characterization with 49.9 ohm and 220 pF, but measure
  the real `AMP_OUT` pulse and peak error before freezing either value.

Physical and procurement inputs:

- [x] Use the purchased pair of seller-cut BC-408 blocks, each approximately
  50 x 50 x 10 mm (`BC408-505010-1FP`). The listing specifies one polished
  50 x 50 mm face; the opposite face and sides are smooth water-saw cuts.
- [x] The scintillator provenance decision is resolved. The seller describes
  these blocks as virgin material water-saw cut from a large BC-408 block, not
  reclaimed pieces. Inspect the delivered parts against the listing before
  removing the option to return or report a mismatch.
- [x] Couple the 6 mm SiPM at the center of the polished 50 x 50 mm face with a
  thin grease layer. Use a compliant clamp with hard stops so pressure is
  repeatable and the sensor package is not the structural stop.
- [x] Use the board outlines, mounting holes, connector coordinates, cable exits,
  optical stack, and adjustable-frame datums in the mechanical interface-control
  section below.
- [x] Begin schematic and footprint capture from the exact selected-part drawings
  in `docs/datasheets/`. A datasheet check, 1:1 print, and physical-part check are
  fabrication-release verification gates; they do not remain open design choices
  and do not block schematic capture.

## Scope and architecture

Revision A answers a narrow question: can two small scintillators produce stable
single-channel counts and a statistically significant excess of aligned prompt
coincidences over misaligned and delayed controls?

```text
protected 5 V input
  +-- local 3.3 V regulator ------------------------+-- both heads
  +-- adjustable 25.8-27.6 V nominal SiPM bias ----+-- both heads
  +-- diode-protected analog supply ----------------+-- both heads

head A: scintillator -> SiPM -> gain -+-> comparator -> one-shot -> trigger A
                                      +-> peak capture/hold -> buffered peak A
head B: scintillator -> SiPM -> gain -+-> comparator -> one-shot -> trigger B
                                      +-> peak capture/hold -> buffered peak B
peaks -> shared dual 12-bit SPI ADC --+
triggers/ADC -> Cora Z7 JA -> synchronization -> coincidence -> PS/USB log
```

Use two identical `detector_head` assemblies and one `power_interface`
assembly. Keep amplification and thresholding at each detector; do not send raw
SiPM pulses over the head cable. The Cora and detector share ground, but the
Cora Pmod 3.3 V pins are intentionally not connected to local 3.3 V.

Revision A includes uncalibrated pulse-height capture but no position
measurement. It cannot by itself provide calibrated particle-energy spectra,
tracks, scattering tomography, or a spatial image. A
"transmission" result is limited to long-duration count-rate comparisons
through a broad geometric aperture.

## Detector-head circuit

Build two copies around an onsemi `MICROFC-60035-SMT-TR`, two dual
`TPH2502-SR` amplifiers, one dual `TLV3502AIDR`, and one
`SN74LVC1G123DCTR`.

### SiPM footprint and bias

The custom SiPM footprint blocks release until two people have checked the
current manufacturer package drawing and a 1:1 print against the physical part.

| SiPM pin | Revision A connection |
|---:|---|
| 1, anode | `SIPM_RAW` |
| 2, fast output | No connect and no routed trace |
| 3, cathode | `BIAS_LOCAL` |
| 4, no connect | Soldered to the shared ground plane through a thermal relief |
| 5, center paddle | Mechanical clearance only; no copper, paste, or solder |

The standard-output network is:

```text
BIAS_27V -- 100 ohm --+-- pin 3
                      +-- 10 nF / 100 V to GND, at pin 3
                      +-- 1 uF / 50 V X7R to GND

pin 1 -- SIPM_RAW -- 49.9 ohm -- GND
                  +-- 100 nF -- amplifier input

pin 4 -- short thermal relief -- shared GND plane
```

The 49.9 ohm sense resistor favors pulse amplitude in this low-rate instrument.
Do not short pin 1 directly to the plane: its voltage across this resistor is
the standard-output signal. Pin 4, by contrast, is the package's no-connect
terminal and is grounded directly only to give it a defined potential.
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

### Local peak capture and hold

Tap `AMP_OUT` with the CMOS input of a second `TPH2502-SR`; do not insert
anything into the amplifier-to-comparator path. Channel A of the added device is
a feedback-enclosed peak charger and channel B buffers the held voltage:

```text
AMP_OUT ------------------------------ U3A non-inverting input
PEAK_HOLD ---------------------------- U3A inverting input
U3A output -- R_CHG -- BAS70 anode
BAS70 cathode ------------------------ PEAK_HOLD

PEAK_HOLD -- C_HOLD -- GND
PEAK_HOLD ---------------------------- U3B non-inverting input
U3B output --------------------------- U3B inverting input
U3B output -- 100 ohm ---------------- PEAK_OUT

PEAK_HOLD -- Q_RESET or U_RESET ------ VBASE
PEAK_RESET -- 100 kohm -- GND
```

Use Nexperia `BAS70,215`, pin 1 anode, pin 3 cathode, with pin 2 unconnected.
Its Schottky construction avoids stored-charge recovery when the charging
amplifier output falls; its specified reverse leakage is still part of the hold
error and must be measured. A low-leakage junction diode with microsecond
reverse recovery is not an equivalent substitution in this peak path.

U3A must drive one diode drop above `PEAK_HOLD`. Because U3A and the original
gain stage share `+5VA`, the peak path cannot reproduce an `AMP_OUT` pulse that
approaches the positive rail; it will saturate roughly one BAS70 forward drop
below U3A's loaded high-output limit. Characterize and flag that upper nonlinear
region. If normal events reach it, a reviewed gain or supply/topology change is
required; changing `R_CHG`, `C_HOLD`, or ADC scaling cannot restore a clipped
peak.

Provide one 0805 footprint each for `R_CHG` and `C_HOLD`. The provisional first
population is 49.9 ohm and 220 pF C0G. Buy 22, 49.9, 100, and 220 ohm charging
resistors and 100 pF, 220 pF, 470 pF, and 1 nF 50 V C0G capacitors for
characterization. Do not change other gain, threshold, ADC-divider, or timing
values to compensate for an unmeasured peak circuit. A larger capacitor reduces
droop and switch charge-injection error but requires more current and pulse area
to reach the true peak; a larger charging resistor limits the TPH2502 and BAS70
current but increases acquisition error on a narrow pulse. The 49.9 ohm starting
value bounds the idealized current from a 5 V amplifier step to about 100 mA,
the BAS70 non-repetitive limit, before amplifier and diode voltage drops.

Fit exactly one of these active-high reset implementations across `PEAK_HOLD`
and `VBASE`:

| Variant | Selected part and wiring | Consequence |
|---|---|---|
| Cost-optimized, default | Nexperia `BSS138P,215`: drain to `PEAK_HOLD`, source to `VBASE`, gate to `PEAK_RESET` | Active-production, inexpensive, and fast, but its datasheet permits up to 1 uA drain leakage at 60 V and does not guarantee on-resistance at 3.3 V. Both are acceptable only after measuring droop and reset residue at the actual sub-5 V signal and 0-40 deg C. |
| Precision option | TI `TMUX1101DCKR`: D to `PEAK_HOLD`, S to `VBASE`, SEL to `PEAK_RESET`, VDD to `+5VA`, GND to ground | 3 pA typical leakage, 80 pA maximum off leakage at 5 V and 25 deg C, 4 ohm maximum on-resistance, 1.8 V-compatible fail-safe logic, and -1.5 pC typical charge injection; costs more and uses an SC70-5 footprint. |

For `BSS138P,215`, pin 1 is gate, pin 2 source, and pin 3 drain. For
`TMUX1101DCKR`, pin 1 is D, pin 2 S, pin 3 ground, pin 4 SEL, and pin 5 VDD.
The MOSFET body diode must point from `VBASE` toward `PEAK_HOLD`; reversed
source/drain orientation would clamp every positive peak. Put both alternate
footprints on the PCB but mark them mutually exclusive in schematic fields and
assembly output. The reset switch returns the hold node to the 50 mV baseline,
not ground, so closing reset does not force the peak-charging amplifier to drive
continuously. `C_HOLD` returns to ground so its pulse-charging current does not
disturb `VBASE`.

Use `delta V = I_leak * t_hold / C_HOLD` when reviewing measured retention. As
an intentionally pessimistic illustration, the BSS138P's 1 uA datasheet limit
at 60 V would imply about 0.23 V loss in 50 us with 220 pF; the actual drain
voltage is below 5 V, but no lower maximum is guaranteed. The cost variant is
therefore a characterize-and-bin option, not a precision claim. The TMUX1101
removes that reset-device uncertainty, but BAS70 reverse leakage, both TPH2502
inputs, capacitor insulation, and PCB contamination remain in the total.

Power U3 from `+5VA`, place 100 nF at the IC, and use the existing nearby 4.7 uF
head bypass. Keep U3A, `R_CHG`, the diode, `C_HOLD`, reset part, and U3B in that
order with a very small `PEAK_HOLD` island. Flux residue and probe contamination
can dominate the intended leakage; keep the node away from the bias rail,
connector contamination, and solder-mask openings other than its test pad. The
100 ohm U3B output resistor isolates cable capacitance and is outside the peak
feedback loop.

The hold circuit captures the largest pulse since the last reset; it does not
know which pulse caused a later coincidence. ADC-mode firmware must therefore
reset both heads after every rejected single once its coincidence window has
expired, and only defer reset when a valid coincidence is being digitized. A
sequence that resets only after accepted coincidences can attach a stale,
larger single-channel peak to a later event and is invalid.

While a peak is held above the input, U3A operates open-loop with its output
near the low rail. The TPH2502 datasheet does not specify overload-recovery time
for this use. The 1 us post-reset re-arm delay below is provisional and must be
increased if injected back-to-back pulses show acquisition error.

### Threshold and trigger

Power the TLV3502 and trigger one-shot from `+3V3_LOCAL`:

```text
AMP_OUT -- 1.00 kohm -- comparator A non-inverting input
VTH ------------------ comparator A inverting input
comparator A output ------------------------------ COMP_RAW

COMP_RAW -- SN74LVC1G123 B input
GND -------------------------------- A input
+3V3_LOCAL -------------------------- CLR input
+3V3_LOCAL -- 2.00 kohm --+---------- Rext/Cext
                           +-- 27 pF -- Cext

SN74LVC1G123 Q -- 0 ohm R_STRETCH (fitted) --+-- 100 ohm -- TRIG_OUT
COMP_RAW -------- 0 ohm R_DIRECT (DNP) ------+
```

The 1 kohm input resistor limits current when the amplifier exceeds the
comparator rail. Include DNP `BAT54S` clamp footprints; do not populate them
unless testing justifies their added capacitance. The TLV3502 already provides
about 6 mV internal hysteresis. Include a DNP 330 kohm positive-feedback
footprint only for measured chatter. Hold the unused comparator in a defined
state: non-inverting input to ground, inverting input to 3.3 V, output open.

Use TI `SN74LVC1G123DCTR` in its 8-pin DCT/SM8 package with 100 nF local
decoupling. TI characterizes 170-200 ns output pulses at 3.3 V with 2 kohm and
28 pF over -40 to 125 deg C; the selected stocked 27 pF C0G part gives a similar
nominal pulse. Accept 150-250 ns at `TRIG_OUT` during bring-up. The B input has a
3 ns minimum trigger-pulse requirement at 3.3 V. Preserve test access to
`COMP_RAW` so that requirement can be checked on the real board.

`R_STRETCH` and `R_DIRECT` are mutually exclusive. Populate only
`R_STRETCH` for revision A. The direct path may be selected later only after
measuring `COMP_RAW` at 24 ns or longer; never populate both links because the
comparator and one-shot outputs would contend.

Generate an adjustable threshold of approximately 0-0.53 V:

```text
+3V3_LOCAL -- 4.70 kohm --+-- 1.00 kohm -- GND
                           +-- 1 uF -- GND
                           +-- top of 10 kohm 10-turn pot
pot bottom -- GND; pot wiper -- VTH; VTH -- 10 nF -- GND
```

For the `3296W-1-103LF`, connect pin 3 to the divider node, pin 1 to ground,
and pin 2 (wiper) to `VTH`. Clockwise rotation raises the threshold. Mark
`VTH + CW` on the silkscreen; the meter reading, not turns from an end stop,
defines the setting.

Begin at a measured `VTH = 100 mV`. With a 50 mV baseline, this is about
3.7 mV referred to `SIPM_RAW`; the real operating point comes from a threshold
scan, not pot rotation.

Provide a 1x2, 2.54 mm injection header: pin 1 is `INJECT` and reaches
`SIPM_RAW` through 499 ohm; pin 2 is ground. Mark both functions on both board
sides. Use it without an installed SiPM first. Verify generator level and
polarity on a scope before connecting it to a biased sensor.

Provide labeled probe points for `BIAS_27V`, `BIAS_LOCAL`, `+5VA`,
`+3V3_LOCAL`, `VBASE`, `SIPM_RAW`, `AMP_OUT`, `VTH`, `COMP_RAW`,
`TRIG_OUT`, `PEAK_HOLD`, `PEAK_OUT`, and `PEAK_RESET`, and close ground loops
at the fast analog and held-signal nodes.

## Power/interface circuit

### Power rails

The 5 V rail is required: it directly powers all eight TPH2502 amplifier
channels and the MAX5026 bias converter, and it feeds the TLV75533 regulator
that powers all four TLV3502 comparator channels and both trigger one-shots.
The approximate normal load becomes about 70 mA. A conservative design budget
is 150 mA, including analog quiescent current, the ADC, the bias converter,
dividers, tolerance, and bring-up margin.

| Load from the 5 V input | Typical | Conservative component allowance |
|---|---:|---:|
| Eight TPH2502 amplifier channels | 52 mA | 96 mA |
| Four TLV3502 comparator channels, through the LDO | 12.8 mA | 20 mA |
| Two SN74LVC1G123 one-shots, through the LDO | under 0.1 mA idle | 1 mA active allowance |
| MCP3202 ADC, through the LDO | under 0.6 mA active | 1 mA |
| MAX5026, bias load, LDO, and dividers | about 3 mA | 15 mA |
| **Expected / allocated total** | **about 70 mA** | **133 mA; use 150 mA budget** |

Use a regulated Phihong `PSAC05A-050L6-R` 5 V, 1 A, Class II wall adapter and a
Same Sky `PJ-102AH` board jack. The connection is center-positive; the adapter's
5.5 x 2.1 mm plug mates with the jack's nominal 2.0 mm center pin. Feed it
through:

```text
5 V input -> 500 mA resettable fuse -> SS14 Schottky
            -> +5VA_PRELINK -> 0 ohm current link -> +5VA
```

The adapter is specified at 5 V +/-5%; require 4.75-5.25 V at the jack under
load. Put 10 uF and 100 nF at `+5VA`. Fit a clearly marked 0 ohm 0805 current
link between `+5VA_PRELINK` and `+5VA`; do not omit it for space. A
`TLV75533PDBVR`, with its datasheet capacitors, generates
`+3V3_LOCAL`. The adapter's 1 A capability does not replace the on-board 500 mA
PTC. Before the heads are fitted, begin with a 100 mA current limit. With both
four-channel head front ends installed, use a 150 mA initial system limit and
increase it only when measured load justifies doing so.

Use a mostly unbroken ground plane on each PCB. The Class II detector supply is
floating until the detector is connected to the Cora; Pmod pins 5 and 11 then
provide the one intentional DC reference between detector ground and Cora
ground. The several head-cable ground wires are nearby returns on that same net,
not separately named grounds. Do not create split planes. An earth-referenced
oscilloscope can introduce another ground bond during testing, so connect its
ground deliberately and keep probe loops short.

Do not allow either board to back-power the other through the Pmod. Test with
the Cora off and detector on, then detector off and Cora on.

### SiPM bias supply

Use `MAX5026EUT+T` in the manufacturer's adjustable step-up topology.

`MAX5028` is not an equivalent fixed-value simplification. It replaces the
external feedback divider with an internal nominal 30 V setting, specified at
approximately 29-31 V. That can exceed the recommended 5 V overvoltage for a
24.2 V-breakdown SiPM and cannot be tuned for device or temperature variation.
The `MAX5026` retains the same 3-11 V input range but exposes the 1.25 V feedback
node. (`MAX5025` is also adjustable, but its 4.5 V minimum input gives less
margin after the input Schottky diode and 5 V source tolerance.)

| Function | Revision A value |
|---|---|
| Input bypass | 4.7 uF / 16 V X7R plus 100 nF |
| Inductor | 47 uH shielded, DCR <1 ohm, saturation current >=350 mA |
| Boost diode | 60 V Schottky, >=0.5 A pulse capability |
| Raw output | 2 x 1 uF / 50 V X7R, 1206 |
| Feedback top | 147 kohm, 0.1% |
| Feedback bottom | 6.98 kohm, 0.1%, 25 ppm/deg C, plus 500 ohm 10-turn rheostat |
| Distribution filter | 100 ohm, then 1 uF / 50 V and 10 nF / 100 V |
| Discharge | 1 Mohm from filtered bias to ground |

Wire the `3296W-1-501LF` as a fail-safe rheostat: pin 3 connects to the 6.98
kohm resistor; pins 1 and 2 are tied together and connect to ground. Clockwise
rotation then reduces the added bottom resistance and raises the bias. A lost
wiper contact leaves the full track rather than opening the feedback path.
The MAX5026 relation, including feedback-pin current, is approximately:

```text
VOUT = VFB * (1 + RTOP / RBOTTOM) + IFB * RTOP
```

With 147 kohm and 6.98 kohm, the nominal span is about 25.83 V at 500 ohm trim
and 27.59 V at zero trim, using typical 1.25 V `VFB` and 110 nA `IFB`. A 27.2 V
setpoint requires approximately 105 ohm of trim using typical feedback current,
before measurement corrections.

For the normal-operation upper bound, use `VFB = 1.288 V`, `IFB = 310 nA`, the
147 kohm resistor at +0.1%, the 6.98 kohm resistor at -0.1%, and opposing
25 ppm/deg C temperature drift from 21 deg C to the specified 0 deg C lower
limit. Treat the trimmer as 0 ohm in this maximum-output case; its resistance
and tolerance can only lower the output while its wiper remains intact. The
result is 28.54 V; use **28.55 V** as the documented bound over 0-40 deg C. At
0 deg C, a minimum specified 24.2 V breakdown shifted by the 21.5 mV/deg C
coefficient is about 23.75 V, leaving about 0.21 V below the recommended 5 V
maximum overvoltage.

This is a component-tolerance bound with the feedback path intact, not a clamp
or a single-fault guarantee. An open or shorted feedback part can still produce
an unsafe voltage. Start at maximum bottom resistance, measure with a
high-impedance meter, and set 27.2 V. Do not operate below 0 deg C without
recalculating the limit or lowering the measured bias, and never exceed the
individual part's measured breakdown plus 5.0 V.

Pull `SHDN` low with 100 kohm. Use a fitted 1x2, 2.54 mm header and removable
shunt: pin 1 is `SHDN`, pin 2 is `+5VA`, open is `BIAS OFF`, and shunted is
`BIAS ON`. Do not fit a board switch in revision A. Shutdown stops switching
but does not isolate the output; the inductor and diode can leave the output
near the input voltage. Always measure the rail and wait for the bleeder before
handling it.

The 1 Mohm bleeder discharges stored charge after the boost branch loses input
power; it does not eliminate diode feed-through while `+5VA` is present. At
27 V it draws only 27 uA, and at a fed-through 5 V it draws only 5 uA—far too
little to pull down a source that can deliver milliamps. With roughly 3-5 uF of
distributed nominal bias capacitance, the first-order discharge time constant
is roughly 3-5 seconds, subject to MLCC DC derating and connected heads. Measure
the real time to the chosen handling threshold.

Expose `HV_RAW`, `BIAS_27V`, `FB`, `SHDN`, and adjacent grounds. Keep the IC,
inductor, diode, and first output capacitor in a very small switching loop. Keep
LX copper small and route feedback away from LX and the inductor.

### Pulse-height ADC

Use one Microchip `MCP3202-BI/SN` in SOIC-8 on the power/interface board,
powered from a filtered copy of `+3V3_LOCAL`:

```text
+3V3_LOCAL -- 10 ohm -- +3V3_ADC
                         +-- 4.7 uF -- GND
                         +-- 100 nF -- GND, at MCP3202 pin 8

MCP3202 pin 1  CS/SHDN -- ADC_CS_N; 10 kohm to +3V3_ADC
MCP3202 pin 2  CH0 ----- ADC_A
MCP3202 pin 3  CH1 ----- ADC_B
MCP3202 pin 4  VSS ----- GND
MCP3202 pin 5  DIN ----- ADC_MOSI
MCP3202 pin 6  DOUT ---- ADC_MISO
MCP3202 pin 7  CLK ----- ADC_SCLK
MCP3202 pin 8  VDD ----- +3V3_ADC
```

The ADC supply is also its conversion reference. Pulse height must therefore be
calculated from the measured `+3V3_ADC` rail or a calibrated transfer, not from
an assumed exact 3.300 V reference. This is adequate for broad distributions
and detector comparisons; it is not a precision absolute-energy reference.

Each head output uses the following fixed attenuator and charge reservoir at
the ADC pins:

```text
head U3B -- 100 ohm -- PEAK_A/B cable -- 1.00 kohm --+-- ADC_A/B
                                                      +-- 1.65 kohm -- GND
                                                      +-- 1 nF C0G -- GND
```

The nominal end-to-end scale is `1.65 / (0.10 + 1.00 + 1.65) = 0.600`, so a
full-scale ADC code corresponds to about 5.5 V at the buffer for a 3.3 V ADC
rail. This keeps every valid TPH2502 output below the ADC input range even at
the allowed input-supply high limit. The nominal physical input step is about
1.34 mV per code at 3.3 V. Subtract each channel's post-reset baseline code from
its held code; do not assume the analog baseline is zero.

The divider's approximately 0.66 kohm Thevenin resistance and 1 nF reservoir
settle to 12-bit accuracy in about 5.5 us after a step. Wait at least 8 us after
the accepted coincidence edge before starting the first conversion. The local
TPH2502 buffer prevents the ADC divider, cable, and 20 pF ADC sample capacitor
from discharging `C_HOLD`; the 100 ohm head resistor isolates the buffer from
cable and reservoir capacitance. Verify U3B stability and the 8 us settling
allowance on both physical cable lengths.

Run the MCP3202 in single-ended mode with SPI mode 0,0 at no more than 900 kHz.
That clock is within the datasheet's 2.7 V limit and produces at most 50 ksps.
Allow 18 clocks per channel transaction and complete two separate channel
transactions; this ADC is multiplexed, not simultaneous-sampling. Two reads
therefore take about 40 us, but the locally held inputs make their timing
difference harmless if droop passes qualification. Do not lower the clock below
10 kHz during a transaction because the internal sample capacitor loses charge.

Put 4.70 kohm series resistors between JA and `ADC_CS_N`, `ADC_SCLK`,
`ADC_MOSI`, and `ADC_MISO`. Fan `PEAK_RESET` out through one separate 1.00 kohm
resistor per head. Keep the 10 kohm `ADC_CS_N` pull-up at the ADC so DOUT is
high impedance before FPGA configuration. Put 10 kohm pulldowns on the board
side of `ADC_SCLK` and `ADC_MOSI`, and a 100 kohm pulldown on the JA side of the
`ADC_MISO` series resistor; each head already has a 100 kohm `PEAK_RESET`
pulldown. These resistors limit unpowered-input current and define the otherwise
three-state MISO input, but do not replace the required detector-off/Cora-on and
detector-on/Cora-off back-power tests.

Implement `ADC_CS_N` as an open-drain-style FPGA pin: drive it low only during a
transaction and otherwise three-state it so the local 10 kohm resistor pulls it
high. Never actively drive it high. Together with idle-low SCLK/MOSI, high-Z
MISO, and the fail-safe/insulated reset inputs, this avoids a normal DC drive
from a powered Cora into an unpowered detector. The bidirectional off-state test
remains mandatory because FPGA configuration and protection structures still
need physical verification.

Initially, firmware may ignore the ADC and hold `PEAK_RESET` high continuously;
the comparator trigger path remains fully functional. ADC-enabled acquisition
applies only to accepted prompt coincidences. A delayed coincidence pairs the
current A edge with a B edge from 1 ms earlier, after the B hold has necessarily
been reset, so it remains an aggregate control count with no pulse-height
record. Prompt acquisition must use this sequence:

1. At startup, inhibit events, assert `PEAK_RESET` for at least 1 us, deassert
   it, wait at least 1 us, and then arm the coincidence engine.
2. On a first comparator edge, preserve the held peak while the normal
   coincidence window runs. If the window expires without a partner, inhibit
   new events, reset both holds for at least 1 us, release reset, wait at least
   1 us, and re-arm.
3. On an accepted coincidence, inhibit further event acceptance, wait at least
   8 us, read channel A and then B at 900 kHz or slower, and commit both codes
   with the coincident timestamp and trigger metadata. Continue monitoring both
   comparator edges while busy; if either channel fires again before the second
   sample is complete, mark the record contaminated and normally discard it,
   because the peak detector can update to the later, larger pulse.
4. Assert reset for at least 1 us, release it, wait at least 1 us, and re-arm.
   Account for the entire inhibited interval as dead time.

At the expected cosmic coincidence rate, the roughly 50 us ADC transaction and
reset dead time is negligible. It is not negligible during generator tests or
at an excessively low threshold, so firmware must count busy rejections and
busy-contaminated records, and software must include them in run metadata. If
either hold exceeds the measured pulse-height error budget across the complete
read interval, use the precision reset switch and/or a larger qualified
`C_HOLD`; do not hide the error with software ordering.

### Head cables

Use identical keyed JST XH, 10-position, straight-through cables and verify every
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
| 9 | `PEAK_OUT` | Buffered held peak, 0 V to `+5VA` |
| 10 | `PEAK_RESET` | Shared active-high reset from FPGA |

Use `B10B-XH-A` headers and `XHP-10` housings. Mark pin 1 on both PCB faces and
print the voltages at pins 1, 3, and 5. Do not use loose Dupont leads in the
finished instrument. Pins 1-8 deliberately retain the original assignment; the
two added slow signals do not replace any power or signal return. `PEAK_RESET`
is one central net fanned out through separate 1 kohm resistors to pins 10 of
both head connectors.

### Cora Z7 interface

Connect to JA using the Digilent `240-109` 6-inch 2x6 Pmod cable and its included
gender changer, with a 2x6, 2.54 mm male header on the power/interface board.
JA is unkeyed, so the continuity map, both mating views, pin-1 marking, and cable
strain relief are release-critical. Do not use loose flywires.

| Pmod pin | Connection |
|---:|---|
| 1 | `TRIG_A`, input to Cora |
| 2 | `TRIG_B`, input to Cora |
| 3 | `ADC_CS_N`, open-drain-style output from Cora |
| 4 | `ADC_SCLK`, output from Cora |
| 5, 11 | Ground |
| 6, 12 | No connect; Cora 3.3 V is not used |
| 7 | `ADC_MOSI`, output from Cora |
| 8 | `ADC_MISO`, input to Cora |
| 9 | `PEAK_RESET`, output from Cora |
| 10 | No connect; reserved 3.3 V I/O |

Place 10 kohm pulldowns at the two trigger inputs. The heads already provide
100 ohm trigger-source damping. Use the ADC-interface series and default-state
resistors specified above on pins 3, 4, and 7-9. Before mating boards, verify
ground continuity and verify that local 3.3 V is open-circuit to Pmod pins 6
and 12.

## PCB and mechanical rules

- Use two-layer, 1.6 mm FR-4, 1 oz copper and hand-assembly-friendly 0805
  passives; use 1206 where high-voltage capacitor performance benefits.
- Use exactly one root schematic per board for revision A; do not introduce
  hierarchical sheets during initial capture.
- Prefer a mostly unbroken ground plane. Do not create a split that forces
  return current around a gap.
- On the head, place sensor, cathode decoupling, sense/coupling parts, amplifier,
  comparator, peak detector, and connector in signal order. Keep raw,
  peak-hold, and feedback traces short.
- Separate `SIPM_RAW` and `AMP_OUT` from LX copper and trigger edges. Provide
  clearance around the bias rail and keep flux residue out of its feedback path.
- Keep `PEAK_HOLD` extremely small and clean. Place its capacitor, diode, reset
  part, and buffer input together, and keep it away from connector contamination
  and digital edges.
- Stop layout review for an ambiguous connector view, crossed ground return,
  long amplifier feedback path, large switch node, or unverified footprint.
- Design for the selected 50 x 50 x 10 mm block. Center the 6 mm SiPM on its
  polished 50 x 50 mm face with a thin, bubble-free optical-grease
  layer. Use a compliant clamp and hard stops for gentle, repeatable pressure;
  do not make the SiPM package the structural stop. Wrap the other surfaces
  first in reflective material, then in a fully opaque layer; electrically
  insulate conductive foil from the PCB. Do not rely on tape tension to load
  the package.
- Start with 50 mm paddle separation in a rigid, repeatable frame; preserve an
  adjustment range of 50-250 mm and the angle reference specified below.

### Mechanical interface control

All dimensions in this section are millimetres. PCB coordinates are viewed
from the component side, with the lower-left corner of the outline's bounding
box at `(0, 0)`, `+X` to the right, and `+Y` away from the cable-exit edge.
The component side is KiCad's front side and faces away from the scintillator;
the optical side is KiCad's back side. Board-edge and hole dimensions are
frozen; component placement may move only within the resulting envelope and
the electrical layout rules above.

#### Detector-head PCB

| Feature | Revision A geometry |
|---|---|
| Outline | 70.0 x 70.0 rectangle with 2.0 corner radii |
| Mounting holes | Four 3.2 NPTH holes at `(5,5)`, `(65,5)`, `(5,65)`, and `(65,65)`; no copper within 1.0 of each finished hole |
| Scintillator projection | Bare 50.0 x 50.0 block centered on the board, nominally `X=10..60`, `Y=10..60` |
| SiPM | Back/optical-side footprint with active-area center at `(35,35)`; in the component-side coordinate view, pad 1 lies in the `X<35, Y>35` quadrant and pad 3 lies in the `X>35, Y<35` quadrant, matching the manufacturer's bottom view |
| Other components | Component side only; no other package or solder joint may protrude from the optical side inside the scintillator projection |
| `HEAD` connector | `B10B-XH-A`, component side, body centered at `(35,8)`, ten-pin axis along X; pin 1 at `(23.75,8)` |
| Head cable exit | Mate normal to the component side, then bend and strain-relieve toward `-Y`; keep the cable outside the active 50 x 50 aperture |

Put unambiguous `OPTICAL SIDE`, `COMPONENT SIDE`, pin-1, and rail markings on
both PCB faces. On the component-side view, orient the JST molded face
toward `+Y`. The pin-1 end and electrical cable table control if a library
graphic or 3D model uses a different visual convention.

The SiPM is the only optical-side component. Transition each required SiPM pad
to the component side immediately beside its land; place the cathode bypass,
sense resistor, coupling capacitor, and their returns directly behind the
sensor before continuing through the signal chain. The pin-5 mechanical paddle
still has no copper, paste, or solder.

#### Power/interface PCB

| Feature | Revision A geometry |
|---|---|
| Outline | 96.0 x 64.0 rectangle with 2.0 corner radii |
| Mounting holes | Four 3.2 NPTH holes at `(4,4)`, `(92,4)`, `(4,60)`, and `(92,60)`; no copper within 1.0 of each finished hole |
| `HEAD_A` | `B10B-XH-A`, component side, body centered at `(62,50)`, ten-pin axis along Y, pin 1 at `(62,61.25)` |
| `HEAD_B` | `B10B-XH-A`, component side, body centered at `(82,50)`, ten-pin axis along Y, pin 1 at `(82,61.25)` |
| Pmod | `TSW-106-08-G-D-RA` with its mating-face plane at `X=96`, centerline `Y=18`, six-position axis along Y, and cable projecting beyond `+X`; derive hole offsets from the Samtec drawing |
| Barrel jack | `PJ-102AH` with its plug-entry plane at `X=0`, centerline `Y=18`, and plug projecting beyond `-X`; derive hole offsets from the Same Sky drawing |
| Head cable exit | Mate normal to the component side, then bend both bundles toward `+Y`; reserve 25 clear normal to the board above the connector bodies for housing and bend relief |
| Pmod strain relief | Restrain the cable or gender changer to the fixed central-board carrier within 25 of the `+X` edge; the header is not the structural restraint |

Place the power-entry and boost islands in the left half, the head-distribution
connectors in the upper-right, and the Pmod interface in the lower-right. Keep
the boost switch node out of the head-connector and Pmod regions. Mount this
board component-side up on at least 6.0 standoffs using the 88 x 56 hole pattern.
Orient both JST molded faces toward `+X`; their pin-1 ends are toward `+Y` as
given by the coordinate table.

The unkeyed Pmod requires three consistent views: the schematic pin table, the
component-side footprint view, and the view looking into the mated cable. Put a
filled pin-1 triangle on both PCB faces. Following Digilent's nonstandard male
peripheral numbering, pads 1 through 6 occupy the inboard (`-X`) row from `+Y`
to `-Y`, and pads 7 through 12 occupy the outboard (`+X`) row in the same
direction. The archived Digilent specification controls this numbering; the
continuity-mapped `240-109` cable and gender changer must confirm the two mating
views before release. A failed continuity check corrects the drawing or
assembly instructions, not the fixed JA net assignment.

Implement ordinary signal test points as 2.0 diameter component-side exposed
copper pads. At `SIPM_RAW`, `AMP_OUT`, `COMP_RAW`, `TRIG_OUT`, `PEAK_HOLD`,
`PEAK_OUT`, `HV_RAW`, and `BIAS_27V`, add a ground-loop footprint within 5.0:
two 1.0 plated holes on 5.0 pitch fitted with a short formed solid-wire loop.
Use cut sections of the selected 2.54 mm breakaway header for `INJECT` and
`BIAS ENABLE`; do not invent another connector family during capture.

#### Optical carrier and adjustable frame

Each head uses the PCB's 60 x 60 mounting-hole pattern as its only interface to
a removable carrier. The carrier centers a nominal 50.0 x 50.0 block on the
SiPM axis and uses a 52.0 x 52.0 nominal replaceable pocket with compliant side
retention, allowing 1.0 nominal wrap thickness per side. If the inspected and
wrapped seller-cut block does not fit that pocket, change only the replaceable
carrier insert; do not move the PCB sensor, holes, or connector.

The carrier has four adjustable hard-stop lands concentric with the PCB holes.
Set the stopped distance from the polished scintillator face to the PCB optical
side to the measured installed SiPM height plus `0.05 +/- 0.03`. Light springs
or compliant washers keep the PCB seated on those stops; the stops, not the
SiPM package, carry clamp load. Fill the resulting nominal 0.05 optical gap
with a thin, bubble-free EJ-550 layer. Cut a centered 7.5 x 7.5 opening in the
reflective and opaque layers at the sensor and electrically insulate any
conductive reflector from the PCB.

Install the upper and lower modules with their polished/sensor faces pointing
outward, so both component sides and cable exits face away from the coincidence
aperture. Define paddle separation as the distance between scintillator
midplanes. The parallel-position carriage must lock from 50 to 250 separation;
use 50 for first measurements. Its zero-angle datum is parallel faces with the
two SiPM/scintillator centers coaxial. Any angle stage rotates about the moving
scintillator center, covers at least `-60` to `+60` degrees, and provides fixed
marks at 0, 15, 30, 45, and 60 degrees in both directions with 1 degree or
better readback. Record center-to-center distance and signed angle for every
nonparallel run.

## FPGA and data path

The purchased Cora Z7-07S uses `XC7Z007S-1CLG400C`. Its direct PL clock is
125 MHz on H16, and its official constraints map JA[0] to Y18 and JA[1] to Y19.
Use the archived 07S master XDC; do not substitute the Cora Z7-10 constraints.

```tcl
set_property -dict { PACKAGE_PIN H16 IOSTANDARD LVCMOS33 } [get_ports { clk }]
create_clock -add -name sys_clk_pin -period 8.000 -waveform {0 4.000} [get_ports { clk }]
set_property -dict { PACKAGE_PIN Y18 IOSTANDARD LVCMOS33 } [get_ports { pulse_a_async }]
set_property -dict { PACKAGE_PIN Y19 IOSTANDARD LVCMOS33 } [get_ports { pulse_b_async }]
set_property -dict { PACKAGE_PIN Y16 IOSTANDARD LVCMOS33 } [get_ports { adc_cs_n }]
set_property -dict { PACKAGE_PIN Y17 IOSTANDARD LVCMOS33 } [get_ports { adc_sclk }]
set_property -dict { PACKAGE_PIN U18 IOSTANDARD LVCMOS33 } [get_ports { adc_mosi }]
set_property -dict { PACKAGE_PIN U19 IOSTANDARD LVCMOS33 } [get_ports { adc_miso }]
set_property -dict { PACKAGE_PIN W18 IOSTANDARD LVCMOS33 } [get_ports { peak_reset }]
```

JA[7] on W19 remains reserved. Do not drive it or reuse it without revising the
Pmod table, XDC, schematic, and this specification together.

Each input needs a two-flop `ASYNC_REG` synchronizer followed by rising-edge
detection. Count 64-bit A singles, B singles, prompt and delayed coincidences,
free-running FPGA ticks, and enabled live ticks. A first edge opens a one-sided
window in which the other edge is accepted; simultaneous edges count once. The
default maximum edge separation is 13 cycles, or 104 ns at 125 MHz. Use 63
cycles (504 ns) for first hardware tests, then shorten it after measuring the
relative path latency. An accepted coincidence starts a 125-cycle lockout;
singles continue counting.

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
capture of a pulse shorter than one destination clock. The populated one-shot
therefore targets 150-250 ns at `TRIG_OUT`; the 24 ns requirement applies only
if the direct-output assembly option is deliberately selected later.

The default one-shot deliberately replaces comparator pulse width with a fixed
nominal 200 ns trigger. FPGA measurements of that width are path diagnostics,
not analog time-over-threshold. True comparator ToT is unavailable in the
default assembly. It may be added later only by qualifying `COMP_RAW` at 24 ns
or longer over the full operating range, selecting the mutually exclusive
direct link, and revising firmware and this document; the pulse-height upgrade
does not relax that gate.

The minimum useful data path is not just RTL counters:

1. Validate counters and timing with synthetic pulses, simulation, and an ILA.
2. Expose coherent snapshots and controls through AXI-Lite to the Zynq PS.
3. Emit a one-second CSV summary over the existing USB/UART connection.
4. Add an event FIFO before enabling pulse-height event logging; per-event ADC
   samples cannot be represented by aggregate one-second counters.

The version-1 register contract below remains the comparator-only first target
and may ignore the ADC. ADC-enabled firmware is a later, reviewed interface
revision. It must atomically enqueue at least the 64-bit accepted-coincidence
tick, both raw 12-bit ADC codes, conversion/reset status, and a sequence number;
expose FIFO overflow, busy-rejection, and busy-contamination counts; and
preserve enough metadata to apply channel baselines and the measured ADC scale
offline. Do not silently append samples to the summary CSV, and do not label the
fixed one-shot width as ToT. A true ToT field is permitted only after the direct
comparator path passes the qualification stated above.

### AXI-Lite register contract

Use a 32-bit, word-aligned AXI-Lite slave. Multiword counters are coherent
because software reads only the latched snapshot bank, low word first. Reserved
bits read zero and writes to them have no effect.

| Offset | Access | Register and revision A behavior |
|---:|:---:|---|
| `0x00` | RO | `DESIGN_ID = 0x4D554F4E` (`MUON`) |
| `0x04` | RO | `VERSION = 0x00010000` (major 1, minor 0) |
| `0x08` | RW | `CONTROL`: bit 0 `ENABLE` |
| `0x0C` | WO | `COMMAND`: bit 0 `SNAPSHOT`, bit 1 `CLEAR`; write-one pulses |
| `0x10` | RO | `STATUS`: bit 0 enabled, bit 1 delay valid, bit 2 snapshot valid, bit 3 configuration error |
| `0x14` | RW | `WINDOW_CYCLES`, default 13; valid 1-65535 while disabled |
| `0x18` | RW | `LOCKOUT_CYCLES`, default 125; valid 0-65535 while disabled |
| `0x1C` | RO | `DELAY_CYCLES = 125000` |
| `0x20` | RO | `SNAPSHOT_SEQ`, increments after each atomic snapshot |
| `0x28/2C` | RO | snapshot `FPGA_TICKS`, low/high; free-running from PL reset |
| `0x30/34` | RO | snapshot `LIVE_TICKS`, low/high; increments while enabled |
| `0x38/3C` | RO | snapshot `SINGLES_A`, low/high |
| `0x40/44` | RO | snapshot `SINGLES_B`, low/high |
| `0x48/4C` | RO | snapshot `PROMPT_COINC`, low/high |
| `0x50/54` | RO | snapshot `DELAYED_COINC`, low/high |
| `0x58` | RW1C | `ERROR_FLAGS`: bit 0 rejected command or configuration write |

All event and live counters are unsigned 64-bit wrapping counters. `CLEAR` is
accepted only while disabled; it clears those counters, snapshot state, and
delayed history, but not `FPGA_TICKS`. Configuration writes while enabled or
out of range are ignored and set the sticky error bit. A `SNAPSHOT` command
copies all counters on one clock edge and then increments `SNAPSHOT_SEQ`.

Define the prompt window by edge separation: with `WINDOW_CYCLES = 13`, two
edges separated by 0 through 13 clocks are accepted and 14 clocks is rejected.
After an accepted pair, each coincidence engine rejects new pairs for the next
`LOCKOUT_CYCLES` complete clocks. Singles counting continues during lockout.

### Delayed coincidence and logging

Implement a 125,000-bit circular memory clocked at 125 MHz with explicit
read-before-write behavior. Each enabled clock writes the synchronized channel-B
edge bit and reads the bit written exactly 125,000 clocks earlier. After the
1 ms fill interval, that bit becomes
`B_DELAYED`. Compare channel A with `B_DELAYED` using a second copy of the same
window logic and its own lockout. This fixed-memory method has no timestamp-FIFO
overflow mode. The 1 ms offset is much larger than the prompt window, so the
delayed pairs cannot be physical prompt partners.

For each run, software performs this fixed sequence:

1. Disable, clear, configure the window and lockout, then enable.
2. Wait for `STATUS.delay_valid`, take an atomic baseline snapshot, and discard
   counts before that baseline.
3. Once per second, request a snapshot, wait for `SNAPSHOT_SEQ` to change, and
   compute unsigned modulo-64-bit deltas from the preceding snapshot.
4. Stop on a sticky error or an unexpected reset/version/sequence change.

The CSV columns are `utc_time`, `snapshot_seq`, `fpga_ticks`, `live_ticks`,
`singles_a`, `singles_b`, `prompt_coinc`, and `delayed_coinc`. `utc_time` is the
host's ISO-8601 UTC time at the end of the interval; `fpga_ticks` is the absolute
snapshot value; the remaining counters are interval deltas. Run metadata records
board and firmware revisions, actual clock/window/lockout/delay, measured bias
and thresholds, temperature, paddle separation and angle, location label, and
notes. ADC-enabled runs additionally record reset variant, fitted `R_CHG` and
`C_HOLD`, measured `+3V3_ADC`, channel baseline/scale calibration, read order,
busy rejections, contaminated records, and FIFO overflow state. Bias, threshold,
temperature, angle, and separation are manually measured in revision A; do not
present them as FPGA telemetry.

For asynchronous singles rates `R_A` and `R_B`, the initial accidental estimate
for a one-sided window `tau` is `R_acc ~= 2 R_A R_B tau`; prefer a delayed-window
measurement made with the same window width.

## Feasibility and remaining design gates

The local analog front end, 3.3 V push-pull triggers, and 125 MHz coincidence
logic form a feasible low-rate prototype. Expected current is far below the
500 mA input protection and LDO rating. A close-geometry CosmicWatch v3X system
using the same 50 x 50 x 10 mm scintillator geometry measured roughly 0.315
coincidences/s, but threshold, optical coupling, separation, and overburden all
differ. Treat that rate as a comparison, not a guarantee. Begin at 50 mm
separation and plan hours, not minutes, for controlled comparisons.

The design is not ready to order until all of these are resolved in KiCad and
bench/review evidence:

- exact SiPM footprint and orientation;
- boost switch-loop and feedback layout;
- connector mating views, cable map, and Pmod mechanical support;
- detector/Cora off-state and back-power behavior;
- raw comparator input width, stretched trigger width, and FPGA capture margin;
- peak acquisition error versus real `AMP_OUT` width for the allowed
  `R_CHG`/`C_HOLD` stuffing matrix, including reset residue and droop through
  the end of the second ADC read;
- U3B cable/ADC settling and stability, ADC transfer calibration, and both
  reset-switch assembly variants actually intended for use; and
- a working PS-to-host summary logger with coherent counter snapshots.

Solderless breadboard tests are appropriate for the threshold divider,
references, and safe 0-3.3 V FPGA pulses. Use a compact PCB or manufacturer
adapter for the boost supply, SiPM node, and high-speed amplifier; breadboard
waveforms are not representative there.

## Primary sources

Part, connector, and board documentation is archived and mapped to exact
manufacturer numbers in [`docs/datasheets/README.md`](datasheets/README.md).
Background references remain the [CosmicWatch v3X paper](https://arxiv.org/html/2508.12111)
and [reference repository](https://github.com/spenceraxani/CosmicWatch-Desktop-Muon-Detector-v3X).
Tool behavior follows the [KiCad 9.0 CLI documentation](https://docs.kicad.org/9.0/en/cli/cli.html).
