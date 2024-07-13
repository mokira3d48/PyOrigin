import os
import logging
import logging.config


if os.path.isfile('logging.conf'):
    logging.config.fileConfig('logging.conf')
