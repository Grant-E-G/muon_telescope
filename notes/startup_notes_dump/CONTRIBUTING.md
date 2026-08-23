# Contributing: Two-Person KiCad Workflow

The goal is to make collaboration boring: small commits, explicit file ownership, and no attempts to merge two independently edited PCB files.

## 1. One shared toolchain

- Install KiCad 10.0.5 on both computers.
- Open projects through their `.kicad_pro` files, not by opening a schematic or board in isolation.
- Keep all custom symbols, footprints, and 3D models inside this repository.
- Do not accept a file-format migration from another KiCad major version during ordinary editing.

KiCad supports macOS and has built-in awareness of Git repositories. The official KiCad documentation also identifies `.kicad_prl` and `fp-info-cache` as local/cache files that do not need version control:

- <https://www.kicad.org/download/macos/>
- <https://docs.kicad.org/10.0/en/kicad/kicad.html>

## 2. Split work by board, not by trace

Create two independent KiCad projects:

```text
hardware/detector_head/detector_head.kicad_pro
hardware/power_interface/power_interface.kicad_pro
```

Each project should contain a project file, schematic, and PCB with the same base name. The two physical detector heads are copies of the same `detector_head` design.

Recommended first ownership split:

| Workstream | Primary owner | Reviewer |
|---|---|---|
| Detector-head schematic and PCB | One collaborator | Other collaborator |
| Power/interface schematic and PCB | Other collaborator | First collaborator |
| Shared SiPM symbol and footprint | One editor at a time | Independent datasheet check by the other person |
| Documentation and review notes | Either person | Other person before merge |

Do not edit the same `.kicad_sch`, `.kicad_pcb`, `.kicad_sym`, or `.kicad_mod` file concurrently. If both people need to work on one board, pair on one computer or take turns through separate commits.

## 3. Shared libraries

Place project-specific libraries in:

```text
hardware/libraries/MuonTelescope.kicad_sym
hardware/libraries/MuonTelescope.pretty/
```

Version the corresponding `sym-lib-table` and `fp-lib-table`. Use project-relative `${KIPRJMOD}` paths so the libraries resolve on macOS and the other workstation without editing absolute paths.

The custom SiPM footprint is safety-critical. Pin 2 must remain unrouted, pin 4 is soldered, and the pin 5 center paddle must not receive paste or solder. One person creates it; the other checks the current onsemi package drawing and a 1:1 print independently.

## 4. Daily Git loop

Before editing:

```bash
git switch main
git pull --ff-only
git switch -c work/<short-task-name>
```

During work:

- Save and close KiCad before switching branches or merging.
- Commit one coherent change at a time.
- Include related library changes in the same commit as the schematic or PCB that uses them.
- Never use a broad formatter or scripted rewrite on KiCad source files.

Before pushing:

```bash
git status
git diff --stat
git add <intentional-files>
git commit -m "board: concise description"
git push -u origin HEAD
```

Open a pull request. The other person reviews the schematic or PCB in KiCad, not only the textual Git diff. Merge only when the branch is up to date and the relevant ERC or DRC results are understood.

Suggested commit prefixes:

```text
docs:       documentation only
head:       detector-head schematic or PCB
power:      power/interface schematic or PCB
lib:        symbol, footprint, or 3D model
fpga:       Cora Z7 firmware or constraints
test:       bring-up procedure or measured result
release:    reviewed manufacturing package
```

## 5. What belongs in Git

Track:

- `*.kicad_pro`
- `*.kicad_sch`
- `*.kicad_pcb`
- `*.kicad_sym`
- `*.kicad_mod` and `*.pretty/`
- `*.kicad_dru`
- `sym-lib-table` and `fp-lib-table`
- Project-owned 3D models
- Documentation, firmware, constraints, test records, and scripts

Ignore local state and automatic backups:

- `*.kicad_prl`
- `fp-info-cache`
- `*-backups/`
- KiCad lock files such as `~*.lck`
- Autosave and editor-temporary files
- OS metadata such as `.DS_Store`

The setup agent should translate this list into the repository `.gitignore`.

## 6. Generated manufacturing files

Do not treat changing Gerbers as design source. The `.kicad_sch`, `.kicad_pcb`, project libraries, and rules are authoritative.

Before the release gate, keep generated Gerbers, drill files, position files, and temporary BOM exports out of normal commits. After Section 18 is signed off:

1. Generate a complete package under `manufacturing/revA-prototype/`.
2. View the Gerbers independently.
3. Commit the package with the exact source revision.
4. Tag that commit, for example `revA-prototype-order-1`.

## 7. Review rule

The second person should be able to answer these questions before a PCB merge:

- Does the schematic match `docs/01_design_spec.md`?
- Do symbol pin numbers and footprint pad numbers match the current datasheets?
- Are signal-current and power-current return loops physically sensible?
- Are the boost switching loop and amplifier feedback loop compact?
- Are raw-signal traces kept away from LX and digital trigger edges?
- Are connector orientation and mating views unambiguous?
- Are all ERC or DRC waivers documented rather than silently ignored?

If a design change conflicts with the specification, update the specification and explain the reason in the same pull request. Do not silently change a component value only in KiCad.
