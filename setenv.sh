#!/bin/bash

DIR_NAME=$(dirname "${BASH_SOURCE[0]}")
ENV_FOLDER=".env"

if [ ! -d "${DIR_NAME}/${ENV_FOLDER}/" ]; then
    python3.7 -m venv "${DIR_NAME}/${ENV_FOLDER}"
fi

source "${DIR_NAME}/${ENV_FOLDER}/bin/activate"

if [ "$1" = "install" ]; then
    pip install --upgrade pip setuptools wheel
    pip install -r "${DIR_NAME}/requirements.txt"
fi

