
####################### BUILD TEST IMAGE ##################################
FROM quay.io/ccsportal/ubuntu:python38-202011062117 AS test-image
    # Set poetry version. installing it via curl honors this env variable

ARG JFROG_USERNAME
ARG JFROG_PASSWORD
ARG K8S_VERSION=v1.18.6

RUN adduser -u 1000 ubuntu --disabled-password --gecos ",,,"

ENV JFROG_USERNAME=$JFROG_USERNAME
ENV JFROG_PASSWORD=$JFROG_PASSWORD

RUN echo $JFROG_USERNAME
RUN echo $JFROG_PASSWORD

ENV APP_ROOT_DIR=/opt/ccs

ENV POETRY_VERSION=1.3.0
    # direct poetry to install at this location
ENV POETRY_HOME="/opt/poetry"
    # no interaction during poetry installs
ENV POETRY_NO_INTERACTION=1
     # python deps root
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PIP_VENV_VERSION=20.1.1
ENV PATH="$POETRY_HOME/bin:${APP_ROOT_DIR}/.venv/bin:$PATH"
RUN python -m pip install --upgrade pip

RUN mkdir -p $APP_ROOT_DIR
WORKDIR $APP_ROOT_DIR

COPY ./pyproject.toml ./
COPY ./scripts ./scripts

#COPY ${APP_ROOT_DIR}/.venv ${APP_ROOT_DIR}/.venv

COPY ./automation ./automation
COPY ./generate_spec.sh $APP_ROOT_DIR
RUN pip install poetry

RUN apt-get update && apt-get install --no-install-recommends -y curl jq libpq-dev gcc python3-dev && \
    curl -sSL https://install.python-poetry.org | python && \
    poetry run pip3 install pip==$PIP_VENV_VERSION

RUN poetry run pip3 install -U setuptools
RUN poetry run pip3 install cryptography=="39.0.1"

RUN apt-get install python3-dev -y && apt-get install libssl-dev -y && apt-get install swig 2.0.10 -y
RUN poetry run pip3 install --upgrade M2Crypto

RUN curl -s -L -o /usr/local/bin/kubectl https://storage.googleapis.com/kubernetes-release/release/${K8S_VERSION}/bin/linux/amd64/kubectl && \
    chmod +x /usr/local/bin/kubectl

RUN pip3 install playwright
RUN playwright install-deps
RUN playwright install chromium

# Due to an open poetry issue: https://github.com/python-poetry/poetry/issues/534
COPY ./dependency.py /opt/poetry/lib/poetry/packages/dependency.py

RUN poetry config http-basic.jfrog $JFROG_USERNAME $JFROG_PASSWORD && \
   poetry install

RUN chmod +x /opt/poetry/bin/poetry

####################### CI Stage ##################################
FROM test-image AS ci-stage

WORKDIR ${APP_ROOT_DIR}

USER root
RUN chmod +x ./scripts/*.sh
# Need to run CI as root since coverage file .coveragerc will need to be generated
# if not run as root we get qlite3.OperationalError: unable to open database file
# TODO: publish test coverage

RUN ./scripts/run-ci.sh