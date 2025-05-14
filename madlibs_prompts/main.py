import uvicorn


class MadlibsApp:
    def __init__(self):
        pass

    def _setup_routes(self):
        pass

    def run(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        uvicorn.run(self.app, host=host, port=port)
