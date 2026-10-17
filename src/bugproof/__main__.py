import uvicorn

from bugproof.config import Settings
from bugproof.web import create_app


def main():
    settings = Settings.from_environment()
    uvicorn.run(create_app(settings), host="0.0.0.0", port=settings.port)


if __name__ == "__main__":
    main()
