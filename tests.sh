#!/usr/bin/bash
# Need pytest installed (pip install pytest)

export PYTHONPATH="$PWD/func"
pytest -vv || { echo "ERROR: Error while running Pytest. Make sure it is installed or check if the tests ran correctly. [CONTINUING SCRIPT]";  }
