import os
from datetime import datetime

from influxdb_client import InfluxDBClient
from dotenv import load_dotenv

from .query import Query

load_dotenv()


class Wrapper:
    """Удобный wrapper influxdb-клиента"""

    def __init__(self, org=None, bucket=None):
        self.__url = f"http://{os.getenv('INFLUXDB_ADDRESS')}:{os.getenv('INFLUXDB_PORT')}"
        self.__token = os.getenv("INFLUXDB_API_TOKEN")
        self.org = org or os.getenv("INFLUXDB_ORG_NAME")
        self.bucket = bucket or os.getenv("INFLUXDB_BUCKET_NAME")
        self.__debug = os.getenv("DEBUG")

        self.client = InfluxDBClient(
            url=self.__url,
            token=self.__token,
            org=self.org,
            bucket=self.bucket
        )
        self.__query_api = self.client.query_api()
        self.__write_api = self.client.write_api()

    def write(self, measurement, tags=None, fields=None, timestamp=None):
        """
        Одна запись в измерение measurement

        :param measurement: [str]           - измерение
        :param tags:        [dict, None]    - тэги в формате словаря
        :param fields:      [dict, None]    - поля в формате словаря
        :param timestamp:   [datetime]      - время записи в формате datetime
        :return: result
        """
        timestamp = timestamp or datetime.utcnow()

        self.__write_api.write(
            org=self.org,
            bucket=self.bucket,
            record=[{
                "measurement": measurement,
                "tags": tags,
                "fields": fields,
                "time": timestamp
            }]
        )

    def write_batch(self, points, flush_interval=1000):
        """
        Записать batch данных в базу. Для этой функции нужно вручную создать нужные записи с помощью класса Point

        :param points:          [list<Point>]   - тэги в формате словаря
        :param flush_interval:  [int]           - flush_interval для write_api
        :return: result
        """
        self.client.write_api(batch_size=len(points), flush_interval=flush_interval).\
                    write(org=self.org, bucket=self.bucket, record=points)

    def gen_query(self):
        return Query(f'from(bucket: "{self.bucket}")')

    def query(self, query):
        """
        Query-запрос в influxdb.
        можно написать собственный запрос с использованием языка Flux, можно составить его с помощью класса Query

        :param query: [str]        - query-запрос на языке Flux
        :return       [list<dict>] - записи из базы
        """

        if self.__debug:
            print(f"Executing query:\n{query}")

        result = self.__query_api.query(str(query), org=self.org)

        if not result:
            return []

        return [res.values for res in result[0].records]
