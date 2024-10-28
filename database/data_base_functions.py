import sqlite3
from configs.config import config
from configs.config import db_path


def get_group_names():
    connection = sqlite3.connect(db_path())
    cursor = connection.cursor()
    cursor.execute('''
            SELECT GROUP_NAME, GROUP_URL FROM GROUPS
            ''')

    group_names = [i[0] for i in cursor.fetchall()]

    connection.close()

    return group_names


def get_group_url(group_name):
    connection = sqlite3.connect(db_path())
    cursor = connection.cursor()
    cursor.execute(f'''
                SELECT GROUP_URL FROM GROUPS WHERE GROUP_NAME = '{group_name}'
                ''')

    group_url = cursor.fetchall()

    connection.close()

    return group_url[0][0]


def get_group_url_by_id(user_id):
    connection = sqlite3.connect(db_path())
    cursor = connection.cursor()
    cursor.execute(f'''
                    SELECT USER_GROUP FROM USERS WHERE USER_ID = '{user_id}'
                    ''')
    user_group = cursor.fetchall()[0][0]
    connection.close()

    return get_group_url(user_group)


def add_user(user_data):
    connection = sqlite3.connect(db_path())
    cursor = connection.cursor()

    cursor.execute(f'''
                INSERT INTO USERS (USER_ID, USER_NAME, USER_GROUP, WEEKLY_MESSAGING, DAILY_MESSAGING) 
                VALUES ('{user_data['user_id']}', '{user_data['user_name']}', '{user_data['user_group']}', 
                '{user_data['weekly_messaging']}', '{user_data['daily_messaging']}');
                ''')
    connection.commit()
    connection.close()


def add_group(group_name, group_url):
    connection = sqlite3.connect(db_path())
    cursor = connection.cursor()

    cursor.execute(f'''
                    INSERT INTO GROUPS (GROUP_NAME, GROUP_URL) 
                    VALUES ('{group_name}', '{group_url}');
                    ''')
    connection.commit()
    connection.close()


def daily_messaging_users_id():
    connection = sqlite3.connect(db_path())
    cursor = connection.cursor()
    cursor.execute(f'''
                        SELECT USER_ID FROM USERS WHERE DAILY_MESSAGING = 1'
                        ''')
    users = cursor.fetchall()
    connection.close()
    return users


def weekly_messaging_users_id():
    connection = sqlite3.connect(db_path())
    cursor = connection.cursor()
    cursor.execute(f'''
                        SELECT USER_ID FROM USERS WHERE WEEKLY_MESSAGING = 1'
                        ''')
    users = cursor.fetchall()
    connection.close()
    return users

