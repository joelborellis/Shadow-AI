import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime
import json

import config

# ----------------------------------------------------------------------------------------------------------
# Prerequistes -
#
# 1. An Azure Cosmos account -
#    https://docs.microsoft.com/azure/cosmos-db/create-cosmosdb-resources-portal#create-an-azure-cosmos-db-account
#
# 2. Microsoft Azure Cosmos PyPi package -
#    https://pypi.python.org/pypi/azure-cosmos/
# ----------------------------------------------------------------------------------------------------------
# Sample - demonstrates the basic CRUD operations on a Item resource for Azure Cosmos
# ----------------------------------------------------------------------------------------------------------

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']

def read_item(container, doc_id, account_number):
    print('\nReading Item by Id\n')

    # We can do an efficient point read lookup on partition key and id
    response = container.read_item(item=doc_id, partition_key=account_number)

    print('Item read by Id {0}'.format(doc_id))
    print('Partition Key: {0}'.format(response.get('partitionKey')))
    print('Subtotal: {0}'.format(response.get('subtotal')))
    
def read_items(container):
    print('\nReading all items in a container\n')

    # NOTE: Use MaxItemCount on Options to control how many items come back per trip to the server
    #       Important to handle throttles whenever you are doing operations such as this that might
    #       result in a 429 (throttled request)
    item_list = list(container.read_all_items(max_item_count=10))

    print('Found {0} items'.format(item_list.__len__()))

    for doc in item_list:
        print('User: {0}'.format(doc.get('user')))

def query_items(container, user):
    print('\nQuerying for an  Item by User\n')

    items = list(container.query_items(
        query="SELECT * FROM r WHERE r.user=@user",
        parameters=[
            { "name":"@user", "value": user }
        ],
        enable_cross_partition_query=True,
    ))

    #print('Item queried by User {0}'.format(items[0].get("user")))
    for item in items:
        print(json.dumps(item, indent=True))
    
def create_items(container):
    print('Creating Items')
    print('\n1.1 Create Item\n')
    
    json = {
      "id": "100",
      "title": "The title of the convo",
      "user": "joelborellis@outlook.com",
      "messages": [
        { "role": "user", "content": "Hello 2" },
        { "role": "assistant", "content": "Hello, how can i help you" },
        { "role": "user", "content": "Hello 2" },
        { "role": "assistant", "content": "Hello, how can i help you" }
      ]
    }

    # Create a SalesOrder object. This object has nested properties and various types including numbers, DateTimes and strings.
    # This can be saved as JSON as is without converting into rows/columns.
    container.create_item(body=json)



def run_sample():
        client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
      
        db = client.get_database_client(DATABASE_ID)
        print('Database with id \'{0}\' was found'.format(DATABASE_ID))
        container = db.get_container_client(CONTAINER_ID)
        print('Container with id \'{0}\' was found'.format(CONTAINER_ID))
        
        
        #read_item(container, 'SalesOrder1', 'Account1')
        #create_items(container)
        query_items(container, "joelborellis@outlook.com")

        print("\nrun_sample done")


if __name__ == '__main__':
    run_sample()
