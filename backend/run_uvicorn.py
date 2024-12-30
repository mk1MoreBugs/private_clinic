import uvicorn

from app.main import app

CONFIG = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="debug",
        reload=True,
    )


if __name__ == "__main__":

    server = uvicorn.Server(CONFIG)
    server.run()
