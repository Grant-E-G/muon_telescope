# Build, validation, and debugging

This is the working checklist for revision A. Stop at a failed gate; later
stages depend on earlier measurements. Record instrument serials, board/firmware
commit, actual voltages, scope settings, and photographs in the run notes rather
than creating a separate form for every test.

## Before buying remaining parts or ordering boards

- [x] Purchased two seller-cut BC-408 blocks, approximately 50 x 50 x 10 mm,
  seller model `BC408-505010-1FP`, with one 50 x 50 mm face polished.
- [x] Provenance concern resolved: the seller describes these as virgin BC-408
  water-saw cut from a large block rather than reclaimed material.
- [ ] On receipt, verify two matched, undamaged 50 x 50 x 10 mm blocks; identify
  the polished face; photograph their condition; and resolve a material,
  geometry, or finish mismatch before assembly.
- [ ] Measure or obtain the breakdown-voltage marking/data for each SiPM.
- [x] Purchased board confirmed as Cora Z7-07S; use and review the archived 07S
  master XDC.
- [ ] Verify every BOM line against stock, lifecycle, package, and distributor
  listing on the purchase day.
- [x] Every currently selected planning-BOM part is mapped to its primary
  document in `docs/datasheets/README.md`; recheck when any part changes.
- [ ] Create both KiCad 10.0.5 projects and project-local library tables.
- [ ] Check the SiPM symbol, footprint, orientation, and no-solder center paddle
  independently against the current datasheet and physical part.
- [ ] Add unambiguous top- and bottom-side pin-1/mating markings to all headers.
- [ ] Print each unusual footprint and connector at 1:1.
- [ ] Run ERC/DRC and `make check`; explain rather than hide any exception.
- [ ] Complete every fabrication-release item near the end of this document.

The expected work sequence is not one continuous weekend. First complete
schematic/layout review and synthetic FPGA tests; then allow for fabrication and
parts lead time; then bring up power, injected analog pulses, SiPMs, and finally
cosmic-ray measurements as separate gates.

## Stage 1: firmware with no detector attached

Use a scope-verified 0-3.3 V pulse source; never put 5 V logic on JA.

- [ ] Simulate A-only, B-only, simultaneous, last-legal-cycle, first-illegal-
  cycle, long-pulse, reset, clear, lockout, snapshot, and rollover cases.
- [ ] Verify the 125 MHz clock and the exact Cora variant's JA pin constraints.
- [ ] Drive A only, B only, split one pulse to both, then introduce a known
  relative delay.
- [ ] Confirm singles equal source pulses and a long input produces one edge.
- [ ] Confirm the 504 ns bring-up and 104 ns normal window boundaries.
- [ ] Verify a 13-cycle edge separation is accepted, 14 is rejected, and the
  prompt and delayed engines have independent 125-cycle lockouts.
- [ ] Verify the 125,000-clock read-before-write delay memory, its 1 ms valid
  transition, reset/refill behavior, and comparison against a software model.
- [ ] Confirm coherent AXI-Lite snapshots and one-second host CSV output.
- [ ] Exercise every documented register, rejected configuration writes,
  sticky-error clearing, atomic 64-bit rollover snapshots, and sequence changes.
- [ ] Leave both inputs low when disconnected; investigate any idle counts.

Gate: the logged counts must agree with generator counts and timing cases before
a detector cable is connected.

## Stage 2: power/interface assembly

Assemble by functional island so a bad rail cannot damage every IC.

1. Fit the barrel jack, PTC, reverse diode, input capacitors, and current link.
   Before plugging it in, verify the adapter is center-positive and 4.75-5.25 V.
   Apply current-limited 5 V and verify `+5VA`, input current, and heating.
2. Fit the LDO and its capacitors. Verify 3.3 V at no load and with a temporary
   30 mA load.
3. Fit the MAX5026 island without installing either SiPM. Set the 500 ohm trim
   to maximum bottom resistance, leave `SHDN` low, and inspect resistance/diode
   orientation before power.
4. Enable bias with a 100 mA initial input limit. Set `BIAS_27V` to 27.2 V with
   a high-impedance meter. Verify the complete approximate 25.8-27.6 V nominal
   adjustment range and confirm the measured maximum remains below 28.55 V,
   without exceeding breakdown plus 5.0 V for the lowest-breakdown sensor.
5. Measure startup, shutdown, `HV_RAW` ripple, filtered bias ripple, bleeder
   discharge, and residual disabled voltage. Do not assume "disabled" is 0 V.
6. With the Cora off, detector on, verify no Pmod supply pin is driven. Repeat
   with detector off and Cora on.

Gate: stable rails, acceptable ripple/temperature, no back-power, and a measured
discharge time must be recorded before attaching a head.

## Stage 3: each detector head without a SiPM

Fit power, TPH2502, TLV3502, SN74LVC1G123, passive networks, headers, and test
points. Fit `R_STRETCH` and leave `R_DIRECT`, the SiPM, and other DNP parts
absent.

- [ ] Continuity-map the head cable pin 1 to pin 1 and verify adjacent ground
  returns. Label that cable; do not rely on wire color alone.
- [ ] Verify connector voltages at the unplugged cable: bias, ground, `+5VA`,
  ground, 3.3 V, ground, inactive trigger, ground.
- [ ] Power the head at a conservative current limit. Check 3.3 V, `VBASE` near
  50 mV, `AMP_OUT` baseline, and the approximately 0-0.53 V threshold range.
- [ ] Inject a low-rate pulse through 499 ohm. Observe `SIPM_RAW`, `AMP_OUT`,
  comparator output, and the far end of the trigger cable using short probe
  grounds.
- [ ] Confirm gain, polarity, threshold behavior, hysteresis, trigger amplitude,
  and ringing. Confirm `COMP_RAW` is at least 3 ns and `TRIG_OUT` is 150-250 ns.
- [ ] Confirm the Cora counts injected singles and coincidences through each
  complete head/cable/channel path.

Gate: both heads pass the same injection limits without optional clamp or
hysteresis parts unless measurements justify and document those changes.

## Stage 4: SiPM and optical assembly

Handle the SiPM with ESD controls. Clean the footprint, inspect under
magnification, align pin 1, solder only the allowed pads, and confirm that the
pin 4 terminal is soldered to ground and the pin 5 paddle has no solder bridge
or paste.

With the assembly dark and the bias disabled:

- [ ] Check resistance from bias to ground and inspect all sensor joints.
- [ ] Set bias to measured breakdown plus about 2.5 V, never above breakdown
  plus 5.0 V and never by trimmer position alone.
- [ ] Enable at a conservative current limit while watching supply current.
- [ ] Observe dark pulses at `SIPM_RAW` and `AMP_OUT`; illuminate only weakly and
  briefly to confirm the response direction.
- [ ] Couple the sensor at the center of the polished 50 x 50 mm face with a thin,
  bubble-free grease layer. Verify the compliant clamp's hard stops provide
  gentle, repeatable pressure. Add reflective wrap, then a fully opaque layer.
- [ ] Compare a covered dark rate before and after pressing, wrapping, and cable
  movement; mechanical motion must not create an apparent detector signal.

Gate: stable dark operation, a reproducible light response, and a passing light-
leak test for each complete head.

## Stage 5: instrument validation

Use 50 mm separation first. Record actual thresholds, bias, ambient or head
temperature, geometry, window, firmware commit, and live time for every run.

1. **Flashlight leak test:** cover the assembled head and move a flashlight over
   seams without shining into exposed electronics. The count rate must not track
   the light.
2. **Threshold scan:** at fixed bias and temperature, measure both singles,
   prompt, and delayed rates over a safe threshold range. Select a stable region,
   not simply the highest rate.
3. **Bias scan:** at fixed measured threshold and temperature, step overvoltage
   conservatively. Stop for excessive current, noise, or instability.
4. **Prompt/delayed control:** implement a delay much longer than physical
   correlation, such as 1 ms, with the same window width and nonoverlapping
   sample. Prompt should significantly exceed delayed in aligned geometry.
5. **Alignment control:** collect equal-live-time aligned and deliberately
   offset runs. Aligned prompt coincidence should be higher.
6. **Angle/transmission:** only after the controls pass, use a rigid angle and
   separation reference. Bracket each changed condition with open-reference
   runs and quote Poisson plus observed drift uncertainty.

Useful data is not scheduled until synthetic-pulse, dark, and light-leak tests
have passed. Depending on acceptance, stable comparisons can require hours or a
day per point.

## Pre-populated debugging checklist

Start at the leftmost failing stage and change one variable at a time. Use a
spring-ground or ground blade on fast analog probes; a long clip lead can create
the ringing it appears to diagnose.

| Symptom | Check first | Likely failure and action |
|---|---|---|
| No input power or immediate PTC trip | Unplug; verify adapter voltage, center polarity, and jack contacts | Wrong adapter, barrel-size/contact mismatch, reversed polarity, or board short; do not bypass the PTC |
| No `+5VA` | Input polarity, PTC drop, SS14 orientation | Reversed connector/diode, tripped PTC, or short; remove power and resistance-check rails |
| Excess input current | Rail resistance and thermal image/finger-safe inspection | Solder bridge, reversed IC, fighting 3.3 V sources; isolate one functional island |
| 3.3 V wrong | LDO pinout, input/output capacitors, unloaded rail | Wrong footprint orientation, short, unstable/incorrect capacitor |
| No high-voltage bias | `+5VA`, `SHDN`, LX, diode, FB | Disabled converter, reversed diode, open feedback, wrong MAX5026 pinout |
| Bias high, above 28.55 V, or trim reversed | Power off; measure 147k, 6.98k, trimmer end-to-end, and wiper | Wrong value, open feedback, or reversed trimmer; never "trim through" an unexplained overvoltage |
| Bias remains near 5 V when disabled | Compare to input and watch discharge | Normal path through inductor/diode plus stored charge; shutdown is not isolation |
| Large 500 kHz bias ripple | Compare `HV_RAW`, bus, and head cathode with short ground | Poor switch loop/filter return, misplaced capacitor, MLCC DC derating, or probe pickup |
| Rail changes when a head is plugged in | Verify all eight cable positions before retry | Mirrored/offset JST housing, connector view error, head short |
| Cora powers while nominally off | Check Pmod pins 6/12 and trigger protection path | Local 3.3 V tied to Pmod or I/O back-power; disconnect and correct before use |
| `VBASE` absent or noisy | Divider midpoint and U2B input/output | Wrong divider, op-amp orientation, capacitive follower load, or supply oscillation |
| No injected amplifier pulse | Probe both sides of coupling cap and U2A pins | Missing 499 ohm DC path, wrong feedback, pulse polarity/level, bad ground reference |
| Gain is wrong | Measure input at PCB, baseline, and resistor values | Generator 50 ohm amplitude convention, loading, swapped 1k/12.4k, clipping |
| Amplifier rings/oscillates | Shorten probe ground; remove external cable; inspect supply | Probe artifact, long feedback loop, poor decoupling; populate feedback C only from measured evidence |
| Comparator always high | Compare `AMP_OUT` baseline to measured `VTH` | Threshold below baseline or comparator inputs reversed |
| Comparator never fires | Lower `VTH` safely and probe comparator pins | Wrong polarity, missing supply, insufficient gain, clamped input, wrong package orientation |
| Multiple trigger edges per pulse | Observe analog and digital together | Threshold chatter/ringing; fix layout/noise before optional external hysteresis |
| `COMP_RAW` works but `TRIG_OUT` does not | Check one-shot supply, A low, CLR high, B input, timing parts, and selection links | Wrong DCT pinout, missing 2k/27pF, `R_STRETCH` open, or both selection links fitted |
| Stretched trigger outside 150-250 ns | Measure 2k and 27pF; probe one-shot timing pins with low capacitance | Wrong timing value, excessive probe capacitance, solder fault, or incorrect footprint |
| Trigger good at head, bad at Cora | Scope both cable ends; continuity-map pins | Cable mapping, missing common ground, Pmod rotation, connector ringing |
| FPGA counts an unplugged input | Measure pulldown and actual JA pin | Missing 10k pulldown, wrong constraint, EMI, floating ground |
| FPGA misses visible pulses | Measure `COMP_RAW`, `TRIG_OUT`, and both Pmod ends against the 8 ns clock | One-shot not selected, trigger below 150 ns, cable fault, wrong pin constraint, or synchronizer/edge-detector bug |
| One physical pulse counts repeatedly | Compare synchronized level and edge pulse | Level counting instead of rising-edge counting, bad synchronizer, or clear logic |
| False event at reset/clear | Simulate and observe input level during command | Edge detector history not reset coherently or clear applied while high |
| Singles work, no injected coincidence | Split one source, use 504 ns window, inspect timestamps | Channel swap, window boundary bug, lockout bug, unequal path delay |
| Injected coincidence works, cosmic does not | Threshold, optical coupling, geometry, sensor response | Misalignment, light collection, window too short, excessive threshold |
| Prompt equals delayed | Verify delay implementation, raise threshold, reduce noise | Accidentals dominate, light leak, delayed samples overlap, or no real common events |
| Delayed count invalid or discontinuous | Check delay-valid status, snapshot baseline, reset history, and sticky errors | Logging started before the 1 ms fill, delay memory is not read-before-write, or configuration changed while enabled |
| Rate follows room light | Move flashlight over every seam | Incomplete opaque wrap or light through cable/PCB opening |
| Rate changes with temperature | Record temperature and measured bias | SiPM breakdown/gain drift; compare equal-temperature runs or add future compensation |
| Two heads differ strongly | Swap complete head cables at central board | If fault follows head: optics/analog; if it stays: cable/central/FPGA channel |
| Rate changes when touching/moving cable | Observe raw and trigger while flexing | Poor shield/return, intermittent crimp, microphonic coupling, loose optical pressure |
| Implausible rate or live time | Compare source counter, wall time, snapshots, overflow | Noncoherent reads, counter rollover, wrong clock, lockout included incorrectly |

## Safety and handling

- Treat the bias as an energy-storage and component-damage hazard even though
  its nominal voltage is below common shock-hazard thresholds.
- Never hot-plug heads or the Pmod. Disable bias, remove 5 V, wait for the
  bleeder, and measure the rail before touching the sensor or cable.
- Use current limiting for every first power-up. Do not bypass the PTC to make a
  fault disappear.
- Never exceed measured SiPM breakdown plus 5.0 V. Bright light at full bias can
  cause excessive current; begin dark.
- Use ESD controls and avoid force or solder under the SiPM center paddle.
- Support the power/interface board mechanically; the unkeyed Pmod connector is
  not a structural bracket.

## Fabrication release gate

Schematic and libraries:

- [ ] `docs/design.md`, schematic values, net names, and BOM agree.
- [ ] Every IC pin and connector mating view matches a current primary source.
- [ ] Every selected part has its available primary documentation and exact-MPN
  mapping under `docs/datasheets/`.
- [ ] SiPM pin 2 has no-connect/no trace, pin 4 has its short ground connection,
  and pin 5 has no copper/paste/solder.
- [ ] Unused IC channels, Pmod inputs, `SHDN`, and trimmer failure state are
  defined.
- [ ] Each head has `R_STRETCH` fitted and `R_DIRECT` absent; the one-shot timing
  path and its test points match `docs/design.md`.
- [ ] Power flags and intentional ERC exceptions are reviewed and documented.
- [ ] Test points support every staged measurement above.

Layout and mechanics:

- [ ] SiPM and all unusual footprints pass independent datasheet, 1:1 print,
  and physical-part review.
- [ ] Boost loop/LX, feedback divider, head analog path, decoupling, and ground
  returns pass independent visual review.
- [ ] High-voltage clearance and capacitor voltage/DC-bias ratings are checked.
- [ ] Connector orientation, reverse-side pin 1, rail labels, mounting holes,
  and Pmod support are unambiguous.
- [ ] Board outline and critical dimensions fit the mechanical model.
- [ ] DNP parts and alternate sense-resistor stuffing are identified on assembly
  drawings.

Outputs and order:

- [ ] KiCad 10.0.5 ERC and DRC, including schematic parity, pass or have reviewed
  written exceptions.
- [ ] Gerber, drill, outline, solder-mask, paste, silkscreen, and copper layers
  are inspected in an independent viewer.
- [ ] BOM manufacturer numbers, packages, quantities, and stock are rechecked.
- [ ] Pick-and-place origin/rotation is checked if assembly is outsourced.
- [ ] The complete release package records the exact source commit, is reviewed
  by the second person, and that commit is tagged before ordering.
