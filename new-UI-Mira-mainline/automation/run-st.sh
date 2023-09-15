#!/bin/bash -x

set -e

current_path=${PWD}
pushd /opt/ccs

file="poetry.lock"

if [ -f "$file" ] ; then
    rm "$file"
fi

running_cm=`cat /configmap/data/infra_clusterinfo.json`
echo "running with configmap: " $running_cm

# Generate spec will install all python libs as well
./generate_spec.sh ${current_path}
popd

pip3 install playwright
playwright install-deps
playwright install chromium
pip uninstall pytest-randomly -y

source /opt/ccs/automation/parser.sh
echo "cluster under test"
echo $ClusterUnderTest
echo "================="
rm -rf /tmp/results || true

export PYTHONPATH="${PYTHONPATH}:/opt/ccs/automation/"

mkdir -p /tmp/results/testrail

poetry run python /opt/ccs/automation/libs/utils/s3/s3-download.py

## test case paths here
#poetry run pytest --alluredir /tmp/results --junitxml=/tmpdir/results/testrail/"STStorageComputeTestResults_Regression.xml" automation/tests/workflows/brownfield/storage_compute/ -v -s -m ${TestType}  || true

poetry run python /opt/ccs/automation/libs/utils/s3/s3-upload.py