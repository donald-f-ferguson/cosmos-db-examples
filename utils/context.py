
# We need to replace this with environment variables or whatever Azure uses for environment vars.

import logging
import azure.cosmos.cosmos_client as cosmos_client

# TODO This cannot be in a file in the project. It must be part of the environment.
db_settings = {
    'host': 'https://ospreydb.documents.azure.com:443/',
    'master_key': '9cEDg64vvLVZVvHS8NJwl99HqkscLC4T7GGe5KaepFysufyagPPtwcq3ksW1yDCNytyopSAEaJZoyya1OX9D9g==',
    'database_id': 'ospreydbv2'
}

client = cosmos_client.CosmosClient(db_settings['host'], {'masterKey': db_settings['master_key']} )
dbs = client.get_database_client("ospreydbv2")

db_settings["database_service"] = dbs

env = {
    "db_settings": db_settings,
    'logging_level': logging.DEBUG,
    'collection_ids':
        {
            "Users": "Users"
        }
}