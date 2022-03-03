import uvicorn
from app.internal.drivers.server import FastAPIServer

app = FastAPIServer.get_app()


def run_app(host='localhost', port=8080):
    uvicorn.run("manage:app", host=host, port=int(port), log_level="info")


if __name__ == '__main__':
    run_app()
