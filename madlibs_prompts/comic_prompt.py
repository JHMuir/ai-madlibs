import dspy


class ComicPromptSignature(dspy.Signature):
    completed_madlibs: str = dspy.InputField(desc="The completed MadLib")
    comic_prompt = dspy.OutputField(
        desc="An enhanced version of the madlibs, suitable for generating a 4 panel comic"
    )
    panel_suggestions = dspy.OutputField(
        desc="Suggestions for how to split the story into 4 coherent sections"
    )


class ComicPromptModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.enhance_prompt = dspy.Predict(ComicPromptSignature)

    def forward(self, completed_madlibs):
        result = self.enhance_prompt(completed_madlibs=completed_madlibs)
        return result
