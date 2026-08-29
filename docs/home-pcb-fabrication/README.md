# Independent home PCB fabrication workflow

Status: prototype process; independent of the telescope design and fabrication
release

Last reviewed: 2026-08-29

This folder covers toner-transfer FR-4 boards up to 70 x 100 mm, etched with MG
Chemicals `415` ferric chloride, printed on the existing Brother `HL-L2370DW`,
drilled on the existing WEN `4208T` press, and joined with coupon-qualified
Litoexpe `GAOC1570` eyelets formed by the matched `GAOC1573` steel tooling in
the stationary drill-press chuck. The direct Amazon pair and its delivered-cost
cases are recorded in [bom.md](bom.md). This
workflow does not approve a telescope PCB or modify its design record.

## Practical safety model

The sensible setup is the open-air balcony, not an indoor room and not an
airtight box. Put the shallow polypropylene working tray inside an ordinary
HDPE or polypropylene storage tub. A second compatible tray resting upside-down
over the working tray is a useful splash shield, but it must retain a visible
vent gap. Keep the whole etching and rinse operation outdoors.

For one run:

- use no more than 100 mL of room-temperature etchant;
- use only plastic containers and tools around the etchant;
- do not heat, spray, bubble, pump, or vigorously agitate it;
- keep the stock bottle closed and outside the working tub when it is not being
  poured;
- stand upwind, keep your face out of the container, and keep doors and windows
  closed nearby; and
- exclude children, pets, food, rain, and any location where a spill could
  reach another balcony, soil, or a drain.

Stay with the etch. If there is a sharp acid odor at the normal standing
position, eye or throat irritation, visible mist, an unexpected reaction, or
insufficient outdoor airflow, set the loose lid in place, move away upwind, and
let the area clear. A lack of odor is not an exposure measurement.

Use splash goggles, long sleeves and pants, closed shoes, and 13-inch reusable
nitrile chemical gloves. Stage a 32 oz eyewash bottle for the immediate first
flush and verify the unobstructed route to a household sink or shower before
pouring. The bottle is finite and intended only as the first response: after
using it, continue flushing at the sink or shower for the etchant SDS's full 30
minutes and call Poison Control or a doctor.

Secondary containment is the main spill control. For a small spill contained
in the tub, keep it there, absorb any remaining free liquid with compatible
inert absorbent, and package all residue for household hazardous waste (HHW).
Do not add bleach, ammonia, solvents, or another cleaner. Baking soda may be
kept for minor surface decontamination only; adding it can foam and heat, and
does not make copper-bearing waste safe for a drain or trash.

## HCl calculation

The copper etch itself does **not** produce hydrogen chloride gas:

```text
Cu + 2 FeCl3 -> CuCl2 + 2 FeCl2
```

The stoichiometric HCl production is therefore zero. The current MG `415` SDS
instead lists 1 wt% HCl already present in a solution with density
1.38-1.49 g/mL. A 100 mL run consequently contains about 1.38-1.49 g HCl in
total. That inventory is a deliberately unrealistic all-released bound, not a
prediction of emissions.

NOAA HAZMAT Report 93-3 gives HCl partial pressures over **2 wt% aqueous HCl**
of 0.0207 Pa at 20 degrees C and 0.0627 Pa at 30 degrees C. Log interpolation
at 25 degrees C gives:

```text
Pv = sqrt(0.0207 * 0.0627) = 0.0360 Pa
surface-equilibrium concentration = Pv / 101325 * 1e6 = 0.356 ppm
```

This 2% aqueous comparison contains twice as much HCl as MG `415`, but it is not
a measured value for the ferric-chloride matrix. Dissolved salt can change HCl
activity, so it is a useful screening value rather than a guaranteed upper
bound.

Using NOAA's simple outdoor-puddle mass-transfer model,

```text
E = A * Km * MW * Pv / (R * T)
Km = 0.0048 * U^0.78 * Z^-0.11 * Sc^-0.67
```

with a conservative 0.0406 m2 exposed surface (the selected tray's full
7 x 9 in physical footprint), 1 m/s wind, 0.229 m along-wind dimension, Schmidt
number 0.9, 25 degrees C,
`MW = 0.03646 kg/mol`, and `R = 8.314 J/(mol K)`, the 2% comparison pressure
gives `Km = 0.00606 m/s`, an HCl evaporation estimate of **0.47 mg/hour**, or
**0.94 mg during a two-hour etch**. A deliberately crude 10x matrix/condition
screen would be 4.7 mg/hour and 9.4 mg in two hours. The corresponding
surface-equilibrium comparisons are 0.36 and 3.6 ppm; the open-air breathing
zone should be lower because of dilution. The model assumes almost the entire
inner surface is exposed, so it does not take credit for the loose cover. Those
two-hour mass estimates are about 0.067% and 0.67%, respectively,
of the approximately 1.4 g inventory.

For context only, the OSHA and NIOSH occupational ceiling for HCl is 5 ppm.
This calculation is not air monitoring or a compliance determination. Its
uncertainty is why the process remains outdoors, cool, unsprayed, loosely
covered, and small-volume. It also shows that splash, eye contact, and disposal
are the dominant practical hazards here—not kilograms of newly generated HCl
gas. MG's broader warning about hydrogen applies if the acidic solution contacts
reactive metals, another reason to use plastic tools and never seal the setup.

## Expected quality

| Feature | Realistic result |
|---|---|
| 0805 and SOIC | Reasonable after a passing coupon |
| 0.65 mm pitch | Possible, but printer/transfer/etch dependent |
| QFN, BGA, controlled impedance | Use a commercial board |
| Double-sided registration | Manual and variable |
| WEN-drilled holes | Usable prototype quality; expect more burrs and bit wear |
| Budget eyelet vias | Functional after joining both sides; received dimensions and coupon still control the layout |

Make a coupon first with the minimum trace/space, a measured 100 mm artwork
dimension, front/back registration marks, ground-plane clearances, and several
2.0 and 2.1 mm eyelet holes. Do not populate a board until the coupon passes
visual inspection and continuity.

## Layout for eyelets

1. Use eyelets as dedicated vias; do not share an eyelet with a component lead.
2. Use the matched Litoexpe `GAOC1570` eyelets (Amazon ASIN `B0DYY6MCZS`) and
   `GAOC1573` forming-tool set (ASIN `B0DYY4NCQW`). The listing publishes a
   2.0 mm barrel OD, 3.5 mm flange OD, and 3.45 mm overall height; “1.5 mm” is
   the nominal opening. Measure at least five received parts and reject split,
   badly out-of-round, or inconsistent parts.
3. Do not freeze the pad diameter until those measurements and the coupon are
   recorded. Size the pad so the complete as-formed collar remains on copper
   with useful inspection and soldering clearance on both sides.
4. Make 2.0 and 2.1 mm coupon holes with the owned Genmitsu `PD30A`. The barrel
   is nominally 2.0 mm, so accept the largest hole that permits insertion
   without force but does not allow excessive wobble after allowing for WEN
   runout. The 2.1 mm bit is larger and less fragile than the smaller tooling
   previously considered. Do not exceed 3.0 mm.
5. The listing describes the eyelet as brass and an associated “gasket” as
   iron. Magnet-test the received fastener and reject it if ferrous material is
   exposed in the current path, corrodes, flakes, or prevents normal solder
   wetting. The formed and soldered coupon must pass continuity before layout.
6. Add bottom-plane antipads around every non-ground hole. A hole through an
   unbroken ground plane is a short, whether or not it contains an eyelet.
7. Keep both eyelet collars accessible for forming, inspection, and joining.

## Workflow

### 1. Artwork and copper

1. Generate top and bottom artwork at 1:1 with explicit mirror settings. Include
   100 mm horizontal and vertical scale bars, 6/8/10/12 mil trace-space tests,
   solid fills, and registration marks on the coupon.
2. Use the Brother desktop driver, not mobile printing. Select the manual feed
   slot and rear face-up output; `Actual size`/100% scaling; one-sided output;
   1200 x 1200 dpi or HQ1200; Graphics mode; Toner Save off; and high density.
   Start with the Labels media setting. Feed one laser-rated transfer sheet at a
   time with its printable surface facing up. The paper instructions override
   the starting media setting if they differ.
3. Measure both printed 100 mm bars. Reject scaling error greater than 0.2 mm,
   skew, broken 8-10 mil features, or pinholes in solid fills. Transfer this
   coupon before assuming the particular toner and paper work together.
4. Prefer a pre-sized blank. Cutting or routing FR-4 creates much more dust than
   drilling a few holes.
5. Wet-clean copper with dish detergent and a dedicated fine nonmetallic pad.
   Do not dry-sand or use steel wool. Capture the residue with the process
   waste.
6. Transfer toner using the transfer-medium instructions and an existing
   household iron or laminator dedicated to workshop use. Keep this dry step
   away from chemistry.
7. Inspect under magnification. Reject smears, missing fine features, or poor
   front/back registration.

### 2. Balcony etch and rinse

1. Place the shallow PP working tray in the larger #2 HDPE or #5 PP tub.
   Dry-fit everything and confirm the tub can retain all liquid staged for the
   run. Before opening etchant, put the panel in the level tray, add 100 mL of
   water, and verify the panel stays covered during a slow, gentle tilt. Reject
   a tray that fails this geometry check.
2. Put on gloves and splash goggles. Open the stock bottle outdoors below face
   level and pour no more than 100 mL. Recap it immediately.
3. Lower the board with plastic tongs and rest the second PP tray upside-down
   over the working tray with a visible gap. Never snap, tape, gasket, or weight
   the cover shut.
4. Keep the room-temperature etch attended. A slow, occasional gentle tilt is
   acceptable if it does not splash; do not shake or use an air bubbler.
5. When unwanted copper is gone, lift the board over the etchant and place it
   directly into the first of two captured-rinse containers. Remove toner by
   wet rubbing, without adding a solvent.
6. Transfer spent etchant to a separate compatible screw-cap waste bottle only
   after no metal remains and no reaction is visible. Label it with its actual
   contents and date. Do not return spent etchant to the stock bottle.

### 3. Waste and cleanup

Fresh or spent etchant, copper-bearing rinses, failed boards, wipes, dust, and
spill residue do not go into a sink, toilet, storm drain, soil, ordinary trash,
or the shop vacuum. Keep liquids closed in compatible labeled containers and
take them through the local HHW program. Confirm local packaging rules before
the first run; San Mateo County's program is linked below.

Clean reusable plastic tools over the captured-rinse container. Damp-wipe dry
work surfaces. Store the original etchant bottle upright, tightly closed, in a
plastic tub away from bases, metals, heat, food, children, and pets.

### 4. Drill on the existing WEN press

The WEN `4208T` is not an ideal high-speed PCB drill, but it will make prototype
holes when the setup is rigid. The selected Genmitsu `PD30A` set contains
solid-carbide spiral-flute drills intended for PCB work, including 2.0 and 2.1
mm sizes; they are not pointed engraving burrs or flat end mills. At the
press's 3,140 RPM maximum, expect slower work, greater thrust, more exit burr/chip-out,
shorter carbide-bit life, and less consistent diameter than a purpose-built PCB
spindle. The coupon decides whether that quality is acceptable.

1. Work outdoors. Clamp the vise to the press table and support the complete
   PCB flat on a clean sacrificial backer. Never hand-hold the board.
2. For the eyelet coupon, drill 2.0 and 2.1 mm holes with the owned 3.175
   mm-shank solid-carbide bits at the highest speed, 3,140 RPM. Tighten the
   chuck at all three key positions and remove the key. Retain the largest hole
   that gives low insertion force without excessive eyelet wobble.
3. Position a shop-vac hood immediately beside and partly around the drill
   point. Start the vacuum before the spindle.
4. Feed vertically with very light pressure and brief pecks. Do not side-load
   or force the brittle bit. Stop for chatter, heating, smoke, excessive force,
   delamination, or a moving board.
5. Inspect the coupon for diameter, registration, burrs, glass breakout, and
   eyelet fit before drilling the real board.
6. Vacuum the board, backer, vise, shroud, and table, then damp-wipe them. Do not
   use compressed air or dry sweeping.

Wear impact-rated eye protection, tie back hair, and remove jewelry and loose
clothing. Do not wear gloves near the rotating spindle.

#### Shop-vac and printed holder

A 3D-printed holder is enough **as the close-capture hood** for a few small
outdoor prototype boards if it is rigid, close to the hole, and paired with a
working dry-dust vacuum setup. It is not a filter by itself and does not make a
generic vacuum a certified HEPA machine.

Use the existing shop vac with a compatible dry collection bag and a serviceable
dry cartridge/filter. Inspect the hose, lid, and filter seals and direct the
exhaust away from people, doors, and windows.
The print must clear the bit, chuck, quill, vise, and full travel; stay fixed
without a hand holding it; and be dry-run with the press unplugged. A small
opening close to the bit is more effective than a large nozzle several inches
away. Stop and improve the hood if a bright side light shows a dust plume.

For this limited outdoor use, do not buy a new certified extractor or HEPA
vacuum. A disposable N95 is reasonable secondary protection if one is already
available or many holes are planned, but source capture and outdoor work remain
the primary controls. Replace a bag or cartridge only if the existing one is
missing, damaged, or unsuitable for dry collection; the exact replacement is
shop-vac-model-specific.

### 5. Form and verify eyelets

1. Deburr the 2.0 and 2.1 mm coupon holes and insert a measured `GAOC1570`
   eyelet into each without force.
2. With the WEN unplugged and its switch off, clamp the `GAOC1573` lower base
   to the table. Put the eyelet factory flange down on its matching support and
   keep the board flat; do not bridge it across vise jaws or a recess.
3. Chuck the `GAOC1573` straight 8 x 98 mm steel forming ram; its listed 8 mm
   diameter is within the WEN's 0.5 in / 12.7 mm chuck capacity. Verify secure
   grip, tighten at all three chuck-key positions, and remove the key.
   Do not use the included hollow punch on FR-4. Align the ram with the eyelet,
   set the depth stop conservatively on scrap, and lower the quill by hand in
   small increments. Never turn on the spindle. Stop rather than applying
   appreciable spindle load; the WEN manual does not give an eyelet-press rating.
4. Reject a split tail, cracked or lifted pad, tilted eyelet, loose fit, or
   deformed board. The formed eyelet provides retention, not a dependable
   electrical joint by itself.
5. Join both collars using the existing assembly equipment. Excessive dwell can
   loosen a marginal eyelet or lift a pad.
6. Inspect both sides under magnification and measure continuity. On the coupon,
   require less than 0.1 ohm after subtracting lead resistance and no
   intermittence during gentle flexing.

## Emergency summary

- **Eyes:** flush immediately with the staged bottle, then continue with
  running water for at least 30 minutes. Remove contacts if easy and call
  Poison Control/doctor without delaying the rinse.
- **Skin:** remove contaminated clothing and rinse with plenty of water.
- **Inhalation:** move to fresh air and seek advice if symptoms persist.
- **Swallowing:** rinse the mouth, do not induce vomiting, and call Poison
  Control.
- **Uncontrolled spill or unusual gas/reaction:** move away and call emergency
  services rather than attempting an improvised cleanup.

US Poison Control: 1-800-222-1222. Call 911 for a life-threatening emergency.

## Primary sources

- [MG Chemicals 415 product page](https://mgchemicals.com/products/circuit-board-design/copper-etchants/ferric-chloride-etching/)
- [MG Chemicals 415 US/Canada SDS](https://www.mgchemicals.com/downloads/msds/01%20English%20Can-USA%20SDS/sds-415-l.pdf)
- [NOAA HAZMAT Report 93-3, hydrochloric-acid evaporation model](https://library.oarcloud.noaa.gov/noaa_documents.lib/NOS/HMRA/HAZMAT_report_93-3.pdf)
- [NIOSH hydrogen-chloride limits](https://www.cdc.gov/niosh/npg/npgd0332.html)
- [Brother HL-L2370DW specifications and manuals](https://support.brother.com/g/b/manualtop.aspx?c=us&lang=en&prod=hll2370dw_us)
- [Genmitsu PD30A PCB drill set](https://www.sainsmart.com/products/genmitsu-30pcs-pcb-drill-bits-set-0-1mm-3-0mm-1-8-shank-pd30a)
- [Genmitsu PCB drill-bit buying guide](../datasheets/home-pcb-fabrication/genmitsu-pcb-drill-bits-buying-guide.pdf)
- [Litoexpe GAOC1570 eyelets, Amazon ASIN B0DYY6MCZS](https://www.amazon.com/dp/B0DYY6MCZS)
- [Litoexpe GAOC1573 tooling, Amazon ASIN B0DYY4NCQW](https://www.amazon.com/dp/B0DYY4NCQW)
- [WEN 4208T product and manual](https://wenproducts.com/products/wen-4208t-2-3-amp-8-inch-5-speed-benchtop-drill-press)
- [NIOSH local-exhaust hood proximity guidance](https://www.cdc.gov/niosh/engcontrols/ecd/detail39.html)
- [First Aid Only personal-eyewash product sheet](../datasheets/home-pcb-fabrication/first-aid-only-eyewash-product-sheet.pdf)
- [San Mateo County household hazardous waste](https://www.smchealth.org/hhw)
