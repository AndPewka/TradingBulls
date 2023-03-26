import os
from datetime import datetime

from influxdb_client import InfluxDBClient
from dotenv import load_dotenv

load_dotenv()


class InfluxdbWrapper:
    """Удобный wrapper influxdb-клиента"""

    def __init__(self, org=None, bucket=None):
        self.url = f"http://{os.getenv('INFLUXDB_ADDRESS')}:{os.getenv('INFLUXDB_PORT')}"
        self.token = os.getenv("INFLUXDB_API_TOKEN")
        self.org = org or os.getenv("INFLUXDB_ORG_NAME")
        self.bucket = bucket or os.getenv("INFLUXDB_BUCKET_NAME")

        self.client = InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org,
            bucket=self.bucket
        )
        self.query_api = self.client.query_api()
        self.write_api = self.client.write_api()

    def write(self, measurement, tags=None, fields=None, timestamp=None):
        """
        Записать данные в измерение measurement

        :param measurement: [str]           - измерение
        :param tags:        [dict, None]    - тэги в формате словаря
        :param fields:      [dict, None]    - поля в формате словаря
        :param timestamp:   [datetime]      - время записи в формате datetime
        :return: result
        """
        timestamp = timestamp or datetime.utcnow()

        self.write_api.write(
            org=self.org,
            bucket=self.bucket,
            record=[{
                "measurement": measurement,
                "tags": tags,
                "fields": fields,
                "time": timestamp
            }]
        )

    def get_from_measurement(
            self,
            measurement,
            last_hours=24,
            filters=None,
            keep_tags=None,
            desc=False,
            limit=None,
            debug=False,
    ):
        """
        Простой query-запрос с получением данных из бд
        Для более сложных можно написать свой query-запрос на языке flux и выполнить с помощью метода query

        :param measurement: [str]               - таблица с измерениями
        :param last_hours:  [int]               - фильтр по времени (берутся записи за последние last_hours часов)
        :param filters:     [dict, None]        - дополнительные фильтры в виде словаря (<тег/поле>: <значение>)
        :param keep_tags:   [list, None]        - список тэгов, которые нужно оставить в результате
        :param desc:        [bool]              - сортировка desc
        :param limit:       [int, None]         - ограничение по количеству записей
        :param debug:       [bool]              - при значении True печатается query запрос
        :return:            [list[dict]]        - список совпадающиих записей из бд в формате словаря
        """

        keep_string = '|> keep(columns: ' + self.stringify(
            ["_field", "_value", "_time"] + keep_tags
        ) + ")" if keep_tags else ''
        filter_string = '|> filter(fn: (r) => ' + " and ".join(
            [f'r["{key}"] == "{value}"' for key, value in filters.items()]
        ) + ")" if filters else ""
        order_string = f'|> sort(columns: ["time"], desc: true)' if desc else ''
        limit_string = f'|> limit(n: {limit})' if limit else ''

        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: -{last_hours}h)
          |> filter(fn: (r) => r["_measurement"] == "{measurement}")
          {filter_string}
          {keep_string}
          {order_string}
          {limit_string}
        '''

        if debug:
            print(f"Executing query: {query}")

        result = self.query(query)

        if not result:
            return []

        return [res.values for res in self.query(query)[0].records]

    def query(self, query):
        """
        Query-запрос в influxdb.
        Когда функционала метода get_from_measurement недостаточно для составления запроса,
        можно написать собственный запрос с использованием языка Flux

        :param query:   [str]   - query-запрос на языке Flux
        :return result
        """
        return self.query_api.query(query, org=self.org)

    @staticmethod
    def stringify(obj):
        return str(list(obj)).replace("'", '"')
