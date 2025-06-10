from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from pathlib import Path


class MadLibsImage:
    def __init__(
        self, api_key: str, model: str = "gemini-2.0-flash-preview-image-generation"
    ):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(
        self, image_prompt: str, output_path: str = "madlibs_generated_image.png"
    ) -> str:
        base_style = """
        Create a simple, cartoon-style illustration in the classic MadLibs book art style with these characteristics:
        - Simple, clean line art with black outlines
        - Bright, vibrant colors (primary and secondary colors)
        - Whimsical, family-friendly cartoon aesthetic
        - Clear, easy-to-read visual composition
        - Simple character designs with exaggerated expressions
        - Minimal background details, focus on main subjects
        - Flat color style (no complex shading or gradients)
        - Similar to children's book illustrations or educational materials
        """

        story_prompt = f"\nIllustrate this story: {image_prompt}"

        technical_instructions = """
        Technical requirements:
        - Use bold, clear colors
        - Keep composition simple and uncluttered
        - Make sure all elements are clearly visible
        - Use a style similar to 1990s educational cartoon illustrations
        - Avoid photorealistic details
        - Focus on clarity and readability over artistic complexity
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"{base_style}\n{story_prompt}\n{technical_instructions}",
            config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
        )

        saved = False
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                image = Image.open(BytesIO((part.inline_data.data)))
                image.save(output_path)
                saved = True
        if saved:
            return Path(output_path)
        else:
            raise Exception("No image generated")
