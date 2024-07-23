#!/bin/bash

# Run the script_runner to generate SQL
echo "Running script_runner to generate SQL..."
docker-compose run --rm script_runner

# Check if script_runner ran successfully
if [ $? -ne 0 ]; then
  echo "script_runner failed. Exiting."
  exit 1
fi

# Start db and other services
echo "Cleaning volumes..."
docker-compose down -v

echo "Starting db and web services..."
docker-compose up -d db

# Start the remaining services
docker-compose up -d web
