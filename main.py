from dotenv import load_dotenv
import os
import logging
from madlibs_prompts.madlibs_app import MadLibsApp
from image_model.dreamlook_trained.run_lora import MadLibsLoRA


def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("LiteLLM").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)
    return logger


if __name__ == "__main__":
    logger = setup_logging()
    load_dotenv()

    # Change this line to the exact variable name in your .env
    api_key = os.environ["GOOGLE_API_KEY"]

    logger.info("Starting main process")
    app = MadLibsApp(api_key=api_key)
    lora = MadLibsLoRA(
        local_lora_path="image_model\dreamlook_trained\models\lora_ukj_style.safetensors"
    )

    topic = input("Enter a topic: ")

    madlib, comic_prompt = app.generate_madlib(topic=topic)
    print(madlib)
    print(comic_prompt.comic_prompt)
    # Uncomment this if you'd like to run lora
    # Beware: there are still a ton of issues that I need to fix. It will most likely not work right, if at all
    # lora.run(prompt=madlib)
