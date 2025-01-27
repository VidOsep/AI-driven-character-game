from openai import OpenAI

#f = open("key.txt", "r")
#openai.api_key = f.read()

client = OpenAI(api_key="INSERT-KEY-HERE") # here you have to insert the openai API key

class Conversation:
    def __init__(self):
        self.active = True  # is the conversation active or on pause

        self.messages = []  # conversation history

    def setup(self, sys_prompt):
        # a system prompt, comes from the code, not from the player
        self.messages.append({"role": "system", "content": sys_prompt})

    def new_prompt(self, text):
        # after the system prompt follow player interactions
        if not self.active:
            return ""

        self.messages.append({"role": "user", "content": text}) # generate a response from openai api
        chat = client.chat.completions.create(
            model="gpt-4o", messages=self.messages
        )
        reply = chat.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply}) # save it to history

        return reply
