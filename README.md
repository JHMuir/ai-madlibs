# Set-Up
Make sure you have Python installed! Preferably through Miniconda. 
When you clone the repository, you may need to pull the lora model using:

```git lfs pull```

Install the requirements using:

```pip install requirements.txt```

You will need to create a .env file with your AI Provider API key. Depending on your provider, you may need to make changes to both main.py and madlibs_prompts\madlibs_app.py. I've made comments on both files on how to configure both different providers.

The LoRA model should work as expected, but I was unable to run inference on it... not sure what's going on. The line that runs the the prompt through LoRA in main.py is commented out. If you'd like to test it, uncomment it. 

To run this program, call the main file from the terminal with:

```python ./main.py```
