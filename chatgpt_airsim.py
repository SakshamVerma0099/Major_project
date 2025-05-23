import openai
import re
import argparse
from airsim_wrapper import *
import math
import numpy as np
import os
import json
import time
import speech_recognition as sr
parser = argparse.ArgumentParser()
parser.add_argument("--prompt", type=str, default="C:/class work/NLP/codes/airsim_basic.txt")
parser.add_argument("--sysprompt", type=str, default="C:/class work/NLP/codes/airsim_basic.txt")
args = parser.parse_args()
recognizer = sr.Recognizer()
with open("config.json", "r") as f:
    config = json.load(f)

print("Initializing ChatGPT...")
openai.api_key = config["OPENAI_API_KEY"]

with open(args.sysprompt, "r") as f:
    sysprompt = f.read()

chat_history = [
    {
        "role": "system",
        "content": sysprompt
    },
    {
        "role": "user",
        "content": "move 10 units up"
    },
    {
        "role": "assistant",
        "content": """```python
aw.fly_to([aw.get_drone_position()[0], aw.get_drone_position()[1], aw.get_drone_position()[2]+10])
```

This code uses the `fly_to()` function to move the drone to a new position that is 10 units up from the current position. It does this by getting the current position of the drone using `get_drone_position()` and then creating a new list with the same X and Y coordinates, but with the Z coordinate increased by 10. The drone will then fly to this new position using `fly_to()`."""
    }
]
def listen_for_speech():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for speech...")

        while True:
            try:
                # Listen to the audio
                audio = recognizer.listen(source)
                print("Recognizing...")

                # Recognize speech using Google's speech recognition API
                text = recognizer.recognize_google(audio)
                print("You said: ", text)
                return text  # Return recognized text if successful
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio. Trying again...")
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service. Trying again...")
            except KeyboardInterrupt:
                print("Program interrupted.")
                break  

def ask(prompt):
    chat_history.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
        temperature=0
    )
    chat_history.append(
        {
            "role": "assistant",
            "content": completion.choices[0].message.content,
        }
    )
    return chat_history[-1]["content"]


print(f"Done.")

code_block_regex = re.compile(r"```(.*?)```", re.DOTALL)


def extract_python_code(content):
    code_blocks = code_block_regex.findall(content)
    if code_blocks:
        full_code = "\n".join(code_blocks)

        if full_code.startswith("python"):
            full_code = full_code[7:]

        return full_code
    else:
        return None


class colors:  # You may need to change color settings
    RED = "\033[31m"
    ENDC = "\033[m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"


print(f"Initializing AirSim...")
aw = AirSimWrapper()
print(f"Done.")

with open(args.prompt, "r") as f:
    prompt = f.read()

ask(prompt)
print("Welcome to the AirSim chatbot! I am ready to help you with your AirSim questions and commands.")

while True:
    question = listen_for_speech()

    if question == "!quit" or question == "!exit":
        break

    if question == "!clear":
        os.system("cls")
        continue

    response = ask(question)

    print(colors.YELLOW + "Chat GPT> ", question+ colors.ENDC)
    print(colors.GREEN + response + colors.ENDC)
    code = extract_python_code(response)
    if code is not None:
        print("Please wait while I run the code in AirSim...")
        exec(extract_python_code(response))
        print(colors.RED + "Done!\n" + colors.ENDC)