#!/bin/bash
BIN="$1"
PREFIX="$2"

if [ -z "$BIN" ] || [ -z "$PREFIX" ]; then
    echo "Usage: ./scripts/benchmark.sh <binary_path> <prefix>"
    exit 1
fi

CSV="results/measurements_${PREFIX}.csv"
echo "run,real_sec,user_sec,sys_sec,max_rss_kb,page_faults,context_switches" > "$CSV"

echo "Running 30 runs for $BIN ($PREFIX)..."
for i in $(seq -w 1 30); do
    LOG_TIME="results/raw_runs/${PREFIX}_time_run_${i}.txt"
    LOG_PERF="results/raw_runs/${PREFIX}_perf_run_${i}.txt"

    /usr/bin/time -v "$BIN" > /dev/null 2> "$LOG_TIME"
    perf stat -e task-clock,context-switches,cpu-migrations,page-faults "$BIN" > /dev/null 2> "$LOG_PERF"

    USER_SEC=$(grep -i "User time (seconds):" "$LOG_TIME" | awk '{print $NF}')
    SYS_SEC=$(grep -i "System time (seconds):" "$LOG_TIME" | awk '{print $NF}')
    ELAPSED_RAW=$(grep -i "Elapsed (wall clock) time" "$LOG_TIME" | awk '{print $NF}')
    MAX_RSS=$(grep -i "Maximum resident set size" "$LOG_TIME" | awk '{print $NF}')
    FAULTS=$(grep -i "Minor (reclaiming a frame) page faults:" "$LOG_TIME" | awk '{print $NF}')
    CS=$(grep -i "voluntary context switches" "$LOG_TIME" | awk '{print $NF}' | head -n 1)

    # Конвертація mm:ss.ss у секунди
    REAL_SEC=$(echo "$ELAPSED_RAW" | awk -F: '{ if (NF==2) print ($1*60)+$2; else if (NF==3) print ($1*3600)+($2*60)+$3; else print $1 }')

    echo "$i,$REAL_SEC,$USER_SEC,$SYS_SEC,$MAX_RSS,$FAULTS,$CS" >> "$CSV"
    echo -n "."
done
echo ""
echo "Done! Data written to $CSV"
