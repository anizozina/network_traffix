from pymongo import MongoClient

MONGODB_CONFIG = {
    # see docker compose
    # NOTE: don't know the reason but can not access mongodb via localhost
    'uri': "mongodb://root:password@192.168.1.11:27017/network_traffic?authSource=admin",
    'database': 'network_traffic'
}


class MongoDBGateway:
    def __init__(self):
        self.client = MongoClient(MONGODB_CONFIG['uri'])
        self.database = self.client[MONGODB_CONFIG['database']
                                    ] if MONGODB_CONFIG['database'] else None

    def get_database(self):
        return self.database

    def write_host_mapping(self, ip: str, host: str):
        collection = self.database['ip_host_mapping']
        result = collection.replace_one(
            {"_id": ip},
            {"_id": ip, "ip_address": ip, "hostname": host},
            upsert=True)
        print(f"Inserted document ID: {result}")

    def get_host_by_ip(self, ip: str):
        collection = self.database['ip_host_mapping']
        result = collection.find_one({"ip_address": ip})
        if result is None:
          return ip
        return result['hostname']

    def close_connection(self):
        if self.client:
            self.client.close()

    def __del__(self):
        self.close_connection()
