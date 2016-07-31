from digipy import DigiPy

d = DigiPy()
d.update()
d.getCategories("SMDResistor", True)
d.getOptions("SMDResistor", "Package / Case", True)

parts = [
    ("SMDResistor", {"Resistance (Ohms)": ["1k"], "Package / Case": "0603 (1608 Metric)"}, 2, True),
    ("SMDResistor", {"Resistance (Ohms)": ["5k"], "Package / Case": "0603 (1608 Metric)"}, 8, True),
    ("SMDResistor", {"Resistance (Ohms)": ["2.2k"], "Package / Case": "0603 (1608 Metric)"}, 1, True),
    ("THResistor", {"Resistance (Ohms)": ["500"]}, 10, True),
    ("CeramicCapacitor", {"Capacitance": ["1pF"], "Package / Case": "0603 (1608 Metric)"}, 47, True),
    ("CeramicCapacitor", {"Capacitance": ["10uF"], "Package / Case": "0603 (1608 Metric)"}, 123, True)
]

d.openCSV()
for part in parts:
    p = d.getPart(part)
    d.writeToCSV(p)
d.closeCSV()