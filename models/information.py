import asyncpg
from config.common import BaseConfig
connection_url = BaseConfig.database_url


class Info:
    @staticmethod
    async def get_countries():
        conn = await asyncpg.connect(connection_url)
        countries = await conn.fetch(f"""
        SELECT country_id, country_name
        FROM countries
        """)
        return countries

    @staticmethod
    async def get_cities():
        conn = await asyncpg.connect(connection_url)
        cities = await conn.fetch(f"""
            SELECT city_id, city_name
            FROM cities
            """)
        return cities

    @staticmethod
    async def get_cities_by_country(country_id: str):
        conn = await asyncpg.connect(connection_url)
        cities = await conn.fetchrow(f"""
                SELECT city_id, city_name
                FROM cities
                WHERE country_id = {country_id}
                """)
        return cities

