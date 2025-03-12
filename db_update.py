from redis_connector import RedisConnector
from get_data import METAR


if __name__ == "__main__":

    metar = METAR()
    metar.get_all_metar_gzip()

    redis = RedisConnector()

    for row in metar.data:
        airport = row["station_id"].strip()
        data = {key: value for key, value in row.items() if key not in ["raw_text", "station_id"]}
        redis.set(airport, data)