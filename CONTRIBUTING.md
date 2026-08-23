# Contributing

This project uses two KiCad projects and small, reviewable Git changes. The two
physical heads are assemblies of the same detector-head design.

```text
hardware/detector_head/detector_head.kicad_pro
hardware/power_interface/power_interface.kicad_pro
```

## Hardware workflow

- Use KiCad 10.0.5 and open a project through its `.kicad_pro` file.
- Do not accept a file-format migration during ordinary editing.
- Only one person edits a given `.kicad_sch`, `.kicad_pcb`, `.kicad_sym`, or
  `.kicad_mod` file at a time. Divide work by board or take turns through
  commits; KiCad files are not safely mergeable by hand.
- Keep custom symbols, footprints, and 3D models under `hardware/libraries/`.
  Commit `sym-lib-table` and `fp-lib-table` with project-relative
  `${KIPRJMOD}` paths.
- Archive each selected part's available primary documentation under
  `docs/datasheets/` and update its exact-part/source entry in the directory
  index when the part changes.
- Open the affected design in KiCad for review. A textual Git diff is useful
  history, not a sufficient electrical or layout review.
- Never run a formatter or scripted rewrite over KiCad source.

The custom SiPM footprint is release-critical. Verify its pad numbers against
the current onsemi package drawing, print it at 1:1, and check the physical
part. Pin 4 is soldered, pin 2 is the unused fast output, and the center paddle
(pin 5) must receive neither solder nor paste.

## Git workflow

Start from an up-to-date branch, make one coherent change at a time, and close
KiCad before changing branches or merging. Include a library edit in the same
commit as the design that first uses it.

Useful commit prefixes are `docs:`, `head:`, `power:`, `lib:`, `fpga:`,
`software:`, `test:`, and `release:`.

Before review:

```sh
git status
git diff --check
make check
```

The hardware review must confirm:

- The schematic still implements `docs/design.md`.
- Symbol pins, footprint pads, polarities, mating views, and cable pin numbers
  match current primary-source documentation.
- The boost switching loop, amplifier feedback loop, and return-current paths
  are compact and separated appropriately.
- ERC/DRC findings are fixed or explained explicitly; no warning is waived just
  to obtain a clean report.
- Power-up, back-power, test-point access, and first-bring-up behavior are safe.

## Manufacturing releases

KiCad source is authoritative; changing Gerbers is not a design change. Keep
temporary fabrication exports out of normal commits. After every release gate
in `docs/build-and-debug.md` passes, generate one complete package under
`hardware/manufacturing/<release-name>/`, inspect it independently, record its
source commit, and tag that commit. Never order directly from an unreviewed
working directory.

## Measurements

Commit only small, useful records with units, configuration, provenance, and a
plain data format such as CSV or JSON. Do not commit personal data, secrets, or
large raw captures. Record the external location and SHA-256 checksum for data
that is too large for Git.
