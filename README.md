# Ping logger

This script pings a given list of hosts with `fping` and reports the measurements (mean, standard deviation, and packet loss) to an InfluxDB server, ideal for display in Grafana.

## Requirements

* Python 3: `argparse`,  `influxdb`, `re`, `shutil`, `statistics`, `subprocess`, `time`, `xdg`, and `yaml` modules.
* [fping](https://fping.org/) package to run ping
* InfluxDB server to receive and store data
* (optional) Grafana installation to graph data

## Setup

### Configuration file

A YAML file is used to store connection details for the InfluxDB server as well as what servers to monitor with `fping`. A sample default file is provided in this repository and should be copied and modified for your environment.

The file at `$XDG_CONFIG_HOME/ping-logger/config.yaml` is used by default but a different file can be specified with the `-c` or `--config` argument.

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
