# DigiPy
DigiPy automatically looks up the cheapest parts on Digikey and writes them to
a CSV file. I think it's best explained by example:

## Example
```python
from digipy import DigiPy

DigiPy = DigiPy() #Initialize DigiPy
DigiPy.update()   #Update part information

# Our parts that we want to find
# The syntax is
#     [(PartType, PartFilters, Quantity, PickCheapest), ... ]
parts = [
    ("SMDResistor", {"Resistance (Ohms)": ["1k"], "Package / Case": "0603 (1608 Metric)"}, 2, True),
    ("SMDResistor", {"Resistance (Ohms)": ["5k"], "Package / Case": "0603 (1608 Metric)"}, 8, True),
    ("SMDResistor", {"Resistance (Ohms)": ["2.2k"], "Package / Case": "0603 (1608 Metric)"}, 1, True),
    ("THResistor", {"Resistance (Ohms)": ["500"]}, 10, True),
    ("CeramicCapacitor", {"Capacitance": ["1pF"], "Package / Case": "0603 (1608 Metric)"}, 47, True),
    ("CeramicCapacitor", {"Capacitance": ["10uF"], "Package / Case": "0603 (1608 Metric)"}, 123, True)
]

# Open CSVFile for writing
DigiPy.openCSV()
for part in parts:  # Iterate over our parts, looking each on :e up
    partInformation = DigiPy.getPart(part) # Get part information
    DigiPy.writeToCSV(partInformation)     # Write to CSV file
DigiPy.closeCSV() # Close CSV
```
### Output
| Part Number        |       Price      |Tolerance |Value | Package            |
|--------------------|------------------|----------|------|--------------------|
| 311-1.0KGRCT-ND    | 0.10000 @ qty2   | +/-5%    | 1k   | 0603 (1608 Metric) |
| PNM0603-5.0KBCT-ND | 2.93000 @ qty8   | +/-0.1%  | 5k   | 0603 (1608 Metric) |
| 311-2.20KHRCT-ND   | 0.10000 @ qty1   | +/-1%    | 2.2k | 0603 (1608 Metric) |
| 53J500E-ND         | 0.43100 @ qty10  | +/-5%    | 500  | Axial              |
| 1276-1095-1-ND     | 0.02640 @ qty47  | +/-0.1pF | 1pF  | 0603 (1608 Metric) |
| 490-3298-1-ND      | 0.04420 @ qty123 | +/-20%   | 10uF | 0603 (1608 Metric) |
#### Raw Output
```
311-1.0KGRCT-ND,0.10000 @ qty2,+/-5%,1k,0603 (1608 Metric)
PNM0603-5.0KBCT-ND,2.93000 @ qty8,+/-0.1%,5k,0603 (1608 Metric)
311-2.20KHRCT-ND,0.10000 @ qty1,+/-1%,2.2k,0603 (1608 Metric)
53J500E-ND,0.43100 @ qty10,+/-5%,500,Axial
1276-1095-1-ND,0.02640 @ qty47,+/-0.1pF,1pF,0603 (1608 Metric)
490-3298-1-ND,0.04420 @ qty123,+/-20%,10uF,0603 (1608 Metric)
```
## Features
#### Translations
The "parts" catalog is very small right now, and probably will be expanded in
the future. Right now, it looks like this:

```python
self.catalog = {'SMDResistor': 'resistors/chip-resistor-surface-mount/65769',
                'THResistor': 'resistors/through-hole-resistors/66690',
                'CeramicCapacitor': 'capacitors/ceramic-capacitors/131083'}

self.translateGuide = {1: 'SMDResistor',
                       2: 'THResistor',
                       3: 'CeramicCapacitor'}
```

Adding to it is easy, just navigate to Digikey like normal, and extract this part from the URL.

> www.digikey.com/product-search/en/**resistors/chip-resistor-surface-mount/65769**

In the future, this might be automated, but you're stuck with your own wits for now.

## Installation

1. Download/Clone the code and place digipy.py in the same directory as your code.
2. Install [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup) if you havn't already :stew:
3. Party 'cause you're done :tada:

## Note

This was made to solve a specific problem. Please don't expect much more development.
Moreover, don't treat this as good code, as it's at least 10% hotfix. :collision:

<center>:rocket:</center>
