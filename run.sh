#!/bin/bash
BASE_DIR=$(realpath "$(dirname $0)")

VENV_DIR=${BASE_DIR}/venv
source ${VENV_DIR}/bin/activate
python ${BASE_DIR}/main.py
