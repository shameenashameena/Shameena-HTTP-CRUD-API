import os
from azure.cosmos import CosmosClient, exceptions, PartitionKey

COSMOS_URL = os.getenv("COSMOS_U") 
COSMOS_KEY = os.getenv("COSMOS_K") 
DB_NAME = os.getenv("COSMOS_DB") 
CONTAINER_NAME = os.getenv("COSMOS_CONTAINER") 

class CosmosClientWrapper:
    def __init__(self):
        self.client = CosmosClient(COSMOS_URL, COSMOS_KEY)
        self.db = self.client.create_database_if_not_exists(id=DB_NAME)
        self.container = self.db.create_container_if_not_exists(
            id=CONTAINER_NAME, 
            partition_key=PartitionKey(path="/Id"),
            offer_throughput=400
        )

    def create_item(self, item: dict):
        # validating price numeric
        try:
            item["price"] = float(item["price"])
        except Exception:
            raise ValueError("price must be numeric")
        return self.container.create_item(body=item)

    def read_items(self):
        query = "SELECT * FROM c"
        return list(self.container.query_items(query=query, enable_cross_partition_query=True))

    def read_item(self, id):
        try:
            return self.container.read_item(item=id, partition_key=id)
        except exceptions.CosmosResourceNotFoundError:
            return None

    def update_item(self, id, body: dict):
        existing = self.read_item(id)
        if not existing:
            return None
        # merge and replace
        existing.update(body)
        return self.container.replace_item(item=id, body=existing)

    def delete_item(self, id):
        try:
            self.container.delete_item(item=id, partition_key=id)
            return True
        except exceptions.CosmosResourceNotFoundError:
            return False
