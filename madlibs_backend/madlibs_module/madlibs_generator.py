from .comic_prompt import ComicPromptModule
from .madlibs_template import MadLibsTemplateModule
import dspy
import re
from pprint import pprint
import logging

logger = logging.getLogger(__name__)


class MadlibsMismatchException(Exception):
    pass


class MadLibsGenerator:
    def __init__(self, api_key: str):
        logging.info("Initializing MadLibsApp......")
        lm = dspy.LM(
            # Change the model name here to your specified to provider
            # For example, to change to OpenAI, change it to model="openai/gpt-4o"
            # To view all providers, navigate to https://docs.litellm.ai/docs/providers
            model="gemini/gemini-2.0-flash",
            api_key=api_key,
            cache=False,
            temperature=1.0,
        )
        dspy.configure(lm=lm, api_key=api_key)
        self.madlibs_generator = MadLibsTemplateModule()
        self.comicprompt_generator = ComicPromptModule()
        logging.info("MadLibsApp successfully initialized")

    def generate_madlib(self, topic: str):
        result = self.madlibs_generator(topic)
        template, placeholder_words = result.template, result.word_types
        pprint(template)
        pattern = r"\{([^}]+)\}"
        word_types_needed = re.findall(pattern, template)
        if placeholder_words != word_types_needed:
            logging.error("Mismatch detected between words extracted and words needed")
            raise MadlibsMismatchException(
                "Mismatch between words extracted and words needed"
            )
        user_inputs = self.collect_user_inputs(placeholder_words=placeholder_words)
        completed_madlib = self.fill_template(
            template=template,
            placeholder_words=placeholder_words,
            user_inputs=user_inputs,
        )
        comic_prompt = self.comicprompt_generator(completed_madlib)
        return completed_madlib, comic_prompt

    def collect_user_inputs(self, placeholder_words):
        user_inputs = []
        for word in placeholder_words:
            user_input = input(f"Enter a/an {word}: ")
            user_inputs.append(user_input)
        return user_inputs

    def fill_template(self, template, placeholder_words, user_inputs):
        completed = template

        for word, user_input in zip(placeholder_words, user_inputs):
            placeholder = f"{{{word}}}"
            completed = completed.replace(placeholder, user_input, 1)
        return completed
