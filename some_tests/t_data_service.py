from DataService.cosmos_db_data_service import DataService
from datetime import datetime
import json
import copy
import azure.cosmos.exceptions as c_exceptions
import flatten_dict


def t1():
    obj = {
        "email": "zaphod@hitchiker.org",
        "id": "zaphod@hitchiker.org",
        "name": {
            "last_name": "Beeblebrox",
            "first_name": "Zaphod"
        },
        "company_id": "number42.com",
        "created_date": datetime.now().isoformat()
    }
    ds = DataService()
    res = ds.create("Users", obj)
    print("T1 res = ", res)

    res = ds.delete("Users", obj["id"])
    print("T1, delete res = ",json.dumps(res, indent=2, default=str))

    res = ds.delete("Users", obj["id"])
    print("T1, 2nd delete res = ", json.dumps(res, indent=2, default=str))


def t2():
    obj1 = {
        "email": "zaphod@hitchiker.org",
        "id": "zaphod@hitchiker.org",
        "name": {
            "last_name": "Beeblebrox",
            "first_name": "Zaphod"
        },
        "company_id": "number42.com",
        "created_timestamp": datetime.now().isoformat()
    }
    ds = DataService()
    res = ds.create("Users", obj1)
    print("T2 res = ", obj1)

    obj2 = copy.deepcopy(res)
    obj2["created_timestamp"] = datetime.now().isoformat()
    res2 = ds.update("Users", obj2["id"], obj2)
    print("T2 update res = ", res2)

    res3 = ds.update("Users", res["id"], res)
    print("T2 2nd update res = ", res3)

    res = ds.delete("Users", res2["id"])
    print("T2, delete res = ", json.dumps(res, indent=2, default=str))

    res = ds.delete("Users", res2["id"])
    print("T2, 2nd delete res = ", json.dumps(res, indent=2, default=str))


def t3():
    obj1 = {
        "email": "zaphod@hitchiker.org",
        "id": "zaphod@hitchiker.org",
        "name": {
            "last_name": "Beeblebrox",
            "first_name": "Zaphod"
        },
        "company_id": "number42.com",
        "created_timestamp": datetime.now().isoformat()
    }
    ds = DataService()

    try:
        res1 = ds.delete("Users", obj1["id"])
        print("T3 delete res = ", json.dumps(res1))
    except c_exceptions.CosmosResourceNotFoundError as e:
        print("Object not found. This is OK.")

    res = ds.create("Users", obj1)
    print("T3 create res = ", json.dumps(res, indent=3))

    res2 = ds.get_by_id("Users", obj_id=obj1["id"])
    print("T3 get_by_id = ", json.dumps(res2, indent=3))

    res3 = ds.delete("Users", res2["id"])
    print("T3, delete res = ", json.dumps(res3, indent=2, default=str))


def t4():
    obj1 = {
        "email": "zaphod@hitchiker.org",
        "id": "zaphod@hitchiker.org",
        "name": {
            "last_name": "Beeblebrox",
            "first_name": "Zaphod"
        },
        "company_id": "number42.com",
        "created_timestamp": datetime.now().isoformat()
    }

    ar = flatten_dict.flatten(obj1)
    print("Flattened = ", ar)

    template = {
        "name": {
            "last_name": "Beeblebrox",
            "first_name": "Zaphod"
        },
        "company_id": "number42.com"
    }
    ds = DataService()
    res =  ds.query("Users", template)
    x = res.by_page()
    print("Res = ", str(res))
    for o in res:
        pass
        print("T4 res = ", json.dumps(o, indent=2, default=str))



#t1()
#t2()
#t3()
t4()