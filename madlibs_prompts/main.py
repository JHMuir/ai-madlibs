from dotenv import load_dotenv
import os

from madlibs_app import MadLibsApp

if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ["GOOGLE_API_KEY"]

    app = MadLibsApp(api_key=api_key)

    topic = input("Enter a topic: ")

    try:
        madlib, comic_prompt = app.generate_madlib(topic=topic)
        print(madlib)
        print(comic_prompt)
    except Exception as e:
        print(f"Error: {e}")
