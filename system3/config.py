"""
config
------

Global nordlys config.

:Author: Krisztian Balog
:Author: Faegheh Hasibi
"""
import logging
import os
from file_utils import FileUtils
from logging_utils import PrintHandler


def load_nordlys_config(file_name):
    """Loads nordlys config file. If local file is provided, global one is ignored."""
    config_path = os.sep.join([BASE_DIR, "config"])
    local_config = os.sep.join([config_path, "local", file_name])
    if os.path.exists(local_config):
        return FileUtils.load_config(local_config)
    else:
        return FileUtils.load_config(os.sep.join([config_path, file_name]))


# global variable for entity linking
KB_SNAPSHOT = None

# Nordlys DIRs
NORDLYS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




# config for Elasticsearch
ELASTIC_CONFIG = load_nordlys_config("elastic.json")
ELASTIC_HOSTS = ELASTIC_CONFIG["hosts"]
ELASTIC_SETTINGS = ELASTIC_CONFIG["settings"]
ELASTIC_INDICES = ELASTIC_CONFIG["indices"]
ELASTIC_TTI_INDICES = ELASTIC_CONFIG["tti_indices"]


# config for RequestLogger
LOGGING_PATH = os.sep.join([BASE_DIR, "logs"])
# config for PrintLogger (PLOGGER)
LOGGING_LEVEL = logging.INFO
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("elasticsearch").setLevel(logging.WARNING)
PLOGGER = logging.getLogger("nordlys")
PLOGGER.addHandler(PrintHandler(LOGGING_LEVEL).ch)
PLOGGER.setLevel(LOGGING_LEVEL)
PLOGGER.propagate = 0