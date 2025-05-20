import os
import uvicorn
from dotenv import load_dotenv

import dspy

load_dotenv()

api_key = os.environ["GOOGLE_API_KEY"]

lm = dspy.LM(model="gemini/gemini-2.0-flash", api_key=api_key)
dspy.configure(lm=lm)


class MadlibsApp:
    def __init__(self):
        pass

    def _setup_routes(self):
        pass

    def run(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        uvicorn.run(self.app, host=host, port=port)
