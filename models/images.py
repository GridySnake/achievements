class Images:
    @staticmethod
    async def create_image(path: str, image_type: str, conn):
        image_id = await conn.fetchrow("""select max(image_id) from images""")
        image_id = dict(image_id)['max']
        if image_id is not None:
            image_id += 1
        else:
            image_id = 0
        await conn.execute(f"""
                               insert into images(image_id, href, image_type, create_date) values(
                               {image_id}, '{path}', '{image_type}', statement_timestamp())
                            """)
        return image_id

    @staticmethod
    async def remove_image(image_id: int, conn):
        pathname = await conn.fetchrow(f"""select directory, href
                                            from images as i
                                            left join images_directories as id on i.image_type = id.image_type
                                            where image_id = {image_id}
                                            """)
        await conn.execute(f"""
                                delete from images
                                where image_id = {image_id}
                                """)
        return pathname
