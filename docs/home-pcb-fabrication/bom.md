# Home PCB fabrication BOM

This is a standalone process BOM. It is not part of the telescope electronics
BOM. Links and indicative prices were checked 2026-08-25; verify stock, price,
shipping, voltage, SDS revision, and exact option before ordering.

Quantities cover one workstation and several small prototypes. “Required”
means the process may not run without that function. Existing equipment is
acceptable only when it meets the stated specification.

## Safety blockers to resolve before ordering chemistry

| Requirement | Selected item/source | Qty. | Indicative cost | Decision note |
|---|---|---:|---:|---|
| Continuous hands-free eyewash | Speakman `SE-582` plumbed, stay-open, ANSI/ISEA Z358.1 eyewash: [manufacturer](https://speakman.com/product/traditional-series-se-582-wall-mounted-eyewash-with-stainless-steel-bowl/), [DigiKey](https://www.digikey.com/en/products/detail/industrialsupplies-com/SE-582/14075833) | 1 | $478.83 plus plumbing | Required unless an existing installed unit can immediately deliver suitable water continuously for the MG SDS's 30-minute rinse. A 9-gallon/15-minute bottle station alone is insufficient for this chemical. Install and test before buying etchant. Also stage an immediately accessible body-drench shower/hose that does not require passing a locked door. |
| Chemical glove | Ansell AlphaTec `02-100`, correct hand size: [manufacturer](https://www.ansell.com/us/en/products/alphatec-02-100), [single-pair source](https://www.thesafetysupplycompany.co.uk/p/9056306/ansell-alphatec-02-100-polyethylene-nylon-white-gauntlet-gloves-pair-an-02-100) | 2 pairs | about $19/pair plus shipping | Provisional selection with broad Type A barrier performance. **Do not rely on it until Ansell confirms use time for exact MG 415 (37–42% FeCl3 plus 1% HCl).** MG's SDS says glove material and breakthrough must be checked with the glove manufacturer. Replace after contamination/damage. |
| Chemical splash goggles | 3M GoggleGear 500 `GG501SGAF`, ANSI D3/D4, indirect vent: [manufacturer](https://www.3m.com/3M/en_US/p/dc/v000244796/), [Grainger](https://www.grainger.com/product/3M-Safety-Goggles-Clear-Lens-48TK90) | 1 | $31.51 | Required; ordinary safety glasses are not the selected splash control. Confirm facial seal and compatibility with prescription eyewear. |
| Secondary face protection | 3M `82783` H8A headgear with WP96 clear shield: [manufacturer](https://www.3m.com/3M/en_US/p/d/v000153070/), [Grainger](https://www.grainger.com/product/3M-Face-Shield-Clear-2ELZ3) | 1 | $53.65 | Required for pouring, board removal, and waste transfer; wear over goggles. |
| Chemical apron | Ansell AlphaTec `56-100`, 33 x 44 in, 18 mil PVC: [manufacturer](https://www.ansell.com/us/en/products/alphatec-56-100), [Grainger](https://www.grainger.com/product/ALPHATEC-Bib-Apron-Vinyl-9UCE3) | 1 | $15.82 | Required with long sleeves, long pants, and closed chemical-resistant footwear. Apron is partial-body protection, not a suit. |
| Spill plan and legal disposal | [San Mateo County HHW](https://www.smchealth.org/hhw), 650-372-6200, hhw@smcgov.org | 1 confirmed appointment/path | Free for county residents | Confirm accepted containers and quantities before generating waste. The label says Danger, so it is illegal in trash or drains locally. |

The glove and eyewash rows are purchase gates, not optional upgrades. If their
requirements cannot be met, use a commercial PCB service.

## Imaging and etching

| Function | Exact item/source | Qty. | Indicative cost | Notes |
|---|---|---:|---:|---|
| Copper clad | MG Chemicals `540`, double-sided, 1 oz copper, nominal 1.6 mm FR-4, 3 x 5 in: [manufacturer family](https://mgchemicals.com/products/circuit-board-design/copper-clad-board/), [DigiKey](https://www.digikey.com/en/products/detail/mg-chemicals/540/2177370) | 3–5 | $15.75 each | Avoid home panel cutting where possible. Confirm actual thickness against the 2.2 mm rivet length on coupon. |
| Toner transfer | Techniks Press-n-Peel Blue `TEK-5`, five sheets: [US source](https://aretronics.com/products/techniks-press-peel-pc-board-kit), [Fortex](https://www.fortex.co.uk/product/press-n-peel-pcb-transfer/) | 1 | $11.95 | Use a known compatible laser printer/toner and prove scale/transfer on coupon. |
| Dedicated dry heat tool | Cricut EasyPress Mini, three-setting model: [manufacturer](https://cricut.com/en-us/cricut-heat-presses/cricut-easypress-mini/easypress-mini.html) | 1 | $49.99 | Dedicated to fabrication, never food/clothing. Settings are not a PCB specification; calibrate transfer on coupon and keep moving as its instructions require. |
| Ferric chloride | MG Chemicals `415-1L`, ready-to-use liquid: [manufacturer](https://mgchemicals.com/products/circuit-board-design/copper-etchants/ferric-chloride-etching/), [DigiKey](https://www.digikey.com/en/products/detail/mg-chemicals/415-1L/9657988) | 1 | $23.75 | Required chemistry. Use at room temperature outdoors in a vented tray. Never seal reacting metal and etchant together. Retain original packaging, label, and SDS. |
| Covered working tray | Thermo Scientific Nalgene `6910-0618` PP tray with cover, 18 x 6 x 2.6 in: [manufacturer](https://www.thermofisher.com/order/catalog/product/jp/en/6910-0618PK) | 1 | check quote | Use the cover loose only as a splash shield; do not seal or latch. Verify the board fits flat before pouring. |
| Secondary containment | Dynalon `107334` welded PP spill tray, 22 x 26 x 4 in internal dimensions (37.49 L): [manufacturer](https://www.dynalon.com/PublicStore/product/Rectangular-Tray-PP-and-HDPE%2C325.aspx?sku=709), [Grainger](https://www.grainger.com/product/Lab-Tray-Rectangular-9EKP2) | 1 | $206.01 | Provides at least 2 in nominal clearance around the 18 x 6 in working tray and holds far more than the working volume. Physically dry-fit the exact trays before ordering etchant, verify material compatibility, and inspect all welds/surfaces before every use. |
| Board handling | Thermo Scientific Nalgene `6320-0010` PP scissor forceps: [manufacturer insert](https://documents.thermofisher.com/TFS-Assets%2FLCD%2Fmanuals%2FNalgene-Forceps-EN-8-0400-14-1210.pdf), [Fisher](https://www.fishersci.com/shop/products/nalgene-polypropylene-scissor-type-forceps/10309) | 1 | sold mainly in packs; check quote | Dedicated nonmetallic tool. Test grip on a wet scrap board before etching. |
| Captured rinses | Two additional PP/HDPE trays plus compatible, HHW-approved screw containers and hazard labels | 2 trays; 2 containers | local source | Source only after the local HHW program confirms material, closure, label, and volume. Never use food/drink containers. |
| Cleaning | Mild dish detergent, dedicated fine nonmetallic abrasive pad, lint-free wipes, distilled water | 1 set | $15–25 | Wet methods only. Capture all liquid and solids. Do not use steel wool or dry sanding. |
| Small-spill supplies | CHEMSORB Acid Neutralizing Absorbent `SP60AN-LB2`, 2 lb bag: [manufacturer/direct source](https://chemsorb.com/products/chemsorb-acid-neutralizing-absorbent), plus dedicated nonmetallic scoop and HHW-approved container | 1 bag and cleanup set | $15.85 plus scoop/container | Provisional candidate: **do not rely on it until CHEMSORB confirms compatibility with the exact MG 415 mixture.** Its SDS requires compatibility testing and says acid contact generates carbon dioxide; use only outdoors, never seal active residue, and never use with bleach or hydrofluoric acid. Secondary containment is the primary control. This is for a small accidental spill, not waste neutralization. |

## Drilling and dust capture

| Function | Exact item/source | Qty. | Indicative cost | Notes |
|---|---|---:|---:|---|
| Existing drill press | WEN `4208T` 2.3 A, five-speed drill press: [manufacturer](https://wenproducts.com/products/wen-4208t-2-3-amp-8-inch-5-speed-benchtop-drill-press), [user's purchase listing](https://www.amazon.com/dp/B08ZVT5JKC), [local manual](../datasheets/home-pcb-fabrication/wen-4208t-manual.pdf) | 1 existing | $0 incremental | **Not accepted for FR-4 yet.** It is rigid and its 1.5–13 mm chuck accepts a 3.175 mm shank, but it tops out at 3,140 RPM versus the bits' 53,000–60,000 RPM recommendations. Its manual limits intended drilling to wood/metal and warns about other materials. Obtain written WEN approval for FR-4 and written bit-maker speed/feed guidance at no more than 3,140 RPM, then qualify on a coupon; otherwise outsource drilling or revise the workflow for a PCB-rated drill. |
| Existing workholding | User-owned drill-press vise plus a flat sacrificial backer and low-profile clamps | 1 set | $0–30 incremental | Record the vise MPN. Bolt/clamp the vise to the table, support the entire PCB on the backer, and secure the sandwich without bowing it. Never grip only the thin PCB edge or hand-hold the work. Dry-run full quill/shroud clearance. |
| 0.8 mm test drill | MIPEC solid-carbide PCB drill 0.8 mm, 3.175 mm shank: [manufacturer/source](https://www.mipec.eu/pcb-drill-0-8-mm/) | 3 | check EUR price | Manufacturer starting point is 60,000 RPM. Use only in the written-approved rigid setup; brittle sharp tool. |
| 0.9 mm test drill | MIPEC solid-carbide PCB drill 0.9 mm, 3.175 mm shank: [manufacturer/source](https://www.mipec.eu/pcb-drill-0-9-mm/) | 3 | check EUR price | Manufacturer starting point is 53,000 RPM. Select final diameter only from rivet coupon. |
| Preferred dust extractor | Dustless Tools `D1606` 16-gallon H13 HEPA Wet+Dry Dustless Vac: [manufacturer/direct source](https://dustlesstools.com/product/16-gal-hepa-wetdry-dustlessvac-with/) | 1 | $594.99 | Manufacturer states the complete unit is individually certified and filters 99.97% at 0.3 micrometres. Use only for dry FR-4 dust in this workflow; never collect etchant or rinse liquid. Continue to drill outdoors. |
| Replacement dust bags | Dustless Tools `D1351` 12–18 gallon HEPA Wunderbags, linked from the [D1606 product page](https://dustlesstools.com/product/16-gal-hepa-wetdry-dustlessvac-with/) | 1 pack | check price | Manufacturer-recommended bag. Change and seal outdoors per instructions; do not run without the specified bag/filter. |
| Source-capture shroud | Custom 3D-printed close-fitting drill shroud plus hose adapter, mechanically fixed to press/table/bench | 1 | $5–20 filament/hardware | A holder is acceptable only as the hood. It must clear the bit, chuck, quill, vise, board, and full press travel; nearly enclose the source; stay immediately adjacent; and pass the coupon dust check. It does not turn a generic shop vacuum into a HEPA system. |
| Outdoor electrical protection | Existing correctly rated GFCI-protected circuit, or Southwire `14880004-6` 6 ft, 120 V/15 A, 12/3 SJTW GFCI tri-cord if suitable: [manufacturer](https://www.southwire.com/power-management/extension-cords/6-ft-120v-15a-yel-12-3-cable-gfci-tri-cord/p/14880004-6), [retailer](https://www.zoro.com/southwire-gfci-6ft-right-angle-tricord-tap-14880004-6/i/G215388396/) | 1 | existing or check price | Test before each use; keep connections dry/elevated. Sum drill/extractor running and starting loads and obey all nameplate, cord, GFCI, receptacle, and circuit limits. Three outlets do not create extra circuit capacity; use separate suitable circuits if required. |
| Secondary respiratory protection | 3M `62093` medium P100 kit (retail model `62093HA1-C`), including a `6200` facepiece and pair of `7093` filters: [manufacturer](https://www.3m.com/3M/en_US/p/d/b10013085/), [Home Depot](https://www.homedepot.com/p/202080148) | 1 kit | $36.97 | For drilling particulates only, secondary to capture and outdoor work. Buy this medium-size kit only if it fits; otherwise obtain a NIOSH-approved small/large P100 assembly selected and fitted to the user. No facial hair may cross the seal. Perform the instructions' seal check every time. This particulate setup does not protect against etchant vapor and does not correct poor capture. |
| Hearing protection | Properly fitted plugs or muffs | 1 | $10–30 | Use according to measured/expected tool and extractor noise. |

### Existing shop-vac substitution rule

The D1606 extractor may be omitted only for an outdoor coupon trial if the
existing vacuum has its manufacturer's finest compatible dry-dust bag and
high-efficiency cartridge installed together, all seals are sound, the exhaust
is directed away from people/buildings, and the printed shroud passes the dust
check. Record the vacuum, bag, filter, hose, and adapter MPNs. Do not describe
that assembly as a certified HEPA system unless the complete vacuum has that
manufacturer certification. It is not accepted for indoor/shared-air drilling.

## Rivet system

Fortex does not publish separate manufacturer part numbers for the selectable
options on this product page; order by the exact option names below rather
than inventing an MPN.

| Function | Exact Fortex ordering option | Qty. | Indicative cost | Notes |
|---|---|---:|---:|---|
| Rivet press | `Favorit Press` on the [PTH400 product page](https://www.fortex.co.uk/product/favorit-through-hole-mechanical-plating/) | 1 | within page range £12–£299; verify selected-option price | 200 mm throat, adjustable depth limiter. |
| Rivet tooling | `Tool Set 0.60mm` on the same [PTH400 page](https://www.fortex.co.uk/product/favorit-through-hole-mechanical-plating/) | 1 | verify option | Must match the selected 0.6 mm-ID rivet. |
| Copper rivets | `1000 x Rivets 0.60mm` on the same [PTH400 page](https://www.fortex.co.uk/product/favorit-through-hole-mechanical-plating/) | 1 bag | verify option | Published geometry: 0.6 mm ID, 0.8 mm OD, 2.2 mm length, 1.3 mm head, 0.1 mm wall. A nominal 1.6 mm board leaves only 0.6 mm of rivet length for forming; verify actual board thickness and flare on coupon. |

Both 0.8 and 0.9 mm drills are deliberately included. Fortex publishes 0.8 mm
as the required hole for this rivet and a separate note to add 0.1 mm for CNC
drilling. A home setup has uncharacterized runout, so the coupon—not a guessed
rule—selects the final bit.

## Assembly consumables

| Function | Exact item/source | Qty. | Indicative cost | Notes |
|---|---|---:|---:|---|
| Existing solder-fume extraction | User-owned complete source-capture setup; record its exact manufacturer/model and filter, hose, and nozzle MPNs before use | 1 existing | $0 incremental | No extractor purchase added. Verify the current manual rates it for solder fume, all specified filters are fitted and serviceable, airflow is normal, and a trial plume is captured before crossing the breathing zone. Buy only its manufacturer-specified replacement filters. Keep it separate from etchant, wet flux carrier, FR-4 dust, and spill cleanup unless its manual explicitly permits that material. |
| Temperature-controlled soldering station | Hakko `FX888DX-010BY`, 120 V, 100 W, supplied with `FX-8801-02` iron and `T18-D16` tip: [manufacturer](https://hakkousa.com/products/soldering/fx-888dx.html), [DigiKey](https://www.digikey.com/en/products/detail/american-hakko-products-inc/FX888DX-010BY/24390014) | 1 | $133.81 | Required unless an existing grounded, temperature-controlled station is equivalent. Use the lowest setting that makes a prompt sound joint; excessive dwell can loosen a rivet or lift a pad. Return the iron to its stand whenever it leaves the joint. |
| Solder wire | MG Chemicals `4900-18G`, SAC305, 0.81 mm, REL0 resin-flux core: [manufacturer](https://mgchemicals.com/products/soldering-supplies/solder-wire/lead-free-solder/), [DigiKey](https://www.digikey.com/en/products/detail/mg-chemicals/4900-18G/14563346) | 1 pocket pack | $23.79 | Solder both rivet collars with minimal dwell. Resin flux fumes require capture. |
| Optional supplemental flux | MG Chemicals `836LFNC-P`, ORL0 no-clean flux pen: [manufacturer](https://mgchemicals.com/products/soldering-supplies/flux-pens/lead-free-flux-pen/), [DigiKey](https://www.digikey.com/en/products/detail/mg-chemicals/836lfnc-p/22481709) | 0 or 1 | $18.48 | Do not buy/use unless the coupon proves it is needed. Highly flammable alcohol mixture: apply minimally in a separate dry area with every ignition source and the existing extractor off/absent; cap and remove the pen and wait for complete evaporation before soldering. Pen is resin-free; solder wire is not. |
| Inspection | 10x illuminated loupe or microscope; multimeter with relative/lead-zero function | 1 each | existing or $50–200 | Required to inspect holes/rivets and measure coupon continuity. Record exact existing equipment models in the run log. |

## Cost decision

Starting from no safety or fabrication equipment, the required eyewash,
preferred dust extractor, suitable drill, rivet press, PPE, and consumables make
this a four-figure setup before plumbing and shipping. This workflow is most
rational when the equipment already exists, the learning objective itself is
valuable, or many boards will be prototyped. For a few boards, commercial PCB
fabrication is safer, more repeatable, and usually less expensive.
