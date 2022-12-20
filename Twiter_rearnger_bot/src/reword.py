

import os 
import openai


API_KEY_OPEN_AI = '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'


openai.api_key = API_KEY_OPEN_AI
def ReArrange(InputText):
    OutputText = ''
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="reword the text below\n"+str(InputText),
    temperature=0.7,
    max_tokens=64,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )
    OutputText = response["choices"][0]["text"]
    return OutputText

