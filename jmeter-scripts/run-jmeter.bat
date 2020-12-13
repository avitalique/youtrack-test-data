@echo off
@rem Get timestamp
for /f %%a in ('WMIC OS GET LocalDateTime ^| find "."') do set DTS=%%a

@rem Verify CLI arguments
if %1.==. goto PrintUsage
if not %1==create if not %1==delete goto InvalidCommand
if %1==delete if %2.==. goto MissingArgument

@rem Set params
set JMETER_HOME=c:\apache-jmeter-5.4
set BASE_DIR=%CD%
set INPUT_DATA_DIR=%BASE_DIR%\input-data
set OUTPUT_DATA_DIR=%BASE_DIR%\created-data

set PROJECT_ID=YT
set RUN_ID=%PROJECT_ID%_%DTS:~0,8%-%DTS:~8,4%
set RUN_TYPE=%1

set IS_CREATE=false
if %1==create set IS_CREATE=true

set IS_DELETE=false
if %1==delete set IS_DELETE=true

set CREATED_DATASET_PREFIX=%2_
if %2.==. set CREATED_DATASET_PREFIX=%RUN_ID%_

@rem Set JMETER_ARGS
set JMETER_ARGS=-n
set JMETER_ARGS=%JMETER_ARGS% -p %BASE_DIR%\YT_TestData.properties
set JMETER_ARGS=%JMETER_ARGS% -t %BASE_DIR%\YT_TestData.jmx
set JMETER_ARGS=%JMETER_ARGS% -j %OUTPUT_DATA_DIR%\%RUN_ID%_jmeter.log
set JMETER_ARGS=%JMETER_ARGS% -Jyt.create=%IS_CREATE%
set JMETER_ARGS=%JMETER_ARGS% -Jyt.delete=%IS_DELETE%
set JMETER_ARGS=%JMETER_ARGS% -Jyt.project_id=%PROJECT_ID%
set JMETER_ARGS=%JMETER_ARGS% -Jyt.run.id=%RUN_ID%
set JMETER_ARGS=%JMETER_ARGS% -Jyt.run.type=%RUN_TYPE%
set JMETER_ARGS=%JMETER_ARGS% -Jyt.path.dataset.projects=%INPUT_DATA_DIR%\projects_json-strings.csv
set JMETER_ARGS=%JMETER_ARGS% -Jyt.path.dataset.users=%INPUT_DATA_DIR%\users_json-strings.csv
set JMETER_ARGS=%JMETER_ARGS% -Jyt.path.dataset.issues=%INPUT_DATA_DIR%\issues_json-strings.csv
set JMETER_ARGS=%JMETER_ARGS% -Jyt.path.output_dir=%OUTPUT_DATA_DIR%
set JMETER_ARGS=%JMETER_ARGS% -Jyt.path.dataset.created_projects=%OUTPUT_DATA_DIR%\%CREATED_DATASET_PREFIX%created_projects.csv
set JMETER_ARGS=%JMETER_ARGS% -Jyt.path.dataset.created_users=%OUTPUT_DATA_DIR%\%CREATED_DATASET_PREFIX%created_users.csv
set JMETER_ARGS=%JMETER_ARGS% -Jyt.path.dataset.created_issues=%OUTPUT_DATA_DIR%\%CREATED_DATASET_PREFIX%created_issues.csv
set JMETER_ARGS=%JMETER_ARGS% -Jyt.path.dataset.created_links=%OUTPUT_DATA_DIR%\%CREATED_DATASET_PREFIX%issue_links.csv

@rem Create output dir if not exists
if not exist "%OUTPUT_DATA_DIR%" mkdir "%OUTPUT_DATA_DIR%"

@rem Start JMeter
cd %JMETER_HOME%
set HEAP=-Xms1g -Xmx4g -XX:MaxMetaspaceSize=256m
set VERBOSE_GC=-verbose:gc ^
		-Xloggc:%OUTPUT_DATA_DIR%\%RUN_ID%_gc_jmeter_%%p.log ^
		-XX:+PrintGCDetails -XX:+PrintGCCause -XX:+PrintTenuringDistribution ^
		-XX:+PrintHeapAtGC -XX:+PrintGCApplicationConcurrentTime ^
		-XX:+PrintGCApplicationStoppedTime ^
		-XX:+PrintGCDateStamps ^
		-XX:+PrintAdaptiveSizePolicy

%JMETER_HOME%\bin\jmeter.bat %JMETER_ARGS%
goto End

:InvalidCommand
echo Invalid argument: %1
goto PrintUsage

:MissingArgument
echo Missing argument CREATED_DATASET_PREFIX
goto PrintUsage

:PrintUsage
echo "Usage: run-jmeter.bat {create|delete} [CREATED_DATASET_PREFIX]"
echo.
echo 	run-jmeter.bat create
echo		run-jmeter.bat delete YT_20201212-1249
echo.
pause

:End
