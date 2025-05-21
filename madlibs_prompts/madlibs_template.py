import dspy


class MadLibsTemplateSignature(dspy.Signature):
    topic: str = dspy.InputField(desc="The topic for the MadLibs template")
    template: str = dspy.OutputField(
        desc="A MadLibs template with placeholders for word types. The placeholders should be within curly brackets and all lower case."
    )
    word_types: list[str] = dspy.OutputField(
        desc="A list of the exact placeholder word types used in the template, in the order they were used"
    )


class MadLibsTemplateModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_template = dspy.Predict(MadLibsTemplateSignature)

    def forward(self, topic):
        result = self.generate_template(topic=topic)
        return result
