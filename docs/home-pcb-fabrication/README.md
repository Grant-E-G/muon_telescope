# Independent home PCB fabrication workflow

Status: reviewed prototype draft; chemical work remains blocked by the listed
safety gates and this is not a fabrication release

Last reviewed: 2026-08-25

This folder is intentionally independent of the telescope design, project BOM,
and release workflow. It describes a small-batch toner-transfer process for
experimental FR-4 boards. It does not approve any telescope board for use and
does not change `docs/design.md` or `docs/build-and-debug.md`.

The separately sourced equipment and consumables are in [bom.md](bom.md).
Read the current safety data sheet (SDS) for every chemical before each run;
the SDS and product label override this workflow.

## Safety decision

Do **not** etch in a sealed box or airtight bottle. The expected copper/ferric
chloride etch reaction does not normally evolve hydrogen, but the commercial
mixture also contains hydrochloric acid and its current SDS warns generally
that metal contact can form flammable hydrogen and that prolonged metal contact
in an enclosed space can produce explosive quantities. A closed reaction
vessel is therefore outside the manufacturer's safety guidance and creates an
avoidable pressure and ignition hazard.

The accepted arrangement is:

- perform the entire etch outdoors, not in a shared garage or room;
- use a shallow PP/PPCO or HDPE working tray inside a larger compatible
  secondary-containment tray;
- place a loose, non-latching cover over the working tray as a splash shield,
  leaving it vented at all times;
- work at room temperature, with no heater, air bubbler, pump, atomizer, or
  spray;
- stay upwind and away from doors, windows, ignition sources, vehicles, metal
  tools, soil, gutters, and storm drains; and
- open, inspect, rinse, and transfer the board outdoors. Do not carry a tray of
  reacting etchant through the house.

The original capped chemical bottle may be transported in clean secondary
containment. That is different from sealing copper and etchant together.

Stop and outsource the PCB if any of these controls is unavailable:

- immediate hands-free flushing water capable of at least 30 minutes of
  continuous eye irrigation, as required by the selected etchant SDS, plus an
  immediately available body-drench route;
- a stable outdoor location with secondary containment;
- confirmed chemical-resistant gloves, sealed splash goggles, protective
  clothing, and a second adult aware of the emergency plan;
- a legal household-hazardous-waste path for all etchant and contaminated
  rinses; or
- safe dust capture and a rigid drill setup.

## Expected quality

This is a prototype process, not a substitute for plated-through,
solder-masked, impedance-controlled commercial fabrication.

| Feature | Realistic expectation |
|---|---|
| 0805 and SOIC footprints | Reasonable after a passing process coupon |
| 0.65 mm pitch | Possible, but must pass the exact printer/transfer/etch coupon |
| Fine-pitch, QFN thermal pads, BGAs | Do not use this process |
| Double-sided registration | Manual and variable; inspect every pad and hole |
| Riveted vias | Mechanically useful but larger and less repeatable than plated vias |
| Handheld household-drill holes | Poor position, angle, and diameter control; not accepted for rivets |
| Existing WEN `4208T` press and vise | Better position and perpendicularity than a hand drill, but **not yet accepted for FR-4**; see the drilling gate below |
| Purpose-built high-speed PCB drill | Best expected hole wall, registration, and bit life; still requires a process coupon |

The selected 0.8 and 0.9 mm carbide drills list recommended speeds of 60,000
and 53,000 RPM respectively. The WEN `4208T` reaches only 3,140 RPM: about
19 and 17 times slower. Its chuck does accept the drills' 3.175 mm shanks and
the press/vise improve rigidity, but those facts do not resolve the speed
mismatch. More importantly, the WEN manual describes the tool as designed for
wood and metal and warns that drilling other materials can cause fire, injury,
or tool damage. FR-4 is a glass-fiber/epoxy composite, not either listed
material.

Do not use the `4208T` on FR-4 unless WEN confirms that exact use in writing
and the drill manufacturer supplies a safe speed/feed recommendation at or
below 3,140 RPM. If both confirmations are obtained, the result is still
coupon-qualified prototype quality: reject chipped, delaminated, oversize,
angled, rough, or misregistered holes. Otherwise have the holes or complete
boards made commercially, or revise this workflow around a purpose-built
PCB-rated high-speed drill. A successful-looking hole alone cannot override a
manufacturer safety warning.

Ask WEN at `techsupport@wenproducts.com` and MIPEC at `info@mipec.eu`. State
the exact models, 1.6 mm copper-clad FR-4, 0.8/0.9 mm carbide drill diameters,
3.175 mm shank, and the WEN's 3,140 RPM maximum; request permitted speed, feed,
pecking, dust-control, and tool-life limits rather than a general assurance.

## Layout gates before artwork

1. Use the rivets as dedicated vias. Do not share a rivet hole with a component
   lead unless that exact stack-up is proven on the coupon.
2. The selected 0.6 mm-ID rivet has a 0.8 mm OD and 1.3 mm head. Start with a
   2.0 mm pad on both sides and validate it on the coupon before reducing it.
3. Provide both 0.8 and 0.9 mm test holes. Fortex calls for a 0.8 mm hole and
   separately notes a 0.1 mm oversize for CNC drilling. Home-tool runout is
   unknown, so choose the smallest coupon hole that seats the rivet without
   force and forms a sound flare.
4. A solid, unetched bottom ground plane is safe only when **every** hole that
   touches it is ground. Any non-ground rivet or through-hole in a solid bottom
   plane is a short circuit. Either etch bottom-side antipads/clearances around
   every non-ground hole or restrict all through-holes to ground and keep all
   other circuitry surface-mount on top.
5. Place rivets where both collars remain accessible for inspection and
   soldering. Keep them clear of component bodies and probe areas.
6. Add a coupon to the panel containing the minimum trace/space, smallest pad,
   double-side registration marks, ground-plane antipads, and several rivet
   holes of each candidate diameter.

## 1. Pre-run gate

Do not start until every box is checked.

- [ ] Current MG 415 SDS and emergency number are printed or available without
  unlocking a phone.
- [ ] Poison Control number is available: US 1-800-222-1222; call 911 for a
  life-threatening emergency.
- [ ] Hands-free flushing water has been activated and tested. It can run for
  at least 30 minutes and is reachable immediately without doors or obstacles.
  The body-drench route is also clear and working.
- [ ] A second adult knows the chemical, location, first-aid steps, and how to
  call for help. Do not do the chemical pour alone.
- [ ] Weather is dry and calm enough to control splashes; the table is level
  and cannot be bumped.
- [ ] Children, pets, food, drinks, and unrelated work are excluded.
- [ ] Working tray, loose cover, secondary tray, plastic forceps, waste
  container, labels, absorbent, and water for captured rinsing are staged.
- [ ] CHEMSORB has confirmed `SP60AN-LB2` compatibility with the exact current
  MG 415 mixture. Its SDS says to test compatibility, warns that acid contact
  forms carbon dioxide, and requires well-ventilated use. Do not count an
  unconfirmed absorbent as a spill control.
- [ ] The glove manufacturer has confirmed the selected glove model and
  breakthrough/use time for the exact MG 415 mixture. The SDS explicitly says
  it cannot recommend a glove material without this check.
- [ ] Indirect-vent D3 splash goggles fit and seal. A face shield is worn over
  them for pouring and board removal; it is not a substitute for goggles.
- [ ] Chemical apron, long sleeves, long pants, and closed chemical-resistant
  footwear are on. Contact lenses are removed.
- [ ] Household-hazardous-waste acceptance and packaging instructions have
  been confirmed before waste is generated.
- [ ] Drilling will be outsourced, or written WEN approval for `4208T`/FR-4
  use and written bit-maker guidance for no more than 3,140 RPM are filed.
- [ ] The existing solder-fume extractor's exact model and consumable MPNs are
  recorded, its current manual has been checked, and its source capture works.

## 2. Process coupon

Fabricate the coupon before any functional board. It must use the same board,
printer, toner, transfer sheet, heat tool, artwork settings, etchant batch,
drilling setup, and rivet tooling as the planned board.

Record:

- printer model, toner cartridge MPN, driver, density, scaling, and measured
  100 mm artwork dimension;
- copper-clad MPN and measured thickness;
- heat-tool model/setting, transfer time, and pressure method;
- outdoor temperature, etchant lot, reuse count, volume, and etch time;
- drill model, written material/speed approvals, indicated speed, bit size,
  bit use count, vise, backer, and shroud;
- solder-fume extractor model, filter and nozzle/hose MPNs, filter condition,
  and source-capture check;
- hole measurements, chosen rivet hole, press depth-stop setting, and
  resistance before and after soldering; and
- macro photographs of transfer, etch, holes, and both rivet collars.

The coupon passes only if:

- there are no opens, copper whiskers, bridged spaces, lifted pads, or
  undercut traces under magnification;
- the printed scale error is acceptable for every footprint;
- front/back registration keeps every drill inside both annular rings;
- the chosen hole accepts the rivet without splitting or slop;
- the formed collars are concentric, seated, and free of board damage; and
- each soldered rivet is below 0.1 ohm after subtracting probe-lead resistance,
  and remains continuous during gentle board flexing.

Failing any item means adjust the process and make a new coupon.

## 3. Artwork and copper preparation

1. Generate top and bottom artwork at 1:1 scale with explicit mirror settings.
   Print the dimensioned coupon first and measure it; never assume printer
   scaling is exact.
2. Cut the pre-sized blank only if unavoidable. Prefer buying a blank already
   near final size because sawing or routing FR-4 creates much more dust than
   drilling.
3. Wet-clean the copper with water, a small amount of dish detergent, and a
   dedicated nonmetallic fine abrasive pad. Do not dry-sand. Capture the wash
   water and residue for HHW with the other process waste.
4. Rinse with captured clean water, dry with a lint-free wipe, and handle only
   by the edges. Do not use steel wool: fragments can rust or short traces.
5. Transfer the toner in a ventilated nonliving workspace using a dedicated
   dry heat tool and the transfer-medium instructions. Keep this electrical
   step completely separate from the etchant station.
6. Inspect under magnification. Repair only isolated pinholes with a known
   etch-resistant marker. Reject broad smears, wrinkles, missing fine features,
   or uncertain double-side registration.

Do not add acetone, lacquer thinner, photoresist chemistry, immersion tin, or
DIY solder mask to this workflow. They add hazards without solving the main
process-control limits. Remove toner later by wet mechanical rubbing.

## 4. Outdoor etching

1. Put the shallow PP/PPCO working tray inside the larger secondary tray. The
   secondary tray must hold more than the entire working volume.
2. Place only nonmetallic tools in the containment area. Keep all flames,
   sparks, heaters, switches that may arc, and soldering equipment away.
3. Put on the verified PPE. Open the original MG 415 bottle outdoors, upwind,
   and below face level.
4. Pour only enough room-temperature etchant to cover the copper when the board
   lies flat. Close the original bottle immediately.
5. Lower the board with polypropylene forceps. Slide or tilt the tray cover so
   it blocks direct splashes but retains a visible, unobstructed vent gap. Do
   not latch, gasket, tape, weight, or otherwise seal it.
6. Keep the tray level in secondary containment and continuously attended. Do
   not shake, rock, spray, bubble, pump, or heat the solution. If a stationary,
   room-temperature etch is too slow to preserve the artwork, stop and use a
   commercial fabricator instead of adding agitation or heat to this process.
7. Lift one edge of the loose cover while standing upwind to inspect. Keep face
   and body out of the opening. Replace the loose cover between checks.
8. As soon as unwanted copper is gone, use polypropylene forceps to lift the
   board. Drain it over the working tray without shaking.
9. Move it directly into a first captured-rinse tray, then a second captured
   rinse. A squeeze bottle may rinse the **board** over the waste tray; it is
   not an emergency eyewash.
10. Keeping all residue wet and over a captured-rinse tray, remove toner by
    gentle mechanical rubbing. Do not dry-sand or introduce a solvent. Capture
    the toner debris and rinse, then let the board dry completely before it
    approaches the drill station.
11. Leave the original stock bottle closed. After removing the board, make sure
    no metal remains in the working tray and no reaction or gas generation is
    continuing. Following MG and local HHW instructions, transfer spent etchant
    outdoors into a separate compatible, labeled container; do not return it to
    unused stock. Do not close a waste container while it is reacting or
    off-gassing, and never improvise a food or beverage container.

Do not assume a lack of visible fumes means a lack of exposure. MG 415 contains
hydrogen chloride, has pH below 2, causes serious eye damage, irritates skin and
airways, and is corrosive to metal.

## 5. Waste and cleanup

- Never pour fresh or spent etchant, copper-bearing rinse water, neutralized
  sludge, or cleanup water into a sink, toilet, street drain, soil, or trash.
- Do not neutralize waste as a disposal method. Neutralization can heat,
  splatter, and create a second handling step; the current SDS still directs
  hazardous-waste disposal.
- Capture all rinses, used wipes, failed boards, contaminated absorbent, toner
  debris, and spent etchant in compatible, closed, clearly labeled containers
  accepted by the local HHW program. Do not mix unrelated wastes.
- In San Mateo County, labeled corrosive household waste is illegal in trash or
  drains. Confirm an appointment and packaging with the HHW program at
  650-372-6200 or hhw@smcgov.org before the run.
- For a small spill, keep people away, wear PPE, prevent entry to drains, and
  use the confirmed neutralizing absorbent exactly as its instructions direct.
  Neutralization can heat the mixture, and the selected candidate releases
  carbon dioxide on acid contact. Work outdoors, keep the reaction vented, and
  let it finish and cool before collecting the residue as hazardous waste. Do
  not use it on bleach or hydrofluoric acid, or mix the residue with other
  waste. For a spill outside the staged secondary tray, an exposure, unknown
  reaction, or anything the prepared supplies cannot contain, leave the area
  and call emergency services/chemical emergency support.
- Store the original tightly closed bottle upright in compatible secondary
  containment, dry and away from bases, oxidizers, metals, heat, children, and
  pets. Retain the original label and SDS.

## 6. Drilling and FR-4 dust control

FR-4 machining releases glass-fiber/resin dust that can irritate eyes, skin,
nose, throat, and lungs. Dust control is an engineering-control problem, not
just a mask choice.

### Conditional drill setup

This setup becomes accepted only after the material and speed confirmations
above are filed with the run record. Without them, outsource drilling.

1. Work outdoors in dry weather, upwind of the vacuum exhaust and away from
   doors/windows. Outdoor work remains required even with HEPA capture.
2. Use grounded, intact cords and a GFCI-protected supply. Test the GFCI before
   use, keep plugs and connections dry and elevated, and use only outdoor-rated
   extensions. Check the drill and extractor nameplates and starting loads;
   never exceed a receptacle, GFCI, cord, or branch-circuit rating. Use separate
   suitable circuits if necessary rather than overloading a three-way outlet.
3. Bolt the WEN press to a stable bench and bolt or clamp the vise to the table.
   Square the table to the spindle. Support the PCB flat on a sacrificial
   backer and clamp the board/backer sandwich without bending it; a vise merely
   pinching the PCB edge is not adequate. Never hand-hold either piece.
4. With the press unplugged, install a new, undamaged solid-carbide PCB bit with
   a 3.175 mm shank, center it, tighten all three chuck-key positions, and
   remove the key. Check runout, bit clearance, backer support, vise security,
   and alignment before power-up.
5. Put a rigid shroud around the bit/board contact point and connect it to a
   sealed HEPA dust extractor with its specified fleece/fine-dust bag. Start
   extraction before drilling and leave it on through cleanup.
6. Wear impact-rated eye protection. Carbide bits are brittle and can shatter.
   Tie hair, remove jewelry and loose clothing, and keep hands clear. Do not
   wear gloves near the rotating spindle.
7. Set any approved spindle speed with the press unplugged and the belt cover
   closed afterward. Let the spindle reach full speed before feeding. Use only
   the written bit-maker feed guidance; never compensate for insufficient
   speed with force, side load, or hand wobbling. Stop at chatter, heat, smoke,
   excessive thrust, bit slip, or any board damage.
8. Do not blow dust with compressed air or sweep it dry. Vacuum the board,
   backer, shroud, vise, table, and bench, then damp-wipe them. Bag the wipe and
   spent backer.
9. Remove the vacuum bag outdoors following the extractor instructions. Seal
   it before bringing the extractor inside. Never use the dust extractor for
   etchant, rinse water, or any other liquid.

### Is a 3D-printed shop-vac holder enough?

It can be enough **as the hood-positioning part**, but not as the dust-control
system. Capture falls rapidly as a nozzle moves away from the source. The print
must:

- be rigidly fixed independently of the operator and unable to touch the bit,
  chuck, quill, vise, workpiece, or any point in the full press travel;
- surround as much of the drilling point as practical, with the opening only
  large enough for board movement and clear viewing;
- keep the pickup immediately adjacent to the bit without creating a pinch or
  snag hazard;
- fit the hose without a leak or a reducer so small that airflow collapses; and
- survive a full dry run at maximum spindle speed before a bit is installed.

An ordinary shop vacuum with a retrofit cartridge can leak fine dust around
the lid, hose, or filter and may re-emit it through the exhaust. A label on the
filter alone does not certify the whole vacuum. The preferred system is a
manufacturer-specified HEPA extractor, fleece bag, filter, hose, and adapter.

If the existing shop vacuum is used for a low-cost outdoor trial, install both
the manufacturer's finest dry-dust bag and compatible high-efficiency filter,
inspect every seal, direct exhaust away from people/buildings, use a well-fitted
N95 or P100 as secondary protection, and drill only a coupon. This is a
lower-confidence outdoor control, not approval for indoor use. Stop if a bright
sidelight shows a plume or contrasting paper around the fixture collects dust;
absence of visible dust is necessary but does not prove complete capture.

The BOM's P100 setup is particulate protection for drilling only. Do not treat
it as permission to etch indoors or as protection from ferric-chloride/hydrogen-
chloride vapor. Respirator selection does not replace the outdoor, vented etch
arrangement.

## 7. Forming and soldering rivets

1. Select 0.8 or 0.9 mm from the passing coupon; do not mix sizes in a run.
2. Deburr only with a gentle wet method or a purpose-made deburring tool under
   extraction. Do not enlarge a bad carbide-drilled hole by hand wobbling.
3. Insert the 0.6 mm-ID copper rivet with its factory head fully seated.
4. Install the matching Fortex 0.60 mm upper/lower tooling. Adjust the depth
   stop on scrap, then form the collar squarely. Excess force can crush FR-4 or
   split the pad; too little leaves a loose connection.
5. Inspect both collars under magnification. Reject cracks, tilt, pad lift,
   loose fit, or incomplete flare.
6. For durable electrical continuity, solder both collars with minimal dwell
   after forming, then clean only if residue interferes with inspection. Rivet
   manuals warn that soldering heat can loosen a marginal mechanical joint.
7. Measure continuity and gently flex-test as specified for the coupon. Record
   every failure; do not rework a damaged via into acceptance.

## 8. Assembly and final inspection

- Before assembly, record the exact manufacturer/model of the existing
  solder-fume extractor and every filter, hose, and nozzle. Check its current
  manual, correct filter installation, filter-change indication, hose/seal
  condition, and airflow. Do not proceed unless the manufacturer rates it for
  solder fume and a trial joint's plume is captured before it crosses the
  breathing zone.
- Put its source-capture nozzle close to and slightly behind the joint. Start
  extraction before heating and leave it on until visible fume clears. Follow
  the unit's filter indicator and current manual; do not bypass or wash filters
  unless the manufacturer explicitly instructs that maintenance.
- Use the selected SAC305 wire in a ventilated soldering area. The separate
  836LFNC-P pen is rosin/resin-free, but the selected 4900 solder wire contains
  REL0 resin flux. The complete process is therefore **not** rosin-free.
- Do not use supplemental liquid flux unless the coupon demonstrates that the
  resin-cored wire alone is inadequate. The 836LFNC-P pen is highly flammable
  and can cause eye irritation and drowsiness/dizziness. In a separate dry,
  ventilated location with the iron and every ignition source absent, apply the
  minimum amount, cap and remove the pen, and wait until its alcohol carrier is
  completely evaporated before moving to the soldering station or applying
  heat.
- Keep the existing solder-fume system dedicated to soldering. Unless its exact
  current manual explicitly permits another material, never use it for wet
  flux carrier, etchant, corrosive gas, drilling dust, or chemical-spill
  cleanup, and never use the drilling vacuum for solder fume.
- Lead-free does not mean fume-free. The current Canada/USA `4900-18G` SDS
  classifies the rosin-containing wire as a skin and respiratory sensitizer
  and warns that repeated exposure to rosin flux fumes can cause asthma.
  Capture fumes at the joint, avoid skin contact, and wash hands after
  handling boards and solder. Stop exposure and obtain medical advice for a
  rash, wheezing, breathing difficulty, or asthma-like symptoms.
- Bare copper oxidizes. Assemble promptly and store finished boards dry; do not
  add immersion-tin chemistry to this workflow.
- Inspect every trace/space, pad, antipad, hole, and rivet under magnification.
  Check for shorts to the bottom plane before fitting components.
- Power only through a current-limited bench supply and the finished board's
  separately reviewed bring-up plan. This fabrication document does not define
  an electrical release.

## Emergency first aid summary

Follow the current product SDS and emergency personnel, not this summary.

- **Eyes:** begin water irrigation immediately and continue for at least 30
  minutes. Remove contacts if easy while rinsing. Call Poison Control/doctor
  immediately; do not delay rinsing to make the call.
- **Skin:** remove contaminated clothing and rinse with plenty of water. Obtain
  medical advice for irritation or burns.
- **Inhalation:** move to fresh air and call Poison Control/doctor if unwell.
- **Swallowing:** rinse mouth, do not induce vomiting, and call Poison Control.
- **Fire or suspected gas buildup:** do not operate switches or approach with
  an ignition source. Leave the area and call 911.

## Primary safety and process sources

- [MG Chemicals 415 ferric chloride product page](https://mgchemicals.com/products/circuit-board-design/copper-etchants/ferric-chloride-etching/)
- [MG Chemicals 415 US/Canada SDS, issue 2026-01-26](https://www.mgchemicals.com/downloads/msds/01%20English%20Can-USA%20SDS/sds-415-l.pdf)
- [MG Chemicals 836LFNC-P product page](https://mgchemicals.com/products/soldering-supplies/flux-pens/lead-free-flux-pen/)
- [MG Chemicals 836LFNC-P Canada/USA SDS](https://www.mgchemicals.com/downloads/msds/01%20English%20Can-USA%20SDS/sds-836lfnc-p.pdf)
- [MG Chemicals 4900 solder-wire product page](https://mgchemicals.com/products/soldering-supplies/solder-wire/lead-free-solder/)
- [MG Chemicals 4900-18G Canada/USA SDS](https://www.mgchemicals.com/downloads/msds/01%20English%20Can-USA%20SDS/sds-4900-18g.pdf)
- [Fortex PTH400 system and rivet dimensions](https://www.fortex.co.uk/product/favorit-through-hole-mechanical-plating/)
- [MIPEC 0.8 mm PCB drill parameters](https://www.mipec.eu/pcb-drill-0-8-mm/)
- [MIPEC 0.9 mm PCB drill parameters](https://www.mipec.eu/pcb-drill-0-9-mm/)
- [WEN 4208T product page and linked manual](https://wenproducts.com/products/wen-4208t-2-3-amp-8-inch-5-speed-benchtop-drill-press)
- [NIOSH fibrous-glass-dust guidance](https://www.cdc.gov/niosh/npg/npgd0288.html)
- [NIOSH local-exhaust hood proximity guidance](https://www.cdc.gov/niosh/engcontrols/ecd/detail39.html)
- [OSHA immediate flushing requirement for corrosives](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.151)
- [San Mateo County household hazardous waste](https://www.smchealth.org/hhw)
