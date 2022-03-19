class InfoGet:
    @staticmethod
    async def get_countries(conn):
        countries = await conn.fetch(f"""
        select country_id, country_name
        from countries
        """)
        return countries

    @staticmethod
    async def get_country_by_iso(iso: str, conn):
        countries = await conn.fetch(f"""
            select country_name
            from countries
            where country_code = '{iso}'
            """)
        return countries

    @staticmethod
    async def get_cities(conn):
        cities = await conn.fetch(f"""
            select city_id, city_name, country_id
            from cities
            """)
        return cities

    @staticmethod
    async def get_cities_by_country(country_id: str, conn):
        cities = await conn.fetch(f"""
                select city_id, city_name
                from cities
                where country_id = {country_id}
                """)
        return cities

    @staticmethod
    async def get_services(conn):
        services = await conn.fetch(f"""
                    select service_id, service_name
                    from external_services
                    """)
        return services

    @staticmethod
    async def get_languages(conn):
        languages = await conn.fetch(f"""
                        select language_id, language_native
                        from languages
                        """)
        return languages

    @staticmethod
    async def get_language_by_id(language_id, conn):
        language = await conn.fetch(f"""
                        select language_native
                        from languages
                        where language_id = {language_id}
                        """)
        return language

    @staticmethod
    async def get_spheres(conn):
        spheres = await conn.fetch(f"""
                            select distinct sphere_id, sphere_name
                            from spheres
                            """)
        return spheres

    @staticmethod
    async def get_subspheres(conn):
        subspheres = await conn.fetch(f"""
                                select subsphere_id, subsphere_name, sphere_id
                                from spheres
                                """)
        return subspheres

    @staticmethod
    async def get_spheres_subspheres_by_id(subspheres_id: list, conn):
        subspheres = await conn.fetch(f"""
                                    select sphere_name, subsphere_name
                                    from spheres
                                    where subsphere_id = any(array{subspheres_id})
                                    """)
        return subspheres

    @staticmethod
    async def get_sphere_id_by_subsphere_id(subsphere_id: list, conn):
        sphere = await conn.fetchrow(f"""
                                    select sphere_id
                                    from spheres
                                    where subsphere_id = {subsphere_id}
                                    """)
        return sphere['sphere_id']

    @staticmethod
    async def get_conditions(owner_type: int, conn):
        conditions = await conn.fetch(f"""
                                            select generate_condition_id, condition_name
                                            from generate_conditions
                                            where owner_type = {owner_type}
                                        """)
        return conditions
