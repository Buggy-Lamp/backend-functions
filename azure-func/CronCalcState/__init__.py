import datetime
import logging

import azure.functions as func
from azure.cosmos import CosmosClient

from .. import functions
from ..constants import DB_CONTAINER_ID


container = functions.getContainer(DB_CONTAINER_ID)


def main(statetimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if statetimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
