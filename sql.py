# coding=utf-8
from getpass import getpass
from mysql.connector import connect, Error, ProgrammingError


class Connection:

    def __init__(self, host, user, password):
        self.__host = host
        self.__user = user
        self.__password = password
        self.connection = self.__connect_to_db()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closing connection after exit in with.

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """

        self.close()

    def __connect_to_db(self, **kwargs):
        try:
            connection = connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                **kwargs
            )
            return connection
        except Error as e:
            print(e)

    def close(self):
        """
        Closing connection to db.

        :return:
        """

        self.connection.close()

    def use_db(self, db_name):
        """
        Connect or switch db.

        :param db_name:
        :return:
        """

        show_db_query = "USE {0}".format(db_name)
        cursor = self.connection.cursor()
        cursor.execute(show_db_query)

    def create_db(self, db_name):
        create_db_query = "CREATE DATABASE {0}".format(db_name)
        cursor = self.connection.cursor()
        cursor.execute(create_db_query)

    def show_db(self):
        show_db_query = "SHOW DATABASES"
        cursor = self.connection.cursor()
        cursor.execute(show_db_query)
        return cursor

    def create_table(self, table_name, **kwargs):
        """
        Creating db table.

        :param table_name:
        :param kwargs: { 'table_name': ('Type', 'args') } - describing table structure.
        :return:
        """

        create_table_query = """
            CREATE TABLE {0}(
                id INT AUTO_INCREMENT PRIMARY KEY,
        """.format(table_name)

        cursor = self.connection.cursor()
        for key, value in kwargs.items():
            create_table_query += "{0} {1}".format(key, value[0])
            if len(value) > 1:
                create_table_query += " {0},".format(value[1])
            create_table_query += ",\n"
        create_table_query = create_table_query[:-2]
        create_table_query += "\n)"
        cursor.execute(create_table_query)
        self.connection.commit()

    def insert_in_table(self, db_name, **kwargs):
        columns_name = '(' + ','.join(name for name in kwargs.keys()) + ')\n'
        insert_query = """
            INSERT INTO movies {0}
        """.format(columns_name)


def class_sql(user, password):
    # Первый вариант который я начал реализовывать,
    # но понял что слишком переусложняю требования ТЗ,
    # поэтому оставил написания класса на моменте с insert`ом.
    # По сути это продолжалось писаться только для себя, с вопросом "А получится ли?".

    """
    Function displaying basing skills for work with MySQL.

    :param user:
    :param password:
    :return:
    """
    with Connection('localhost', user, password) as connection:
        connection.create_db('test_user')
        connection.use_db('test_user')
        connection.create_table('users',
                                **{
                                    'name': ('VARCHAR(100)',),
                                    'age': ('INT',),
                                    'surname': ('VARCHAR(100)',),
                                    'patronymic': ('VARCHAR(100)',),
                                })


def sql_users(user, password):
    """
    Function displaying basing skills for work with MySQL.

    :param user:
    :param password:
    :return:
    """
    connection = None
    try:
        # Connect to  mysql
        connection = connect(
            host='localhost',
            user=user,
            password=password
        )
        cursor = connection.cursor(buffered=True)

        # Creating and connecting database
        create_db_query = "CREATE DATABASE users_test"
        cursor.execute(create_db_query)
        show_db_query = "USE users_test"
        cursor.execute(show_db_query)

        # Creating users table
        create_table_query = """
                    CREATE TABLE users(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100),
                        age INT,
                        surname VARCHAR(100),
                        patronymic VARCHAR(100)
                        )
                """
        cursor.execute(create_table_query)
        connection.commit()

        # Inserting data to table
        insert_query = """
        INSERT INTO users (name, surname, age , patronymic)
        VALUES
            ("Piter", "Bortnikov", 26, "Genadievich"),
            ("Ivan", "Latynin", 27, "Afonasyevich"),
            ("Boris", "Demichkin", 57, "Smenovich"),
            ("Georgy", "Kolym", 52, "Arkadeivich"),
            ("Simeon", "Kolym", 32, "Arkadeivich"),
            ("Alexandr", "Ratnikov", 52, "Pavlovich")
        """
        cursor.execute(insert_query)
        connection.commit()

        #  Selecting all records
        print_result(cursor, "SELECT * FROM users")

        #  Selecting people with a given last name
        surname = 'Kolym'
        select_movies_query = "SELECT * FROM users WHERE surname='{0}'".format(surname)
        print_result(cursor, select_movies_query)

        #  Increasing people age on 1 with a given last name
        update_query = """  
           UPDATE users SET age = age + 1 WHERE surname = '{0}'
        """.format(surname)
        cursor.execute(update_query)
        connection.commit()
        print_result(cursor, select_movies_query)

        #  Deleting people with a given last name
        del_surname = 'Ratnikov'
        delete_query = "DELETE FROM users WHERE surname = '{0}'".format(del_surname)
        cursor.execute(delete_query)
        connection.commit()

        print_result(cursor, "SELECT * FROM users")

    except Error as e:
        print(e)
    finally:
        #  Closing connection after end of function
        if connection:
            connection.close()


def print_result(cursor, query):
    """
    Function for selecting from db and output in stream.

    :param cursor:
    :param query:
    :return:
    """
    cursor.execute(query)
    for row in cursor.fetchall():
        print row
    print '-*' * 10
