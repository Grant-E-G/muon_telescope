# Home PCB fabrication BOM

This is a standalone BOM for the workflow in this folder. It is not part of the
telescope electronics BOM. Links and indicative prices were checked
2026-08-25; verify stock, shipping, size, and current SDS before ordering.

The list assumes the following are already owned: a compatible laser printer,
a workshop iron or laminator, the WEN `4208T` and vise, a shop vac, ordinary
hand tools, magnification, and a multimeter.

## Minimal etch setup

| Function | Selected item/source | Qty. | Indicative cost | Notes |
|---|---|---:|---:|---|
| Copper clad | MG Chemicals `540`, double-sided 1 oz copper, nominal 1.6 mm FR-4, 3 x 5 in: [manufacturer](https://mgchemicals.com/products/circuit-board-design/copper-clad-board/), [DigiKey](https://www.digikey.com/en/products/detail/mg-chemicals/540/2177370) | 1-2 | $15.75 each | Buy pre-sized blanks to avoid cutting FR-4. One can be divided only if an existing dust-controlled cutting method is available. |
| Toner transfer | Techniks Press-n-Peel Blue `TEK-5`, five sheets: [source](https://aretronics.com/products/techniks-press-peel-pc-board-kit) | 1 | $11.95 | Enough to qualify the printer and make several small boards. |
| Etchant | MG Chemicals `415-1L` ready-to-use ferric chloride: [manufacturer](https://mgchemicals.com/products/circuit-board-design/copper-etchants/ferric-chloride-etching/), [DigiKey](https://www.digikey.com/en/products/detail/mg-chemicals/415-1L/9657988) | 1 | $23.75 | Use no more than 100 mL per run at room temperature. Keep the original bottle and label. |
| Working container | Cambro `2SFSPP190`, 2 qt polypropylene container: [source](https://www.restaurantsupply.com/cambro-2sfspp190-camsquare-2-qt-translucent-food-container), plus `SFC2SCPP190` polyethylene lid: [source](https://www.officedepot.com/a/products/3041570/Cambro-CamSquare-Lid-4-Qt-12H/) | 1 each | $4.65 + $5.79 | The 7.25 in square base fits a 3 x 5 in board. Rest the lid loosely with a visible vent gap; never snap it closed during an etch. Mark both pieces chemical-use-only. |
| Secondary containment | Existing or local #2 HDPE/#5 PP storage tub, at least 2 L and large enough for the working container | 1 | $0-15 | Inspect for cracks and dry-fit it. It is containment, not an airtight chamber. |
| Handling, rinse, and waste | Plastic tongs; two reused/labeled #2 HDPE or #5 PP rinse containers; compatible screw-cap waste bottle; labels; wipes; small bag of inert absorbent | 1 small set | about $10-20 | Household products are adequate if clean, compatible, dedicated to chemicals, and not food/drink containers. Confirm the waste bottle with the local HHW program. |

## Minimum personal protection

| Function | Selected item/source | Qty. | Indicative cost | Notes |
|---|---|---:|---:|---|
| Splash goggles | Pyramex `G205`, ANSI Z87+ and D3: [manufacturer](https://www.pyramex.com/products/chemical-splash-goggle-d3), [single-unit source](https://hdsupplysolutions.com/p/pyramex-chemical-splash-goggles-clear-body-clear-lens-p414897) | 1 | $2.33 | Use for chemical splashes; fit-check before the run. No separate face shield is required for this 100 mL setup. |
| Chemical gloves | SHOWA `730-[size]`, 13 in, 15 mil reusable nitrile: [manufacturer](https://www.showagroup.com/us-en/shop/730/), [size 9 example](https://www.grainger.com/product/SHOWA-Chemical-Resistant-Gloves-4JF19) | 1-2 correctly sized pairs | $3.51/pair; some sellers require 12 | For brief splash handling, not deliberate immersion. Rinse the exterior after a splash and replace damaged or degraded gloves. Do not wear them at the drill press. |
| Immediate eye flush | Honeywell Eyesaline 32 oz `32-000455-0000` (retail suffix `-H5`): [manufacturer](https://ppe.honeywell.com/us/en/shop/first-aid/eyesaline-personal-eyewash-bottles/personal-sterile-saline-eyewash-bottles-12-pack), [single-unit source](https://www.webstaurantstore.com/honeywell-eyesaline-32-oz-personal-eyewash-bottle-32-000455-0000-h5/86932000455.html) | 1 | $15.49 | First flush only. Its manufacturer says it supplements rather than replaces primary irrigation; continue immediately at the tested household sink/shower for the SDS's 30 minutes. Replace at expiration or after opening. |

Long sleeves, long pants, closed shoes, and an immediately accessible household
sink or shower are existing provisions, not BOM purchases. The earlier plumbed
eyewash, face shield, apron, specialty spill kit, and second-adult requirement
have been removed.

## Drilling with owned equipment

| Function | Selected item/source | Qty. | Indicative cost | Notes |
|---|---|---:|---:|---|
| Drill press | Existing WEN `4208T`: [manufacturer](https://wenproducts.com/products/wen-4208t-2-3-amp-8-inch-5-speed-benchtop-drill-press), [user listing](https://www.amazon.com/dp/B08ZVT5JKC), [local manual](../datasheets/home-pcb-fabrication/wen-4208t-manual.pdf) | 1 existing | $0 | Use the vise, full backer support, highest speed, and light feed. Qualify hole and rivet quality on a coupon. |
| Overdrill bits | MIPEC 1.0 mm solid-carbide PCB drill, 3.175 mm shank: [manufacturer/source](https://www.mipec.eu/pcb-drill-1-0-mm/) | 2 | check current EUR price | Nominally gives 0.1 mm clearance around the cheap rivet's listed 0.9 mm shank. Buy a spare because carbide is brittle; confirm the actual finished hole and fit on the coupon. |
| Dust capture | 3D-printed close-capture hood/holder and hose adapter | 1 | about $5 filament/hardware | Rigidly mount beside the drill point and dry-run full quill travel. A printed holder is adequate for this small outdoor workflow when paired with the bag/filter below. |
| Vacuum filtration | Existing shop vac plus its manufacturer's compatible dry collection bag and best high-efficiency/HEPA cartridge | 1 existing set | $0 if already fitted; model-dependent otherwise | Do not order generic parts until the exact shop-vac model is known. Direct exhaust outdoors away from people and inspect all seals. No new $600 extractor or P100 kit is included. |

## Budget rivet system

This deliberately substitutes a hobby setting method for a purpose-built rivet
press. The Amazon rivet listing has no manufacturer drawing and has appeared under
different generic brands, so buy by the exact dimensions and inspect the
delivered lot. The center punch is a forming tool here, not a precision die.

| Function | Exact item/source | Qty. | Indicative cost | Notes |
|---|---|---:|---:|---|
| Hollow PCB rivets | Generic `M0.9(d) x 2.5(L) mm` hollow PCB via rivets, Amazon ASIN `B015CV377O`: [Amazon](https://www.amazon.com/dp/B015CV377O) | 1 pack, listing says 1000 | about $7.99; verify | Nominal 0.9 mm shank OD and 2.5 mm length. Material and head-diameter claims vary across copies of the listing; measure the received lot before freezing pads or holes. |
| Forming punch | ADI adjustable automatic center punch, Amazon ASIN `B08LG98JK9`: [Amazon](https://www.amazon.com/dp/B08LG98JK9) | 1 | about $9; verify | Use minimum force and one centered stroke at a time. Its pointed tip produces a rough flare, not the controlled roll of a matched die. |
| Backing surface | Existing clean, flat steel bench block or solid steel plate | 1 existing | $0 | Must support the factory flange and surrounding board without rocking. Do not set a rivet across open vise jaws. |

## Budget summary

The previously priced purchases are about **$100-145** for one or two blanks,
depending on whether a containment tub and compatible shop-vac consumables are
already present. The complete budget rivet system adds about **$17**, making
roughly **$120-175 plus drill bits and shipping** a practical starting range.
