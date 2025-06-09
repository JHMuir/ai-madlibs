import torch
from diffusers import StableDiffusionXLPipeline
import logging


class MadLibsLoRA:
    def __init__(self, local_lora_path: str):
        logging.info("Intializing MadLibsLoRA....")
        self.pipeline = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            use_safetensors=True,
        )
        self.pipeline.load_lora_weights(local_lora_path)
        logging.info("MadLibsLoRA successfully initialized")

    def run(self, prompt: str, save_path: str = "output.txt"):
        image = self.pipeline(
            prompt=f"4 panel comic in ukj style:\n {prompt}", num_inference_steps=30
        ).images[0]
        image.save(save_path)


# 1: Prewritten daily madlib -> spaces. 5-6 predetemined spaces
# 2: Prewritten FULL madlib -> finds 5-6 adj, nouns, verbs, replaces with spaces
# 3: Classic madlibs -> words only, no context
# 4: Fully generated
#
# -> Image model
# "Every morning, the [adjective] [noun] jumps over the [adjective] [animal] to get to the [place] before breakfast."
#
#
