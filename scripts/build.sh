#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

ROOT_DIR="${DIR/\/scripts/}"

# create venv
python3 -m venv $ROOT_DIR/.venv

# source it!
source $ROOT_DIR/.venv/bin/activate

# install deps
pip install -r $ROOT_DIR/requirements.txt

# build it!
pyinstaller $ROOT_DIR/pytdl.py \
  --distpath $ROOT_DIR/dist \
  --workpath $ROOT_DIR/build \
  --specpath $ROOT_DIR/specs
