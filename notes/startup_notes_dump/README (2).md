# FPGA Muon Telescope

This repository contains the electronics, PCB, FPGA, and bring-up work for a two-plane plastic-scintillator muon telescope built around a Digilent Cora Z7.

## Current design

Revision A uses:

- Two identical detector-head PCBs.
- One shared power/interface PCB.
- One onsemi MICROFC-60035-SMT-TR 6 mm SiPM per head.
- Local TPH2502 amplification and TLV3502 threshold comparison on each head.
- A MAX5026 adjustable SiPM-bias supply on the power/interface board.
- Two 3.3 V trigger signals sent to the Cora Z7 for counting and coincidence.

Keeping the amplifier and comparator beside each SiPM prevents the raw millivolt signal from crossing the detector frame.

## Status

The design is ready for schematic capture and PCB layout, but it has not yet been validated in hardware. The first fabrication is an engineering prototype.

**Do not order PCBs until every item in Section 18 of the design specification is signed off.**

## Read these first

The documents have different roles. If they disagree, use the order below.

1. [`docs/01_design_spec.md`](docs/01_design_spec.md) - authoritative electrical values, parts, interfaces, safety limits, test requirements, and release gate.
2. [`docs/03_kicad_implementation_guide.md`](docs/03_kicad_implementation_guide.md) - short guidance for translating the specification into schematics and PCB layout.
3. [`docs/02_electronics_theory_review.md`](docs/02_electronics_theory_review.md) - explanatory background: what each block does, why it exists, and how noise, loss, signal current, and power current interact.
4. [`CONTRIBUTING.md`](CONTRIBUTING.md) - the two-person Git and KiCad workflow.
5. [`AGENTS.md`](AGENTS.md) - constraints for coding agents working in this repository.

The Markdown sources are authoritative. Generated PDFs are convenience copies and should not be edited directly.

## Intended repository layout

```text
muon-telescope/
|-- README.md
|-- CONTRIBUTING.md
|-- AGENTS.md
|-- docs/
|   |-- 01_design_spec.md
|   |-- 02_electronics_theory_review.md
|   `-- 03_kicad_implementation_guide.md
|-- hardware/
|   |-- detector_head/
|   |-- power_interface/
|   `-- libraries/
|       |-- MuonTelescope.kicad_sym
|       `-- MuonTelescope.pretty/
|-- firmware/
|-- test/
`-- manufacturing/
```

There are three physical PCBs but only two PCB designs: fabricate the detector-head design twice.

## Toolchain lock

This repository targets **KiCad 10.0.5**. Both collaborators should use that exact release when the initial project files are created.

Do not let a later KiCad major version rewrite the project files until both collaborators intentionally migrate together. KiCad 10.0.5 supports macOS 12 and newer, so the same project can be edited on the Mac and the other workstation.

## Attribution

The detector architecture and several analog values are derived from the CosmicWatch v3X design. Preserve the attribution and licensing notes in the design specification when publishing this work.
