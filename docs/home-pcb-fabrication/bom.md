# Cost-optimized home PCB fabrication BOM

This is a standalone BOM for the workflow in this folder, not part of the
telescope electronics BOM. Prices and links were checked 2026-08-25. Amazon
prices are volatile, so the table gives a **buy ceiling**: skip that listing if
it costs more and select the same dimensions/material from another seller.

The objective is a useful stock of consumables, not one board at industrial
lab prices. Generic items require incoming inspection and a process coupon.
Compare **delivered** cost, not the item price. The target assumes one combined
Amazon order and local pickup at Anchor Electronics, IKEA, and Harbor Freight.
Do not pay parcel shipping for a $2 container, tong, bottle, or punch; substitute
the same material and dimensions locally when shipping erases the saving.

## Already owned: buy nothing

| Function | Existing item | Added cost | Use |
|---|---|---:|---|
| Printer | Brother `HL-L2370DW`: [specifications](https://support.brother.com/g/b/spec.aspx?c=us_ot&lang=en&prod=hll2370dw_us), [local guide](../datasheets/home-pcb-fabrication/brother-hl-l2370dw-online-user-guide.pdf) | $0 | Use the installed toner and the manual feed/rear face-up path. The coupon qualifies the toner and transfer paper together. |
| Transfer heat | Existing workshop iron or laminator | $0 | No new press or laminator. |
| Drill | WEN `4208T` and vise: [manufacturer](https://wenproducts.com/products/wen-4208t-2-3-amp-8-inch-5-speed-benchtop-drill-press), [local manual](../datasheets/home-pcb-fabrication/wen-4208t-manual.pdf) | $0 | Highest speed, full backer support, light feed, and a coupon first. |
| Dust collection | Existing shop vac, serviceable dry cartridge/filter, and collection bag if already available | $0 | Use outdoors with a close-capture hood and direct exhaust away from people. Do not buy a new extractor. |
| Assembly and inspection | Existing assembly equipment, multimeter, magnification, ordinary hand tools, and a flat steel block/plate | $0 | No assembly or soldering supplies are part of this BOM. |

## Consumables and containers

| Function | Cost-optimized selection | Qty. | Target / buy ceiling | Notes |
|---|---|---:|---:|---|
| Copper clad | GeeBat `GB0021`, Amazon ASIN `B01MRG7NHC`, ten nominal 70 x 100 x 1.5 mm double-sided FR-4 blanks: [Amazon](https://www.amazon.com/dp/B01MRG7NHC) | 1 pack | target $14, **do not exceed $18** | Much lower unit cost than individual branded blanks. Copper weight is not documented; inspect flatness, thickness, copper adhesion, and etch time on the coupon. Maximum board size becomes 70 x 100 mm. If a larger board is actually needed, buy one MG Chemicals `540` 3 x 5 in blank instead of both options. |
| Toner-transfer paper | Ximimark `XQJ=LY251-XQJ-FBA`, 20 A4 PCB-transfer sheets, Amazon ASIN `B07MYXK4WJ`: [Amazon](https://www.amazon.com/dp/B07MYXK4WJ) | 1 pack | target $9, **do not exceed $12** | This replaces the branded five-sheet pack. Later Brother printer/toner combinations are variable, so do not buy a second pack until the artwork coupon transfers cleanly. |
| Etchant | MG Chemicals `415-1L` ready-to-use ferric chloride: [manufacturer](https://mgchemicals.com/products/circuit-board-design/copper-etchants/ferric-chloride-etching/), [Anchor Electronics](https://anchor-electronics.com/product/mgchemicals-415-ferric-chloride/) | 1 | $18.01 listed; **do not exceed $20 before tax** | Local pickup avoids hazardous-material shipping. Use at most 100 mL in the working box and reuse it while it still etches acceptably; keep fresh and used material separately labeled. |
| Working box | IKEA SAMLA `701.029.72`, 1-gallon polypropylene box: [IKEA](https://www.ikea.com/us/en/p/samla-box-clear-70102972/), with PP lid `504.550.88`: [IKEA](https://www.ikea.com/us/en/p/samla-lid-for-box-1-gallon-clear-50455088/) | 1 each | $3.99 + $1.00 | Fits these blanks. Rest the lid loosely with a visible vent gap during an etch; never latch it closed. The HCl model conservatively uses its full 11 x 7.5 in top footprint. Mark both pieces chemical-use-only. IKEA currently imposes an online minimum of two, so buy one in store or substitute a local #5 PP box rather than paying for extras. |
| Secondary containment | IKEA SAMLA `401.029.78`, 3-gallon polypropylene box: [IKEA](https://www.ikea.com/us/en/p/samla-box-clear-40102978/) | 1 | $2.99 | No lid is required. It replaces the specialty Dynalon tray and must remain large enough to hold all liquid staged for the run. |
| Board handling | Local all-plastic serving tongs; [low-cost example](https://www.walmart.com/c/kp/plastic-serving-utensils) | 1 | $1-2 | Inspect for exposed metal, cracks, or a hollow section that can trap etchant. Dedicate it to chemical work. |
| Rinse containers | Two clean, reused #2 HDPE or #5 PP household containers with identifying labels | 2 | $0 | Permanently mark them chemical-use-only. Do not use glass or metal. |
| Waste bottle | 32 oz HDPE bottle with PP screw cap, U.S. Plastic item `97365`: [source](https://www.usplastic.com/catalog/item.aspx?itemid=165118), or a local equivalent | 1 | $1.89 before shipping; **buy locally if shipping dominates** | Confirm the container and size with the local HHW program. Deface it and label actual contents and date. A larger compatible bottle is needed if captured rinse volume will exceed 32 oz. |

## Minimum personal protection

| Function | Selected item/source | Qty. | Target cost | Notes |
|---|---|---:|---:|---|
| Splash goggles | Pyramex `G205`, ANSI Z87+ and D3: [manufacturer](https://www.pyramex.com/products/chemical-splash-goggle-d3), [single-unit source](https://hdsupplysolutions.com/p/pyramex-chemical-splash-goggles-clear-body-clear-lens-p414897) | 1 | $2.33 before shipping | If shipping exceeds the item price, buy an equivalent locally: indirect-vent chemical-splash goggles marked D3, not ordinary safety glasses. |
| Chemical gloves | SHOWA `730-[size]`, 13 in, 15 mil reusable nitrile: [manufacturer](https://www.showagroup.com/us-en/shop/730/), [size 9 example](https://www.grainger.com/product/SHOWA-Chemical-Resistant-Gloves-4JF19) | 1 correctly sized pair | $3.51; **do not buy a case** | Brief splash handling only. Rinse the exterior after a splash and replace damaged gloves. Never wear them at the drill press. |
| Immediate eye flush | First Aid Only `24-202-001`, single 32 oz eye-flush station: [product sheet](../datasheets/home-pcb-fabrication/first-aid-only-eyewash-product-sheet.pdf), [clearance source](https://blackboxsafety.com/products/first-aid-only-eyewash-station-24-202-001) | 1 | target $5.40, **do not exceed $15** | The linked price is limited inventory. If it is gone, buy one fresh, sealed 32 oz personal eye-flush bottle locally rather than an elaborate station. This is immediate first flush only; continue at the already-tested household sink/shower for the etchant SDS's 30 minutes. Check the expiration before accepting it and replace after opening. |

Long sleeves, long pants, closed shoes, an unobstructed route to a household
sink/shower, ordinary wipes, and labels are existing household provisions.

## Drilling and dust capture

| Function | Cost-optimized selection | Qty. | Target / buy ceiling | Notes |
|---|---|---:|---:|---|
| 1.0 mm overdrill bits | Harfington `f25070700ux0179`, ten 1.0 mm solid-carbide twist drills, 3.175 mm shank, 10 mm flute, 38 mm overall: [Harfington](https://www.harfington.com/products/p-1889293) | 1 pack | $6.54; **do not exceed $8 before shipping** | These are actual spiral-flute PCB drills, not pointed engraving burrs. The nominal 0.1 mm diametral clearance over a 0.9 mm rivet is deliberate. Reject chipped or bent bits and qualify the measured hole and delivered rivet together on the coupon. |
| Close-capture hood | 3D-printed shop-vac nozzle/holder using existing filament and common hardware | 1 | about $1 incremental material | Rigidly mount it beside the bit and dry-run full quill travel. The print is a hood, not a filter. |
| Vacuum consumables | Existing compatible dry collection bag and serviceable cartridge/filter | 1 set | $0 if already fitted | For a few holes outdoors, do not buy a new HEPA vacuum. Replace only a missing or damaged model-specific filter/bag. |

## Complete budget rivet system

The rivet system is intentionally a crude hobby method. It does **not** include
a purpose-built press or matched forming dies.

| Function | Exact item/source | Qty. | Target / buy ceiling | Notes |
|---|---|---:|---:|---|
| Hollow PCB rivets | Generic `M0.9(d) x 2.5(L) mm` hollow PCB via rivets, Amazon ASIN `B015CV377O`: [Amazon](https://www.amazon.com/dp/B015CV377O) | 1 pack, listing says 1000 | target $8, **do not exceed $10** | Nominal 0.9 mm shank OD. Material and head claims vary; measure the delivered lot before freezing pads or holes. |
| Forming punch | PITTSBURGH PRO automatic center punch, Harbor Freight SKU `621`: [Harbor Freight](https://www.harborfreight.com/spring-loaded-center-punch-621.html) | 1 | $3.99 in store | No hammer or matched die is needed. This model is not adjustable; control the flare by stopping after one light push-to-strike stroke and inspecting before another. Its pointed tip makes a rough retaining flare, not a precision rolled head. |
| Backing surface | Existing clean, flat steel block or plate | 1 | $0 | Support the factory flange and surrounding board without rocking. |

The rivets and forming punch cost **$11.98**. Including ten proper carbide PCB
drills, the complete drilling-and-rivet subsystem is **$18.52**.

## Realistic total

Using every priced purchase above and the target prices gives approximately:

| Group | Target subtotal |
|---|---:|
| Ten blanks, 20 transfer sheets, and 1 L etchant | $41 |
| Both PP boxes, loose lid, tongs, and waste bottle | $11 |
| Goggles, one reusable glove pair, and eyewash bottle | $12 |
| Ten drill bits and printed hood material | $8 |
| Rivets and forming punch | $12 |
| **Target startup total** | **about $84 plus tax/shipping** |

Reuse of suitable boxes, tongs, and a waste bottle reduces that to roughly
**$73**. Treat **$85-95 before tax and shipping** as the realistic startup
range because the generic Amazon prices move and the $5.40 eyewash is a
clearance item. The purchase leaves ten blanks,
twenty transfer sheets, ten bits, and
roughly one thousand rivets; it is not a one-board cost. After the reusable
safety items and tools are owned, the consumable cost of another small board is
roughly **$4-8**, depending mainly on failed transfers and etchant reuse.

## Explicitly not required

- no Dynalon or other laboratory secondary-containment tray;
- no purpose-built PCB rivet press, matched forming dies, or imported single
  drill bits;
- no plumbed eyewash, face shield, specialty spill kit, chemical apron, or
  respirator for this small outdoor process;
- no new HEPA dust extractor; and
- no soldering or fume-extraction purchases.
