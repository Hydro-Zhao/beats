#!/usr/bin/python3

import csv
import json

stats = {}

with open('stats.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        name = row[0]
        row.remove(name)
        if len(row) > 1:
            stats[name] = row
        else:
            stats[name] = row[0]

print(json.dumps(stats, indent=1))
with open('stats.json', 'w') as fp:
    json.dump(stats, fp)
