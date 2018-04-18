#!/usr/bin/python3

import requests
import shutil
import statistics
import subprocess
import time

# Configure fping.

ping_count = 10

target_host_list = [
    'example.com',
    'example.net',
    'example.org',
    'FILL_IN_THIS_VALUE'
]
concatenated_hosts = '\n'.join(target_host_list)

# Configure InfluxDB.

this_host_name = 'FILL_IN_THIS_VALUE'
timestamp = int(time.time())

influxdb_connection = {
    'server': 'https://FILL_IN_THIS_VALUE:8086',
    'database': 'FILL_IN_THIS_VALUE',
    'username': 'FILL_IN_THIS_VALUE',
    'password': 'FILL_IN_THIS_VALUE'
}

# Define functions.

def convert_to_point(line):
    host = line.split(':')[0].rstrip()

    pings = line.split(':')[1].lstrip().split(' ')
    pings = [float(ping) for ping in pings if ping != '-']

    if len(pings) == 0:
        return

    minimum = min(pings)
    average = "{0:.2f}".format(statistics.mean(pings))
    maximum = max(pings)
    standard_deviation = "{0:.2f}".format(statistics.pstdev(pings))
    tags = [
        'ping',
        'origin=' + this_host_name,
        'host=' + host
    ]
    fields = [
        'min=' + str(minimum),
        'avg=' + str(average),
        'max=' + str(maximum),
        'sd=' + str(standard_deviation)
    ]

    return(','.join(tags) + ' ' + ','.join(fields) + ' ' + str(timestamp))

# Now run the test!

fping_run = subprocess.run([shutil.which('fping'), '-C', str(ping_count), '-q', '-R'], input=concatenated_hosts, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
fping_output_lines = fping_run.stdout.splitlines()
points = []

for line in fping_output_lines:
    point = convert_to_point(line)

    if point is not None:
        points.append(point)

# Post the results to InfluxDB.

influxdb_post = requests.post(
    influxdb_connection['server'] + '/write?db=' + influxdb_connection['database'] + '&precision=s',
    auth = (influxdb_connection['username'], influxdb_connection['password']),
    data = '\n'.join(points)
)
