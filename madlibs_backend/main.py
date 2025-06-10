from dotenv import load_dotenv
import os
import logging

# from madlibs_module.madlibs_generator import MadLibsGenerator
# from madlibs_module.madlibs_image import MadLibsImage
from madlibs_module.madlibs_api import MadLibsAPI


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
    api = MadLibsAPI(api_key=api_key)
    api.run()
    # app = MadLibsGenerator(api_key=api_key)
    # # lora = MadLibsLoRA(
    # #     local_lora_path="image_model\dreamlook_trained\models\lora_ukj_style.safetensors"
    # # )
    # image_gen = MadLibsImage(api_key=api_key)
    # topic = input("Enter a topic: ")

    # madlib, comic_prompt = app.generate_madlib(topic=topic)
    # print(madlib)
    # print(comic_prompt.comic_prompt)
    # image_gen.generate(madlib)
    # Uncomment this if you'd like to run lora
    # Beware: there are still a ton of issues that I need to fix. It will most likely not work right, if at all
    # lora.run(prompt=madlib)
