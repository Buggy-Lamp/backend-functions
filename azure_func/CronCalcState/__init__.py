import datetime
import logging

import azure.functions as func
from azure.cosmos import CosmosClient

from ..constants import DB_ENDPOINT, DB_KEY, DB_DATABASE_ID, DB_CONTAINER_ID


client = CosmosClient(DB_ENDPOINT, DB_KEY)

database = client.get_database_client(DB_DATABASE_ID)
container = database.get_container_client(DB_CONTAINER_ID)


def main(statetimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if statetimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
