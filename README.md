# Ping logger

This script pings a given list of hosts with `fping` and reports the measurements (minimum, mean, maximum, standard deviation) to an InfluxDB server, ideal for display in Grafana.

## Requirements

* Python 3
  * `requests` module
  * `statistics` module
  * `subprocess` module
  * `time` module
* [fping](https://fping.org/) package to run ping
* InfluxDB server to receive and store data
* (optional) Grafana installation to graph data

## Setup

### Script variables

1. Set the list of hosts to be monitored in the `target_host_list` variable. It is a string list.
2. Set the name of the host conducting the monitoring in `this_host_name`. This is useful if you want to run the script from multiple locations and identify the hosts that are reporting data.
3. Configure the InfluxDB host, database, and credentials with the `influxdb_connection` dictionary.

In short, where you see `FILL_IN_THIS_VALUE` is where you need to configure the values for your specific environment.

### Cron job

The schedule can, of course, be modified. To run the script every minute, for example:

```
* * * * * /home/nicholas/ping-logger.py
```

