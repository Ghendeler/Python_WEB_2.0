from configparser import ConfigParser

from sqlalchemy.engine import create_engine


def connect():
    parser = ConfigParser()
    parser.read("config.ini")

    db = {}
    if parser.has_section("postgresql"):
        params = parser.items("postgresql")
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format("postgresql", "config.ini")
        )

    database = db["database"]
    host = db["host"]
    user = db["user"]
    password = db["password"]
    port = db["port"]

    connection = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    engine = create_engine(connection, echo=True)
    return engine


if __name__ == "__main__":
    connect()
