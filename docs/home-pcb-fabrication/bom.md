# Cost-optimized home PCB fabrication BOM

This is a standalone BOM for the workflow in this folder, not part of the
telescope electronics BOM. Prices and links were checked 2026-08-27. Amazon
prices, sellers, quantities, and fulfillment are volatile, so the tables give
a **delivered buy ceiling** (item plus mandatory shipping, before sales tax):
skip a listing above that price or when the seller does not identify the
required item precisely.

The objective is a useful stock of consumables, not one board at industrial
lab prices. Generic items require incoming inspection and a process coupon.
Compare **delivered** cost, not the item price. A dedicated one-hour pickup trip
is not free: prefer an Amazon or other shipped option below its recorded ceiling
and use a local source when it can be combined with another trip.

An Amazon listing is only a source option. It does not permit a different
chemical, plastic, PPE model, glove size, or tool. Record the seller and
delivered price at checkout, then verify the received manufacturer identity,
quantity, material, size, lot, and expiration date when applicable.

## Amazon convenience-sourcing record

This table supplements the cost-optimized line-item tables below. Exact-part
search links are used when Amazon divides sizes or sellers among listings.
“Reuse” is deliberately the $0 Amazon option.

| Function | Amazon option | Reference price / ceiling | Checkout and receipt requirement |
|---|---|---:|---|
| Copper-clad stock | [GeeBat GB0021, ASIN B01MRG7NHC](https://www.amazon.com/dp/B01MRG7NHC) | target $14; **$18 delivered ceiling** | Verify ten nominal 70 x 100 x 1.5 mm double-sided copper-clad FR-4 blanks. |
| Toner-transfer paper | [Ximimark XQJ=LY251-XQJ-FBA, ASIN B07MYXK4WJ](https://www.amazon.com/dp/B07MYXK4WJ) | target $9; **$12 delivered ceiling** | Verify 20 A4 sheets intended for laser-toner PCB transfer. |
| Ferric-chloride etchant | [MG Chemicals 415-1L, ASIN B005T8Y20W](https://www.amazon.com/dp/B005T8Y20W) | user-observed $21 on 2026-08-27; **$25 delivered ceiling** | Preferred over a dedicated one-hour drive. Verify sealed MG `415-1L`, nominal 1 L package (945 mL net contents), with no leak or crystallized closure. |
| PP working bath with lid | Conditional Cambro 4 qt two-pack, bundle model `4RPP2PKB190`, [ASIN B0CZ552H67](https://www.amazon.com/dp/B0CZ552H67), [price record](https://pricehistory.app/p/cambro-food-storage-containers-lids-bpa-free-btT17CSj); recorded square alternative: [exact `4SFSPP190` search](https://www.amazon.com/s?k=Cambro+4SFSPP190) plus [lid `SFC2-452`, ASIN B07SPVM8ZZ](https://www.amazon.com/dp/B07SPVM8ZZ) | two-pack recently about $17.50-19.08; **$20 delivered ceiling** | Reuse a verified container first. Amazon describes the two-pack material only as “plastic,” so do not qualify it at checkout. Accept only a body molded `PP`/resin-code-5 and a lid explicitly marked compatible PP or HDPE, with enough panel clearance, no metal, and no hollow handle. `SFC2-452` is described only as polyethylene and commonly sold six at a time, so it remains unqualified and poor value unless its exact resin grade is documented. |
| PP secondary containment | [Amazon exact-MPN search for Cambro 12SFSPP190](https://www.amazon.com/s?k=Cambro+12SFSPP190); otherwise [generic PP bus-box search](https://www.amazon.com/s?k=polypropylene+bus+box) | **$20 delivered ceiling** | Reuse first. Require exact `12SFSPP190` or a body molded `PP`/resin-code-5, and capacity for the full working bath plus spill margin. Do not accept clear polycarbonate `12SFSCW135`, which is a different material and MPN. |
| Board-handling tongs | [Amazon search for one-piece polypropylene tongs](https://www.amazon.com/s?k=one+piece+polypropylene+tongs) | **$8 delivered ceiling** | Reuse first. Accept only one-piece PP without a metal spring, fastener, insert, or hollow liquid-trapping handle. |
| Rinse containers | Reuse two verified HDPE or PP containers | $0 | Label for PCB work and never return to food use. |
| Spent-etchant bottle | Reuse a compatible screw-cap HDPE bottle; conditional [Amazon search for Nalgene 312104-0032](https://www.amazon.com/s?k=Nalgene+312104-0032) | $0 reused; **$25 delivered ceiling** if a new bottle is necessary | Require an HDPE body, compatible nonmetal cap, leak-free closure, and at least 1 L capacity. The Nalgene item is a candidate, not selected; selecting it requires primary-documentation mapping in the datasheet index. Never pour spent etchant down a drain. |
| Splash goggles | [Amazon search for Pyramex G205](https://www.amazon.com/s?k=Pyramex+G205) | **$8 delivered ceiling** | Verify exact model `G205`, indirect ventilation, intact lens and strap, and no safety-glasses substitution. |
| Chemical gloves | [Amazon search for SHOWA 730](https://www.amazon.com/s?k=SHOWA+730+nitrile+chemical+gloves) | **$8 delivered ceiling** | Select and record the wearer's size. Verify exact `730-[size]`, 13 in nominal length, 15 mil nominal thickness, and an intact pair. |
| Immediate eye flush | [First Aid Only / PhysiciansCare 24-202, ASIN B002A6AFDY](https://www.amazon.com/dp/B002A6AFDY) | target $20; **$22 delivered ceiling** | Verify the received station and bottle identity against the archived `24-202-001` product sheet, 32 fl oz fill, intact seal, and usable expiration. Reject an obscured model, reduced volume, damaged seal, or short-dated bottle. |
| Carbide drill bits | [Amazon search for Harfington f25070700ux0179](https://www.amazon.com/s?k=Harfington+f25070700ux0179) | **$12 delivered ceiling** | The manufacturer-direct shipped listing remains acceptable. Verify the exact ten-piece 1.0 mm set, 3.175 mm shank, 10 mm flute, and 38 mm overall length; inspect every tip. |
| Printed drill hood | Print from repository source | about $1 material | No Amazon purchase. Record filament and the successful vacuum-capture test in the build log. |
| Vacuum and filter/bag | Existing vacuum only | $0 | Verify the current filter/bag is fitted and serviceable. Do not buy an unqualified substitute from a recommendation carousel. |
| Through-hole rivets | [ASIN B015CV377O](https://www.amazon.com/dp/B015CV377O) | target $8; **$10 delivered ceiling** | Verify the listing quantity and the stated 0.9 mm shank OD / 2.5 mm length, then measure the delivered lot before committing a board hole size. |
| Rivet punch | [NEIKO 02638A, ASIN B008DXYOLC](https://www.amazon.com/dp/B008DXYOLC) | target $11; **$13 delivered ceiling** | Amazon alternative to local Pittsburgh SKU `621`. Verify exact adjustable automatic center punch `02638A`, straight S2 tip, smooth push-to-strike action, and working force adjustment. |
| Rivet backing surface | Existing flat steel scrap or anvil | $0 | Buy nothing unless the existing surface fails a scrap-coupon test. |

The eye-flush and NEIKO entries are qualified sourcing alternatives; record the
accepted received identity below. The Nalgene bottle remains only a candidate.
Selecting it requires adding its exact primary documentation and source mapping
to `docs/datasheets/README.md` in the same change. The Cambro Amazon choices
are also candidates until the delivered resin marks and exact component MPNs
are known; archive and map Cambro primary documentation if either is selected.

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
| Etchant | MG Chemicals `415-1L` ready-to-use ferric chloride: [manufacturer](https://mgchemicals.com/products/circuit-board-design/copper-etchants/ferric-chloride-etching/), [Amazon ASIN B005T8Y20W](https://www.amazon.com/dp/B005T8Y20W), [Anchor Electronics](https://anchor-electronics.com/product/mgchemicals-415-ferric-chloride/) | 1 | Amazon observed $21; **do not exceed $25 delivered** | The $21 Amazon option is preferred to a dedicated one-hour pickup drive. Use the $18.01 Anchor option only on a combined trip. Use at most 100 mL in the working box and reuse it while it still etches acceptably; keep fresh and used material separately labeled. |
| Working box | IKEA SAMLA `701.029.72`, 1-gallon polypropylene box: [IKEA](https://www.ikea.com/us/en/p/samla-box-clear-70102972/), with PP lid `504.550.88`: [IKEA](https://www.ikea.com/us/en/p/samla-lid-for-box-1-gallon-clear-50455088/) | 1 each | $3.99 + $1.00 | Fits these blanks. Rest the lid loosely with a visible vent gap during an etch; never latch it closed. The HCl model conservatively uses its full 11 x 7.5 in top footprint. Mark both pieces chemical-use-only. IKEA currently imposes an online minimum of two, so buy one in store or substitute a local #5 PP box rather than paying for extras. |
| Secondary containment | IKEA SAMLA `401.029.78`, 3-gallon polypropylene box: [IKEA](https://www.ikea.com/us/en/p/samla-box-clear-40102978/) | 1 | $2.99 | No lid is required. It replaces the specialty Dynalon tray and must remain large enough to hold all liquid staged for the run. |
| Board handling | Local all-plastic serving tongs; [low-cost example](https://www.walmart.com/c/kp/plastic-serving-utensils) | 1 | $1-2 | Inspect for exposed metal, cracks, or a hollow section that can trap etchant. Dedicate it to chemical work. |
| Rinse containers | Two clean, reused #2 HDPE or #5 PP household containers with identifying labels | 2 | $0 | Permanently mark them chemical-use-only. Do not use glass or metal. |
| Waste bottle | 32 oz HDPE bottle with PP screw cap, U.S. Plastic item `97365`: [source](https://www.usplastic.com/catalog/item.aspx?itemid=165118), or a local equivalent | 1 | $1.89 before shipping; **buy locally if shipping dominates** | Confirm the container and size with the local HHW program. Deface it and label actual contents and date. A larger compatible bottle is needed if captured rinse volume will exceed 32 oz. |

## Minimum personal protection

| Function | Selected item/source | Qty. | Target cost | Notes |
|---|---|---:|---:|---|
| Splash goggles | Pyramex `G205`, ANSI Z87+ and D3: [manufacturer](https://www.pyramex.com/products/chemical-splash-goggle-d3), [Amazon exact-model search](https://www.amazon.com/s?k=Pyramex+G205), [single-unit source](https://hdsupplysolutions.com/p/pyramex-chemical-splash-goggles-clear-body-clear-lens-p414897) | 1 | **do not exceed $8 delivered** | Buy the exact `G205` on Amazon or combine the cheaper source with another order. Indirect-vent chemical-splash goggles marked D3 are required; ordinary safety glasses are not a substitute. |
| Chemical gloves | SHOWA `730-[size]`, 13 in, 15 mil reusable nitrile: [manufacturer](https://www.showagroup.com/us-en/shop/730/), [Amazon exact-model search](https://www.amazon.com/s?k=SHOWA+730+nitrile+chemical+gloves), [size 9 example](https://www.grainger.com/product/SHOWA-Chemical-Resistant-Gloves-4JF19) | 1 correctly sized pair | **do not exceed $8 delivered; do not buy a case** | Record the selected size. Brief splash handling only. Rinse the exterior after a splash and replace damaged gloves. Never wear them at the drill press. |
| Immediate eye flush | First Aid Only `24-202-001`, single 32 oz eye-flush station: [product sheet](../datasheets/home-pcb-fabrication/first-aid-only-eyewash-product-sheet.pdf), [Amazon candidate ASIN B002A6AFDY](https://www.amazon.com/dp/B002A6AFDY), [clearance source](https://blackboxsafety.com/products/first-aid-only-eyewash-station-24-202-001) | 1 | target $20 on Amazon; **do not exceed $22 delivered** | Confirm exact model identity against the product sheet before accepting an Amazon listing; record the received model and expiration below. This is immediate first flush only; continue at the already-tested household sink/shower for the etchant SDS's 30 minutes. Replace after opening. |

Long sleeves, long pants, closed shoes, an unobstructed route to a household
sink/shower, ordinary wipes, and labels are existing household provisions.

## Drilling and dust capture

| Function | Cost-optimized selection | Qty. | Target / buy ceiling | Notes |
|---|---|---:|---:|---|
| 1.0 mm overdrill bits | Harfington `f25070700ux0179`, ten 1.0 mm solid-carbide twist drills, 3.175 mm shank, 10 mm flute, 38 mm overall: [Harfington](https://www.harfington.com/products/p-1889293), [Amazon exact-MPN search](https://www.amazon.com/s?k=Harfington+f25070700ux0179) | 1 pack | target $6.54 direct; **do not exceed $12 delivered** | These are actual spiral-flute PCB drills, not pointed engraving burrs. The nominal 0.1 mm diametral clearance over a 0.9 mm rivet is deliberate. Reject chipped or bent bits and qualify the measured hole and delivered rivet together on the coupon. |
| Close-capture hood | 3D-printed shop-vac nozzle/holder using existing filament and common hardware | 1 | about $1 incremental material | Rigidly mount it beside the bit and dry-run full quill travel. The print is a hood, not a filter. |
| Vacuum consumables | Existing compatible dry collection bag and serviceable cartridge/filter | 1 set | $0 if already fitted | For a few holes outdoors, do not buy a new HEPA vacuum. Replace only a missing or damaged model-specific filter/bag. |

## Complete budget rivet system

The rivet system is intentionally a crude hobby method. It does **not** include
a purpose-built press or matched forming dies.

| Function | Exact item/source | Qty. | Target / buy ceiling | Notes |
|---|---|---:|---:|---|
| Hollow PCB rivets | Generic `M0.9(d) x 2.5(L) mm` hollow PCB via rivets, Amazon ASIN `B015CV377O`: [Amazon](https://www.amazon.com/dp/B015CV377O) | 1 pack, listing says 1000 | target $8, **do not exceed $10** | Nominal 0.9 mm shank OD. Material and head claims vary; measure the delivered lot before freezing pads or holes. |
| Forming punch | NEIKO adjustable automatic center punch `02638A`: [manufacturer](https://neikotools.com/products/neiko-02638a-5-automatic-center-hole-punch-adjustable-impact-spring-loaded-puncher-tool), [Amazon ASIN B008DXYOLC](https://www.amazon.com/dp/B008DXYOLC); or PITTSBURGH PRO automatic center punch, Harbor Freight SKU `621`: [Harbor Freight](https://www.harborfreight.com/spring-loaded-center-punch-621.html) | 1 | Amazon target $11, **do not exceed $13 delivered**; Pittsburgh $3.99 on a combined trip | No hammer or matched die is needed. Start the adjustable NEIKO at minimum force. Stop after one light push-to-strike stroke and inspect before another. Either pointed tip makes a rough retaining flare, not a precision rolled head. |
| Backing surface | Existing clean, flat steel block or plate | 1 | $0 | Support the factory flange and surrounding board without rocking. |

The Amazon rivets and NEIKO punch target is **about $19**. Including ten proper
carbide PCB drills, the printed hood material, and the Amazon convenience
allowances, plan **about $27** for the complete drilling-and-rivet subsystem.

## Realistic total

The Amazon-first plan below uses the observed or target values, with the full
Amazon allowances for goggles and gloves. It assumes suitable reused PP/HDPE
containers and tongs; buying the inexpensive IKEA items on an already-planned
trip adds about $11.

| Group | Target subtotal |
|---|---:|
| Ten blanks, 20 transfer sheets, and MG `415-1L` from Amazon | $44 |
| Reused verified PP/HDPE boxes, tongs, and waste bottle | $0 |
| Goggles, one reusable glove pair, and Amazon eyewash allowance | up to $36 |
| Ten drill bits and printed hood material | $8 |
| Rivets and NEIKO forming punch | $19 |
| **Amazon-first startup plan** | **about $107 delivered before sales tax** |

Treat **$105-120 delivered before sales tax** as the realistic startup
range with reused containers. The item-by-item Amazon ceilings total $129
before any container purchases. Do not spend the possible additional $73 at
the generic Amazon container ceilings: reuse verified items or obtain the $11
local set during another trip. The purchase leaves ten blanks, twenty transfer
sheets, ten bits, and roughly one thousand rivets; it is not a one-board cost.
After the reusable safety items and tools are owned, the consumable cost of
another small board is roughly **$4-8**, depending mainly on failed transfers
and etchant reuse.

## Purchase and receipt ledger

Change `not ordered` to `ordered`, then `received` and `accepted` or `rejected`.
Record the actual marketplace seller because it can change under an ASIN. Use
delivered cost including shipping and tax. Do not commit a delivery address,
payment details, or a full marketplace order number to this repository.

| Function | Planned identity | Qty. | Status | Order date / seller / delivered cost | Receipt identity, lot or expiration, and acceptance evidence |
|---|---|---:|---|---|---|
| Copper-clad stock | GeeBat `GB0021`, ASIN `B01MRG7NHC` | 1 pack | not ordered | — | Record measured count, panel dimensions/thickness, flatness, and coupon result. |
| Toner-transfer paper | Ximimark `XQJ=LY251-XQJ-FBA`, ASIN `B07MYXK4WJ` | 1 pack | not ordered | — | Record sheet count and Brother toner-transfer coupon result. |
| Ferric-chloride etchant | MG Chemicals `415-1L`, ASIN `B005T8Y20W` | 1 | not ordered | — | Record exact label identity, lot/date code, seal and bottle condition, and net-volume marking. |
| Working bath and lid | Reused verified PP, IKEA SAMLA, or accepted Amazon PP item | 1 set | not ordered | — | Record source/MPN if bought, molded resin mark, internal dimensions, lid fit, and absence of metal/hollows. |
| Secondary containment | Reused verified PP, IKEA SAMLA, or accepted Amazon PP item | 1 | not ordered | — | Record source/MPN if bought, molded resin mark, and containment-volume check. |
| Board-handling tongs | Reused or one-piece PP | 1 | not ordered | — | Record material marking and inspection for metal, cracks, and trapped-volume features. |
| Rinse containers | Reused HDPE or PP | 2 | not ordered | — | Record resin marks, volume, closure, and chemical-use labels. |
| Spent-etchant bottle | Reused HDPE/compatible cap or separately qualified exact item | 1 | not ordered | — | Record body/cap materials, capacity, leak test, HHW acceptance, contents label, and first-use date. |
| Splash goggles | Pyramex `G205` | 1 | not ordered | — | Record exact model/markings and lens, vent, and strap inspection. |
| Chemical gloves | SHOWA `730-[size]` | 1 pair | not ordered | — | Record exact model, selected size, package/lot code, and condition. |
| Immediate eye flush | First Aid Only `24-202-001`; Amazon ASIN `B002A6AFDY` only after identity check | 1 | not ordered | — | Record exact received MPN, 32 fl oz marking, lot, expiration, intact seal, and mount condition. |
| Carbide drills | Harfington `f25070700ux0179`, 1.0 mm | 1 pack | not ordered | — | Record exact MPN, count, dimensions, tip inspection, and drilled coupon diameter. |
| Printed hood | Repository design | 1 | not made | — | Record filament, print revision, mounting, quill-clearance check, and capture-test result. |
| Vacuum filter/bag | Existing model-compatible items | 1 set | inspect existing | — | Record vacuum model, filter/bag identity and condition, and exhaust-direction check. |
| Hollow rivets | `M0.9(d) x 2.5(L) mm`, ASIN `B015CV377O` | 1 pack | not ordered | — | Record seller, quantity, material claim, measured shank/head/length sample, and coupon result. |
| Forming punch | NEIKO `02638A`, ASIN `B008DXYOLC`; or Pittsburgh SKU `621` | 1 | not ordered | — | Record exact received model, tip condition, mechanism/adjustment check, and minimum-force rivet coupon result. |
| Backing surface | Existing flat steel block or plate | 1 | inspect existing | — | Record flatness/cleanliness check and coupon support result. |

## Explicitly not required

- no Dynalon or other laboratory secondary-containment tray;
- no purpose-built PCB rivet press, matched forming dies, or imported single
  drill bits;
- no plumbed eyewash, face shield, specialty spill kit, chemical apron, or
  respirator for this small outdoor process;
- no new HEPA dust extractor; and
- no soldering or fume-extraction purchases.
