# PCB validation workflow

## Purpose

Provide one repeatable, command-line pre-fabrication check for a KiCad project.
The first target is the unfinished muon-detector head. The checker must report
what is known, what failed, and what still needs measurement or human review. A
passing command is evidence, not proof that a mixed-signal board will work.

`docs/design.md` remains the reviewed electrical and mechanical authority. This
document defines validation workflow only.

## Keep the evidence compact

Run the workflow with:

```sh
make check
```

Run the engine on another repository or project with:

```sh
/path/to/kicad/python scripts/kicad-check.py path/to/project_base \
    --profile path/to/validation.json \
    --output build/checks
```

Omit `--profile` for generic ERC, DRC/parity, reference/pour inference,
routing, fabrication-export, and render checks. A profile uses schema version 1
and may add stackup/via constraints, reference-plane mappings, sensitive and
aggressor nets, edge rates, supply-current assumptions, geometry and pin/net
expectations, analytical noise inputs, and declarative ngspice jobs.

Maintain one reusable implementation in `scripts/kicad-check.py`. It accepts a
KiCad project base path and works without repository-specific assumptions. An
optional, co-located `validation.json` profile supplies machine-readable design
intent, expected geometry, important nets, edge rates, and model assumptions.
This separation keeps reusable mechanisms out of agent prompts and keeps
project facts out of the generic code.

For each checked project, generate one main report and two board-review images
under `build/checks/`. Raw ERC/DRC JSON, refilled board copies, netlists, and
fabrication files are temporary inputs to the report and must not become a
permanent directory tree.

Add another committed file only when it is a real engineering input that
cannot reasonably live in the checker or an existing design document. Do not
create one script or report per component, circuit block, or KiCad command.

## Status model

The consolidated report uses three states:

- `PASS`: the automated check met its stated criterion.
- `WARNING`: evidence is incomplete or needs human judgment.
- `BLOCKING`: the current source must not be fabricated.

The checker exits zero only when it has no blocking findings. It should still
finish the remaining safe checks and write the report after finding a failure.
ERC/DRC exclusions are included in the run and unexplained exclusions are
blocking; the workflow never hides them to obtain a green result.

## Checks implemented now

### Source and KiCad

- Require the repository's locked KiCad 9.0.9.
- Require the project, schematic, PCB, and custom-rule files.
- Reject empty, duplicate, or `REF**` references.
- Export a schematic netlist and compare KiCad's PCB/schematic parity.
- Refill zones only in a temporary copy before DRC so the source is not
  silently rewritten.
- Run ERC and DRC with all severities and exclusions enabled.

### Revision-A design intent

The checker records the present component inventory and tests the objective
items that can be checked without guessing:

- 70 x 70 mm head outline and frozen hole/sensor/connector coordinates;
- 3.2 mm NPTH mounting holes;
- SiPM alone on the optical side;
- SiPM pad 1 on `SIPM_RAW`, pad 2 unconnected, pad 3 on `BIAS_LOCAL`, pad 4 on
  ground, and no electrical pad 5;
- two head `TPH2502-SR` devices, the trigger one-shot, peak-hold/reset nets,
  ten-position head connector, and required test points;
- shared `MCP3202-BI/SN` presence in the power/interface project.

These checks intentionally make the current, older schematic fail rather than
mistaking clean geometry for agreement with `docs/design.md`.

Datasheet-backed pin and package review is not reducible to DRC. The automatic
checks above catch known invariants; final release still requires the primary-
document and physical-part reviews in `docs/build-and-debug.md`.

### Layout and home fabrication

- Report footprint, track, via, zone, layer, width, and per-net route totals.
- Verify the 1.6 mm, two-layer stack and actual track/via geometry.
- Require every via to satisfy the checked-in rivet rule.
- Report non-ground routing on the nominal ground-plane layer.
- Report distances between sensitive analog and fast/bias routes.
- Enforce configured pad-to-pad proximity limits for local bypass and other
  placement-critical loops.
- Sample whether the configured reference-plane pour actually exists under
  each routed signal, instead of treating a zone outline as a solid plane.
- Export Gerbers and separate plated/non-plated drill files to a temporary
  directory and verify that the expected files are nonempty.
- Render top and bottom views for human inspection. Render generation is a
  pass; visual correctness remains a human-review item.

This is a fabrication smoke test, not manufacturing approval. Release Gerbers
must still pass the independent visual review and release gates.

## Noise and EMI calculations

The report includes calculations that are meaningful for the actual routed
layout and labels their assumptions:

- approximate microstrip impedance and propagation delay for each used trace
  width, using the KiCad stackup dielectric height and relative permittivity;
- per-net reference coverage and distributed capacitance from the present pour;
- a configurable closer-plane comparison, including impedance, capacitance,
  delay, and an idealized loop-area/radiation ratio;
- routed lengths of `SIPM_RAW`, `AMP_IN`, `AMP_OUT`, comparator output,
  `TRIG`, supply, bias, and feedback nets;
- the transmission-line critical length based on the TLV3502's 1.5 ns output
  edge from the archived TI datasheet;
- approximate trace capacitance for the amplifier feedback route and the
  resulting illustrative pole with the 12.4 kohm feedback resistor;
- 35 micrometre copper resistance bounds for the routed supply networks;
- a first-order front-end noise floor using the TPH2502's archived 6.5
  nV/sqrt(Hz) voltage-noise density, 120 MHz gain-bandwidth product, the 13.4
  noise gain, and 49.9 ohm sense resistor at 300 K.

The impedance calculation ignores copper thickness, solder mask, weave, and
manufacturer variation. The noise result excludes detector dark pulses,
comparator noise, power/bias ripple, pickup, and stability peaking. It is a
lower-bound sanity calculation, not a prediction of measured count rate.

No credible radiated-emissions number, crosstalk waveform, power-distribution
impedance, or amplifier stability margin can be obtained from trace geometry
alone. The report therefore exposes return-plane cuts, route adjacency, and
unrouted connections without inventing an EMI pass. Scope measurements and the
staged injected-pulse tests remain required.

## Simulation boundary

Do not build a nominal full-board SPICE model merely to produce a plot. The
current head lacks the reviewed one-shot and peak circuit, and the current
power/interface schematic lacks the ADC and bias supply. Vendor macromodels
and the missing circuits must be checked in before simulations can represent
the board under review.

The generic checker already supports declarative ngspice jobs and numeric
min/max assertions listed in `validation.json`. When representative circuit
netlists exist, register small, question-driven simulations for:

1. SiPM pulse through the amplifier;
2. threshold crossing and one-shot timing;
3. peak acquisition, droop, ADC settling, and reset;
4. bias startup, ripple, and component stress.

Each simulation needs sourced model assumptions, deterministic corners,
numeric measurements, and explicit acceptance criteria from `docs/design.md`.
Until then, the report must say `NOT IMPLEMENTED`, not `PASS`.

## Release boundary

The workflow answers three separate questions:

1. Geometry: can KiCad generate internally consistent fabrication data?
2. Connectivity: does the PCB match its schematic and have complete nets?
3. Design intent: does the schematic/PCB implement the reviewed revision?

Physics and assembly remain partly empirical. Even after all automated items
pass, fabrication status is only `READY FOR FINAL HUMAN REVIEW`; it is never
`BOARD PROVEN CORRECT`.
