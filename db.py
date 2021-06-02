import pymongo

from bson import ObjectId

db_ip = 'localhost'  # 149.248.7.146 localhost
db_port = 27017
db_name = "reptile_data"
db_table = "forums"


def client():
    return pymongo.MongoClient(db_ip, db_port)


def db():
    return client()[db_name]


def table():
    return db()[db_table]


def insert_many(insert_list):
    return table().insert_many(insert_list)


def insert_one(insert):
    return table().insert_one(insert)


def get_list():
    return list(table().find())


def get_valid_list():
    return list(table().find({"status": 1}))


def get_list_by_status(v, size=50,skip=0):
    return list(table().find({"status": v}).limit(size).skip(skip))


def get_list_by_status_sort(v, size=50, sort=-1):
    return list(table().find({"status": v}).sort("_id", sort).limit(size))


def get_one_by_id(_id):
    return table().find({"_id": ObjectId(_id)})


def update_by_id(_id, v):
    return table().update_one({"_id": ObjectId(_id)}, {"$set": v})


def update_title_by_id(_id, v):
    return update_by_id(_id, {"title": v, "status": 1})


def update_comment_by_id(_id, v):
    return update_by_id(_id, {"comment": v, "status": 1})


def update_t_c_by_id(_id, t, v):
    return update_by_id(_id, {"title": t, "comment": v, "status": 1})


def get_list_by_count(v):
    return table().count_documents({"status": v})


def init_db_data():
    db_list = client().list_database_names()
    if db_name not in db_list:
        with open("data/valid_url_list.txt", "r", encoding='utf-8') as f:
            data_list = f.readlines()
        insert_list = []
        for url in data_list:
            insert_obj = {
                "url": url.replace("\n", ""),
                "title": "",
                "status": 0,
                "comment": ""
            }
            insert_list.append(insert_obj)
        insert_many(insert_list)


def remove_null_comment():
    return table().delete_many({"title": ""})


if __name__ == '__main__':
    # 281, 163-->274,089 274,088
    db_list = client().list_database_names()
    print(db_list)
    print("运行了")

    # print(len(get_list_by_count(1)))
    remove_null_comment()
    # print(len(get_list_by_count(1)))
