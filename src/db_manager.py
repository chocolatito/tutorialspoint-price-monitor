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

    def insert(self, data_list: list[dict], table_name: str = "course") -> None:
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

    def insert_or_update_db(self, result: dict):
        key_list = ["sale_price", "list_price", "course_id"]
        conn, cursor = None, None
        conn, cursor = self.get_connetion()
        course_id_tuple = tuple(result)
        query = ("SELECT course_id, sale_price, list_price, hexdigest"
                 f" FROM course WHERE course_id in {course_id_tuple};")
        sql_result = cursor.execute(query)
        rows = {tup for tup in sql_result.fetchall()}
        course_id_tuple = tuple(set(course_id_tuple)-{tup[0] for tup in rows})
        if course_id_tuple:
            try:
                self.insert([result[course_id] for course_id in course_id_tuple])
            except Exception as e:
                self.logger.critical(f"COULD NOT INSERT: {e}")

        rows = {row for row in rows if result[row[0]]["hexdigest"] != row[-1]}
        print(f"len(rows):: {len(rows)}")
        historical_list = []
        for row in rows:
            item = result[row[0]]
            sale_price_flag = item["sale_price"] != row[1]
            list_price_flag = item["list_price"] != row[2]
            if any([list_price_flag, sale_price_flag]):
                historical_list.append({k: item[k] for k in key_list})
            set_clause = ", ".join(f"{k} = :{k}" for k in item if k != "course_id")
            query = (f"UPDATE course SET {set_clause}"
                     " WHERE course_id = :course_id")
            try:
                cursor.execute(query, item)
                conn.commit()
            except sqlite3.Error as e:
                conn.rollback()
                print(f"Error al actualizar: {e}")
            finally:
                conn.close()
        if historical_list:
            self.insert(historical_list, "historical")
