import sqlite3 as sq

from pydantic import BaseModel

from tgbot.data.config import PATH_DATABASE
from tgbot.utils.const_functions import get_unix, ded
from tgbot.database.db_helper import update_format_where, dict_factory


# Модель таблицы
class VideoModel(BaseModel):
    increment: int
    video_id: int
    video_name: str
    video_size: int
    video_duration: int
    user_id: int
    video_check: int


class Videox():
    storage_name = 'storage_video'

    # Добавление видео
    @staticmethod
    def add(video_id: int, video_name: str, video_size: int, video_duration: int, user_id: int):
        video_check = 0
        if video_name is None:
            video_name = 'none'

        with sq.connect(PATH_DATABASE) as con:
            con.execute(
                ded(f"""
                                INSERT INTO {Videox.storage_name} (
                                    video_id,
                                    video_name,
                                    video_size,
                                    video_duration,
                                    user_id,
                                    video_check
                                    
                                ) VALUES (?, ?, ?, ?, ?, ?)
                            """),
                [
                    video_id,
                    video_name,
                    video_size,
                    video_duration,
                    user_id,
                    video_check,
                ],
            )

    # Получение записи
    @staticmethod
    def get(**kwargs) -> VideoModel:
        with sq.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Videox.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchone()

            if response is not None:
                response = VideoModel(**response)

            return response

    # Получение всех id записей
    @staticmethod
    def get_all_id():
        with sq.connect(PATH_DATABASE) as con:
            total_id = con.execute(f'SELECT video_id FROM {Videox.storage_name}').fetchall()

            return total_id

    # Проверка на уникальное видео
    @staticmethod
    def video_unic(video_name, video_size, video_duration):
        with sq.connect(PATH_DATABASE) as con:
            result = con.execute(
                f'SELECT * FROM {Videox.storage_name} WHERE video_name = ? AND video_size = ? AND video_duration = ?',
                (video_name, video_size, video_duration)).fetchall()

            return not bool(len(result))

    # Удаление видео
    @staticmethod
    def video_delete(video_id):
        with sq.connect(PATH_DATABASE) as con:
            try:
                con.execute(f'DELETE FROM {Videox.storage_name} WHERE video_id = ?', (video_id,))
                return True
            except:
                return False

    # Получение статуса проверки
    @staticmethod
    def video_check_status(video_id):
        with sq.connect(PATH_DATABASE) as con:
            status = con.execute(f'SELECT video_check FROM {Videox.storage_name} WHERE video_id = ?', (video_id,))
            if bool(status[0]):
                return True
            else:
                return False

    # Изменение статуса проверки
    @staticmethod
    def video_change_status(video_id):
        with sq.connect(PATH_DATABASE) as con:
            con.execute(f'UPDATE {Videox.storage_name} SET video_check = ? WHERE video_id = ?', (1, video_id,))

    # Средняя длительность всех видео
    @staticmethod
    def video_avg_all():
        with sq.connect(PATH_DATABASE) as con:
            avg = con.execute(f'SELECT AVG(video_duration) FROM {Videox.storage_name}').fetchall()
            avg = int(avg[0][0])

            return avg
