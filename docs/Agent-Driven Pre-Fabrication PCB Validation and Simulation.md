# Agent-Driven Pre-Fabrication PCB Validation and Simulation

## Purpose

Build a reusable, automated pre-fabrication validation system for KiCad PCB projects.

The immediate target is the muon detector PCB, but the validation infrastructure should be general enough to reuse on future mixed-signal electronics projects.

The goal is not merely to run KiCad ERC and DRC. The goal is to produce a **pre-fabrication evidence bundle** that answers:

1. Does the schematic appear electrically coherent?
2. Does the PCB match the schematic?
3. Are symbols, footprints, pin mappings, orientations, and packages correct?
4. Does the important analog circuitry behave correctly in simulation?
5. Does it continue behaving correctly under reasonable component and signal variation?
6. Are power rails and component ratings sane?
7. Are critical PCB layout decisions reasonable?
8. Do the actual fabrication outputs appear correct?
9. What remains uncertain and requires human review?

The final output should be concise enough for a human to review quickly while retaining all raw reports and simulation results for deeper inspection.

---

# 1. Design Philosophy

Treat PCB validation like software CI.

The desired workflow is:

```text
KiCad source
    ↓
static electrical checks
    ↓
component/datasheet checks
    ↓
circuit simulations
    ↓
layout-aware checks
    ↓
fabrication output generation
    ↓
fabrication-file validation
    ↓
human-readable report
```

The agent should prefer:

- command-line tools
- reproducible scripts
- version-controlled configuration
- machine-readable outputs
- plots and summarized measurements
- explicit PASS / WARNING / FAIL criteria

over:

- GUI-only workflows
- undocumented manual checks
- unexplained KiCad exclusions
- giant full-board simulations that are difficult to reproduce

---

# 2. Desired Validation Directory

Create a structure approximately like:

```text
validation/
├── README.md
├── SUMMARY.md
│
├── static/
│   ├── erc.json
│   ├── drc.json
│   ├── schematic-parity.md
│   ├── component-audit.md
│   ├── footprint-audit.md
│   ├── power-audit.md
│   ├── layout-audit.md
│   ├── manufacturing-audit.md
│   └── exclusions-audit.md
│
├── simulation/
│   ├── README.md
│   │
│   ├── frontend/
│   │   ├── model.cir
│   │   ├── run.sh
│   │   ├── results.csv
│   │   ├── waveform.png
│   │   └── SUMMARY.md
│   │
│   ├── comparator/
│   ├── peak_detector/
│   ├── bias_supply/
│   └── digital_si/
│
├── renders/
│   ├── top.png
│   ├── bottom.png
│   ├── top_3d.png
│   └── bottom_3d.png
│
├── fab/
│   ├── gerbers/
│   ├── drills/
│   ├── bom/
│   ├── position/
│   └── FAB_AUDIT.md
│
└── scripts/
    ├── validate.py
    ├── component_audit.py
    ├── layout_lint.py
    ├── power_audit.py
    └── simulation_report.py
```

Exact implementation may vary if a cleaner architecture exists.

---

# 3. Level 1: KiCad Structural Validation

## 3.1 ERC

Run KiCad Electrical Rules Check using `kicad-cli`.

Generate a machine-readable report when supported.

Example:

```bash
kicad-cli sch erc \
    --format json \
    --severity-all \
    --output validation/static/erc.json \
    <project>.kicad_sch
```

Where available, configure the command to return a nonzero exit status for violations.

The report should classify each finding as:

```text
BLOCKING
REAL WARNING
INTENTIONAL EXCLUSION
NEEDS HUMAN REVIEW
```

Do not silently ignore ERC warnings.

---

## 3.2 PCB DRC

Run KiCad PCB DRC.

Include:

- all enabled design rules
- zone refill before checking
- schematic/PCB parity checking
- unconnected item detection
- clearance violations
- via/drill constraints
- annular-ring checks
- edge clearance
- courtyard overlap where appropriate

Example:

```bash
kicad-cli pcb drc \
    --format json \
    --severity-all \
    --schematic-parity \
    --refill-zones \
    --output validation/static/drc.json \
    <project>.kicad_pcb
```

No fabrication release should occur with unexplained DRC violations.

---

# 4. Audit All ERC/DRC Exclusions

Create:

```text
validation/static/exclusions-audit.md
```

For every explicitly excluded ERC or DRC issue, record:

```text
Rule:
Object/net/component:
Original warning:
Reason for exclusion:
Evidence exclusion is intentional:
Human review required: YES/NO
```

Treat unexplained exclusions as failures.

The principle is:

> An intentionally waived error is acceptable. An error that disappeared because somebody clicked "exclude" months ago is not.

---

# 5. Schematic-to-PCB Parity

Verify that:

- every expected schematic component exists on the PCB
- every PCB component exists in the schematic unless intentionally mechanical
- reference designators agree
- net connectivity agrees
- footprint assignments agree with schematic expectations
- there are no stale PCB components
- there are no unpropagated schematic changes

Generate:

```text
validation/static/schematic-parity.md
```

---

# 6. Datasheet / Component Audit

This is one of the highest-priority checks.

ERC and DRC cannot determine that a symbol or footprint was built incorrectly.

For every important component, compare the KiCad representation against the manufacturer's datasheet.

Priority components include:

- ICs
- photodetectors
- comparators
- amplifiers
- ADCs
- voltage regulators
- switching regulators
- MOSFETs/transistors
- diodes
- polarized capacitors
- connectors
- custom footprints

Generate a table:

```text
| Ref | MPN | Datasheet | Symbol | Footprint | Pin mapping | Package | Orientation | Status |
```

Verify:

- exact manufacturer part number
- exact package variant
- pin number
- pin name/function
- power pins
- NC versus DNC pins
- exposed pad connections
- recommended footprint dimensions
- pad pitch
- component body size
- pin-1 marking
- polarity marking
- connector numbering
- transistor pin ordering
- diode polarity
- mechanical orientation

### Muon detector priority

The custom SiPM / MICROFC-60035 footprint must receive an especially careful check.

Do not consider DRC evidence that the footprint is correct.

A geometrically valid footprint can still have incorrect:

- pad numbering
- orientation
- polarity
- pin assignment
- package rotation

---

# 7. Power-System Audit

Generate:

```text
validation/static/power-audit.md
```

Build a logical representation of the power tree.

For every rail determine:

- source/regulator
- nominal voltage
- expected tolerance
- downstream loads
- expected approximate current
- IC absolute maximum ratings
- capacitor voltage ratings
- regulator input/output requirements
- enable-pin states
- startup conditions
- pullups/pulldowns
- reverse-current concerns
- high-voltage boundaries

Example conceptual tree:

```text
INPUT
  |
  +-- low-voltage regulator
  |     |
  |     +-- analog frontend
  |     +-- comparator
  |     +-- ADC
  |     +-- digital interface
  |
  +-- SiPM bias converter
        |
        +-- photodetector bias
```

Flag:

- inadequate voltage-rating margin
- missing power pins
- floating enables
- questionable startup states
- rails outside component operating limits
- possible paths from high-voltage nets into low-voltage circuitry

---

# 8. Decoupling Audit

For every IC supply pin:

1. identify associated decoupling capacitors
2. record capacitance
3. record capacitor technology if relevant
4. record voltage rating
5. inspect PCB placement
6. inspect ground-return path

Flag:

- missing local bypass capacitor
- bypass capacitor connected through an unnecessarily long path
- shared narrow return path
- unsuitable voltage rating
- large loop area between supply pin, capacitor, and ground

This should be treated as a semantic/layout check rather than merely a schematic-net check.

---

# 9. Circuit Simulation Philosophy

Do **not** attempt to simulate the entire PCB as one giant SPICE circuit unless a compelling reason appears.

Instead build independent testbenches around the important physical questions.

For the muon detector, implement approximately:

1. SiPM/front-end pulse response
2. comparator behavior
3. peak detector + ADC behavior
4. SiPM bias supply
5. optional digital IBIS/SI analysis

Prefer simulations that can be run non-interactively.

ngspice is preferred when practical because it supports:

```bash
ngspice -b simulation.cir
```

and can therefore become part of automated validation.

KiCad's integrated ngspice environment may also be used where convenient.

---

# 10. Simulation A: SiPM → Analog Frontend

## Objective

Determine whether realistic detector pulses produce the expected amplifier signal.

A perfect SiPM model is not required initially.

Start with a physically reasonable equivalent model containing some combination of:

- current pulse source
- detector capacitance
- source resistance if appropriate
- parasitic capacitance where relevant

Test:

- weak event
- nominal event
- large event

Sweep where possible:

- pulse charge/amplitude
- pulse width
- detector capacitance
- important feedback components
- supply variation

Measure:

- peak output voltage
- rise time
- fall time
- overshoot
- undershoot
- settling time
- clipping/saturation
- recovery time
- oscillation/ringing

Generate at minimum:

```text
input pulse
amplifier output
```

on the same or clearly related plots.

### Pass criteria

Create explicit criteria from the actual circuit requirements.

Examples:

```text
No sustained oscillation
No unexpected clipping for nominal event
Output crosses comparator threshold for expected event
Output returns sufficiently near baseline before expected next event
Overshoot remains within acceptable range
```

Do not invent numerical limits without documenting their justification.

---

# 11. Simulation B: Comparator

This is a high-priority simulation.

Feed the frontend output into the actual comparator circuit.

Plot:

```text
analog input
threshold
comparator output
```

Test:

### Signal cases

- noise only
- very weak pulse
- threshold-level pulse
- nominal pulse
- strong pulse

### Parameter variation

Sweep:

- threshold setting
- resistor tolerances
- comparator input offset if model permits
- hysteresis
- supply voltage
- frontend amplitude
- relevant noise assumptions

Measure:

- whether comparator fires
- trigger timing
- propagation delay
- multiple triggering/ringing
- minimum accepted pulse
- output voltage
- compatibility with receiving logic

Explicitly check whether hysteresis behaves as intended.

---

# 12. Simulation C: Peak Detector + Slow ADC

This is especially important because the design intentionally preserves analog amplitude information through:

```text
frontend
   |
   +-- comparator → fast trigger
   |
   +-- peak detector → slow ADC
```

Simulate the complete peak-hold behavior.

Plot:

```text
frontend pulse
peak detector voltage
ADC sampling point/window
```

Determine:

- acquisition time
- peak error
- droop rate
- useful ADC sampling window
- discharge/reset time
- ability to process subsequent pulses

Sweep:

- pulse amplitude
- hold capacitor tolerance
- leakage parameters
- diode characteristics where applicable
- resistor tolerances
- ADC input loading
- sampling delay

The final report should ideally produce a statement like:

```text
ADC sampling from T1 to T2 after comparator trigger
produces less than X% amplitude error over the tested event range.
```

If that cannot be justified, report the unresolved uncertainty.

---

# 13. Simulation D: SiPM Bias Supply

Simulate separately from the detector transient simulation.

Important questions:

- startup behavior
- target bias voltage
- overshoot
- ripple
- regulation
- component stress
- load response
- stability

Sweep:

- input voltage
- load
- feedback resistor tolerance
- output capacitance where relevant

Check every simulated voltage/current against component ratings.

The converter switching waveform does not need to be included in the nanosecond detector simulation unless there is a specific coupling question.

---

# 14. Tolerance / Corner Analysis

A nominal simulation proving that the circuit works once is insufficient.

Run component corners or Monte-Carlo-style perturbations.

At minimum consider:

```text
resistors
capacitors
supply voltage
detector pulse amplitude
detector capacitance
threshold setting
```

Reasonable first-stage analysis may use deterministic corners:

```text
nominal
min/min
min/max
max/min
max/max
```

For critical subcircuits, use broader random sweeps if supported and computationally inexpensive.

The important question is:

> Does the circuit work in a reasonable neighborhood around the nominal design?

rather than:

> Does one nominal SPICE simulation produce a nice waveform?

---

# 15. Automatic Simulation Measurements

Do not generate plots only.

Automatically extract meaningful engineering quantities.

Examples:

```text
Front-end peak amplitude
Front-end rise time
Front-end settling time
Maximum overshoot
Comparator trigger time
Comparator trigger/no-trigger status
Peak-detector acquisition error
Peak-detector droop rate
Peak-detector valid sample window
Bias output voltage
Bias overshoot
Bias ripple
```

Store tabulated results as CSV or JSON where useful.

Plots should supplement quantitative measurements.

---

# 16. Digital Signal Integrity

Full signal-integrity simulation is not initially required.

However, identify the fastest digital interfaces based on **edge rate**, not merely clock frequency.

For relevant FPGA/comparator/digital interfaces:

- identify driver
- identify receiver
- estimate trace length
- inspect termination
- inspect ground reference
- determine driver edge rate if available
- obtain IBIS models if readily available

If IBIS models exist and analysis is straightforward, perform a small test.

Look for:

- excessive overshoot
- undershoot
- ringing
- threshold crossings
- obvious source-termination need

Do not spend large amounts of time constructing a sophisticated SI environment unless initial analysis indicates a genuine problem.

---

# 17. Layout-Aware Semantic Checks

Create:

```text
validation/static/layout-audit.md
```

Inspect at least:

## Sensitive analog input

For the SiPM → amplifier path:

- trace length
- nearby switching nodes
- nearby digital traces
- parasitic capacitance
- ground reference
- input-node copper area
- routing through noisy areas

This path is likely more important than generic high-speed digital concerns.

## Ground

Check:

- continuous ground reference under critical signals
- accidental ground-plane splits
- traces crossing reference discontinuities
- narrow return-current bottlenecks
- high-current/switching returns near analog input paths

## Switching converter

Inspect:

- hot-loop area
- switching-node copper area
- distance from detector frontend
- feedback routing
- ground return
- inductive loop geometry

## Comparator

Inspect:

- threshold/reference routing
- coupling from output to input
- hysteresis routing
- output return path

## ADC / peak detector

Inspect:

- hold capacitor placement
- leakage-sensitive node routing
- nearby noisy signals
- ADC input path

---

# 18. Test-Point Audit

Check that important nodes remain observable during bring-up.

At minimum consider test access for:

```text
input supply
major regulated rails
SiPM bias output
analog frontend output
comparator threshold
comparator output
peak detector output
ADC reference
ground
```

Flag cases where debugging a likely failure would require probing an inaccessible SMD pin.

Good test access substantially reduces Rev-A bring-up difficulty.

---

# 19. Manufacturing Rules

The board has at least two manufacturing targets:

1. professional PCB fabrication
2. conservative home fabrication

Treat these as separate rule sets.

## Professional fabrication

Validate against the chosen manufacturer's requirements.

## Home fabrication

Use substantially more conservative limits for:

- trace width
- clearance
- annular ring
- via diameter
- drill diameter
- copper-to-edge distance
- solderability
- alignment tolerance

The home process may include mechanical rivet vias.

Therefore explicitly validate:

- rivet hole dimensions
- flange clearance
- nearby copper
- mechanical spacing
- ability to access/set the rivet

The board may pass professional-fab rules while failing home-fabrication rules.

Report both independently:

```text
Professional fabrication: PASS

Home fabrication:
WARNING
- 8 traces below preferred width
- 4 clearances below home-process target
- 3 vias incompatible with chosen rivet
```

---

# 20. Board Renders

Generate images of the PCB that can be reviewed by a vision-capable agent and human.

Desired outputs:

```text
top.png
bottom.png
top_3d.png
bottom_3d.png
```

Inspect for:

- backwards connectors
- wrong component orientation
- inaccessible connectors
- polarity ambiguity
- pin-1 marking
- component collisions
- mounting-hole interference
- silkscreen obscuration
- tall-component conflicts
- obvious mechanical problems

For custom or unusual components, compare the rendered physical orientation to photographs/datasheet drawings.

---

# 21. Fabrication File Generation

Generate the same files that would actually be uploaded to the PCB manufacturer.

At minimum:

```text
Gerbers
drill files
BOM
position/pick-and-place files if relevant
```

Where useful, also produce:

```text
STEP
IPC-2581
interactive HTML BOM
```

The fabrication artifacts themselves should be treated as validation targets.

---

# 22. Fabrication-File Audit

Do not assume that because KiCad looks correct, the exported manufacturing package is correct.

Inspect:

- board outline
- copper layers
- solder mask
- silkscreen
- plated holes
- non-plated holes
- drill sizes
- layer count
- board dimensions
- mounting holes
- component reference markings

Generate:

```text
validation/fab/FAB_AUDIT.md
```

The object being manufactured is the exported dataset, not the KiCad GUI state.

---

# 23. BOM / Procurement Audit

For each populated component verify:

- MPN
- manufacturer
- package
- quantity
- footprint compatibility
- basic electrical rating

Flag:

- obsolete parts
- wrong package variants
- ambiguous generic parts
- footprint/MPN mismatch
- insufficient voltage rating
- insufficient power rating

Availability/lifecycle checks may be performed when convenient but should not block electrical validation unless the part cannot realistically be obtained.

---

# 24. Optional Interactive HTML BOM

Generate an InteractiveHtmlBom or equivalent if straightforward.

This is useful for:

- visual component review
- assembly
- debugging
- checking reference designators
- associating BOM entries with physical PCB locations

It is not itself an electrical validator.

---

# 25. What Not to Spend Large Amounts of Time On Initially

For this board, avoid building elaborate analysis systems for:

## Full-board electromagnetic simulation

Not justified for the initial revision unless a concrete electromagnetic problem appears.

## Large-scale PDN simulation

The board is relatively low-current.

Simple current/voltage-drop calculations and good layout practices should be sufficient initially.

## Exotic high-speed digital simulation

Do not treat a modest FPGA clock frequency as equivalent to a multi-gigabit interface.

Edge rate matters.

Perform small IBIS or termination checks where useful, but do not make this the main validation effort.

---

# 26. Professional-Altium Capabilities We Are Trying to Approximate

Altium's professional value comes largely from integrating several tasks into one design database:

```text
component data
    ↓
schematic
    ↓
constraints
    ↓
PCB
    ↓
simulation
    ↓
manufacturing
    ↓
controlled release
```

We should recover the useful portions through:

```text
KiCad
+
Git
+
kicad-cli
+
ngspice
+
IBIS where useful
+
Python/static lint
+
datasheet auditing
+
fabrication artifact inspection
+
CI
```

Do not attempt to clone every Altium capability.

Prioritize validation that materially reduces first-revision failure probability.

---

# 27. Priority Ranking for the Muon Detector

Spend effort roughly in this order:

## Priority 1: Component correctness

Especially:

- SiPM footprint
- SiPM polarity
- amplifier pinout
- comparator pinout
- ADC pinout
- connector orientation

## Priority 2: Frontend transient behavior

Verify:

```text
SiPM pulse → amplifier
```

## Priority 3: Comparator behavior

Verify:

```text
amplifier → comparator threshold → digital trigger
```

## Priority 4: Peak detector

Verify:

```text
amplifier → peak hold → ADC
```

especially the valid ADC sampling window.

## Priority 5: Bias supply

Verify:

- correct voltage
- startup
- ripple
- stability
- separation from low-voltage circuits

## Priority 6: Analog PCB layout

Especially the SiPM/front-end input.

## Priority 7: Fabrication outputs

Inspect exactly what will be sent to the manufacturer.

## Priority 8: Digital SI

Perform limited analysis where the physical routing or edge rates justify it.

---

# 28. Final SUMMARY.md Format

The entire validation system should ultimately reduce its results to a short report.

Example:

```markdown
# PCB Pre-Fabrication Validation

## Overall status

FAIL

## Blocking issues

1. U3 footprint pin 4 does not agree with manufacturer datasheet.
2. Comparator output voltage may exceed receiving device's allowed input voltage.
3. `/RESET` is unconnected.

## Significant warnings

1. Peak-detector droop reaches 7.8% at 10 ms.
2. C17 voltage rating has insufficient margin.
3. SiPM input trace passes near the bias-converter switching node.

## Minor issues

1. D4 polarity is not clearly indicated on silkscreen.
2. TP5 is difficult to probe after assembly.

## Passed

- ERC
- PCB DRC
- schematic/PCB parity
- professional manufacturing geometry
- boost-converter startup
- mounting-hole clearance
- comparator nominal simulation

## Simulation summary

Frontend:
PASS

Comparator:
PASS

Peak detector:
WARNING

Bias supply:
PASS

Digital SI:
NOT REQUIRED / PASS / WARNING

## Human review requested

1. Confirm SiPM physical orientation.
2. Inspect frontend ground-return geometry.
3. Confirm connector J3 mating orientation.
4. Review peak-detector sampling-window requirement.

## Fabrication recommendation

DO NOT FABRICATE

Blocking issues must be resolved first.
```

When everything passes:

```text
FABRICATION RECOMMENDATION: READY FOR FINAL HUMAN REVIEW
```

Do **not** report:

```text
BOARD PROVEN CORRECT
```

Simulation and static analysis reduce uncertainty but do not prove that real mixed-signal hardware will behave exactly as simulated.

---

# 29. CI Integration

Once the local workflow works reliably, make it runnable from one command.

For example:

```bash
./validation/run_all.sh
```

or:

```bash
make validate
```

Eventually integrate deterministic portions into GitHub CI.

A commit or pull request should be able to produce:

```text
ERC: PASS
DRC: PASS
PARITY: PASS
COMPONENT AUDIT: PASS
MANUFACTURING: PASS
SIMULATION: PASS/WARNING
```

Simulation plots and reports should be retained as artifacts where practical.

---

# 30. General Engineering Principle

The validation system should distinguish three different questions:

### Geometry

> Can this PCB be manufactured?

Answered primarily by:

- DRC
- manufacturing constraints
- Gerber/drill inspection

### Connectivity

> Did we connect the things we intended to connect?

Answered primarily by:

- ERC
- schematic/PCB parity
- net inspection

### Physics

> Will the connected circuit actually behave the way we expect?

Answered primarily by:

- SPICE
- tolerance analysis
- SI analysis where justified
- datasheet reasoning
- layout review

Passing the first two does **not** imply the third.

The purpose of this project is to build all three levels into the pre-fabrication process.

---

# 31. Initial Definition of Done

For the first implementation, consider the validation infrastructure useful when the agent can automatically produce:

- [ ] ERC report
- [ ] DRC report
- [ ] schematic/PCB parity report
- [ ] ERC/DRC exclusions audit
- [ ] component/datasheet audit
- [ ] custom-footprint audit
- [ ] power-tree audit
- [ ] decoupling audit
- [ ] frontend SPICE simulation
- [ ] comparator SPICE simulation
- [ ] peak-detector SPICE simulation
- [ ] bias-supply simulation
- [ ] tolerance/corner results
- [ ] quantitative simulation measurements
- [ ] top/bottom PCB renders
- [ ] basic layout audit
- [ ] professional-fab rule audit
- [ ] home-fabrication rule audit
- [ ] Gerber/drill generation
- [ ] fabrication-file audit
- [ ] concise `SUMMARY.md`

Do not block initial implementation on sophisticated electromagnetic or PDN simulation.

The first objective is a system that reliably catches **ordinary expensive mistakes** before PCB fabrication.

---

# 32. Expected Outcome

The desired progression for PCB revisions is:

```text
Without validation:

Rev A:
"Does it even work?"

Rev B:
"Fix obvious mistakes."

Rev C:
"Now investigate analog performance."
```

versus:

```text
With validation:

Rev A:
"Basic topology, footprinting, connectivity,
and nominal circuit behavior have already
been challenged before fabrication."

Bring-up can focus on:
noise
real detector behavior
parasitics
EMI
component-model inaccuracies
and actual performance.
```

That is the purpose of this validation infrastructure.