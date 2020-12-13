import json
from CustomerService.user_service.UserService import UserService

def t1():
    cs = UserService()
    id = "zaphod@hitchiker.org"
    res = cs.get_by_id(id)
    print("T1 res = ", json.dumps(res, indent=2))


t1()