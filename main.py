from dotenv import load_dotenv
import os

from madlibs_prompts.madlibs_app import MadLibsApp
from image_model.dreamlook_trained.run_lora import MadLibsLoRA

if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ["GOOGLE_API_KEY"]

    app = MadLibsApp(api_key=api_key)
    lora = MadLibsLoRA(
        local_lora_path="image_model\dreamlook_trained\models\lora_ukj_style.safetensors"
    )

    topic = input("Enter a topic: ")

    madlib, comic_prompt = app.generate_madlib(topic=topic)
    print(madlib)
    print(comic_prompt.comic_prompt)
    print(type(comic_prompt.comic_prompt))
    lora.run(prompt=madlib)
