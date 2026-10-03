# Revision A shopping list

Reviewed against `docs/design.md` and native KiCad **9.0.9** schematic BOM
exports on **2026-10-02**. Prices below are USD public DigiKey US price tiers
observed during this review, extended at the recommended buy quantities and
rounded per line. They are an estimate, not a saved cart or distributor quote;
shipping, cold-pack/air service, tariffs, and tax are excluded. Recheck the
exact manufacturer number and availability at checkout.

Every selected manufacturer number is mapped to an archived primary document
in [`docs/datasheets/README.md`](datasheets/README.md). Distributor links below
are for availability and ordering; the archived manufacturer document controls
electrical and mechanical design. The paste index explicitly records its older
local TDS revision and the current manufacturer revision checked online.

Quantities assemble two identical detector heads and one power/interface board.
PCB quantities assume five of each design are fabricated, but only two heads and
one central board are initially populated. The already-owned Cora Z7-07S, lab
power supply, oscilloscope, T-962 oven, other soldering equipment, ESD supplies,
and ordinary tools are excluded.

## Cart reconciliation, 2026-10-02 21:24:46 export

The revised 61-line DigiKey cart includes the missing 25 x 100 ohm and
10 x 330 kohm resistors and the user-selected TS391SNL paste. Its merchandise
subtotal is $206.38, superseding the earlier planning estimate below.
The only backorder in that export is 10 x C0805C106K8PACTU ($1.15).
Replace that line with 10 x KEMET C0805C106K8PAC7210, cut-tape SKU
`399-C0805C106K8PAC7210CT-ND`
([DigiKey](https://www.digikey.com/en/products/detail/kemet/C0805C106K8PAC7210/12701235)).
The accessed listing shows stock and $0.115 each at ten, retaining the $206.38
subtotal before shipping, tax, and tariffs; checkout availability controls.
The archived exact-part manufacturer specification confirms 10 uF, 10 V,
+/-10%, X5R, 0805, 2.0 x 1.25 mm and 1.40 mm maximum thickness, matching
the head C5 requirement without changing circuit values or the footprint.

## Review and ordering basis

The default fitted counts match two copies of the `hardware/muon_detector_head`
schematic plus one `hardware/power_interface` schematic, including values, case
sizes, and DNP states. The exports have no populated `MPN` fields: generic passive
values and connector abbreviations are mapped to the exact parts below by
value, voltage, dielectric, tolerance, footprint, and reviewed design intent.
This is a procurement reconciliation, not fabrication approval.

- Keep four TPH2502 amplifiers, two one-shots, the MCP3202, two complete
  ten-conductor head cables, and the default BSS138P resets. TMUX1101 and its
  head C18 bypass remain DNP; R18 direct-trigger links also remain DNP.
- The head C5 10 uF/0805 X5R and C6 100 nF/100 V X7R entries were already in
  the list but missing from the datasheet index; their documentation is now
  covered. The 100 nF/50 V fitted total is 15, or 17 with precision resets.
- Buy `BAS70,235` cut tape instead of backordered `BAS70,215`. Nexperia
  identifies both as the same BAS70 SOT23 device; only reel packing differs.
  The schematic's `BAS70,215` value remains valid electrically; record the
  actual `,235` ordering suffix in the assembly record.
- Bourns 3296W trimmers are **25-turn**, correcting the former 10-turn text.
  Resistance, footprint, and wiring are unchanged.
- Most ICs get one spare; the four amplifiers get two. Cheap diodes/MOSFETs
  use the economical ten-piece tier. Resistors get ten each, or twenty for
  100 ohm and 1 kohm. Capacitors cover loss and characterization. No third
  $24.25 SiPM is included; add one only if that spare is worth the cost.
- The cart includes small quantities of the DNP clamp, hysteresis resistor,
  and feedback capacitor for debugging, plus the full allowed peak-stuffing
  matrix. Buying them does not authorize populating DNP sites.

Stock exception: the `TSW-120-07-G-S` strip is factory-stock/available-to-order,
not confirmed DigiKey warehouse stock. The displayed $2.56 is the DigiKey
order price; a marketplace seller may have different pricing/shipping. Check
its delivery date. All other recommended lines showed sufficient stock in the
accessed listings; the `BAS70,235` listing had only 71 pieces, so recheck it.

## Critical and active parts

| Function | Manufacturer part | Package | Design qty | Buy qty | Checked source | Each at buy qty | Line total |
| --- | --- | --- | ---: | ---: | --- | ---: | ---: |
| 6 mm, 35 um SiPM | onsemi `MICROFC-60035-SMT-TR` | custom SMT | 2 | 2 | [DigiKey](https://www.digikey.com/en/products/detail/onsemi/MICROFC-60035-SMT-TR/9742618), [datasheet](https://www.onsemi.com/pdf/datasheet/microc-series-d.pdf) | $24.25 | $48.50 |
| Dual high-speed amplifier | 3PEAK `TPH2502-SR` | SOP-8 | 4 | 6 | [DigiKey](https://www.digikey.com/en/products/detail/3peak/TPH2502-SR/22229182), [datasheet](https://static.3peak.com/res/doc/ds/Datasheet_TPH2501-TPH2502-TPH2503-TPH2504.pdf) | $1.12 | $6.72 |
| Dual fast comparator | TI `TLV3502AIDR` | SOIC-8 | 2 | 3 | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TLV3502AIDR/1669430), [datasheet](https://www.ti.com/lit/gpn/TLV3502) | $5.15 | $15.45 |
| Trigger one-shot | TI `SN74LVC1G123DCTR`; DigiKey cut-tape SKU `296-18758-1-ND` | DCT/SM8 | 2 | 3 | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G123DCTR/863597), [datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc1g123.pdf) | $1.73 | $5.19 |
| Dual 12-bit SPI ADC | Microchip `MCP3202-BI/SN` | SOIC-8 | 1 | 2 | [DigiKey](https://www.digikey.com/en/products/detail/microchip-technology/MCP3202-BI-SN/319432), [datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/21034F.pdf) | $3.82 | $7.64 |
| Peak-detector Schottky diode | Nexperia `BAS70,235`; cut tape `1727-BAS70,235CT-ND` | SOT-23 | 2 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/nexperia-usa-inc/BAS70-235/1232098), [datasheet](https://assets.nexperia.com/documents/data-sheet/BAS70.pdf) | $0.129 | $1.29 |
| Cost peak-reset MOSFET, default | Nexperia `BSS138P,215` | SOT-23 | 2 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/nexperia-usa-inc/BSS138P-215/2779827), [datasheet](https://assets.nexperia.com/documents/data-sheet/BSS138P.pdf) | $0.126 | $1.26 |
| Precision peak-reset switch, alternate | TI `TMUX1101DCKR` | SC70-5 | 0 (2 alternate footprints) | 0 (optional 3) | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TMUX1101DCKR/10442439), [datasheet](https://www.ti.com/lit/ds/symlink/tmux1101.pdf) | $1.91 | $0.00 |
| Adjustable boost controller | ADI/Maxim `MAX5026EUT+T`; DigiKey cut-tape SKU `MAX5026EUT+TCT-ND` | SOT-23-6 | 1 | 2 | [DigiKey](https://www.digikey.com/en/products/detail/analog-devices-inc-maxim-integrated/MAX5026EUT-T/1516355), [datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/max5025-max5028.pdf) | $1.95 | $3.90 |
| 3.3 V, 500 mA LDO | TI `TLV75533PDBVR` | SOT-23-5 | 1 | 3 | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TLV75533PDBVR/9356541), [datasheet](https://www.ti.com/lit/gpn/TLV755P) | $0.42 | $1.26 |
| 47 uH shielded inductor | Bourns `SRN6045-470M` | 6 x 6 mm SMT | 1 | 2 | [DigiKey](https://www.digikey.com/en/products/detail/bourns-inc/SRN6045-470M/2756124) | $0.43 | $0.86 |
| 60 V boost Schottky | onsemi `SS16HE` | SOD-323HE (onsemi CASE 477AD; not SMA) | 1 | 3 | [DigiKey](https://www.digikey.com/en/products/detail/onsemi/SS16HE/6009714) | $0.59 | $1.77 |
| 40 V input Schottky | onsemi `SS14` | SMA | 1 | 3 | [DigiKey](https://www.digikey.com/en/products/detail/onsemi/SS14/965474) | $0.44 | $1.32 |
| 6 V, 500 mA resettable fuse | Littelfuse `1206L050YR` | 1206 | 1 | 3 | [DigiKey](https://www.digikey.com/en/products/detail/littelfuse-inc/1206L050YR/455721) | $0.64 | $1.92 |
| Bias trim, 500 ohm, 25 turn | Bourns `3296W-1-501LF` | through-hole | 1 | 2 | [DigiKey](https://www.digikey.com/en/products/detail/bourns-inc/3296W-1-501LF/1088057) | $2.39 | $4.78 |
| Threshold trim, 10 kohm, 25 turn | Bourns `3296W-1-103LF` | through-hole | 2 | 3 | [DigiKey](https://www.digikey.com/en/products/detail/bourns-inc/3296W-1-103LF/1088045) | $2.39 | $7.17 |
| Optional input clamp, DNP | Diodes Inc. `BAT54S-7-F` | SOT-23 | 0 | 5 | [DigiKey](https://www.digikey.com/en/products/detail/diodes-incorporated/BAT54S-7-F/717925) | $0.22 | $1.10 |

The five purchased DNP clamps are debugging stock, not default assembly.
Three optional TMUX1101 switches (two plus one spare) add $5.73; the capacitor
order already covers their two bypass capacitors. Fit one reset technology per
head, never both. If budget allows, a third SiPM adds $24.25 and is the most useful active-part spare.
Distributor suffixes describe packaging, not different silicon: `CT-ND` is
DigiKey cut tape, `TR-ND` is the full tape-and-reel option, and `DKR-ND` is a
Digi-Reel. Keep `MAX5026EUT+T` as the manufacturer number in KiCad.

## Resistors

Use 0805, 1%, 100 ppm/deg C or better unless noted. Design quantity includes
both heads and the central board. Buy at least ten of each inexpensive value so
hand assembly is not stopped by a lost part.

| Value and role | Recommended part | Design qty | Buy qty | Source | Each at buy qty | Line total |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| 0 ohm current and trigger-selection links | Yageo `RC0805JR-070RL` | 3 (plus 2 DNP footprints) | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805JR-070RL/728216) | $0.019 | $0.19 |
| 10.0 ohm ADC-supply filter | Yageo `RC0805FR-0710RL` | 1 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-0710RL/727534) | $0.054 | $0.54 |
| 22.0 ohm peak charging, characterization alternate | Yageo `RC0805FR-0722RL` | 0 (2 stuffing options) | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-0722RL/727735) | $0.034 | $0.34 |
| 49.9 ohm SiPM sense | Yageo `RC0805FR-0749R9L` | 2 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-0749R9L/727984) | $0.034 | $0.34 |
| 56.0 ohm peak charging, characterization alternate | Yageo `RC0805FR-0756RL` | 0 (2 stuffing options) | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-0756RL/728032) | $0.034 | $0.34 |
| 82.0 ohm peak charging, provisional | Yageo `RC0805FR-0782RL` | 2 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-0782RL/728164) | $0.034 | $0.34 |
| 100 ohm bias filters, trigger damping, peak-output isolation, and peak-charging alternate | Yageo `RC0805FR-07100RL` | 7 (plus 2 stuffing options) | 20 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-07100RL/727543) | $0.034 | $0.68 |
| 499 ohm input bias and injection | Yageo `RC0805FR-07499RL` | 4 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-07499RL/727986) | $0.034 | $0.34 |
| 1.00 kohm gain, comparator, threshold, ADC input, and reset fanout | Yageo `RC0805FR-071KL` | 10 | 20 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-071KL/727444) | $0.034 | $0.68 |
| 1.65 kohm ADC attenuator bottom | Yageo `RC0805FR-071K65L` | 2 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-071K65L/727509) | $0.034 | $0.34 |
| 2.00 kohm baseline dividers and one-shot timing | Yageo `RC0805FR-072KL` | 4 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-072KL/730611) | $0.034 | $0.34 |
| 4.70 kohm threshold divider and JA/ADC SPI series | Yageo `RC0805FR-074K7L` | 6 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-074K7L/727929) | $0.034 | $0.34 |
| 10.0 kohm FPGA trigger pulldowns | Yageo `RC0805FR-0710KL` | 2 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-0710KL/727535) | $0.034 | $0.34 |
| 12.4 kohm gain feedback | Yageo `RC0805FR-0712K4L` | 2 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-0712K4L/727572) | $0.034 | $0.34 |
| 100 kohm shutdown, reset, and SPI default-state resistors | Yageo `RC0805FR-07100KL` | 7 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-07100KL/727544) | $0.036 | $0.36 |
| 130 kohm baseline divider | Yageo `RC0805FR-07130KL` | 2 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-07130KL/727590) | $0.034 | $0.34 |
| 330 kohm external hysteresis, DNP | Yageo `RC0805FR-07330KL` | 0 (2 footprints) | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-07330KL/727867) | $0.034 | $0.34 |
| 1 Mohm bias bleeder | Yageo `RC0805FR-071ML` | 1 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-071ML/727445) | $0.034 | $0.34 |
| 220 ohm peak charging, characterization alternate | Yageo `RC0805FR-07220RL` | 0 (2 stuffing options) | 10 | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0805FR-07220RL/730688) | $0.034 | $0.34 |
| 147 kohm boost feedback, 0.1% | Panasonic `ERA-6AEB1473V` | 1 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/panasonic-industry/ERA-6AEB1473V/3074965) | $0.070 | $0.70 |
| 6.98 kohm boost feedback, 0.1% | Panasonic `ERA-6AEB6981V` | 1 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/panasonic-industry/ERA-6AEB6981V/2025740) | $0.070 | $0.70 |

The ten purchased 10.0 ohm `RC0805FR-0710RL` resistors cover the fitted
ADC filter, two alternate SiPM-sense parts, and spares. The quantities above
also include at least five of every peak-charging value. Do not install a
different `R_CHG` or sense value on only one channel without recording it.

## Capacitors

MLCC capacitance falls under DC bias. Preserve the listed voltage rating and
case size, especially on the 27 V rail; do not substitute a smaller package
solely because its printed nominal capacitance matches.

| Value and dielectric | Recommended part | Design qty | Buy qty | Source | Each at buy qty | Line total |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| 100 nF, 50 V, X7R, 0805 | KEMET `C0805C104K5RACTU` | 15 (plus 2 for precision-reset variant) | 25 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C0805C104K5RACTU/411169) | $0.100 | $2.50 |
| 100 nF, 100 V, X7R, 0805, head bias entry | KEMET `C0805C104K1RACTU` | 2 | 5 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C0805C104K1RACTU/754748) | $0.450 | $2.25 |
| 1 uF, 16 V, X7R, 0805 | KEMET `C0805C105K4RACTU` | 6 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C0805C105K4RACTU/416047) | $0.193 | $1.93 |
| 4.7 uF, 16 V, X7R, 0805 | KEMET `C0805C475K4RACTU` | 4 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C0805C475K4RACTU/3317621) | $0.211 | $2.11 |
| 10 uF, 10 V, X7R, 1206 | KEMET `C1206C106K8RACTU` | 1 | 3 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C1206C106K8RACTU/1090842) | $1.02 | $3.06 |
| 10 uF, 10 V, X5R, 0805, head 3.3 V entry | KEMET `C0805C106K8PACTU` | 2 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C0805C106K8PACTU/1090830) | $0.115 | $1.15 |
| 1 uF, 50 V, X7R, 1206 | KEMET `C1206C105K5RACTU` | 5 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C1206C105K5RACTU/2215096) | $0.287 | $2.87 |
| 10 nF, 100 V, C0G, 0805 | KEMET `C0805C103J1GACTU` | 5 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C0805C103J1GACTU/2211703) | $0.396 | $3.96 |
| 27 pF, 50 V, C0G, 0805 | KEMET `C0805C270J5GACTU` | 2 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C0805C270J5GACTU/411113) | $0.092 | $0.92 |
| 100 pF, 50 V, C0G, 0805, hold alternate | KEMET `C0805C101J5GACTU` | 0 (2 stuffing options) | 10 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C0805C101J5GACTU/411397) | $0.106 | $1.06 |
| 220 pF, 50 V, C0G, 0805, provisional hold | KEMET `C0805C221J5GACTU` | 2 | 10 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C0805C221J5GACTU/411402) | $0.115 | $1.15 |
| 470 pF, 50 V, C0G, 0805, hold alternate | KEMET `C0805C471J5GACTU` | 0 (2 stuffing options) | 10 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C0805C471J5GACTU/411132) | $0.150 | $1.50 |
| 1 nF, 50 V, C0G, 0805, ADC reservoir/hold alternate | KEMET `C0805C102J5GACTU` | 2 (plus 2 stuffing options) | 10 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C0805C102J5GACTU/411135) | $0.095 | $0.95 |
| 2.2 pF, 50 V, C0G, 0805, DNP | KEMET `C0805C229C5GACTU` | 0 (2 footprints) | 5 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C0805C229C5GACTU/3522727) | $0.460 | $2.30 |

The TLV755 schematic must follow the selected regulator datasheet. The total
above reserves one close input and one output 1 uF capacitor for that LDO.

## Connectors and cable

Factory-crimped leads avoid buying a specialized JST XH crimp tool and a reel-
quantity contact. Insert the contacts fully, pull-test each lead, then perform a
pin-numbered continuity test on every finished cable.

| Function | Manufacturer part | Design qty | Buy qty | Source | Each at buy qty | Line total |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| 10-pin board headers, two central and two heads | JST `B10B-XH-A(LF)(SN)` | 4 | 5 | [DigiKey](https://www.digikey.com/en/products/detail/jst-sales-america-inc/B10B-XH-A/1651051) | $0.39 | $1.95 |
| 10-pin cable housings | JST `XHP-10` | 4 | 6 | [DigiKey](https://www.digikey.com/en/products/detail/jst-sales-america-inc/XHP-10/1651008) | $0.15 | $0.90 |
| 12-inch XH-to-XH 22 AWG precrimp lead | JST `ASXHSXH22K305` | 20 | 25 | [DigiKey](https://www.digikey.com/en/products/detail/jst-sales-america-inc/ASXHSXH22K305/6684932) | $0.7168 | $17.92 |
| 5 V center-positive board jack | Same Sky `PJ-102AH` | 1 | 2 | [DigiKey](https://www.digikey.com/en/products/detail/same-sky-formerly-cui-devices/PJ-102AH/408448) | $0.77 | $1.54 |
| Regulated 5 V, 1 A Class II wall adapter | Phihong `PSAC05A-050L6-R` | 1 | 1 | [DigiKey](https://www.digikey.com/en/products/detail/phihong-usa/PSAC05A-050L6-R/5418482) | $5.40 | $5.40 |
| Right-angle 2x6 Pmod header | Samtec `TSW-106-08-G-D-RA` | 1 | 2 | [DigiKey](https://www.digikey.com/en/products/detail/samtec-inc/TSW-106-08-G-D-RA/1101718) | $1.39 | $2.78 |
| 6-inch 2x6 Pmod cable with gender changer | Digilent `240-109` | 1 | 1 | [DigiKey](https://www.digikey.com/en/products/detail/digilent-inc/240-109/4090168) | $5.00 | $5.00 |
| Breakaway 2.54 mm header for inject/jumpers | Samtec `TSW-120-07-G-S` | 6 pins | 1 | [DigiKey](https://www.digikey.com/en/products/detail/samtec-inc/TSW-120-07-G-S/1101307) | $2.56 | $2.56 |
| 2.54 mm shorting shunts | Samtec `SNT-100-BK-G` | 1 | 3 | [DigiKey](https://www.digikey.com/en/products/detail/samtec-inc/SNT-100-BK-G/1756763) | $0.31 | $0.93 |

The selected adapter removes the exposed-contact and remote-end ambiguity of a
power pigtail. Before first use, verify center-positive polarity and voltage at
the board jack. Continuity-map the unkeyed Pmod cable and gender changer, label
pin 1 at both ends, and strain-relieve the central board.

Use PCB-integrated probe pads and **16 formed solid-wire ground loops**
(7 per head, 2 central); reserve about 0.5 m of suitable bare/tinned wire from
bench stock. One 20-pin breakaway strip supplies all three 2-pin headers, with
14 pins left over. Only the central bias-enable header needs a shunt; buy three
so two are spares. Twenty precrimp leads make the two cables; five are spares.

## Scintillator, optical, mechanical, and fabrication

Optical couplant updated 2026-10-02 to Silicone Solutions SS-988, sold online
with a published price. Buy one 0.4 oz tube; this is ample for two thin SiPM
interfaces. The non-curing optical silicone gel has reported refractive index
1.466 and 99.99% transmission at 400 and 450 nm through 1 cm. These properties
support selection for blue scintillator coupling; compatibility with the exact
BC-408 and SiPM package materials has not been independently qualified.
Check a small area before final assembly. Store sealed below 70 F for the
manufacturer's 545-day shelf-life guarantee. Checkout controls delivery.

| Item | Qty | Checked source or requirement | Planning cost |
|---|---:|---|---:|
| Purchased BC-408 block, 50 x 50 x 10 mm, one face polished | 2 | [Purchased listing](https://www.ebay.com/itm/254751779655); seller model `BC408-505010-1FP`, $25 each or $22.50 each at quantity two when checked. The seller describes virgin BC-408 water-saw cut from a large block; one 50 x 50 mm face is polished and the other face and sides are smooth cut. See [manufacturer BC-408 properties](https://luxiumsolutions.com/radiation-detection-scintillators/plastic-scintillators/bc400-bc404-bc408-bc412-bc416). | $45 |
| Silicone Solutions `SS-988` non-curing optical coupling gel, 0.4 oz tube | 1 | [Manufacturer online checkout](https://siliconesolutions.com/ss-988.html), checked 2026-10-02 | $44.08 |
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

## Lead-free solder paste for the T-962

Buy **one Chip Quik `SMDLTLFP` 15 g / 5 cc syringe**, DigiKey
`SMDLTLFP-ND`: **$15.95** ([DigiKey](https://www.digikey.com/en/products/detail/chip-quik-inc/SMDLTLFP/2682721)).
This is Sn42/Bi57.6/Ag0.4 low-temperature, no-clean, T3 solder paste, melting at
138 deg C. The manufacturer's current profile peaks at about **165 deg C**.
That lower process temperature is a practical starting point for this small
stationary prototype and the T-962, subject to a measured board profile; it is
not proof that an arbitrary factory oven preset is suitable. One syringe is
ample for three small assemblies and practice; buy it near assembly time.

Use the [current Chip Quik technical sheet](https://www.chipquik.com/datasheets/SMDLTLFP.pdf)
and the assembly process in [build-and-debug.md](build-and-debug.md#reflow-and-cleaning).
Store at 3-8 deg C, do not freeze, and allow four hours to reach room temperature
before opening/use. Keep solder materials lead-free throughout; do not mix this
bismuth paste with leaded solder. Retain the designed mechanical supports and
cable strain relief. Through-hole connectors and trimmers are hand-soldered
using existing lead-free wire after oven work, not reflowed with the SMT parts.

## Revised cost

These totals include **all numeric Buy qty entries**, including inexpensive
DNP debugging parts and the characterization matrix. Optional TMUX switches
and a third SiPM are excluded. No electronics are assumed already purchased.

| Category | Recommended order subtotal |
|---|---:|
| Active/power parts and trimmers, including spares | $111.15 |
| Resistors, including stuffing/debug options | $8.81 |
| Capacitors, including stuffing/debug options | $29.61 |
| Adapter, connectors, cables, headers and shunts | $38.98 |
| One syringe lead-free paste | $16.95 |
| **DigiKey merchandise estimate** | **$206.38** |
| SS-988 ($44.08) and wrapping allowance ($10) | $54.08 |
| Frame and fasteners, retained allowance | $10-25 |
| PCB fabrication, retained allowance | $35-55 |
| Optional stencil, separate allowance | $0-15 |
| **Remaining purchases before shipping/tax/tariffs** | **$305.46-$355.46** |
| Already-purchased scintillators, historical listing cost | $45.00 |
| **Whole-project parts cost including scintillators** | **$350.46-$400.46** |

The non-DigiKey rows remain planning allowances, not fresh supplier quotes.
The oven, Cora, instruments, cleaning/profiling equipment, and bench wire are
owned/tooling assumptions and are excluded. If a board thermocouple/logger is
not available, borrow one or budget it separately before reflow. Do not add the
already-purchased scintillators to the remaining order. A third SiPM adds
$24.25; the three-switch precision-reset trial adds $5.73. Delivery charges
require checkout, especially for paste and the factory-stock header strip.

## Release-time reconciliation

Before ordering:

1. Export the BOM from both reviewed KiCad schematics.
2. Compare every reference, value, footprint, DNP state, and quantity with this
   document and resolve differences deliberately.
3. Recheck every link and manufacturer datasheet; reject brokered or ambiguous
   substitutions for the SiPM, boost, amplifier, comparator, and LDO.
4. Use the explicit Buy qty column (assembly margin is already included);
   decide separately whether to add the optional third SiPM or precision resets.
5. Save the distributor quotes or order confirmation with the build record, not
   as a replacement for manufacturer part numbers in KiCad.
