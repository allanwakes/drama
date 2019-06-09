class PGWrapper:
    def __init__(self, pg_pool):
        self.pg_pool = pg_pool

    async def fetch(self, sql, *args, **kwargs):
        async with self.pg_pool.acquire() as connection:
            return await connection.fetch(sql, *args, **kwargs)

    async def fetchrow(self, sql, *args, **kwargs):
        async with self.pg_pool.acquire() as connection:
            return await connection.fetchrow(sql, *args, **kwargs)

    async def execute(self, sql, *args, **kwargs):
        async with self.pg_pool.acquire() as connection:
            return await connection.execute(sql, *args, **kwargs)
