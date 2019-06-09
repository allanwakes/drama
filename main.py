from sanic import Sanic
from sanic.response import json
from count_words import get_nicename
from asyncpg import create_pool

from utils import PGWrapper

app = Sanic()


@app.listener('before_server_start')
async def init(app, loop):
    app.pg_pool = await create_pool(
        dsn="postgresql://demo:password@127.0.0.1:5432/demo", min_size=5, max_size=10, loop=loop)
    app.pg = PGWrapper(app.pg_pool)


@app.listener('after_server_stop')
async def finish(app, loop):
    await app.pg_pool.close()


@app.route("/task", methods=["GET", ])
async def test(request):
    circulator = request.args.get('address')
    endwith = request.args.get('endwith')
    if not circulator or not endwith:
        return json({"status": 500, "message": "wrong parameters"})

    pg = request.app.pg
    value = await pg.fetchrow(
        '''
        SELECT i.status from issue_token_project as i
        WHERE i.circulator = $1
        ''', circulator
    )
    if value:
        return json({"status": 200, "data": value.get("status")})
    else:
        await pg.execute(
            '''
            INSERT INTO issue_token_project(circulator, issuer, issuer_sk, status) VALUES($1, $2, $3, $4)
            ''', circulator, None, None, 0
        )
        get_nicename.send(endwith, circulator)
        return json({"status": 200, "data": "project created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
