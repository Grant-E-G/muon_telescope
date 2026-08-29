# Revision A planning BOM

Checked 2026-08-23. Prices are USD, quantity-one planning values, not quotes;
stock, marketplace listings, shipping, tariffs, and tax can change. Recheck the
manufacturer number, package, lifecycle, and stock on the order date. The KiCad-
generated BOM must be reconciled to this document before fabrication.

Every selected manufacturer number is mapped to an archived primary document
in [`docs/datasheets/README.md`](datasheets/README.md). Distributor links below
are for availability and ordering; the archived manufacturer document controls
electrical and mechanical design.

Quantities assemble two identical detector heads and one power/interface board.
PCB quantities assume five of each design are fabricated, but only two heads and
one central board are initially populated. The already-owned Cora Z7-07S, lab
power supply, oscilloscope, soldering equipment, ESD supplies, and ordinary tools
are excluded.

## Critical and active parts

| Function | Manufacturer part | Package | Design qty | Buy qty | Checked source | Approx. each |
|---|---|---|---:|---:|---|---:|
| 6 mm, 35 um SiPM | onsemi `MICROFC-60035-SMT-TR` | custom SMT | 2 | 2 | [DigiKey](https://www.digikey.com/en/products/detail/onsemi/MICROFC-60035-SMT-TR/9742618), [datasheet](https://www.onsemi.com/pdf/datasheet/microc-series-d.pdf) | $24.25 |
| Dual high-speed amplifier | 3PEAK `TPH2502-SR` | SOP-8 | 2 | 2 | [DigiKey](https://www.digikey.com/en/products/detail/3peak/TPH2502-SR/22229182), [datasheet](https://static.3peak.com/res/doc/ds/Datasheet_TPH2501-TPH2502-TPH2503-TPH2504.pdf) | $1.12 |
| Dual fast comparator | TI `TLV3502AIDR` | SOIC-8 | 2 | 2 | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TLV3502AIDR/1669430), [datasheet](https://www.ti.com/lit/gpn/TLV3502) | $5.15 |
| Trigger one-shot | TI `SN74LVC1G123DCTR`; DigiKey cut-tape SKU `296-18758-1-ND` | DCT/SM8 | 2 | 3 | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G123DCTR/863597), [datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc1g123.pdf) | $1.73 |
| Adjustable boost controller | ADI/Maxim `MAX5026EUT+T`; DigiKey cut-tape SKU `MAX5026EUT+TCT-ND` | SOT-23-6 | 1 | 1 | [DigiKey](https://www.digikey.com/en/products/detail/analog-devices-inc-maxim-integrated/MAX5026EUT-T/1516355), [datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/max5025-max5028.pdf) | $1.95 |
| 3.3 V, 500 mA LDO | TI `TLV75533PDBVR` | SOT-23-5 | 1 | 1 | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TLV75533PDBVR/9356541), [datasheet](https://www.ti.com/lit/gpn/TLV755P) | $0.75 |
| 47 uH shielded inductor | Bourns `SRN6045-470M` | 6 x 6 mm SMT | 1 | 1 | [DigiKey](https://www.digikey.com/en/products/detail/bourns-inc/SRN6045-470M/2756124) | $0.60 |
| 60 V boost Schottky | onsemi `SS16HE` | SMA | 1 | 1 | [DigiKey](https://www.digikey.com/en/products/detail/onsemi/SS16HE/6009714) | $0.59 |
| 40 V input Schottky | onsemi `SS14` | SMA | 1 | 1 | [DigiKey](https://www.digikey.com/en/products/detail/onsemi/SS14/965474) | $0.44 |
| 6 V, 500 mA resettable fuse | Littelfuse `1206L050YR` | 1206 | 1 | 1 | [DigiKey](https://www.digikey.com/en/products/detail/littelfuse-inc/1206L050YR/455721) | $0.64 |
| Bias trim, 500 ohm, 10 turn | Bourns `3296W-1-501LF` | through-hole | 1 | 1 | [DigiKey](https://www.digikey.com/en/products?keywords=3296W-1-501LF) | $2.39 |
| Threshold trim, 10 kohm, 10 turn | Bourns `3296W-1-103LF` | through-hole | 2 | 2 | [DigiKey](https://www.digikey.com/en/products?keywords=3296W-1-103LF) | $2.39 |
| Optional input clamp, DNP | Diodes Inc. `BAT54S-7-F` | SOT-23 | 0 | 2 | [DigiKey](https://www.digikey.com/en/products?keywords=BAT54S-7-F) | $0.25 |

The two DNP clamps are optional prototypes, not default assembly. If budget
allows, a third SiPM adds $24.25 and is the most useful active-part spare.
Distributor suffixes describe packaging, not different silicon: `CT-ND` is
DigiKey cut tape, `TR-ND` is the full tape-and-reel option, and `DKR-ND` is a
Digi-Reel. Keep `MAX5026EUT+T` as the manufacturer number in KiCad.

## Resistors

Use 0805, 1%, 100 ppm/deg C or better unless noted. Design quantity includes
both heads and the central board. Buy at least ten of each inexpensive value so
hand assembly is not stopped by a lost part.

| Value and role | Recommended part | Design qty | Source |
|---|---|---:|---|
| 0 ohm current and trigger-selection links | Yageo `RC0805JR-070RL` | 3 (plus 2 DNP footprints) | [DigiKey](https://www.digikey.com/en/products?keywords=RC0805JR-070RL) |
| 49.9 ohm SiPM sense | Yageo `RC0805FR-0749R9L` | 2 | [DigiKey](https://www.digikey.com/en/products?keywords=RC0805FR-0749R9L) |
| 100 ohm bias filters and trigger damping | Yageo `RC0805FR-07100RL` | 5 | [DigiKey](https://www.digikey.com/en/products?keywords=RC0805FR-07100RL) |
| 499 ohm input bias and injection | Yageo `RC0805FR-07499RL` | 4 | [DigiKey](https://www.digikey.com/en/products?keywords=RC0805FR-07499RL) |
| 1.00 kohm gain, comparator, threshold | Yageo `RC0805FR-071KL` | 6 | [DigiKey](https://www.digikey.com/en/products?keywords=RC0805FR-071KL) |
| 2.00 kohm baseline dividers and one-shot timing | Yageo `RC0805FR-072KL` | 4 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-072KL/730611) |
| 4.70 kohm threshold divider | Yageo `RC0805FR-074K7L` | 2 | [DigiKey](https://www.digikey.com/en/products?keywords=RC0805FR-074K7L) |
| 10.0 kohm FPGA pulldown | Yageo `RC0805FR-0710KL` | 2 | [DigiKey](https://www.digikey.com/en/products?keywords=RC0805FR-0710KL) |
| 12.4 kohm gain feedback | Yageo `RC0805FR-0712K4L` | 2 | [DigiKey](https://www.digikey.com/en/products?keywords=RC0805FR-0712K4L) |
| 100 kohm shutdown pulldown | Yageo `RC0805FR-07100KL` | 1 | [DigiKey](https://www.digikey.com/en/products?keywords=RC0805FR-07100KL) |
| 130 kohm baseline divider | Yageo `RC0805FR-07130KL` | 2 | [DigiKey](https://www.digikey.com/en/products?keywords=RC0805FR-07130KL) |
| 330 kohm external hysteresis, DNP | Yageo `RC0805FR-07330KL` | 0 (2 footprints) | [DigiKey](https://www.digikey.com/en/products?keywords=RC0805FR-07330KL) |
| 1 Mohm bias bleeder | Yageo `RC0805FR-071ML` | 1 | [DigiKey](https://www.digikey.com/en/products?keywords=RC0805FR-071ML) |
| 147 kohm boost feedback, 0.1% | Panasonic `ERA-6AEB1473V` | 1 | [DigiKey](https://www.digikey.com/en/products?keywords=ERA-6AEB1473V) |
| 6.98 kohm boost feedback, 0.1% | Panasonic `ERA-6AEB6981V` | 1 | [DigiKey](https://www.digikey.com/en/products?keywords=ERA-6AEB6981V) |

Buy two 10.0 ohm `RC0805FR-0710RL` resistors as alternate head stuffing parts;
do not install them silently on only one channel.

## Capacitors

MLCC capacitance falls under DC bias. Preserve the listed voltage rating and
case size, especially on the 27 V rail; do not substitute a smaller package
solely because its printed nominal capacitance matches.

| Value and dielectric | Recommended part | Design qty | Buy qty | Source |
|---|---|---:|---:|---|
| 100 nF, 50 V, X7R, 0805 | KEMET `C0805C104K5RACTU` | 12 | 20 | [DigiKey](https://www.digikey.com/en/products?keywords=C0805C104K5RACTU) |
| 1 uF, 16 V, X7R, 0805 | KEMET `C0805C105K4RACTU` | 6 | 10 | [DigiKey](https://www.digikey.com/en/products?keywords=C0805C105K4RACTU) |
| 4.7 uF, 16 V, X7R, 0805 | KEMET `C0805C475K4RACTU` | 3 | 5 | [DigiKey](https://www.digikey.com/en/products?keywords=C0805C475K4RACTU) |
| 10 uF, 10 V, X7R, 1206 | KEMET `C1206C106K8RACTU` | 1 | 2 | [DigiKey](https://www.digikey.com/en/products?keywords=C1206C106K8RACTU) |
| 1 uF, 50 V, X7R, 1206 | KEMET `C1206C105K5RACTU` | 5 | 10 | [DigiKey](https://www.digikey.com/en/products?keywords=C1206C105K5RACTU) |
| 10 nF, 100 V, C0G, 0805 | KEMET `C0805C103J1GACTU` | 5 | 10 | [DigiKey](https://www.digikey.com/en/products?keywords=C0805C103J1GACTU) |
| 27 pF, 50 V, C0G, 0805 | KEMET `C0805C270J5GACTU` | 2 | 5 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C0805C270J5GACTU/411113) |
| 2.2 pF, 50 V, C0G, 0805, DNP | KEMET `C0805C229C5GACTU` | 0 (2 footprints) | 5 | [DigiKey](https://www.digikey.com/en/products?keywords=C0805C229C5GACTU) |

The TLV755 schematic must follow the selected regulator datasheet. The total
above reserves one close input and one output 1 uF capacitor for that LDO.

## Connectors and cable

Factory-crimped leads avoid buying a specialized JST XH crimp tool and a reel-
quantity contact. Insert the contacts fully, pull-test each lead, then perform a
pin-numbered continuity test on every finished cable.

| Function | Manufacturer part | Design / buy qty | Source | Approx. each |
|---|---|---:|---|---:|
| 8-pin board headers, two central and two heads | JST `B8B-XH-A(LF)(SN)` | 4 | [DigiKey](https://www.digikey.com/en/products/detail/jst-sales-america-inc/B8B-XH-A/1651049) | $0.65 |
| 8-pin cable housings | JST `XHP-8` | 4 | [DigiKey](https://www.digikey.com/en/products?keywords=XHP-8) | $0.20 |
| 12-inch XH-to-XH 22 AWG precrimp lead | JST `ASXHSXH22K305` | 16 | [DigiKey](https://www.digikey.com/en/products/detail/jst-sales-america-inc/ASXHSXH22K305/6684932) | $0.80 |
| 5 V center-positive board jack | Same Sky `PJ-102AH` | 1 | [DigiKey](https://www.digikey.com/en/products/detail/same-sky-formerly-cui-devices/PJ-102AH/408448) | $1.30 |
| Regulated 5 V, 1 A Class II wall adapter | Phihong `PSAC05A-050L6-R` | 1 | [DigiKey](https://www.digikey.com/en/products/detail/phihong-usa/PSAC05A-050L6-R/5418482) | $5.40 |
| Right-angle 2x6 Pmod header | Samtec `TSW-106-08-G-D-RA` | 1 | [Mouser](https://www.mouser.com/ProductDetail/Samtec/TSW-106-08-G-D-RA) | $2.11 |
| 6-inch 2x6 Pmod cable with gender changer | Digilent `240-109` | 1 | [Digilent](https://digilent.com/shop/2x6-pin-pmod-cable/) | $5.00 |
| Breakaway 2.54 mm header for inject/jumpers | Samtec `TSW-120-07-G-S` | 1 strip | [DigiKey](https://www.digikey.com/en/products/detail/samtec-inc/TSW-120-07-G-S/1101307) | $2.99 |
| 2.54 mm shorting shunts | Samtec `SNT-100-BK-G` | 2 | [DigiKey](https://www.digikey.com/en/products?keywords=SNT-100-BK-G) | $0.35 |

The selected adapter removes the exposed-contact and remote-end ambiguity of a
power pigtail. Before first use, verify center-positive polarity and voltage at
the board jack. Continuity-map the unkeyed Pmod cable and gender changer, label
pin 1 at both ends, and strain-relieve the central board.

Use PCB-integrated probe pads plus fitted ground loops rather than purchasing a
large number of generic test-point terminals.

## Scintillator, optical, mechanical, and fabrication

| Item | Qty | Checked source or requirement | Planning cost |
|---|---:|---|---:|
| Purchased BC-408 block, 50 x 50 x 10 mm, one face polished | 2 | [Purchased listing](https://www.ebay.com/itm/254751779655); seller model `BC408-505010-1FP`, $25 each or $22.50 each at quantity two when checked. The seller describes virgin BC-408 water-saw cut from a large block; one 50 x 50 mm face is polished and the other face and sides are smooth cut. See [manufacturer BC-408 properties](https://luxiumsolutions.com/radiation-detection-scintillators/plastic-scintillators/bc400-bc404-bc408-bc412-bc416). | $45 |
| EJ-550 optical coupling compound | 1 | [Surplus listing](https://www.ebay.com/itm/157806378831), $16.50 when checked; [technical sheet](https://www-eng.lbl.gov/~shuman/NEXT/MATERIALS%26COMPONENTS/WLS_materials/optical-grease_EJ550.pdf) | $16.50 |
| Reflective foil and opaque wrap/tape | 1 set | Local consumable; document the actual material used | $10 |
| Rigid adjustable frame and fasteners | 1 | Design under `hardware/mechanical/`; use existing stock where practical | $10-25 |
| Five 70 x 70 mm detector-head plus five 96 x 64 mm power/interface PCBs | 10 boards | Frozen revision A outlines are in `docs/design.md`; quote the chosen fabricator from the reviewed KiCad boards. The [JLCPCB quote tool](https://jlcpcb.com/quote) is a planning reference, not a selected supplier | $35-55 |
| Optional stainless stencil | 1 | Quote with fabrication package if it improves SiPM process control | $0-15 |

The scintillator geometry and provenance decisions are resolved. The seller
identifies the purchased pieces as virgin material cut from a large BC-408 block
with a water-cooled saw. Incoming inspection still verifies quantity,
dimensions, damage, and which broad face is polished before optical or
mechanical work begins. Back up project-owned mechanical models in Git; link to
a third-party source and license rather than copying an unlicensed model.

## Cost reality

Using the purchased scintillator blocks and assembling by hand gives this
planning range:

| Category | Planning subtotal |
|---|---:|
| Two scintillators | $45 |
| Critical semiconductors, power parts, and trimmers | $79 |
| Passives including order-quantity margin | $20-25 |
| Power adapter, connectors, precrimp leads, and headers | $30-35 |
| Optical compound and wrapping | $26.50 |
| PCBs and optional stencil allowance | $35-55 |
| Frame and fasteners | $10-25 |
| **Parts subtotal before shipping/tax** | **about $246-291** |

A realistic delivered total is roughly **$280-350**, depending mainly on PCB
shipping, frame stock, and whether consumables are already available. The
subtotal includes the purchased scintillators at their listing price but not
tax or shipping. Do not use the optimistic subtotal as authorization for the
remaining purchases.

## Release-time reconciliation

Before ordering:

1. Export the BOM from both reviewed KiCad schematics.
2. Compare every reference, value, footprint, DNP state, and quantity with this
   document and resolve differences deliberately.
3. Recheck every link and manufacturer datasheet; reject brokered or ambiguous
   substitutions for the SiPM, boost, amplifier, comparator, and LDO.
4. Add at least 10% passive/connector assembly margin and decide explicitly
   whether the third SiPM is worth the cost.
5. Save the distributor quotes or order confirmation with the build record, not
   as a replacement for manufacturer part numbers in KiCad.
