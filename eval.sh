#!/bin/bash
node networker.js &
pid=$!
docker compose up
kill $pid
# Get the IDs of the last 3 containers used
container_ids=$(docker ps -a --format "{{.ID}}" | tail -n 3)

# Define the folder you want to copy
folder_to_copy="/app/rl_server/logs/"

# Define the destination directory in your user's home directory
destination_directory="."

# Create the destination directory if it doesn't exist
mkdir -p "$destination_directory"

# Loop through the container IDs and copy the folder
for container_id in $container_ids; do
    # Extract the folder from the container
    docker cp "$container_id:$folder_to_copy" "$destination_directory"
done

python plotter.py
