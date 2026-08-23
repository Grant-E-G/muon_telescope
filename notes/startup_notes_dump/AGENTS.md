# Agent Instructions

This repository contains a mixed-signal detector whose raw SiPM signal is only a few millivolts. Treat electrical values, package pinouts, return-current geometry, and release checks as design constraints, not suggestions.

## Source-of-truth order

1. `docs/01_design_spec.md` is normative.
2. `docs/03_kicad_implementation_guide.md` explains implementation.
3. `docs/02_electronics_theory_review.md` explains theory and design intent.

When documents disagree, stop and report the conflict. Do not choose silently.

## Locked architecture

- Two identical detector-head PCBs plus one shared power/interface PCB.
- onsemi MICROFC-60035-SMT-TR 6 mm SiPM using the standard output.
- TPH2502 local amplifier and TLV3502 local comparator on each head.
- MAX5026 adjustable bias generation on the power/interface board.
- Only power, bias, grounds, and a 3.3 V trigger cross each head cable.
- The Cora Z7 Pmod 3.3 V rail is not tied to the detector's local 3.3 V regulator.

Do not substitute the older dual-use 1 mm SiPM or fast-output architecture into this revision.

## Repository setup task

An agent initializing the repository should:

1. Require KiCad 10.0.5 and record any intentional toolchain change before creating or rewriting project files.
2. Create the directory structure shown in `README.md`.
3. Create separate KiCad projects named `detector_head` and `power_interface`.
4. Create project-local symbol and footprint libraries under `hardware/libraries/`.
5. Configure `sym-lib-table` and `fp-lib-table` with `${KIPRJMOD}`-relative paths.
6. Add a KiCad-appropriate `.gitignore` consistent with `CONTRIBUTING.md`.
7. Add no guessed schematic connections, footprints, or component substitutions.
8. Commit the empty project structure before circuit capture begins.

## Editing constraints

- Preserve exact manufacturer part numbers and tolerances from the design specification.
- Verify every custom symbol pin number and footprint pad against the current manufacturer datasheet.
- Never put copper, mask opening, or paste on a no-solder mechanical pad merely because a generic footprint generator does so.
- Do not auto-migrate the project to another KiCad major version.
- Do not reannotate the full design after references have been reviewed.
- Do not modify generated KiCad source text by regex unless the change is mechanically necessary and followed by opening, saving, ERC/DRC, and visual review in KiCad.
- Keep source changes focused. Do not mix documentation cleanup, electrical redesign, and board routing in one commit.
- Preserve unrelated user changes in a dirty worktree.

## Electrical-change rule

Any change to a component value, part number, connector pinout, supply voltage, threshold range, gain, bias range, or FPGA timing must include:

1. The reason for the change.
2. The calculation or primary-source datasheet evidence.
3. The corresponding update to `docs/01_design_spec.md`.
4. A note describing how the change will be tested.

## Release rule

Do not claim the design is ready to order until every Section 18 item in `docs/01_design_spec.md` is signed off. The first fabrication remains an engineering prototype even after that checklist is complete.
