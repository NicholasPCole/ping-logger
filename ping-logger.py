#!/usr/bin/env python3

import influxdb
import os
import re
import shutil
import statistics
import subprocess
import time
import yaml


def post_to_influxdb():
    """Formats fping output and posts it to an InfluxDB server."""

    points = []

    # An example fping output line looks like this:
    #
    # example.com : 3.56 1.88 - - - 1.18 1.28 1.39 4.67 1.27
    for line in fping_output_lines:
        host = re.split(' +: +', line)[0]
        responses = re.split(' +: +', line)[1].split(' ')
        pings = [float(response) for response in responses if response != '-']

        if len(pings) == 0:
            continue

        points.append({
            "time": time.strftime('%Y-%m-%dT%H:%M:%SZ', start_timestamp),
            "measurement": "ping",
            "tags": {
                "src": config['src_host_name'],
                "dest": host
            },
            "fields": {
                "avg": round(statistics.mean(pings), 2),
                "sd": round(statistics.pstdev(pings), 2),
                "loss": round(responses.count("-") / config['ping_count'], 2)
            }
        })

    client = influxdb.InfluxDBClient(**config['influxdb'])
    client.write_points(points, time_precision='s')


# Load the configuration.

config = yaml.safe_load(open(os.getenv('HOME')
                             + '/.config/ping-logger/config.yaml'))
concatenated_hosts = '\n'.join(config['dest_hosts'])

# Now run the test!

start_timestamp = time.gmtime()
fping_run = subprocess.run([shutil.which('fping'), '-C',
                           str(config['ping_count']), '-q', '-R'],
                           input=concatenated_hosts, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, universal_newlines=True)
fping_output_lines = fping_run.stdout.splitlines()
post_to_influxdb()
