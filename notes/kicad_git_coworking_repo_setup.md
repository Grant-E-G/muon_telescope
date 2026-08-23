# KiCad Git Co-Working Repository Setup

## Purpose

Set up the Muon detector PCB repository so two people can work from Linux and macOS with ordinary Git while minimizing KiCad version, library-path, and merge problems.

This document is an implementation brief for the agent configuring the repository. Preserve any existing design work and unrelated user changes.

## Required outcome

The completed repository must provide:

1. A clearly recorded KiCad version.
2. Portable project-local symbol and footprint libraries.
3. Correct Git ignore and line-ending rules.
4. A schematic structure that supports parallel work on separate sheets.
5. A single-writer workflow for files that are not safely co-editable, especially the PCB.
6. One simple command for ERC/DRC once real schematic and PCB files exist.
7. Short contributor instructions suitable for developers already familiar with Git.
8. A clean method for tagging and reproducing fabrication releases.

## Non-negotiable collaboration rule

KiCad files are structured text, but Git does not understand their electrical or geometric semantics. Automatic textual merges can produce broken UUID relationships, connectivity, or balanced-but-incorrect design data.

- Different hierarchical schematic files may be edited concurrently.
- The same `.kicad_sch` file must have only one active editor at a time.
- The root schematic, `.kicad_pro`, and shared library tables are integration-owned files.
- The `.kicad_pcb` file must have only one active editor at a time.
- Do not configure an automatic custom merge driver for KiCad files.
- If a schematic or PCB conflict occurs, retain one complete version and replay the smaller losing edit in the KiCad GUI. Do not casually hand-merge the S-expressions.

Git is being used for version control, review, rollback, and releases. It is not being treated as simultaneous live editing.

## KiCad version decision

Inspect the repository before changing any KiCad files.

- If no meaningful KiCad design files exist, standardize on **KiCad 10.0.5** for both collaborators.
- If meaningful KiCad 9 files already exist, standardize on **KiCad 9.0.9** for the current build weekend.
- Do not silently migrate an existing project between major versions.
- If a major-version migration is chosen, perform it as a dedicated commit before either collaborator creates a feature branch.
- Record the exact selected version in the repository `README.md` and in `docs/decisions/0001-kicad-version.md`.
- Both collaborators must use the same major version. Using the same point release is strongly preferred.
- Use stable releases only. Do not use nightlies or release candidates.

The macOS user should install KiCad from the official DMG. Current KiCad supports macOS 12 or newer and Intel and Apple Silicon systems. The working clone should live somewhere such as `~/src/muon-detector`, not in an iCloud-synchronized Desktop or Documents folder.

## Target repository structure

Adapt this structure around existing files rather than blindly moving or renaming them:

```text
repo-root/
├── README.md
├── CONTRIBUTING.md
├── .gitattributes
├── .gitignore
├── Makefile
├── hardware/
│   └── muon-detector/
│       ├── muon-detector.kicad_pro
│       ├── muon-detector.kicad_sch
│       ├── bias-power.kicad_sch
│       ├── sensor-front-end.kicad_sch
│       ├── comparator-output.kicad_sch
│       ├── connectors-testpoints.kicad_sch
│       ├── muon-detector.kicad_pcb
│       ├── muon-detector.kicad_dru
│       ├── muon-detector.kicad_jobset
│       ├── sym-lib-table
│       ├── fp-lib-table
│       ├── muon-symbols.kicad_sym
│       ├── muon-footprints.pretty/
│       └── models/
├── docs/
│   ├── architecture.md
│   ├── interfaces.md
│   ├── fabrication.md
│   └── decisions/
│       └── 0001-kicad-version.md
├── scripts/
│   └── find-kicad-cli.sh
└── build/
```

`build/` is disposable and ignored. Do not create fabricated schematic or PCB contents merely to satisfy this tree. Create real KiCad project and sheet files through KiCad, or preserve existing ones.

## Schematic decomposition

The root schematic should contain the functional sheet boxes and the interfaces between them. The intended first-pass split is:

| Sheet | Responsibility |
| --- | --- |
| `bias-power.kicad_sch` | Input power, regulation, SiPM bias/boost converter, filtering, enable, and power-good behavior |
| `sensor-front-end.kicad_sch` | SiPM connection, bias decoupling, amplifier, gain/bandwidth components, and analog test points |
| `comparator-output.kicad_sch` | Threshold/reference generation, comparator, pulse shaping if used, digital output, and indicator behavior |
| `connectors-testpoints.kicad_sch` | External connectors, power entry, grounding connections, debug access, mounting-related electrical items, and labeled test points |

Before parallel work begins, create and review the sheet interfaces. Record them in `docs/interfaces.md`, including:

- Signal name and direction.
- Expected voltage range or logic level.
- Source and load impedance where relevant.
- Bandwidth or edge-rate requirement.
- Ground/reference domain.
- Whether a signal is analog, power, or digital.
- Any sequencing or enable behavior.
- Intended test point.

The top-level sheet and interfaces should be committed as a shared baseline before the collaborators branch.

Do not perform global annotation, bulk symbol updates, bulk footprint reassignment, or PCB synchronization during parallel sheet work. The integration owner performs those operations after merging the child sheets.

## Library portability

Use the normal installed KiCad libraries for standard parts. Store custom, modified, or downloaded project-specific items inside the repository.

Requirements:

- Project-specific symbols go in `muon-symbols.kicad_sym`.
- Project-specific footprints go in `muon-footprints.pretty/` as individual `.kicad_mod` files.
- Small project-specific STEP models go in `models/`.
- Commit `sym-lib-table` and `fp-lib-table`.
- All project-local library and model paths must use `${KIPRJMOD}` rather than absolute filesystem paths.
- Record the source URL, manufacturer part number, datasheet revision, and license for each imported third-party asset.
- Do not vendor the complete official KiCad symbol, footprint, or 3D-model libraries.
- Do not use Git LFS for `.kicad_sch`, `.kicad_pcb`, `.kicad_pro`, `.kicad_sym`, or `.kicad_mod` files.
- Git LFS may be considered later only for genuinely large binary STEP or image assets.

Use lowercase filenames and avoid case-only renames because the default macOS filesystem is usually case-insensitive while Linux filesystems are commonly case-sensitive.

## Required `.gitignore`

Add or merge the following rules without deleting unrelated existing rules:

```gitignore
# macOS
.DS_Store

# KiCad temporary files and caches
*.000
*.bak
*.bck
*.kicad_pcb-bak
*.kicad_sch-bak
*-backups/
*-cache*
*~
~*
_autosave-*
\#auto_saved_files\#
*.tmp
fp-info-cache
~*.lck
.history/
*.kicad_prl

# Locally generated output
/build/
```

Do not globally ignore PDF, CSV, Gerber, drill, or placement extensions. Those may be intentionally retained in a tagged fabrication-release directory later. Normal intermediate exports should be directed into `build/`.

## Required `.gitattributes`

Add or merge:

```gitattributes
* text=auto

*.kicad_pro    text eol=lf
*.kicad_sch    text eol=lf
*.kicad_pcb    text eol=lf
*.kicad_sym    text eol=lf
*.kicad_mod    text eol=lf
*.kicad_dru    text eol=lf
*.kicad_wks    text eol=lf
*.kicad_jobset text eol=lf

*.step binary
*.stp  binary
*.pdf  binary
*.png  binary
*.jpg  binary
```

Do not mark KiCad design files as binary or route them through LFS. Their textual history remains useful even though same-file merging is unsafe.

## Contributor workflow

Put the following short workflow in `CONTRIBUTING.md`:

1. Save and close the KiCad editors before switching branches, pulling, rebasing, or merging.
2. Update local `main` with `git pull --ff-only`.
3. Create a short-lived feature branch.
4. Edit only the assigned schematic sheet or currently checked-out integration file.
5. Save and close KiCad before reviewing Git changes.
6. Run available checks.
7. Commit a logically coherent change and push it.
8. Open a pull request and state which KiCad files were intentionally changed.
9. Review the design in KiCad. Do not rely solely on the GitHub textual diff.
10. Merge only after confirming that no one else has unmerged work in the same KiCad file.

Recommend these local Git settings without changing global user configuration automatically:

```bash
git config pull.ff only
git config fetch.prune true
```

Example branch names:

```text
grant/bias-power
wife/comparator-output
grant/pcb-placement
wife/footprint-review
```

Avoid personal names in permanent design filenames. Names are acceptable in temporary branch names.

## File ownership during the initial build

Add a small current-work table to `CONTRIBUTING.md` or `docs/interfaces.md`. It is a coordination aid, not a technical locking system.

| File or operation | Policy |
| --- | --- |
| Individual child schematic | One assigned editor; different child sheets may be edited concurrently |
| Root schematic | Integration owner only during a parallel work period |
| `.kicad_pro` and library tables | Integration owner, or explicitly coordinated edit |
| Custom symbol file | One editor at a time |
| Individual footprint files | Concurrent work is acceptable only on different `.kicad_mod` files |
| PCB file | One editor at a time, without exception |
| Annotation and update-PCB-from-schematic | Integration owner after schematic merge |
| Fabrication output | Generated from a reviewed, tagged commit |

Do not introduce Git LFS locking or a custom lock server for a two-person weekend project. Verbal coordination plus the ownership table is lower friction.

## ERC, DRC, and the single check command

KiCad supports ERC, DRC, schematic/PCB parity checks, and jobsets from `kicad-cli`.

Create `scripts/find-kicad-cli.sh` so the repository can locate:

- `kicad-cli` from `PATH` on Linux.
- `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli` on macOS.

The script must fail with a concise installation message if neither exists. It must not install software or modify shell startup files.

Once real project files exist, provide:

```bash
make check
```

The check should:

1. Verify that the detected KiCad major version matches the version recorded by the repository.
2. Create output only under `build/`.
3. Run schematic ERC for error-level violations.
4. Run PCB DRC for error-level violations.
5. Include schematic/PCB parity checking when supported by the selected version.
6. Return nonzero when error-level violations are present.
7. Print the report paths on completion or failure.

Do not run the check automatically as a pre-commit hook. Draft commits are valuable recovery points and may intentionally contain incomplete circuitry.

If the repository does not yet contain real schematic and PCB files, create the wrapper and a documented placeholder target that explains what is missing. Do not create fake CAD data or report a successful ERC/DRC that did not run.

Prefer a committed `.kicad_jobset` as the shared source of release/export settings when practical. A thin `Makefile` may invoke the jobset or direct CLI commands.

## Pull requests and review

Pull requests should contain a brief hardware-specific checklist:

```markdown
## Change

- Functional change:
- KiCad files intentionally changed:
- Interfaces changed:

## Verification

- [ ] Opened successfully using the repository KiCad version
- [ ] ERC reviewed
- [ ] DRC reviewed if PCB changed
- [ ] Schematic/PCB parity checked if applicable
- [ ] Footprints checked against manufacturer datasheets
- [ ] No unintended bulk rewrite or version migration
```

Add this as `.github/pull_request_template.md` if the repository is hosted on GitHub.

Protecting `main` against force pushes and accidental direct pushes is recommended, but do not block repository setup if remote administration is unavailable. Requiring one review for every minor documentation change is unnecessary. A second-person review should be required by convention for PCB, footprint, connector pinout, power, or fabrication changes.

## Fabrication release process

Gerbers and associated manufacturing files are build artifacts. They must be traceable to source.

Before ordering a board:

1. Start from a clean working tree.
2. Run the repository checks.
3. Generate outputs into `build/` from the committed jobset or documented command.
4. Review Gerbers in an independent viewer.
5. Record board house, stackup, design-rule assumptions, and special instructions in `docs/fabrication.md`.
6. Commit any final source or documentation change.
7. Create an annotated Git tag such as `pcb-rev-a-ordered`.
8. Generate or verify the fabrication ZIP from that exact tagged commit.
9. Attach the ZIP and reports to a GitHub release, or store them in a clearly named release directory if GitHub releases are unavailable.

Do not mix ordinary generated files into the source directories.

## Mac onboarding notes for `README.md`

Include a compact section:

```markdown
### macOS setup

1. Confirm macOS with `sw_vers -productVersion`.
2. Install the repository-specified stable KiCad release from the official DMG.
3. Clone into a non-iCloud location such as `~/src/muon-detector`.
4. Open `hardware/muon-detector/muon-detector.kicad_pro`, not an individual sheet in standalone mode.
5. Select the default official KiCad libraries when prompted.
6. Confirm custom libraries load without absolute-path warnings.
7. Run `make check` once the project contains a complete schematic and PCB.
```

A three-button mouse or scroll-wheel mouse is strongly recommended for PCB work. Use KiCad's default stroke fonts unless a project-specific font is deliberately bundled.

## Do not over-engineer the setup

For the initial project, do not add:

- Docker or a dev container.
- Nix or another environment manager.
- KiBot or a large third-party automation stack.
- A custom semantic merge driver.
- Git LFS for normal KiCad design files.
- Mandatory pre-commit ERC/DRC.
- A database-backed parts system.
- A large vendored copy of KiCad's official libraries.

These may become useful later, but they add setup and debugging work before the first board exists. The initial repository should remain understandable to someone who knows Git and has just installed KiCad.

## Acceptance tests

The setup is complete when all applicable checks below pass:

- [ ] Existing user files and unrelated working-tree changes were preserved.
- [ ] The chosen KiCad version is recorded in `README.md` and the decision record.
- [ ] The Mac and Linux installations can open the same `.kicad_pro` without format-conversion prompts.
- [ ] The project clone works from two different absolute filesystem locations.
- [ ] No committed library or model path contains a collaborator's home directory.
- [ ] Project-local libraries use `${KIPRJMOD}`.
- [ ] Custom symbols and footprints are committed.
- [ ] Backups, locks, `.history`, `.kicad_prl`, and `build/` are ignored.
- [ ] KiCad source files are normalized to LF and remain normal Git text files.
- [ ] Two branches that modify different child schematic files merge cleanly.
- [ ] The documented process prevents two people from independently editing the PCB.
- [ ] `make check` runs real ERC/DRC or clearly reports that the real CAD files do not yet exist.
- [ ] Generated check and fabrication output remains under `build/`.
- [ ] The pull-request template exists when using GitHub.
- [ ] Fabrication releases can be tied to an annotated Git tag.
- [ ] No nightly software, automated major-version migration, or unnecessary infrastructure was introduced.

## Expected handoff from the setup agent

The agent should finish by reporting:

1. The KiCad version selected and why.
2. Every file added or modified.
3. Whether existing KiCad files were moved, renamed, or migrated.
4. How custom library paths were verified.
5. The exact command used for repository checks and its result.
6. Any work that could not be completed until the project is opened in the KiCad GUI.
7. Any detected existing merge risk or uncommitted user change that was deliberately left untouched.

## References

- [KiCad macOS downloads](https://www.kicad.org/download/macos/)
- [KiCad system requirements](https://www.kicad.org/help/system-requirements/)
- [KiCad project files and Git integration](https://docs.kicad.org/9.0/en/kicad/kicad.html)
- [KiCad project-local footprint libraries and `${KIPRJMOD}`](https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html#_path_variable_substitution)
- [KiCad command-line interface](https://docs.kicad.org/9.0/en/cli/cli.html)
- [GitHub's maintained KiCad `.gitignore` template](https://github.com/github/gitignore/blob/main/KiCad.gitignore)
