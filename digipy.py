# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import csv
import os

reload(sys)
sys.setdefaultencoding('utf-8')  # Not exactly the right way to handle things, but it works.


class DigiPy:
    class Parts:
        def __init__(self):
            self.parts = []
            self.catalog = {'SMDResistor': 'resistors/chip-resistor-surface-mount/65769',
                            'THResistor': 'resistors/through-hole-resistors/66690',
                            'CeramicCapacitor': 'capacitors/ceramic-capacitors/131083'}
            self.translateGuide = {1: 'SMDResistor',
                                   2: 'THResistor',
                                   3: 'CeramicCapacitor'}

        class Part:
            def __init__(self, name):
                self.name = name
                self.Filters = []

        class Filter:
            def __init__(self, header):
                self.header = header
                self.options = {}
                self.list = []
                self.key = ""

        pass

    class InvalidPart(Exception):
        def __init__(self, *args, **kwargs):
            Exception.__init__(self, *args, **kwargs)

    def checkInput(self, inputs):
        for input in inputs:
            if input == None:
                return False
        return True

    def listParts(self):
        for category in self.Parts.catalog:
            print category
        return

    def update(self, part=None):
        if not self.checkInput([part]):
            for i in range(1, len(self.Parts.translateGuide)+1):
                part = d.translate(i)
                d.update(part)
        else:
            self.download(part)

    def download(self, part):
        self.Parts.parts.append(self.Parts.Part(part))
        Part = self.Parts.parts[-1]
        r = requests.get('http://www.digikey.com/product-search/en/' + self.Parts.catalog[part] + '?pageSize=1')
        s = BeautifulSoup(r.content, 'html.parser')
        headers = s.find_all('th')
        keys = []
        for select in s.find_all('select', class_='filter-selectors'):
            keys.append(select['name'])
        results = s.find_all('tr', id='appliedFilterOptions')[0].find_all('td', class_='ptable-param')
        i = 0

        for result in results:
            f = self.Parts.Filter(headers[i].string)
            f.key = keys[i]
            i += 1
            for option in result.find_all('option'):
                optionString = option.string.replace('\n                                                        ',
                                                     '').replace(
                    '\n                                                    ', '').replace('µ', 'u')
                f.options[optionString] = option['value']
                f.list.append(optionString)
            Part.Filters.append(f)

    def getPartInstance(self, partName):
        for part in self.Parts.parts:
            if part.name == partName:
                return part
        print "Updating ..."
        self.update(partName)
        for part in self.Parts.parts:
            if part.name == partName:
                return part
        print "Please update " + partName + ", no instance found"
        raise self.InvalidPart

    def getCategories(self, inputPart=None, pOut=False):
        Part = self.getPartInstance(inputPart)
        if pOut:
            print "Categories in " + Part.name + ":"
        i = 0
        categories = {}
        for filter in Part.Filters:
            i += 1
            if pOut:
                print str(i) + "\t:\t" + filter.header
            categories[i] = filter.header
        return categories

    def getOptions(self, inputPart=None, inputFilter=None, pOut=False):
        if not self.checkInput([inputPart]):
            self.listParts()
            return
        Part = self.getPartInstance(inputPart)
        options = {}
        for filter in Part.Filters:
            if filter.header == inputFilter:
                for i in range(0, len(filter.list)):
                    if pOut:
                        print str(i + 1) + "\t:\t" + filter.list[i]
                    options[i + 1] = filter.list[i]
            elif inputFilter == None:
                for i in range(0, len(filter.list)):
                    if pOut:
                        print str(i + 1) + "\t:\t" + filter.list[i]
                    options[i + 1] = filter.list[i]
        return options

    def getPart(self, partType=None, filterOptions=None, quantity=1, cheapest=False):
        if(type(partType)==tuple):
            cheapest = partType[3]
            quantity = partType[2]
            filterOptions = partType[1]
            partType = partType[0]
        print partType
        Part = self.getPartInstance(partType)
        for filter in Part.Filters:
            for inputFilter in filterOptions:
                if filter.header == inputFilter:
                    for i in range(0, len(filter.list)):
                        for option in filterOptions[filter.header]:
                            if filter.list[i] == option:
                                url = "http://www.digikey.com/product-search/en/" + self.Parts.catalog[Part.name] + \
                                      "?" + filter.key + "=" + filter.options[filter.list[i]]
                                if cheapest:
                                    url += "&ColumnSort=1000011&pageSize=1&quantity=" + str(quantity)
                                r = requests.get(url)
                                s = BeautifulSoup(r.content, 'html.parser')
                                partPN = s.find_all("td", class_="tr-dkPartNumber")[0].find("a").string
                                if "CeramicCapacitor" == partType:
                                    partValue = s.find_all("td", class_="13")[0].get_text().replace('\n', '').replace(
                                        ' ', '').replace('µ', 'u')
                                elif ("SMDResistor" == partType) or ("THResistor" == partType):
                                    partValue = s.find_all("td", class_="1")[0].get_text().replace('\n', '').replace(
                                        ' ', '').replace('±', '+/-')
                                partPackage = s.find_all("td", class_="16")[0].get_text().replace('\n', '').replace(
                                    '  ',
                                    '')
                                partTolerance = s.find_all("td", class_="3")[0].get_text().replace('\n', '').replace(
                                    '  ', '').replace('µ', 'u').replace('±', '+/-')
                                price = s.find_all("td", class_="tr-unitPrice")[0].get_text().replace('\n', '').replace(
                                    ' ', '').replace('@', ' @ ')

                                return {"SKU": str(partPN), "Price": str(price), "Value": str(partValue),
                                        "Package / Case": str(partPackage), "Tolerance": str(partTolerance)}

    def translate(self, number=None):
        if self.checkInput([number]):
            return self.Parts.translateGuide[number]
        else:
            for num in self.Parts.translateGuide:
                print str(num) + ":\t" + self.Parts.translateGuide[num]

    def translateCategories(self, inputPart, catNum):
        categories = self.getCategories(inputPart)
        return categories[catNum]

    def tC(self, inputPart, catNum):
        return self.translateCategories(inputPart, catNum)

    def translateOptions(self, inputPart, inputCategory, catNum):
        options = d.getOptions(inputPart, inputCategory)
        return options[catNum]

    def tO(self, inputPart, inputCategory, catNum):
        return self.translateOptions(inputPart, inputCategory, catNum)

    def openCSV(self, fileName="BOM.csv"):
        self.csvfile = open(fileName, 'wb')

    def closeCSV(self):
        self.csvfile.close()

    def writeToCSV(self, part):
        f = csv.writer(self.csvfile)
        row = ()
        for value in part:
            row += (part[value],)
        f.writerow(row)

    def __init__(self):
        self.version = 0.1
        self.author = "Michael Uttmark"
        self.Parts = self.Parts()


d = DigiPy()
d.update()

parts = [
    ("SMDResistor", {"Resistance (Ohms)": ["1k"], d.tC(d.translate(1), 11): "0603 (1608 Metric)"}, 2, True),
    ("SMDResistor", {"Resistance (Ohms)": ["5k"], d.tC(d.translate(1), 11): "0603 (1608 Metric)"}, 8, True),
    ("SMDResistor", {"Resistance (Ohms)": ["2.2k"], d.tC(d.translate(1), 11): "0603 (1608 Metric)"}, 1, True),
    ("THResistor", {"Resistance (Ohms)": ["500"]}, 10, True),
    ("CeramicCapacitor", {"Capacitance": ["1pF"], "Package / Case": "0603 (1608 Metric)"}, 47, True),
    ("CeramicCapacitor", {"Capacitance": ["10uF"], "Package / Case": "0603 (1608 Metric)"}, 123, True)
]

d.openCSV()
for part in parts:
    p = d.getPart(part)
    d.writeToCSV(p)
d.closeCSV()
