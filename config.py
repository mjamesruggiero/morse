import os
import logging

logging.basicConfig(level=logging.INFO, format="%(lineno)d\t%(message)s")


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    #port = 54321 if host == "localhost" else 5432
    port = 5432
    password = os.environ.get("DB_PASSWORD", "abc123")
    user, db_name = "allocation", "allocation"
    uri = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    logging.debug(f"postgresql URI -> {uri}")
    return uri


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"
