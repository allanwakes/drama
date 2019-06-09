import dramatiq
import requests
from dramatiq.brokers.redis import RedisBroker
from stellar_base.keypair import Keypair
import time

from base import Session
from models import Project


redis_broker = RedisBroker(url="redis://localhost:6379/2")
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def count_words(url):
    response = requests.get(url)
    count = len(response.text.split(" "))
    print(f"There are {count} words at {url!r}.")


@dramatiq.actor
def get_nicename(end, circulator):
    start = time.time()
    # candidate = None
    # cd_sk = None
    while True:
        keypair = Keypair.random()
        issuer_pk = keypair.address().decode()
        issuer_sk = keypair.seed().decode()
        if issuer_pk.endswith(end):
            candidate = issuer_pk
            cd_sk = issuer_sk
            break

    print(f"we give a {candidate} in {time.time() - start} seconds.")
    session = Session()
    p = session.query(Project).filter(Project.circulator == circulator).first()
    p.issuer = candidate
    p.issuer_sk = cd_sk
    p.status = 1
    session.commit()
    session.close()


if __name__ == '__main__':
    get_nicename.send("RAY")
