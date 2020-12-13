#! /bin/sh

print_usage() {
  usage="Usage: run-jmeter.sh {create|delete} [CREATED_DATASET_PREFIX]

    run-jmeter.sh create
    run-jmeter.sh delete YT_20201212-1249
  "
  echo "$usage"
  exit
}

# Verify CLI arguments
if [ $# -eq 0 ]; then
  print_usage
fi

if [[ "$1" != "create" && "$1" != "delete" ]]; then
  echo "Invalid argument: $1"
  print_usage
fi

if [[ "$1" == "delete" && -z "$2" ]]; then
  echo "Missing argument CREATED_DATASET_PREFIX"
  print_usage
fi

# Set params
JMETER_HOME=~/jmeter
BASE_DIR="$(pwd)"
INPUT_DATA_DIR="${BASE_DIR}/input-data"
OUTPUT_DATA_DIR="${BASE_DIR}/created-data"

PROJECT_ID=YT
RUN_ID="${PROJECT_ID}_$(date +"%Y%m%d-%H%M")"
RUN_TYPE=$1

if [ "$1" = "create" ]; then
  IS_CREATE=true
else
  IS_CREATE=false
fi

if [ "$1" = "delete" ]; then
  IS_DELETE=true
else
  IS_DELETE=false
fi

if [ -z "$2" ]; then
  CREATED_DATASET_PREFIX="${RUN_ID}_"
else
  CREATED_DATASET_PREFIX="$2_"
fi

# Set JMETER_ARGS
JMETER_ARGS="-n"
JMETER_ARGS="${JMETER_ARGS} -p ${BASE_DIR}/YT_TestData.properties"
JMETER_ARGS="${JMETER_ARGS} -t ${BASE_DIR}/YT_TestData.jmx"
JMETER_ARGS="${JMETER_ARGS} -j ${OUTPUT_DATA_DIR}/${RUN_ID}_jmeter.log"
JMETER_ARGS="${JMETER_ARGS} -Jyt.create=${IS_CREATE}"
JMETER_ARGS="${JMETER_ARGS} -Jyt.delete=${IS_DELETE}"
JMETER_ARGS="${JMETER_ARGS} -Jyt.project_id=${PROJECT_ID}"
JMETER_ARGS="${JMETER_ARGS} -Jyt.run.id=${RUN_ID}"
JMETER_ARGS="${JMETER_ARGS} -Jyt.run.type=${RUN_TYPE}"
JMETER_ARGS="${JMETER_ARGS} -Jyt.path.dataset.projects=${INPUT_DATA_DIR}/projects_json-strings.csv"
JMETER_ARGS="${JMETER_ARGS} -Jyt.path.dataset.users=${INPUT_DATA_DIR}/users_json-strings.csv"
JMETER_ARGS="${JMETER_ARGS} -Jyt.path.dataset.issues=${INPUT_DATA_DIR}/issues_json-strings.csv"
JMETER_ARGS="${JMETER_ARGS} -Jyt.path.output_dir=${OUTPUT_DATA_DIR}"
JMETER_ARGS="${JMETER_ARGS} -Jyt.path.dataset.created_projects=${OUTPUT_DATA_DIR}/${CREATED_DATASET_PREFIX}created_projects.csv"
JMETER_ARGS="${JMETER_ARGS} -Jyt.path.dataset.created_users=${OUTPUT_DATA_DIR}/${CREATED_DATASET_PREFIX}created_users.csv"
JMETER_ARGS="${JMETER_ARGS} -Jyt.path.dataset.created_issues=${OUTPUT_DATA_DIR}/${CREATED_DATASET_PREFIX}created_issues.csv"
JMETER_ARGS="${JMETER_ARGS} -Jyt.path.dataset.created_links=${OUTPUT_DATA_DIR}/${CREATED_DATASET_PREFIX}issue_links.csv"
#JMETER_ARGS="${JMETER_ARGS} -Jsummariser.ignore_transaction_controller_sample_result=false"

# Set Java heap size
export HEAP="-Xms1g -Xmx4g -XX:MaxMetaspaceSize=256m"

# Create output dir if not exists
[ -d "$OUTPUT_DATA_DIR" ] || mkdir "$OUTPUT_DATA_DIR"

# Enable GC verbose
# export VERBOSE_GC="-Xlog:gc*,gc+age=trace,gc+heap=debug:file=${OUTPUT_DATA_DIR}/${RUN_ID}_gc_jmeter_%p.log"

# Run JMeter
${JMETER_HOME}/bin/jmeter.sh $JMETER_ARGS
