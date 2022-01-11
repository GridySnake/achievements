import asyncpg
from config.common import BaseConfig
connection_url = BaseConfig.database_url


class InfoGet:
    @staticmethod
    async def get_countries():
        conn = await asyncpg.connect(connection_url)
        countries = await conn.fetch(f"""
        select country_id, country_name
        from countries
        """)
        return countries

    @staticmethod
    async def get_country_by_iso(iso: str):
        conn = await asyncpg.connect(connection_url)
        countries = await conn.fetch(f"""
            select country_name
            from countries
            where country_code = '{iso}'
            """)
        return countries

    @staticmethod
    async def get_cities():
        conn = await asyncpg.connect(connection_url)
        cities = await conn.fetch(f"""
            select city_id, city_name, country_id
            from cities
            """)
        return cities

    @staticmethod
    async def get_cities_by_country(country_id: str):
        conn = await asyncpg.connect(connection_url)
        cities = await conn.fetch(f"""
                select city_id, city_name
                from cities
                where country_id = {country_id}
                """)
        return cities

    @staticmethod
    async def get_services():
        conn = await asyncpg.connect(connection_url)
        services = await conn.fetch(f"""
                    select service_id, service_name
                    from external_services
                    """)
        return services

    @staticmethod
    async def get_languages():
        conn = await asyncpg.connect(connection_url)
        languages = await conn.fetch(f"""
                        select language_id, language_native
                        from languages
                        """)
        return languages

    @staticmethod
    async def get_language_by_id(language_id):
        conn = await asyncpg.connect(connection_url)
        language = await conn.fetch(f"""
                        select language_native
                        from languages
                        where language_id = {language_id}
                        """)
        return language

