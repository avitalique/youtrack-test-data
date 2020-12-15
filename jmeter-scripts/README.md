# JMeter script for YouTrack test data
JMeter script for YouTrack test data manipulation:

* populate YouTrack with pre-generated test dataset
* clean up created test data

## Requirements
Apache JMeter 5.0+

Requires `InfluxBackendListenerClient`

## Running

To run the script, use `.sh` (for Unix) or `.bat` (for Windows) files:

* `run-jmeter.sh`: run script in JMeter CLI mode
* `start-jmeter-GUI.sh`: start JMeter in GUI mode (for development/debug purposes)

```
Usage: run-jmeter.sh {create|delete} [CREATED_DATASET_PREFIX]
```

### Create test data
To populate a YouTrack instance with test data, run the command:

```
$ run-jmeter.sh create
```

### Deleted created data
To clean up test data previously created with this script, run the command:

```
$ run-jmeter.sh delete CREATED_DATASET_PREFIX
```

Example:

```
$ run-jmeter.sh delete YT_20201214-2028
```

### Running in background
To run script in background use `nohup`, e.g.

```
$ nohup ./run-jmeter.sh create > console.log 2>&1 &

$ nohup ./run-jmeter.sh delete YT_20201214-2028 > console.log 2>&1 &
```

## Configuration
The script depends on JMeter properties to be provided in `YT_TestData.properties` file and with JMETER_ARGS in `run-jmeter.sh`
