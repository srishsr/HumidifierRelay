#!/bin/bash
BASE_DIR=$(realpath "$(dirname $0)")

VENV_DIR=${BASE_DIR}/../venv
if [ ! -d "${VENV_DIR}" ]; then
    echo "Creating venv"
    python -m venv "${VENV_DIR}"
fi

sudo apt-get update
sudo apt-get install -y i2c-tools libgpiod-dev python3-libgpiod libopenblas-dev
source ${VENV_DIR}/bin/activate
python -m pip uninstall -y RPi.GPIO
python -m pip install -r ${BASE_DIR}/requirements.txt
