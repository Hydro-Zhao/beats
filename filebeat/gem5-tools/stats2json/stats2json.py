#!/usr/bin/python3

import csv
import json

stats = {}

with open('stats.txt', newline='') as csvfile:
    #spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    # TODO: read every line of the file, and split by ' ', then the follows are the same
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
