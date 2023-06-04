#!/bin/bash

# Function to check if .env exists and create the environment if necessary
check_and_create_environment() {
    local folder=$1
    local environment=".env_$folder"

    if [ -d "$folder/$environment" ]; then
        echo "+ Python environment already exists in $folder."
    else
        echo "+ Creating Python environment in $folder..."
        python3 -m venv "$folder/$environment"
        echo "+ Python environment created in $folder."
    fi

    echo "- - - - - - - "
}

# Main script
directories=("data_generator" "model_trainer" "chat_backend")

for directory in "${directories[@]}"; do
    echo "Checking environment in $directory..."
    check_and_create_environment "$directory"
done
