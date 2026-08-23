# Muon Telescope

This repository contains the complete design record for a two-layer cosmic-ray
muon telescope: electronics, FPGA firmware, host software, mechanical CAD,
manufacturing releases, and measurement records.

The first build is an engineering prototype. It uses two identical
50 mm x 50 mm x 10 mm plastic-scintillator detector heads and a central
power/interface board connected to a Digilent Cora Z7. It is intended to count
single-channel events and two-layer coincidences. It is **not** an energy
spectrometer, position tracker, or scattering-tomography system.

No PCB is approved for ordering yet. The current design and its remaining
release gates are recorded in [docs/design.md](docs/design.md) and
[docs/build-and-debug.md](docs/build-and-debug.md).

## Read first

1. [docs/design.md](docs/design.md) — authoritative electrical, FPGA, and
   measurement specification.
2. [docs/build-and-debug.md](docs/build-and-debug.md) — staged build, release
   gates, acceptance tests, and pre-populated debugging checklist.
3. [docs/bom.md](docs/bom.md) — sourced planning BOM and cost assumptions.
4. [docs/theory.md](docs/theory.md) — concise explanation of the signal chain
   and what the measurements can support.
5. [CONTRIBUTING.md](CONTRIBUTING.md) — KiCad and Git collaboration rules.

When documents disagree, `docs/design.md` wins unless a reviewed change updates
it. KiCad source becomes authoritative for connectivity only after the schematic
has been reviewed against that specification.

## Repository layout

```text
docs/                       Design, theory, BOM, build, debug, and datasheets
hardware/detector_head/     One KiCad design, assembled twice
hardware/power_interface/   Central power and Cora Z7 interface KiCad design
hardware/libraries/         Project symbols, footprints, and electrical 3D models
hardware/mechanical/        Frame, enclosure, and non-electrical CAD
hardware/manufacturing/     Reviewed, tagged fabrication packages only
firmware/                   Cora Z7 programmable-logic design and constraints
software/                   Host-side capture and analysis tools
data/                       Small, curated calibration and measurement records
scripts/                    Repeatable project checks
```

Keep source files near the subsystem they describe. Do not create another
directory or README unless it removes a real ambiguity. Large raw captures and
third-party source archives do not belong in Git; part datasheets are the
intentional exception and live in `docs/datasheets/`. For large raw captures,
record their external source and a checksum instead.

## Toolchain and routine checks

- KiCad **10.0.5** is the locked hardware file-format version.
- Run `make check` before a hardware pull request and before a fabrication
  release. The check intentionally fails if the locked KiCad version or either
  KiCad project is missing.
- Preserve project-owned libraries and 3D models in this repository. Use
  project-relative `${KIPRJMOD}` library paths.

## Coding guidelines

- Prefer Rust for implementation work. Use Python as a backup, with type checking.
- Prefer functional code when possible. Relax this guideline when it causes performance issues.
- Long functions are fine.
- Avoid inheritance. Object-oriented design is generally discouraged.
- Avoid excessive code fragmentation. Longer files are acceptable when they keep related logic together.
- Lint code aggressively. Use Black for Python formatting.
- Shorter code is almost always better code.

## Attribution and license

The detector dimensions and front-end starting point were informed by the
[CosmicWatch Desktop Muon Detector v3X](https://github.com/spenceraxani/CosmicWatch-Desktop-Muon-Detector-v3X)
and its [2025 design paper](https://arxiv.org/html/2508.12111). No CosmicWatch
design files are copied here; consult its CC BY-NC 4.0 license before reusing
them. Original material in this repository is licensed under [MIT](LICENSE).
