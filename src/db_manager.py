from logging import Logger
import sqlite3
from src import constants
from src import utils


class DBManager:
    @staticmethod
    def create_database():
        conn = sqlite3.connect(constants.DB_NAME)
        for script_str in constants.SCRIPT_LIST:
            cursor = conn.cursor()
            cursor.execute(script_str)
            conn.commit()
        cursor.close()
        conn.close()

    def __init__(self, base_logger: Logger) -> None:
        self.logger = utils.adapter_log(
            base_logger=base_logger,
            worket_id={"worker_id": "DB_MANAGER"})

    def get_connetion(self):
        try:
            conn = sqlite3.connect(constants.DB_NAME)
            cursor = conn.cursor()
            return conn, cursor
        except Exception as e:
            self.logger.error(f"COULD NOT GET - <conn>, <cursor>: {e}")
            raise e

    def get_query_insert(self, table_name: str, single_record: dict) -> None:
        key_list = single_record.keys()
        columns = ", ".join(key_list)
        template_values = ", ".join([f":{k}" for k in key_list])
        return f"INSERT INTO {table_name} ({columns}) VALUES ({template_values})"

    def insert(self, data_list: list[dict], table_name: str = "monitor") -> None:
        conn, cursor = None, None
        conn, cursor = self.get_connetion()
        try:
            query = self.get_query_insert(table_name, data_list[0])
            cursor.executemany(query, data_list)
            conn.commit()
            self.logger.info("All rows were inserted")
        except Exception as e:
            raise e
        finally:
            if conn:
                cursor.close()
                conn.close()
