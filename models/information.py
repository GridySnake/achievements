class InfoGet:
    @staticmethod
    async def get_countries(conn):
        countries = await conn.fetch(f"""
        select country_id, country_name_native as country_name
        from countries
        """)
        return [dict(i) for i in countries]

    @staticmethod
    async def get_country_by_iso(iso: str, conn):
        countries = await conn.fetch(f"""
            select country_id, country_name
            from countries
            where country_code = '{iso}'
            """)
        return [dict(i) for i in countries]

    @staticmethod
    async def get_cities(conn):
        cities = await conn.fetch(f"""
            select city_id, city_name, country_id
            from cities
            """)
        return [dict(i) for i in cities]

    @staticmethod
    async def get_cities_by_country(country_id: str, conn):
        cities = await conn.fetch(f"""
                select city_id, city_name
                from cities
                where country_id = {country_id}
                """)
        return [dict(i) for i in cities]

    @staticmethod
    async def get_services(conn):
        services = await conn.fetch(f"""
                    select service_id, service_name
                    from external_services
                    """)
        return [dict(i) for i in services]

    @staticmethod
    async def get_languages(conn):
        languages = await conn.fetch(f"""
                        select language_id, language_native
                        from languages
                        """)
        return [dict(i) for i in languages]

    @staticmethod
    async def get_language_by_id(language_id, conn):
        language = await conn.fetchrow(f"""
                        select language_native
                        from languages
                        where language_id = {language_id}
                        """)
        return language['language_native']

    @staticmethod
    async def get_spheres(conn):
        spheres = await conn.fetch(f"""
                            select distinct sphere_id, sphere_name
                            from spheres
                            """)
        return [dict(i) for i in spheres]

    @staticmethod
    async def get_subspheres(conn):
        subspheres = await conn.fetch(f"""
                                select subsphere_id, subsphere_name, sphere_id
                                from spheres
                                """)
        return [dict(i) for i in subspheres]

    @staticmethod
    async def get_spheres_subspheres_by_id(subspheres_id: list, conn):
        subspheres = await conn.fetch(f"""
                                    select sphere_name, subsphere_name
                                    from spheres
                                    where subsphere_id = any(array{subspheres_id})
                                    """)
        return [dict(i) for i in subspheres]

    @staticmethod
    async def get_sphere_id_by_subsphere_id(subsphere_id: list, conn):
        sphere = await conn.fetchrow(f"""
                                    select sphere_id
                                    from spheres
                                    where subsphere_id = {subsphere_id}
                                    """)
        return sphere['sphere_id']

    @staticmethod
    async def get_subsphere_id_by_sphere_id(sphere_id: str, conn):
        sphere = await conn.fetch(f"""
                                        select subsphere_id::varchar, subsphere_name
                                        from spheres
                                        where sphere_id = {sphere_id}
                                        """)
        return [dict(i) for i in sphere]

    @staticmethod
    async def get_agg_par_by_group_id(group_id: str, conn):
        agg = await conn.fetch(f"""
                                   select distinct aggregate_id::varchar, aggregate_name
                                   from achi_generate_conditions
                                   where condition_group_id = {group_id}
                                   """)
        if len(agg) <= 1:
            parameters = await conn.fetch(f"""
                                               select parameter_id::varchar, parameter_name
                                               from achi_generate_conditions
                                               where condition_group_id = {group_id}
                                               """)
            parameters = [dict(i) for i in parameters]
            agg = None
        else:
            parameters = None
            agg = [dict(i) for i in agg]
        return agg, parameters

    @staticmethod
    async def get_agg_par_by_service_id(service_id: str, conn):
        agg = await conn.fetch(f"""
                                   select distinct aggregate_id::varchar, aggregate_name
                                   from achi_generate_conditions
                                   where service_id = {service_id}
                                   """)
        if len(agg) <= 1:
            parameters = await conn.fetch(f"""
                                               select parameter_id::varchar, parameter_name
                                               from achi_generate_conditions
                                               where service_id = {service_id}
                                               """)
            parameters = [dict(i) for i in parameters]
            agg = None
        else:
            parameters = None
            agg = [dict(i) for i in agg]
        return agg, parameters

    @staticmethod
    async def get_par_by_agg_id_group_id(agg_id: str, group_id: str, conn):
        parameters = await conn.fetch(f"""
                                          select parameter_id::varchar, parameter_name
                                          from achi_generate_conditions
                                          where condition_group_id = {group_id} and aggregate_id = {agg_id}
                                          """)
        return [dict(i) for i in parameters]

    @staticmethod
    async def get_conditions_by_parameter(parameter_id: str, conn):
        condition = await conn.fetchrow(f"""
                                         select condition_group_id, aggregate_id
                                         from achi_generate_conditions
                                         where parameter_id = {parameter_id}
                                      """)
        return condition

    @staticmethod
    async def get_par_by_agg_id_group_id_service(agg_id: str, group_id: str, service_id: str, conn):
        parameters = await conn.fetch(f"""
                                              select parameter_id::varchar, parameter_name
                                              from achi_generate_conditions
                                              where condition_group_id = {group_id} 
                                                and aggregate_id = {agg_id} and service_id = {service_id}
                                              """)
        return [dict(i) for i in parameters]

    @staticmethod
    async def get_conditions(owner_type: int, conn):
        conditions = await conn.fetch(f"""
                                            select generate_condition_id, condition_name
                                            from generate_conditions
                                            where owner_type = {owner_type}
                                        """)
        return [dict(i) for i in conditions]
