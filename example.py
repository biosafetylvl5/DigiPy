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