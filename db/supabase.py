import os
from supabase import create_client, Client

import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('GitHub API is starting up')

_ = load_dotenv(find_dotenv())

SUPABASE_URL = os.environ['SUPABASE_URL']
SUPABASE_KEY = os.environ['SUPABASE_KEY']
logger.info('~~~~~~~SUPABASE_URL')
logger.info(SUPABASE_URL)
logger.info('~~~~~~~SUPABASE_KEY')
logger.info(SUPABASE_KEY)

supabase: Client = create_client(url, key)