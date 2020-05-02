import csv
import collections
from datetime import datetime

input_columns = collections.defaultdict(list)
output_columns = ['Incydent', 'Data_otwarcia', 'Termin_Realizacji', 'Czas_Realizacji']

inputCsv = 'zgloszenia.csv'
outputCsv = 'zgloszenia_wynik.csv'
reports = []

# Report model

class Report:

    datetime_pattern = '%d.%m.%Y %H:%M'

    def __init__(self, id, do, tr):
        self.id = id
        self.do = do
        self.tr = tr

    def calculate_diff(self):
        doDate = datetime.strptime(self.do, self.datetime_pattern)
        trDate = datetime.strptime(self.tr, self.datetime_pattern)
        return trDate - doDate

# Open

with open(inputCsv, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    dictReader = csv.DictReader(csvfile, delimiter=';')
    for row in dictReader:
        for (k,v) in row.items():
            input_columns[k].append(v)

columnIds = input_columns['# Incydentu']
columnDOs = input_columns['Data Otwarcia']
columnTRs = input_columns['Termin realizacji']

for i, item in enumerate(columnIds, start = 0):
    reports.append(Report(item, columnDOs[i], columnTRs[i]))

sortedReports = sorted(reports, key = lambda report: report.calculate_diff())

# Save

with open(outputCsv, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(output_columns)
    for report in sortedReports:
        writer.writerow([
            report.id,
            report.do,
            report.tr,
            str(report.calculate_diff())
        ])
