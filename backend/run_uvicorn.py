import uvicorn

from app.main import app

CONFIG = uvicorn.Config(
        app,
        host="localhost",
        port=8080,
        log_level="debug",
    )


if __name__ == "__main__":

    server = uvicorn.Server(CONFIG)
    server.run()
