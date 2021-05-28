import psycopg2 as psycopg2
import os
from exceptions import NotFoundTransfer, NotFoundUser, NotFound, NotFoundTool, NotFoundLocation, NotEnoughTools, \
    HaveNewLocation


DATABASE = os.getenv('POSTGRES_DB')
USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
HOST = os.getenv("POSTGRES_DB_HOST")
PORT = "5432"

def delete_user(user_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
        if cur.fetchone() is None:
            print("Пользователь не найдет")
            raise NotFoundUser(f"User {user_id} not found ")
        else:
            cur.execute(f"DELETE FROM users WHERE id = '{user_id}'")
            print(f"{user_id} is deleted")


def get_all_users():
    answer = []
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users ORDER BY id ASC")
        for i in cur.fetchall():
            answer.append(f"{i[0]}   {i[1]}")
    return answer


# Users DB
def get_all_worker():
    answer = []
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE worker = true ORDER BY id ASC")
        for i in cur.fetchall():
            answer.append(f"{i[0]}   {i[1]}")
    return answer


def get_all_staff():
    answer = []
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE staff = true ORDER BY id ASC")
        for i in cur.fetchall():
            answer.append(f"{i[0]}   {i[1]}")
    return answer


def get_all_admin():
    answer = []
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE admin = true ORDER BY id ASC")
        for i in cur.fetchall():
            answer.append(f"{i[0]}   {i[1]}")
    return answer


def get_all_creators():
    answer = []
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE creator = true ORDER BY id ASC")
        for i in cur.fetchall():
            answer.append(f"{i[0]}   {i[1]}")
    return answer


def add_worker(user_id, user_name):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
        if cur.fetchone() is None:
            cur.execute(
                f"INSERT INTO users (id,       name,    worker ,staff ,admin,creator) VALUES (%s,%s,%s,%s,%s,%s)",
                (user_id, user_name, True, False, False, False))
            print("Пользователь создан!")
        else:
            cur.execute(f"SELECT worker FROM users WHERE id = '{user_id}'")

            if not cur.fetchone()[0]:
                cur.execute(f"UPDATE users SET worker = True WHERE id = '{user_id}'")
                print("Пользователь обновлен!")
            else:
                print("Пользователь уже worker")


def delete_worker(user_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
        if cur.fetchone() is None:
            print("Пользователь не найдет")
            raise NotFoundUser(f"User {user_id} not found ")
        else:
            cur.execute(f"UPDATE users SET worker = False WHERE id = '{user_id}'")
            print(f"{user_id} больше не Worker")


def add_staff(user_id, user_name):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
        if cur.fetchone() is None:
            cur.execute(
                f"INSERT INTO users (id,       name,    worker ,staff ,admin,creator) VALUES (%s,%s,%s,%s,%s,%s)",
                (user_id, user_name, True, True, False, False))
            print("Пользователь создан!")
        else:
            cur.execute(f"SELECT staff FROM users WHERE id = '{user_id}'")

            if not cur.fetchone()[0]:
                cur.execute(f"UPDATE users SET staff = True WHERE id = '{user_id}'")
                print("Пользователь обновлен!")
            else:
                print("Пользователь уже staff")


def delete_staff(user_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
        if cur.fetchone() is None:
            print("Пользователь не найдет")
            raise NotFoundUser(f"User {user_id} not found ")
        else:
            cur.execute(f"UPDATE users SET staff = False WHERE id = '{user_id}'")
            print(f"User {user_id} больше не staff")


def add_admin(user_id, user_name):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
        if cur.fetchone() is None:
            cur.execute(
                f"INSERT INTO users (id,       name,    worker ,staff ,admin,creator) VALUES (%s,%s,%s,%s,%s,%s)",
                (user_id, user_name, True, True, True, False))
            print("Пользователь создан!")
        else:
            cur.execute(f"SELECT admin FROM users WHERE id = '{user_id}'")

            if not cur.fetchone()[0]:
                cur.execute(f"UPDATE users SET admin = True WHERE id = '{user_id}'")
                print("Пользователь обновлен!")
            else:
                print("Пользователь уже admin")


def delete_admin(user_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
        if cur.fetchone() is None:
            print("Пользователь не найдет")
            raise NotFoundUser(f"User {user_id} not found ")
        else:
            cur.execute(f"UPDATE users SET admin = False WHERE id = '{user_id}'")
            print(f"{user_id} больше не admin")


def add_creator(user_id, user_name):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
        if cur.fetchone() is None:
            cur.execute(
                f"INSERT INTO users (id,       name,    worker ,staff ,admin,creator) VALUES (%s,%s,%s,%s,%s,%s)",
                (user_id, user_name, True, True, True, True))
            print("Пользователь создан!")
        else:
            cur.execute(f"SELECT creator FROM users WHERE id = '{user_id}'")

            if not cur.fetchone()[0]:
                cur.execute(f"UPDATE users SET creator = True WHERE id = '{user_id}'")
                print("Пользователь обновлен!")
            else:
                print("Пользователь уже creator")


def delete_creator(user_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
        if cur.fetchone() is None:
            print("Пользователь не найдет")
            raise NotFoundUser(f"User {user_id} not found ")
        else:
            cur.execute(f"UPDATE users SET creator = False WHERE id = '{user_id}'")
            print(f"{user_id} больше не admin")


def get_user_status(user_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM users WHERE id = {user_id}")
        if cur.fetchone is None:
            print(f"Users with id {user_id} not found")
            raise NotFoundUser(f"Users with id {user_id} not found")
        else:
            cur.execute(f"SELECT worker, staff, admin, creator FROM users WHERE id = {user_id}")
            status = cur.fetchone()  # worker staff admin creator
            return status



# Locations DB
def add_location(name: str):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()

        cur.execute("""
        insert into locations (name) VALUES ('%s')
        """ % name)
        print(f"Локация {name} добавлена")


def delete_location(id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM locations WHERE id = {id}")
        if cur.fetchone() is None:
            print("Location not found")
            raise NotFound(f"Location {id} not found")
        else:
            cur.execute(f"DELETE FROM locations WHERE id = {id}")
            print(f"Location {id} deleted")


def get_locations():
    res = []
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM locations ORDER BY id ASC")
        for e in cur.fetchall():
            res.append(f"{e[0]}    {e[1]}")
    return res


# Tools DB
def add_tool(id_location, number, name):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM locations WHERE id = {id_location}")
        if cur.fetchone() is None:
            raise NotFoundLocation(f"Location with id {id_location} not found")

        cur.execute(f'INSERT INTO tools (id_location, name, number) VALUES(%s,%s,%s)', (id_location, name, number))
        print(f"Tools {name} добавлен на location {id_location} в количесве {number}")


def delete_tool(id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM tools WHERE id = {id}")
        if cur.fetchone() is None:
            print("Tools not found")
            raise NotFound(f"Tool with id {id} not found")
        else:
            cur.execute(f"DELETE FROM tools WHERE id = {id}")
            print(f"Tools with id {id} deleted")


def get_tools():
    res = []
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM tools ORDER BY id ASC")
        for e in cur.fetchall():
            res.append(f"{e[0]}---{e[1]}---{e[3]}---{e[2]}")
    return res


# Transfers DB
def create_transfer(user_id, id_tool, new_id, number):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM tools WHERE id = {id_tool}")
        if cur.fetchone() is None:
            raise NotFoundTool(f"Tool with id = {id_tool} not found")
        else:
            cur.execute(f"SELECT id_location FROM tools WHERE id = {id_tool}")
            last_id = cur.fetchone()[0]
        cur.execute(f"SELECT id FROM locations WHERE id = {new_id}")
        if cur.fetchone() is None:
            raise NotFoundLocation(f"Location with {new_id} not found")
        cur.execute(f"SELECT id FROM locations WHERE id = {last_id}")
        if cur.fetchone() is None:
            raise NotFoundLocation(f"Location with {last_id} not found")
        cur.execute(f"SELECT number FROM tools WHERE id = {id_tool}")
        number_db = cur.fetchone()[0]
        if number > number_db:
            raise NotEnoughTools(f"Tool with id = {id_tool} not have number  = {number}, only {number_db}")
        else:
            cur.execute(f"INSERT INTO transfers (id_user, id_last_location, id_new_location,id_tool, number) VALUES("
                        f"%s,%s,%s,%s,%s)", (user_id, last_id, new_id, id_tool, number))
            print("Tool добавлен в очередь на перемещение")


def create_transfer_with_accept(user_id, id_tool, new_id, number):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM tools WHERE id = {id_tool}")
        if cur.fetchone() is None:
            raise NotFoundTool(f"Tool with id = {id_tool} not found")
        else:
            cur.execute(f"SELECT * FROM tools WHERE id = {id_tool}")
            tool = cur.fetchone()
            last_id = tool[0]

        cur.execute(f"SELECT id FROM locations WHERE id = {new_id}")
        if cur.fetchone() is None:
            raise NotFoundLocation(f"Location with {new_id} not found")
        cur.execute(f"SELECT id FROM locations WHERE id = {last_id}")
        if cur.fetchone() is None:
            raise NotFoundLocation(f"Location with {last_id} not found")
        cur.execute(f"SELECT number FROM tools WHERE id = {id_tool}")
        number_db = cur.fetchone()[0]
        if number > number_db:
            raise NotEnoughTools(f"Tool with id = {id_tool} not have number  = {number}, only {number_db}")
        elif number == number_db:
            cur.execute(f"UPDATE tools SET id_location = %s WHERE id = {id_tool}" % new_id)
            print("Tool with all number update location")
        else:
            cur.execute(f"UPDATE tools SET number = %s WHERE id = {id_tool}" % (number_db - number))
            cur.execute(f'INSERT INTO tools (id_location, name, number) VALUES(%s,%s,%s)',
                        (tool[1], tool[2], number))
            print(f"Tools with id = {tool[0]} добавлен на location {new_id} в количестве {number}")


def accept_transfer(id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM transfers WHERE id = {id}")
        if cur.fetchone() is None:
            raise NotFoundTransfer(f"Transfer with id = {id} not found")
        else:
            cur.execute(f"SELECT * FROM transfers WHERE id = {id}")
            id, id_user, last_id, new_id, id_tool, number = cur.fetchone()
            print(id, id_user, last_id, new_id, id_tool, number)

            cur.execute(f"SELECT id FROM tools WHERE id = {id_tool}")
            if cur.fetchone() is None:
                raise NotFoundTool(f"Tool with id = {id_tool} not found")
            else:
                cur.execute(f"SELECT * FROM tools WHERE id = {id_tool}")
                tool = cur.fetchone()
                print(tool)
                if not last_id == tool[1]:
                    raise HaveNewLocation(
                        f"Tool with id =  {id_tool} have different location from last location = {last_id} ")

            cur.execute(f"SELECT id FROM locations WHERE id = {new_id}")
            if cur.fetchone() is None:
                raise NotFoundLocation(f"Location with {new_id} not found")

            cur.execute(f"SELECT id FROM locations WHERE id = {last_id}")
            if cur.fetchone() is None:
                raise NotFoundLocation(f"Location with {last_id} not found")

            cur.execute(f"SELECT number FROM tools WHERE id = {id_tool}")
            number_db = cur.fetchone()[0]
            if number > number_db:
                raise NotEnoughTools(f"Tool with id = {id_tool} not have number  = {number}, only {number_db}")
            elif number == number_db:
                cur.execute(f"UPDATE tools SET id_location = %s WHERE id = {id_tool}" % new_id)
                print("Tool with all number update location")
            else:
                cur.execute(f"UPDATE tools SET number = %s WHERE id = {id_tool}" % (number_db - number))
                cur.execute(f'INSERT INTO tools (id_location, name, number) VALUES(%s,%s,%s)',
                            (tool[1], tool[2], number))
                print(f"Tools with id = {tool[2]} добавлен на location {new_id} в количестве {number}")
            delete_transfer(id)


def accept_all_transfers():
    answer = []
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM transfers")
        id_transfers = []
        for e in cur.fetchall():
            id_transfers.append(e[0])
        print(id_transfers)
        for id in id_transfers:
            try:
                accept_transfer(id)
                answer.append(f"{id}    выполнин")
            except NotFoundTransfer as e:
                print(e.txt)
                answer.append(f"{id}    не выполнин     {e.txt} ")
            except NotFoundTool as e:
                print(e.txt)
                answer.append(f"{id}    не выполнин     {e.txt} ")
            except HaveNewLocation as e:
                print(e.txt)
                answer.append(f"{id}    не выполнин     {e.txt} ")
            except NotFoundLocation as e:
                print(e.txt)
                answer.append(f"{id}    не выполнин     {e.txt} ")
            except NotEnoughTools as e:
                print(e.txt)
                answer.append(f"{id}    не выполнин     {e.txt} ")
            except Exception as e:
                print(e.txt)
                answer.append(f"{id}    не выполнин не извесная ошибка")

        return answer


def reject_all_transfers():
    answer = []
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM transfers")
        id_transfers = []
        for e in cur.fetchall():
            id_transfers.append(e[0])
        print(id_transfers)
        for id in id_transfers:
            try:
                delete_transfer(id)
                answer.append(f"{id}  отклонен")
            except NotFoundTransfer as e:
                print(e.txt)
                answer.append(f"{id}  не найден   {e.txt} ")

        return answer


def delete_transfer(id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM transfers WHERE id = {id}")
        if cur.fetchone() is None:
            raise NotFound(f"Transfer with id = {id} not found")
        cur.execute(f"DELETE FROM transfers WHERE id = {id}")
        print(f"Transfer with id {id} deleted")


def get_transfers():
    res = []
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM transfers ORDER BY id ASC ")
        for e in cur.fetchall():
            res.append(f"{e[0]}---{e[1]}---{e[3]}---{e[2]}---{e[3]}---{e[5]}")
    return res


def init_database():
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(open("init.sql", "r").read())


