# encoding: utf-8
# import postgresql
# db = postgresql.open('pq://syfdev:SyF1deV081018@54.203.133.192:5432/syf_db01')
# db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, login CHAR(64), password CHAR(64))")

import psycopg2


class dbsession:  # (object):
    """ dbsession
    Класс для взаимодействия с базой данных
    Методы:
    конструктор принимает строку подключения к базе данных
    select(sql) - Принимает строку запроса, возвращает результат выборки
    insert(sql) - Принимает строку запроса, возвращает количество вставленных строк
    update(sql) - Принимает строку запроса, возвращает количество измененных строк
    transaction(command) ["start", "commit", "rollback"] return True | False
    executesql(sql) Принимает строку запроса"""
    __connection = None
    __cursor = None

    def __init__(self, arg):
        # super(sqlExecutor, self).__init__()
        # self.arg = arg
        try:
            print("try connect")
            self.__connection = psycopg2.connect(arg)
            # "host='54.203.133.192' port=5432 user='syfdev' password='SyF1deV081018' dbname='syf_db01'")
            print("Success connect")
            self.__cursor = self.__connection.cursor()
        except psycopg2.Error as err:
            print("Connection error: {}".format(err))
            raise

    def __exit__(self, exception_type, exception_value, traceback):
        if self.__cursor is not None:
            self.__cursor.close()
            print('Database connection closed.')

    def transaction(self, command):
        assert command in ["start", "commit", "rollback"], "dbsession.transaction bad command"
        return True

    def executesql(self, sql):
        print("start executesql")
        cur = self.__connection.cursor()
        rez = cur.execute(sql)
        cur.close()
        print(rez)
        print("end executesql")
        return rez

    def select(self, sql):
        print("start")
        # cur = self.__connection.cursor()
        # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) # by column name
        # cur.execute(sql)
        self.__cursor.execute(sql)
        # data = cur.fetchall()
        data = self.__cursor.fetchall()
        print(data)
        return data

    def insert(self, sql):
        return self.executesql(sql)

    def update(self, sql):
        return self.executesql(sql)


# def main():
#     print("start")
#     try:
#         print("try connect")
#         conn = psycopg2.connect("host='52.35.199.96' port=5432 user='syfdev' password='SyF1deV081018' dbname='syf_db01'")
#         # ip - 52.35.199.96
#         # port - 5432
#         # user - healthyFood
#         # pass - Y24977c1
#         # dbname - healthyfoodbd
#     except psycopg2.Error as err:
#         print("Connection error: {}".format(err))
#
#     # sql = " create table alex(id int, var1 int)"
#     sql = " SELECT schemaname, tablename, tableowner FROM pg_tables LIMIT 10"
#
#     try:
#         print("try conn.cursor()")
#         cur = conn.cursor()
#         # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) # by column name
#         cur.execute(sql)
#         data = cur.fetchall()
#         print(data)
#     except psycopg2.Error as err:
#         print("Query error: {}".format(err))


if __name__ == '__main__':
    input("Press any key to continue.")
    print("start")
    try:
        print("try connect")
        conn = psycopg2.connect("host='52.35.199.96' port=5432 user='syfdev' password='SyF1deV081018' dbname='syf_db01'")
        # ip - 52.35.199.96
        # port - 5432
        # user - healthyFood
        # pass - Y24977c1
        # dbname - healthyfoodbd
    except psycopg2.Error as err:
        print("Connection error: {}".format(err))

    # sql = " create table alex(id int, var1 int)"
    sql = " SELECT schemaname, tablename, tableowner FROM pg_tables LIMIT 10"

    try:
        print("try conn.cursor()")
        cur = conn.cursor()
        # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) # by column name
        cur.execute(sql)
        data = cur.fetchall()
        print(data)
    except psycopg2.Error as err:
        print("Query error: {}".format(err))
    input("Press any key to exit.")
