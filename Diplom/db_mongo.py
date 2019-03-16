from pymongo import MongoClient


def write_to_database(data):
    client = MongoClient()
    mydb = client.vkinder
    mydb_vkinder = mydb.vkinder
    mydb_vkinder.insert_one(data)
