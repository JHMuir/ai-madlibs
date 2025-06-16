from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict
import os
import logging
import uuid
from pathlib import Path
from madlibs_module.madlibs_generator import MadLibsGenerator
from madlibs_module.madlibs_image import MadLibsImage

logger = logging.getLogger(__name__)


class TopicRequest(BaseModel):
    topic: str


class MadLibsTemplate(BaseModel):
    template_id: str
    template: str
    word_types: List[str]
    topic: str


class UserInputsRequest(BaseModel):
    template_id: str
    user_inputs: Dict[str, str]  # {word_type: user_input}


class CompletedMadLib(BaseModel):
    madlib_id: str
    completed_text: str
    comic_prompt: str
    panel_suggestions: str


class ImageGenerationRequest(BaseModel):
    madlib_id: str


class MadLibsAPI:
    def __init__(self, api_key: str):
        self.app = FastAPI(title="MadLibs API", version="0.0.1")
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # In production, specify your frontend URL
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.api_key = api_key
        self.text_generator = MadLibsGenerator(api_key=self.api_key)
        self.image_generator = MadLibsImage(api_key=self.api_key)
        self.templates_store: Dict[str, dict] = {}
        self.madlibs_store: Dict[str, dict] = {}
        self.image_dir = Path("generated_images")
        self.image_dir.mkdir(exist_ok=True)
        self.setup_routes()

    def setup_routes(self):
        self.app.get("/")(self.root)
        self.app.post("/api/generate-template")(self.generate_template)
        self.app.post("/api/submit-madlib")(self.submit_madlib)
        self.app.post("/api/generate-image")(self.generate_image)
        self.app.get("/api/images/{image_filename}")(self.get_image)
        self.app.get("/api/health")(self.health_check)

    async def root(self):
        return {"message": "MadLibs API is Running!"}

    async def generate_template(self, request: TopicRequest):
        try:
            logger.info(f"Generating template for topic: {request.topic}")

            # Generate the template using your existing code
            result = self.text_generator.madlibs_generator(request.topic)

            # Create unique ID for this template
            template_id = str(uuid.uuid4())

            # Store template data
            self.templates_store[template_id] = {
                "template": result.template,
                "word_types": result.word_types,
                "topic": request.topic,
            }

            return MadLibsTemplate(
                template_id=template_id,
                template=result.template,
                word_types=result.word_types,
                topic=request.topic,
            )

        except Exception as e:
            logger.error(f"Error generating template: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    async def submit_madlib(self, request: UserInputsRequest):
        try:
            # Retrieve template
            if request.template_id not in self.templates_store:
                raise HTTPException(status_code=404, detail="Template not found")

            template_data = self.templates_store[request.template_id]

            # Convert user inputs to list in correct order
            user_inputs_list = [
                request.user_inputs.get(word_type, "")
                for word_type in template_data["word_types"]
            ]

            # Fill the template =========================================== FIX???
            completed_madlib = self.text_generator.fill_template(
                template=template_data["template"],
                placeholder_words=template_data["word_types"],
                user_inputs=user_inputs_list,
            )

            # Generate comic prompt
            comic_result = self.text_generator.comicprompt_generator(completed_madlib)

            # Store completed madlib
            madlib_id = str(uuid.uuid4())
            self.madlibs_store[madlib_id] = {
                "completed_text": completed_madlib,
                "comic_prompt": comic_result.comic_prompt,
                "panel_suggestions": comic_result.panel_suggestions,
            }

            return CompletedMadLib(
                madlib_id=madlib_id,
                completed_text=completed_madlib,
                comic_prompt=comic_result.comic_prompt,
                panel_suggestions=comic_result.panel_suggestions,
            )

        except Exception as e:
            logger.error(f"Error completing madlib: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    async def generate_image(self, request: ImageGenerationRequest):
        try:
            # Retrieve madlib data
            if request.madlib_id not in self.madlibs_store:
                raise HTTPException(status_code=404, detail="MadLib not found")

            madlib_data = self.madlibs_store[request.madlib_id]

            # Generate image
            logger.info("Generating image...")

            # Modify the image generator to save with unique filename
            image_filename = f"{request.madlib_id}.png"
            image_path = self.image_dir / image_filename

            # We need to modify the generate method to return the image path
            # For now, we'll use the existing method and assume it saves to a fixed location
            self.image_generator.generate(madlib_data["completed_text"])

            # Move the generated image to our storage location
            import shutil

            if os.path.exists("gemini-native-image.png"):
                shutil.move("gemini-native-image.png", str(image_path))

            return {
                "madlib_id": request.madlib_id,
                "image_url": f"/api/images/{image_filename}",
                "status": "success",
            }

        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    async def get_image(self, image_filename: str):
        """
        Serve generated images
        """
        image_path = self.image_dir / image_filename
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")

        return FileResponse(str(image_path), media_type="image/png")

    # Health check endpoint
    async def health_check(self):
        """Check if the API is healthy and configured properly"""
        return {
            "status": "healthy",
            "api_key_configured": bool(self.api_key),
            "templates_count": len(self.templates_store),
            "madlibs_count": len(self.madlibs_store),
        }

    def run(self):
        import uvicorn

        uvicorn.run(self.app, host="0.0.0.0", port=8000)
