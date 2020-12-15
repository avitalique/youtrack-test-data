# youtrack-test-data
A set of utilities to generate, populate, and clean-up [YouTrack](https://www.jetbrains.com/youtrack/) test data for performance testing purposes.

## Contents

Subdirectory                | Description
----------------------------| -----------
`youtrack-datagen`          | Command line utility to generate randomized test dataset
`jmeter-scripts`            | JMeter script to populate/clean up test data
`jmeter-backend-listener`   | Backend Listener for sending JMeter results to InfluxDB
`grafana-dashboards`        | Grafana dashboards for results visualization

## Documentation

* [youtrack-datagen](youtrack-datagen/README.md) - YouTrack Test Data Generator
* [JMeter script](jmeter-scripts/README.md)