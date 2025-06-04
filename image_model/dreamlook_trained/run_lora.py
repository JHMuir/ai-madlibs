import torch
from diffusers import StableDiffusionXLPipeline


class MadLibsLoRA:
    def __init__(self, local_lora_path: str):
        print("Intializing MadLibsLoRA....")
        self.pipeline = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            use_safetensors=True,
        )
        self.pipeline.load_lora_weights(local_lora_path)
        print("MadLibsLoRA successfully initialized")

    def run(self, prompt: str, save_path: str = "output.txt"):
        image = self.pipeline(
            prompt=f"4 panel comic in ukj style:\n {prompt}", num_inference_steps=30
        ).images[0]
        image.save(save_path)
