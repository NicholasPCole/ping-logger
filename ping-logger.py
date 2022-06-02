#!/usr/bin/env python3

import argparse
import influxdb
import re
import shutil
import statistics
import subprocess
import time
from xdg import XDG_CONFIG_HOME
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

        point_dict = {
            "time": time.strftime('%Y-%m-%dT%H:%M:%SZ', start_timestamp),
            "measurement": "ping",
            "tags": {
                "src": config['src_host_name'],
                "dest": host
            }
        }

        if len(pings) == 0:
            point_dict['fields'] = {
                "loss": 1.0
            }
        else:
            point_dict['fields'] = {
                "avg": round(statistics.mean(pings), 2),
                "sd": round(statistics.pstdev(pings), 2),
                "loss": round(responses.count("-") / config['ping_count'], 2)
            }

        points.append(point_dict)

    client = influxdb.InfluxDBClient(**config['influxdb'])
    client.write_points(points, time_precision='s')


# Load the configuration.

parser = argparse.ArgumentParser(
    description='Ping a list of servers and record performance data')
parser.add_argument('-c', '--config',
                    default=str(XDG_CONFIG_HOME) + '/ping-logger/config.yaml',
                    help=('Configuration file (default is '
                          '$XDG_CONFIG_HOME/ping-logger/config.py)'))
arguments = parser.parse_args()
config = yaml.safe_load(open(arguments.config))
concatenated_hosts = '\n'.join(config['dest_hosts'])

# Now run the test!

start_timestamp = time.gmtime()
fping_run = subprocess.run([shutil.which('fping'), '-C',
                           str(config['ping_count']), '-q', '-R'],
                           input=concatenated_hosts, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, universal_newlines=True)
fping_output_lines = fping_run.stdout.splitlines()
post_to_influxdb()
