#!/bin/bash
total_runs=2
for ((run_number = 0; run_number < total_runs; run_number++)); do

    node networker.js $run_number &
    pid=$!

    start_time=$(date +%s.%N)
    docker compose up
    end_time=$(date +%s.%N)
    elapsed_time=$(awk "BEGIN {print $end_time - $start_time}")

    # Convert elapsed time to minutes and seconds
    minutes=$(awk "BEGIN {print int($elapsed_time / 60)}")
    seconds=$(awk "BEGIN {print int($elapsed_time % 60)}")
    echo "Run number: ${run_number} Elapsed time: ${minutes} minutes and ${seconds} seconds"

    kill $pid

    container_ids=$(docker ps -a --format "{{.ID}}" | tail -n 3)
    folder_to_copy="/app/rl_server/logs/"
    destination_directory="./results/run-$run_number/"
    mkdir -p "$destination_directory"

    for container_id in $container_ids; do
        docker cp "$container_id:$folder_to_copy" "$destination_directory" > /dev/null 2>&1
    done

    python plotter.py $destination_directory

    if [ $run_number -ne $((total_runs - 1)) ]; then
    sleep 5
    fi
done