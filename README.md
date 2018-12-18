# Ping logger

This script pings a given list of hosts with `fping` and reports the measurements (mean, standard deviation, and packet loss) to an InfluxDB server, ideal for display in Grafana.

## Requirements

* Python 3: `influxdb`, `os`, `re`, `shutil`, `statistics`, `subprocess`, `time`, and `yaml` modules.
* [fping](https://fping.org/) package to run ping
* InfluxDB server to receive and store data
* (optional) Grafana installation to graph data

## Setup

### Configuration file

Copy `config.yaml.default` to `~/.config/ping-logger/config.yaml` and fill in the appropriate settings in the new file.

The InfluxDB settings are defined in the [InfluxDBClient documentation](https://influxdb-python.readthedocs.io/en/latest/api-documentation.html#influxdbclient) and passed through as keyword arguments, and some examples are given for `influxdb['host']` and `dest_hosts` to demonstrate the input format. `src_host_name` is used to help identify multiple running instances of the script on different servers.

### Cron job

The schedule can, of course, be modified. To run the script every minute, for example:

```
* * * * * /home/nicholas/ping-logger.py
```

### InfluxDB schema

The following schema is used:

* Database name: defined in `config.yaml`
* Measurement name: `ping`
* Tag keys: `src`, `dest`
* Field keys: `avg`, `sd`, `loss`
