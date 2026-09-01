# How the instrument works

This note explains the design decisions without duplicating the build values in
`design.md`. It is enough background to reason about a waveform or failed test;
it is not a general particle-detector textbook.

## From a muon to a voltage pulse

A charged particle crossing the plastic scintillator deposits energy and
produces a short flash. Reflective wrapping keeps more photons available to the
sensor, opaque wrapping rejects room light, and optical grease reduces reflection
at the scintillator/SiPM boundary.

The SiPM is an array of Geiger-mode avalanche cells. Its bias is set above the
device's measured breakdown voltage by an overvoltage. More overvoltage normally
increases gain and photon-detection efficiency, but also dark counts, optical
crosstalk, and afterpulsing. Breakdown rises with temperature—about 21.5 mV/deg C
for this onsemi family—so a fixed bias does not mean fixed gain.

The 6 mm sensor is also a several-nanofarad capacitive load. Its standard-output
current pulse develops a positive voltage across the anode sense resistor. A
larger resistor gives more voltage but slows recharge; revision A chooses
49.9 ohm for useful amplitude at very low event rates while retaining 10 ohm as
an experiment. Short local connections and cathode bypassing matter as much as
the nominal resistor value.

## Bias and analog signal chain

The MAX5026 stores energy in an inductor and releases it through a Schottky
diode into the high-voltage output. It switches near 500 kHz. The dangerous
noise loop is physically small but carries sharp current edges; a large LX
copper region or long return path turns it into an antenna. The feedback divider
controls average voltage, while the downstream resistor/capacitor filters reduce
switching ripple at the SiPM.

The divider was chosen so specified feedback-reference/current and resistor
tolerances impose a conservative 28.55 V normal-operation ceiling over the
initial 0-40 deg C range. That limit assumes an intact feedback path; it is not
single-fault protection. The meter reading—not the equation or trimmer
position—still sets the 27.2 V operating bias. Shutdown stops switching but does
not put a series switch between input and output; the output can retain charge
or sit near the input through the inductor and diode.

The SiPM pulse is AC-coupled into a TPH2502 amplifier. AC coupling removes the
sensor's DC operating point, and the buffered `VBASE` places the amplifier near
50 mV so a positive pulse has room without forcing the rail-to-rail amplifier to
operate exactly at ground. The non-inverting gain is

```text
gain = 1 + Rfeedback / Rground = 1 + 12.4 kohm / 1.00 kohm = 13.4
```

The coupling capacitor and 499 ohm bias path make a high-pass filter near
3.2 kHz. That corner is far below the pulse bandwidth; its purpose is to define
the DC state, not select muons. The amplifier's bandwidth is ample on paper, but
parasitic capacitance and inductance live in its feedback loop. A poor layout can
oscillate even when the schematic is correct.

## Turning amplitude into an event

The TLV3502 comparator asserts its push-pull output when `AMP_OUT` rises above
`VTH`. Because `AMP_OUT` rests near `VBASE`, the raw-equivalent threshold is

```text
(VTH - VBASE) / amplifier_gain
```

The comparator's internal hysteresis keeps a noisy crossing from toggling
repeatedly. Propagation delay is a few nanoseconds, but the exact crossing time
also depends on pulse amplitude: a large pulse reaches threshold sooner than a
small one. This time walk and unequal analog paths are why the coincidence
window must be measured rather than chosen only from a simulation.

A retriggerable one-shot converts each comparator edge into a nominally 200 ns
logic pulse. This makes synchronous FPGA capture insensitive to the unknown raw
comparator pulse width while preserving the leading-edge timing used for
coincidence. A direct comparator-output path exists only as a mutually exclusive
assembly option for later diagnostics. Consequently, the default FPGA input
does not contain physical time-over-threshold information: its width is set by
the one-shot, not by the time `AMP_OUT` remains above `VTH`.

The amplifier can momentarily rise above the comparator's 3.3 V rail. A series
resistor limits the comparator's protection current. Optional Schottky clamps
are left unpopulated unless the bench shows they are needed, because diode
capacitance can change the timing being measured.

## Capturing pulse height

The comparator reduces a pulse to a yes/no timing edge. In parallel, a second
wideband amplifier acts as a precision peak charger: while `AMP_OUT` rises, it
drives a Schottky diode and hold capacitor until `PEAK_HOLD` follows the pulse.
When the input falls, the diode opens and the capacitor retains the largest
voltage. Another amplifier channel buffers that high-impedance node before it
drives the cable and ADC divider. This separation is what makes a central slow
ADC practical; cable and ADC sampling capacitance do not sit on the nanosecond
signal or the hold capacitor.

The held voltage is the amplified pulse plus the approximately 50 mV baseline.
The ADC input attenuator maps the amplifier's nearly 5 V range into a 3.3 V ADC.
Analysis subtracts a measured post-reset baseline and applies the measured ADC
supply and divider ratio. The ADC codes are useful for threshold placement,
head matching, coupling comparisons, bias/temperature scans, and broad
distributions. Scintillator light collection, SiPM gain/crosstalk, amplifier
response, peak acquisition, and ADC reference are not calibrated well enough
to call the result deposited particle energy.

Peak capture trades speed against retention. A larger hold capacitor droops
less but demands more charge during the narrow pulse. A larger charging
resistor protects the amplifier and diode but slows acquisition. Those are the
only two prototype stuffing values intentionally left open until `AMP_OUT` is
measured. Diode leakage, reset-switch leakage, PCB contamination, and switch
charge injection then set the retained-voltage error.

The hold always contains the largest pulse since reset, not necessarily the
last pulse. Firmware must clear rejected singles after the coincidence window;
otherwise an unrelated earlier peak can be attached to a later coincidence.
For a valid pair, firmware waits for the cable/ADC filter to settle, reads both
multiplexed ADC channels while the local capacitors hold them, resets both
heads, and records the resulting busy interval as dead time. A later pulse can
still raise a held maximum during that interval, so comparator edges remain
monitored and any affected pulse-height record is flagged or discarded.

## Why local electronics and paired grounds help

Every signal flows in a loop. A cable is not merely a list of named wires: its
return conductors determine loop area, susceptibility, and ground shift. Each
head cable therefore pairs bias, analog power, logic power, and trigger with
nearby grounds. The signals traversing the cable are a full-amplitude digital
edge, a reset level, and a buffered slow held voltage; the small,
high-impedance SiPM and peak-hold nodes stay on the head.

The 100 ohm trigger resistor is source damping. It absorbs the initial mismatch
of a practical cable and reduces ringing at the far end. The FPGA-side pulldown
defines a safe low state when a head is disconnected. The detector uses a
floating Class II 5 V adapter. Connecting the Pmod ground then creates its one
intended DC reference to the Cora. Tying their independent 3.3 V regulators
together could create reverse current or a power-up conflict, so the Pmod
supply pins remain open. An earth-referenced scope can add another ground bond
during testing and must be connected deliberately.

## Coincidence and background rejection

One scintillator counts muons, radioactive backgrounds, SiPM dark events, light
leaks, and electronic noise. Requiring both separated paddles to fire within a
short interval rejects most unrelated events. It does not prove that every
accepted event is a muon, but aligned prompt coincidence should exceed a delayed
control if the instrument is working.

Each asynchronous trigger is synchronized to the FPGA clock and converted to a
single rising-edge event. Whichever channel arrives first opens a one-sided
window; the other channel completing the pair produces one coincidence. For
independent singles rates `R_A` and `R_B`, a useful small-window estimate is

```text
R_accidental ~= 2 R_A R_B tau
```

where `tau` is the one-sided window. A delayed coincidence measurement is more
trustworthy because it carries the instrument's real noise and threshold state.
Revision A delays channel B by exactly 1 ms in FPGA memory and applies a second
copy of the prompt algorithm to channel A and delayed B. The offset is far too
large for a physical muon pair, while both engines see the same thresholds and
noise environment. Independent lockouts prevent one ringing or extended event
from producing multiple coincidences, while singles counters remain useful
diagnostics.

At 125 MHz, one clock is 8 ns. A 13-cycle edge separation is 104 ns, and a
two-flop synchronizer adds latency. The one-shot's 150-250 ns acceptance range
ensures that the input remains present across several clocks. The 504 ns
bring-up window helps separate gross timing/connection faults from final-window
tuning; it is not automatically the best scientific setting.

## What a rate means

Muon flux is directional, and two finite paddles accept only trajectories that
cross both. Each selected 50 x 50 mm face has 2,500 mm2 projected area, matching
the nominal CosmicWatch paddle geometry. A square accepts somewhat different
maximum angles toward its corners than toward its edges, so its response is not
perfectly azimuthally symmetric. Increasing separation narrows the geometric
acceptance, lowering the rate while improving angular definition. Threshold,
optical coupling, temperature, nearby material, and live-time handling also
affect the result.

For `N` independent counts in live time `T`, the measured rate is `N/T` and the
counting-only relative uncertainty is approximately `1/sqrt(N)`. That is 10% at
100 counts, 5% at 400, and 2% at 2,500. Systematic changes can be larger, so an
obstructed run should be bracketed by open-reference runs at the same geometry,
thresholds, bias, and as nearly the same temperature as practical.

The useful proof sequence is:

1. synthetic pulses prove the electronics and digital counting;
2. darkness and flashlight tests prove the optical wrap;
3. threshold and bias scans find a stable plateau;
4. prompt exceeds delayed coincidence;
5. aligned exceeds deliberately misaligned coincidence; and
6. only then do angle or transmission comparisons become interpretable.

## Primary sources

Part sources and local copies are indexed in
[`docs/datasheets/README.md`](datasheets/README.md). The system-level comparison
is the [CosmicWatch v3X paper](https://arxiv.org/html/2508.12111).
