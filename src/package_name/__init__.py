import os
import ast
from pathlib import Path
from dotenv import load_dotenv

# loads the configs from .env
load_dotenv()

DEBUG = ast.literal_eval(os.getenv('DEBUG', 'False'))
OUTPUT_DIRPATH = os.getenv('OUTPUT_DIRPATH', 'runs')
LOG_FILEPATH = os.path.join(OUTPUT_DIRPATH, 'logs')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = Path(__file__).resolve().parent

__version__ = '0.1.0'
