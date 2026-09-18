# Accepted prototype layout judgments: detector head and power/interface boards

The physical prototype release is **v0**, dated **2026-09-18**. Both sides of
both boards carry that identifier; the electrical design intent remains
revision A.

Both boards pass `make check` with no blocking findings. The layout still
contains three documented judgment calls. On 2026-09-17, the project owner
accepted all three as good enough for the revision-A engineering prototypes.
The acceptance freezes these layouts; it does not waive the remaining
physical-part, output-inspection, BOM, or release-package gates in
`docs/build-and-debug.md`.

Run `make check` (it needs KiCad 9.0.9 and `ngspice`) and review the reports
and renders under `build/checks/` alongside this list.

## 1. Relaxed ground-return distance for four bypass capacitors

**Where:** `proximity_checks` in `hardware/muon_detector_head/validation.json`
and `hardware/power_interface/validation.json`.

**What changed:** The checks required a bypass capacitor's ground pad to be
within 3.0 mm of the IC ground pin. On these packages, ground (pin 4) and
supply (pin 8) sit on opposite corners. A single component-side capacitor
therefore cannot be within 3.0 mm of both pins. The supply-side 3.0 mm limit
is unchanged; only the ground-side limit was raised.

| Board | Check | Old limit | New limit | Measured |
|---|---|---:|---:|---:|
| Head | U1 (TPH2502, SOIC-8) to C2 | 3.0 mm | 6.0 mm | 5.91 mm |
| Head | U3 (TPH2502, SOIC-8) to C17 | 3.0 mm | 6.0 mm | 5.91 mm |
| Head | U5 (SN74LVC1G123, DCT-8) to C15 | 3.0 mm | 4.5 mm | 3.92 mm |
| Power | U3 (MCP3202, SOIC-8) to C12 | 3.0 mm | 6.0 mm | 5.99 mm |

A brute-force search over capacitor position and rotation gives about 5.5 mm
as the best possible SOIC-8 result. On the real boards, neighbouring parts
push it to about 5.9 mm.

**Alternatives:** Put the capacitor on the back side (not allowed on the head:
the SiPM must be the only optical-side part). Or change the check to measure
each pad's distance to its own ground via instead of pad-to-pad.

**Resolution:** Accepted for the revision-A engineering prototypes. Retain the
configured limits and the measured-distance checks.

## 2. AMP_OUT passes between the R13 pads at 0.25 mm clearance

**Where:** rule `AMP_OUT between R_CHG pads` in
`hardware/muon_detector_head/muon_detector_head.kicad_dru`.

**Why:** The peak-hold checks place R13 within 3 mm of U3 pin 1, the BAS70
(D2) within 3 mm of C16, and C16 within 3 mm of U3 pin 5. C17 must sit at the
top end of U3. Together these leave the chain U3 pin 1 → R13 → D2 → C16 →
U3 pin 5 wrapped around the left side of U3, fencing in pin 3 (AMP_OUT). The
0.3 mm AMP_OUT trace enters pin 3 through the 0.8 mm gap between R13's pads.
That gives 0.25 mm clearance instead of the normal 0.4 mm. The U3A output, R13
and the diode anode follow AMP_OUT to within a diode drop, so the adjacent
signals are nearly identical. 0.25 mm is well within PCBWay's standard
capability.

**Alternatives:**
- A via pair on AMP_OUT. There is currently no room for the inner via.
- Route the chain around U3's other side. That needs the U3/C17 ground limit
  relaxed to about 7.5 mm.

**Resolution:** Accepted for the revision-A engineering prototypes. Retain the
0.25 mm local clearance rule and current route.

## 3. The PEAK_HOLD guard trace is now only a short piece

**Where:** head PCB around U3, C16, D2, Q1, U4 and TP11.

**Design intent:** `docs/design.md` asks for a narrow `PEAK_GUARD` trace that
surrounds the `PEAK_HOLD` island.

**What exists:** The hold node is now very compact. It runs under the U3 body
to C16, D2 pin 3, the Q1 drain, the U4 D pin (TMUX1101 alternate, DNP) and
TP11. Their neighbouring pads leave no legal room for a guard ring. There is
only:

- the U3 pin 6/7 link to R14, and
- a 3.5 mm guard piece beside Q1.

That piece's open end is the intentional `track_dangling` DRC warning.

**Trade-off:** The hold node is smaller, but less of it is guarded against
surface leakage.

**Alternatives:**
- Move the unfitted U4/C18 alternate out of the island to free space.
- Relax the peak-hold placement checks to make room for a full ring.

**Resolution:** Accepted for the revision-A engineering prototypes. Retain the
compact hold node and short guard piece, and qualify droop and leakage on the
bench as required by `docs/build-and-debug.md`.

## Other items for human review

These `make check` warnings were also accepted for the revision-A engineering
prototypes; they remain visible so bring-up and any future revision can address
measured problems rather than assuming the warnings are harmless:

- **Ground-plane coverage:** some routed nets have less than 95% ground plane
  underneath (listed per net in each report).
- **Bottom-layer routing:** some traces run on the B.Cu ground layer, cutting
  the plane.
- **Power board `TRIG_B`:** the trace is 6% over the one-sixth-edge
  transmission-line screen.
- **Head analytic noise floor:** the estimate is model-limited.

The layout for these changes was generated and edited with scripts, not in
the KiCad GUI. Open both boards in KiCad for the visual review that
`CONTRIBUTING.md` requires. The Gerbers under each `fab/` folder were
regenerated from the current boards. They are not a reviewed manufacturing
release.
