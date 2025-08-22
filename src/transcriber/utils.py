import requests


def backend_factory() -> requests.Session:
    session = requests.Session()
    session.verify = False
    return session
