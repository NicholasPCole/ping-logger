# Ping logger

This script pings a given list of hosts with `fping` and reports the measurements (minimum, mean, maximum, standard deviation) to an InfluxDB server, ideal for display in Grafana.

## Requirements

* Python 3: `os`, `requests`, `shutils`, `statistics`, `subprocess`, `time`, and `yaml` modules.
* [fping](https://fping.org/) package to run ping
* InfluxDB server to receive and store data
* (optional) Grafana installation to graph data

## Setup

### Configuration file

Copy `config.yaml.default` to `~/.config/ping-logger/config.yaml` and fill in each of the settings in the new file.

All settings are required, and some examples are given for `influxdb_connection['server']` and `dest_hosts` to demonstrate the input format.

### Cron job

The schedule can, of course, be modified. To run the script every minute, for example:

```
* * * * * /home/nicholas/ping-logger.py
```
