import random
import routeros_api

f_auth = open("auth.txt", "r", encoding='utf-8')
auth = f_auth.read().split('\n')
f_auth.close()

connection = routeros_api.RouterOsApiPool(host=str(auth[2]), port=int(auth[3]), username=str(auth[0]), password=str(auth[1]), plaintext_login=True)
api = connection.get_api()
list_users = api.get_resource('/ip/hotspot/user')
list_hosts = api.get_resource('/ip/hotspot/host/')

def main():
    match input('1 - List users\n2 - Add user (random)\n3 - Remove user\nEnter: '):
        case '1':
            listusers()
        case '2':
            add_user()
        case '3':
            remove_user()
        case _:
            return

def listusers():
    print(list_users.get())

def add_user(auto = True):
        global name
        name = random.randint(111111, 999999)
        try:
            list_users.set(id="*1", name=str(name), comment='Dont change list order fot this user')
        except:
            list_users.add(name=str(name), comment='Dont change list order for this user', profile='default',)
        finally:
            return str(name)

def remove_user():
    global name
    name = None
    list_hosts.remove()
    list_users.remove(id='*1')

if __name__ == "__main__":
    main()