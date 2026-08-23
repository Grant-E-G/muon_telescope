# Muon Telescope Electronics: Short Theory and KiCad Brief

**Companion to:** `01_design_spec.md`  
**Purpose:** Explain what each circuit block does, why it is present, and what matters when drawing the boards in KiCad  
**KiCad target:** KiCad 10.0.5  
**Revision:** 0.3, 2026-08-20

---

## 1. The whole instrument in one page

A muon crossing a plastic scintillator produces a faint flash of blue light. A silicon photomultiplier, or SiPM, converts that flash into a short current pulse. The electronics amplify the pulse, decide whether it is large enough to count, and send a clean digital trigger to the FPGA.

Each detector follows this signal chain:

| Block | What it does | Why it is needed |
|---|---|---|
| Plastic scintillator | Converts a charged-particle crossing into light | A muon is not directly visible to ordinary electronics |
| SiPM | Converts a few collected photons into a current pulse | It is compact, sensitive, and operates below 30 V instead of the hundreds of volts used by a photomultiplier tube |
| 49.9 ohm sense resistor | Converts SiPM current into a small voltage | The amplifier needs a voltage signal |
| AC coupling and VBASE | Removes the DC operating level and places the pulse slightly above ground | The amplifier uses a single 5 V supply and cannot reproduce a signal below ground |
| TPH2502 amplifier | Multiplies the pulse voltage by about 13.4 | The raw pulse is too small for reliable threshold detection |
| TLV3502 comparator | Converts the analog pulse into a clean 0 or 3.3 V decision | The FPGA needs digital logic, not a noisy analog waveform |
| Cora Z7 FPGA | Counts singles, looks for two-detector coincidence, and timestamps events | A real muon should cross both aligned scintillators within a short time window |

The physical build uses:

- Two identical detector-head PCBs, one beside each scintillator.
- One power/interface PCB, containing the 5 V protection, 3.3 V regulator, SiPM-bias boost converter, two head connectors, and Pmod interface.

The amplifier and comparator stay beside the SiPM because the raw signal is only a few millivolts and is easily corrupted by a long cable. The cable carries the much more robust 3.3 V trigger instead.

---

## 2. What the SiPM circuit is doing

The onsemi MICROFC-60035-SMT-TR contains thousands of avalanche photodiode cells. When a photon triggers a cell, that cell produces a repeatable packet of charge. Many fired cells add together into a pulse proportional to the amount of detected light.

The SiPM requires a positive cathode bias above its breakdown voltage. Its breakdown voltage is approximately 24.2-24.7 V, and onsemi recommends operating 1-5 V above breakdown. Revision A therefore provides approximately 27.0-28.9 V and starts near 27.2 V.

The standard output is wired as:

```text
filtered bias -> SiPM cathode
SiPM anode -> 49.9 ohm -> ground
SiPM anode -> raw pulse and amplifier input
```

The 49.9 ohm resistor performs current-to-voltage conversion by Ohm's law. A 200 microamp pulse through 49.9 ohm produces about 10 mV. A 10 ohm alternate resistor gives faster recovery but a smaller voltage. At cosmic-ray rates, the larger 49.9 ohm signal is a reasonable first choice.

### Critical footprint detail

The 6 mm SiPM package is unusual:

- Pin 1 is anode.
- Pin 2 is the fast output and is left floating with no trace in revision A.
- Pin 3 is cathode.
- Pin 4 is a no-connect pad that should still be soldered. It may be grounded or left floating.
- Pin 5 is the center paddle and should not be soldered for this device.

This footprint must be checked against the current onsemi top and bottom views and printed at 1:1 scale before ordering boards.

---

## 3. What the boost circuit is and why it exists

The detector electronics receive 5 V, but the SiPM needs roughly 27-29 V at very low current. A boost converter creates that voltage using an inductor, a switching transistor, a diode, and an output capacitor.

In simplified terms:

1. The MAX5026 turns on its internal switch and builds current in a 47 uH inductor.
2. The switch turns off. The inductor forces its stored energy through a Schottky diode into the high-voltage capacitor.
3. Repeating this at approximately 500 kHz raises the output above the 5 V input.
4. A feedback divider tells the controller when the requested output voltage has been reached.

The MAX5026 was selected because it is specifically intended to generate adjustable low-current voltages up to 36 V, is used in the CosmicWatch reference design, and has a documented 5 V to 30 V example circuit.

Revision A changes the fixed 30 V example into an adjustable, safer range:

```text
feedback top:    147 kohm
feedback bottom: 6.65 kohm + 500 ohm 10-turn trimmer
typical range:   approximately 27.0-28.9 V
```

The output is filtered before reaching either SiPM. The raw converter output passes through 100 ohm and then 1 uF plus 10 nF to ground. Each detector head repeats a smaller local filter. These filters keep the 500 kHz switching ripple out of the millivolt signal path.

The boost converter starts disabled. A 100 kohm pulldown holds `SHDN` low until an enable jumper is installed. This lets you test the 5 V, 3.3 V, amplifier, and comparator circuits before applying bias to an expensive SiPM.

The boost is not suitable for solderless breadboard construction. Its switching loop must be compact, and the feedback trace must stay away from the inductor and LX switching node.

---

## 4. What the amplifier does and why this amplifier was chosen

The raw SiPM signal may be only several millivolts. The TPH2502 channel A is wired as a non-inverting amplifier:

```text
gain = 1 + 12.4 kohm / 1.00 kohm = 13.4
```

A 5 mV raw pulse therefore becomes approximately 67 mV above the baseline. This is large enough to compare against a stable threshold while leaving useful headroom on the 5 V supply.

### Why TPH2502-SR

- It has enough bandwidth and slew rate to preserve a fast SiPM pulse.
- Its inputs and output operate close to the supply rails.
- It works from a 5 V single supply.
- It is inexpensive and the SOP8 package is hand-solderable.
- Its second channel can buffer VBASE, so one dual amplifier completes the head circuit.
- It is close to the amplifier used and measured in the CosmicWatch v3X design.

The extra speed is useful but makes layout important. The 100 nF bypass capacitor, 12.4 kohm feedback resistor, and 1.00 kohm feedback resistor must sit beside the amplifier pins. Long feedback traces can make a fast amplifier ring or oscillate.

### Why AC coupling and VBASE are present

The SiPM pulse passes through a 100 nF series capacitor. A 499 ohm resistor then biases the amplifier input to VBASE. Together they form a high-pass filter near 3.2 kHz, removing slow drift while preserving the fast pulse.

VBASE is approximately 50 mV, made from the local 3.3 V rail with 130 kohm over 2.00 kohm and buffered by TPH2502 channel B. The amplifier output therefore rests slightly above ground instead of trying to sit exactly on its negative rail.

---

## 5. What the comparator does and why it is separate

A comparator answers one question: **is the amplified pulse higher than the threshold?**

The TLV3502 receives:

- `AMP_OUT` on its non-inverting input.
- Adjustable `VTH` on its inverting input.
- 3.3 V power, so its output is directly compatible with the FPGA.

When `AMP_OUT` rises above `VTH`, the output changes rapidly from 0 V to 3.3 V. When the pulse falls back below threshold, it returns to 0 V. The FPGA sees a clean logic pulse whose width is the time the analog pulse remained above threshold.

### Why TLV3502 instead of another op-amp

- It is designed to make fast yes/no decisions rather than reproduce an analog voltage.
- Its propagation delay is about 4.5 ns.
- It has a push-pull output, so no pullup resistor is required.
- Its inputs operate across the relevant voltage range.
- It works directly from 3.3 V.
- It includes about 6 mV of hysteresis.

Hysteresis means the turn-on and turn-off thresholds are slightly different. This prevents a noisy pulse sitting near the threshold from producing several rapid transitions.

The threshold trimmer is deliberately limited to roughly 0-0.53 V. Start near 0.10 V. With a 50 mV amplifier baseline and gain of 13.4, that is approximately equivalent to a 3.7 mV raw pulse:

```text
(100 mV threshold - 50 mV baseline) / 13.4 = 3.7 mV
```

A 1.00 kohm series resistor protects the comparator input if the 5 V amplifier output momentarily rises above the comparator's 3.3 V supply.

---

## 6. Power and FPGA interface

The detector uses its own 5 V input. An SS14 diode protects against reversed polarity, and a 500 mA resettable fuse limits fault current. A TLV75533PDBVR regulator creates the local 3.3 V used by both comparators.

The Cora and detector share ground, but their 3.3 V supplies are not connected. On Pmod JA:

| Physical pin | Connection |
|---:|---|
| 1 | Trigger A |
| 2 | Trigger B |
| 5 | Ground |
| 11 | Ground |
| 6 and 12 | Cora 3.3 V, deliberately unconnected |

The Cora's direct programmable-logic clock is 125 MHz. Each asynchronous trigger first passes through a two-flip-flop synchronizer. The FPGA then edge-detects the synchronized pulses, counts each detector, and records a coincidence when both occur inside the selected window.

An initial 100 ns window becomes 13 clock cycles, or 104 ns at 125 MHz. Comparator pulses should be at least three FPGA clock cycles, about 24 ns, so they are captured reliably.

---

## 7. The minimum circuit information for KiCad

Use two KiCad projects:

1. `detector-head`, fabricated twice.
2. `power-interface`, fabricated once.

### Detector-head values

| Function | Revision A value |
|---|---|
| SiPM | onsemi MICROFC-60035-SMT-TR |
| Sense resistor | 49.9 ohm |
| Input coupling | 100 nF |
| Input bias resistor | 499 ohm to VBASE |
| Amplifier | 3PEAK TPH2502-SR, SOP8, powered from 5 V |
| Amplifier feedback | 12.4 kohm and 1.00 kohm, gain 13.4 |
| VBASE divider | 130 kohm and 2.00 kohm, buffered, about 50 mV |
| Comparator | TI TLV3502AIDR, SOIC-8, powered from 3.3 V |
| Comparator input protection | 1.00 kohm series |
| Threshold | 4.70 kohm, 1.00 kohm, and 10 kohm 10-turn trimmer |
| Trigger output | 100 ohm series resistor |
| Bias filter | 100 ohm, 1 uF / 50 V, and 10 nF / 100 V |

### Power/interface values

| Function | Revision A value |
|---|---|
| 5 V input | JST B2B-XH-A(LF)(SN), XHP-2 housing |
| Input protection | 500 mA resettable fuse and SS14 diode |
| 3.3 V regulator | TLV75533PDBVR |
| Boost converter | MAX5026EUT+T, SOT-23-6 |
| Inductor | 47 uH shielded ferrite, DCR below 1 ohm, saturation current at least 350 mA |
| Boost diode | 60 V Schottky |
| Boost output | Two 1 uF / 50 V ceramic capacitors |
| Feedback | 147 kohm over 6.65 kohm plus 500 ohm trimmer |
| Head connectors | JST B8B-XH-A(LF)(SN), XHP-8 housings |
| FPGA connector | Standard 2x6, 2.54 mm Pmod-compatible right-angle male header |

The detailed schematic nets, connector pinout, test points, DNP options, and bring-up measurements remain in the board-ready build specification.

---

## 8. KiCad workflow for the two of you

One person can capture the detector head while the other captures the power/interface board. Do not edit the same KiCad file simultaneously. Swap projects for review before routing.

### Schematic pass

1. Enter the exact manufacturer part number and datasheet URL for every IC and connector.
2. Create the custom SiPM symbol and footprint from the current onsemi drawing.
3. Add power symbols, no-connect markers, test points, connector pin numbers, and DNP fields.
4. Annotate and assign exact footprints.
5. Run ERC and resolve every result rather than suppressing unexplained warnings.

### Placement pass

On the detector head, place in signal order:

```text
SiPM -> sense resistor -> coupling capacitor -> amplifier -> comparator -> connector
```

On the power board, keep the MAX5026, inductor, diode, and first output capacitor in one tight cluster. Put the feedback divider beside the FB pin and away from LX.

### Routing rules that matter most

- Use a continuous bottom-layer ground plane. Do not split analog and digital ground.
- Keep `SIPM_RAW`, amplifier feedback, and `AMP_OUT` short and local.
- Put every 100 nF bypass capacitor beside its IC supply pin.
- Keep the boost switching loop and LX copper small.
- Keep the bias trace away from the raw SiPM input.
- Route each cabled trigger with an adjacent ground conductor.
- Refill ground zones before every DRC and export.

---

## 9. What can be breadboarded

Reasonable solderless-breadboard exercises:

- The 3.3 V threshold divider and trimmer.
- A slow comparator demonstration.
- 3.3 V FPGA trigger pulses and coincidence logic.
- Pmod pulldowns and indicator LEDs.

Do not use a solderless breadboard to judge:

- The MAX5026 boost converter.
- Raw SiPM pulse quality.
- TPH2502 stability or ringing.
- Nanosecond timing.

If available, the onsemi MICROFC-SMTPA-60035-GEVB adapter provides through-hole pins for a nonfinal SiPM experiment. onsemi warns that its timing is not optimized. The best pre-SiPM test is still injecting a small pulse into the assembled detector-head PCB.

---

## 10. The release checklist

Both designers should verify:

- [ ] SiPM pad numbers match both manufacturer views; pin 4 is soldered, pin 5 is not, and pin 2 has no trace.
- [ ] Head cables are straight through and continuity-tested; Pmod orientation matches Cora JA.
- [ ] Local 3.3 V never connects to Pmod pins 6 or 12.
- [ ] Boost starts disabled, adjusts approximately 27.0-28.9 V, has a compact switching loop, and keeps FB away from LX.
- [ ] Amplifier feedback and bypass parts are beside the IC.
- [ ] Bottom ground plane is continuous; ERC and DRC have no unexplained results.
- [ ] A 1:1 print matches the real assembly, and final Gerbers and drill files pass independent viewing.

If any of the SiPM footprint, Pmod orientation, head cable, or boost layout remains ambiguous, stop before ordering. Those four mistakes can defeat an otherwise correct board.

---

## 11. Primary references

Component references: [onsemi SiPM datasheet](https://www.onsemi.com/download/data-sheet/pdf/microc-series-d.pdf); [onsemi readout note](https://www.onsemi.com/download/application-notes/pdf/and9782-d.pdf); [MAX5026 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/max5025-max5028.pdf); [TPH2502 product page](https://www.3peak.com/high-speed-op-amps/tph2502); and [TLV3502 datasheet](https://www.ti.com/lit/gpn/TLV3502).

Platform and workflow: [Cora Z7 reference manual](https://digilent.com/reference/programmable-logic/cora-z7/reference-manual); [KiCad 10 getting-started guide](https://docs.kicad.org/10.0/en/getting_started_in_kicad/getting_started_in_kicad.html); and [CosmicWatch v3X paper](https://arxiv.org/html/2508.12111).
