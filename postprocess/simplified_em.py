#!/usr/bin/env python3

import json
import csv
import sys
import re
import statistics

with open(sys.argv[1], "r") as f:
    json_data = json.loads(f.read())

cpus_data = json_data["cpus"]

voltages = {}
for arg in sys.argv[2:]:
    cluster, freq, voltage = map(int, re.split(r"\.|=", arg))
    voltages[(cluster, freq)] = voltage

for cpu, cpu_data in cpus_data.items():
    cpu = int(cpu)

    dpcs = []
    for freq, freq_data in cpu_data["freqs"].items():
        freq = int(freq)

        uw = freq_data["active"]["power_mean"] * 1000
        mhz = freq / 1000
        v = voltages[(cpu, freq)] / 1_000_000

        dpc = uw / mhz / v**2
        dpcs.append(dpc)

    print(f"cpu{cpu} = {statistics.mean(dpcs)}")
