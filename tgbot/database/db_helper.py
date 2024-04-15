import sqlite3 as sq

from tgbot.data.config import PATH_DATABASE
from tgbot.utils.const_functions import ded


# Преобразование полученного списка в словарь
def dict_factory(cursor, row) -> dict:
    save_dict = {}

    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]

    return save_dict


# Создание ВСЕХ таблиц для БД
def create_dbx():
    with sq.connect(PATH_DATABASE) as con:
        ############################################################
        # Создание Таблицы с хранением пользователей
        if len(con.execute("PRAGMA table_info(storage_users)").fetchall()) == 8:
            print("DB(storage_users) was found(1/2)")
        else:
            con.execute(
                ded(f"""
                                CREATE TABLE storage_users(
                                    increment INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id INTEGER,
                                    user_balance INTEGER,
                                    user_referral INTEGER,
                                    user_unix INTEGER,
                                    user_ban INTEGER,
                                    video_index INTEGER,
                                    user_warnings INTEGER
                                )
                            """)
            )
            print("DB(storage_users) was not found(1/2) | Creating...")

        if len(con.execute("PRAGMA table_info(storage_video)").fetchall()) == 7:
            print("DB(storage_video) was found(2/2)")
        else:
            con.execute(
                ded(f"""
                                CREATE TABLE storage_video(
                                    increment INTEGER PRIMARY KEY AUTOINCREMENT,
                                    video_id INTEGER,
                                    video_name TEXT,
                                    video_size INTEGER,
                                    video_duration INTEGER,
                                    user_id INTEGER,
                                    video_check INTEGER
                                )
                            """)
            )
            print("DB(storage_video) was not found(2/2) | Creating...")


# Форматирование запроса с аргументами
def update_format_where(sql, parameters: dict) -> tuple[str, list]:
    sql += " WHERE "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())
