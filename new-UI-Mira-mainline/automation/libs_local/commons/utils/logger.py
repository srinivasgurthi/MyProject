import logging

# configure logging with filename, function name and line numbers
logging.basicConfig(
    level="INFO",
    datefmt="%I:%M:%S %p %Z",
    format="%(levelname)s [%(asctime)s - %(filename)s:%(lineno)s::%(funcName)s]\n%(message)s",
)

log = logging.getLogger(__name__)
