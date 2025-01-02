import os


def create_database_url(
        db_host: str = os.getenv("POSTGRES_SERVER"),
        db_port: str = os.getenv("POSTGRES_PORT"),
        db_user: str = os.getenv("POSTGRES_USER"),
        db_name: str = os.getenv("POSTGRES_DB"),
        password_file_path: str = os.getenv("POSTGRES_PASSWORD_FILE"),
) -> str:
    password_file = open(password_file_path, "r")
    db_password = password_file.read()[:-1]
    password_file.close()
    return f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
