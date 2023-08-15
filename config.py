import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://shadow-cosmos.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'y3XtoKo3ibFflPRTw2sqNC6MDa9ySzY37QwmXw5onsRGvG7D6rUBr2HCszNPy8txIfpMhZgetbLEACDbK49ZqQ=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'ShadowConversations'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'Convos'),
}