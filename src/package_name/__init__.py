import os
import ast
import logging
from pathlib import Path
from dotenv import load_dotenv

# loads the configs from .env
load_dotenv()

DEBUG = ast.literal_eval(os.getenv('DEBUG', 'False'))
OUTPUT_DIRPATH = os.getenv('OUTPUT_DIRPATH', 'runs')

os.makedirs(OUTPUT_DIRPATH, exist_ok=True)

# Set up logging:
logging.basicConfig(
    level=(logging.INFO if not DEBUG else logging.DEBUG),
    format='%(levelname)s [%(asctime)s] \t %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(OUTPUT_DIRPATH, "pyorigin.log")),
    ]
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = Path(__file__).resolve().parent

__version__ = '0.1.0'
