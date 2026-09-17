# Muon Telescope Power / Interface PCB — Rev A1 Routing Review

## Decision

Do not fabricate the original `power_interface.kicad_pcb` unchanged. Its
overall topology is reasonable, but 62 distinct same-net contacts depend on
the copper widths overlapping even though the track centerlines do not meet.
Twenty-seven of those contacts had less than 0.10 mm of copper-overlap margin;
several were tangent contacts with effectively zero margin. Two of the
zero/low-margin cases are on `+3V3_ADC` and `+5VA`, so an etch or geometry
edge case could become a functional open circuit.

The Rev A1 board repairs all 62 contacts with 89 short, explicit bridge
segments. No footprint, pad, via, zone, board-outline, schematic, or existing
track was moved or deleted.

## What looks strange but is electrically reasonable

- The long diagonal `BIAS_27V` route is after the 100 ohm / capacitor output
  filter. It is low-current DC distribution, not the MAX5026 switching node.
- The long `+5VA` and `+3V3_LOCAL` routes are 0.6 mm wide. At the declared
  150 mA and 25 mA loads, respectively, their DC loss is not a concern.
- The horizontal tracks between HEAD A and HEAD B distribute common bias and
  power rails. The interleaved ground pins give each signal a nearby return.
- `PEAK_A` and `PEAK_B` are buffered peak-hold outputs in the supplied
  validation model, not raw SiPM avalanche pulses. Their route lengths are
  therefore much less concerning than the screenshot initially suggests.
- Free-angle track geometry is cosmetically unusual but is not, by itself, an
  electrical or PCBWay fabrication problem.

## Positive checks

- Two copper layers, with a board-wide `GND` zone on `B.Cu`.
- 69 total vias, including 37 ground vias.
- Explicit no-copper keepout under L1.
- `LX` is confined to 3.52 mm of 0.5 mm track.
- The MAX5026 input bypass, switch path, diode, first output capacitor, and
  feedback components are locally placed.
- All 12 placement/proximity checks in `validation.json` pass.
- All expected connector and mounting-hole positions match the supplied
  validation coordinates exactly.
- Independent geometry checking found no different-net track-to-track
  clearance violations at 0.20 mm and no definite track-to-pad shorts.
- All inserted repair segments use horizontal, vertical, or 45-degree
  geometry and remain inside the existing local copper envelopes.
- The repaired board file has balanced syntax and preserves every original
  net, footprint, via, zone, and board-edge item.

## Remaining release gate

This environment does not contain KiCad 9, so it was not possible to run
KiCad's own DRC/ERC engine, refill zones, or render final Gerbers. Before
ordering:

1. Open `power_interface.kicad_pro` in KiCad 9.0.9 or newer.
2. Open the PCB, press `B` to refill zones, and save.
3. Run PCB Inspector > Design Rules Checker. Require zero clearance, short,
   unconnected-item, invalid-outline, and malformed-zone errors.
4. Run the schematic ERC and confirm that the intentionally unconnected J5
   pins 6, 10, and 12 and U1 pin 4 are the only open pins.
5. Plot Gerbers and drill files, then inspect them in KiCad Gerber Viewer,
   especially the four power/interface regions and the repaired junctions.

The included library tables point to a sibling `muon_detector_head` project
that was not part of this upload. The board and schematic contain embedded
footprints/symbols and should open, but do not use "Update footprints from
library" unless that sibling library is available.

## Fabrication recommendation

After the native KiCad checks above pass, ordering one low-cost prototype lot
is rational. The remaining risk is normal first-revision analog/power bring-up,
not a visible layout showstopper. Do not pay for a large turnkey assembly run
before one board has been bench-tested.

For first power-up, leave HEAD A, HEAD B, and J5 disconnected; use a current-
limited 5 V supply; verify `+5VA`, `+3V3_LOCAL`, `+3V3_ADC`, `HV_RAW`, and
`BIAS_27V`; then check boost ripple and only afterward attach the detector
heads and controller.
