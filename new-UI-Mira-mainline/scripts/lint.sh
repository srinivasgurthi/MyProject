#!/bin/bash -ex

# directory/directories where the auto-linting will be executed
SRC_DIRS=${1:-"app tests"}

echo "Running linting checks for source code in ${SRC_DIRS} with directory context $(pwd)"

for src_dir in ${SRC_DIRS}
do
    [ ! -d ./${src_dir} ] \
        && echo "Running lint check with incorrect directory context. Directory ${src_dir} not present" \
        && exit 1
done

mypy \
    --ignore-missing-imports \
    --module app

black \
    --check \
    --diff \
    ${SRC_DIRS}

isort \
    --check-only \
    --profile black \
    ${SRC_DIRS}

# Use pyline to (only) generate a code similarity report to avoid large amounts
# of code duplication. (NOTE: only running on the app/ source code directory)
pylint \
    --disable=all \
    --enable=duplicate-code \
    --min-similarity-lines=20 \
    app

# Code complexity/quality checks
# TODO add checks to FT dir once the issues are resolved.
MIN_COMPLEXITY_GRADE="C"
complexity_check="radon cc --show-complexity --min=${MIN_COMPLEXITY_GRADE} app tests/unit_test"
complex_code="$(${complexity_check})"
if [[ ! -z "${complex_code}" ]]; then
    echo "Seeing overly complex code. Reach a minimum grade of ${MIN_COMPLEXITY_GRADE} for files below."
    echo "See https://radon.readthedocs.io/en/latest/intro.html for more info."
    exec ${complexity_check}
    exit 1
fi

# Dead code check. Add more exclusions where necesary (E.g. abstract classes).
vulture \
    --min-confidence=80 \
    --sort-by-size \
    --ignore-decorators "@router.*,@app.*,@abstractmethod" \
    --ignore-names "*_mock" \
    --exclude "*celeryconfig.py,identity_manager.py" \
    ${SRC_DIRS}

# Static security checks. Report only high confidence issues.
bandit \
    --recursive \
    -lll \
    -iii \
    ${SRC_DIRS}