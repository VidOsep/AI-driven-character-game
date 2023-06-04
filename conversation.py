import openai

f = open("key.txt", "r")
openai.api_key = f.read()

class Conversation:
    def __init__(self):
        # Pogovor poteka
        self.active = True

        self.messages = []  # Shranjena preteklost pogovora

    def setup(self,sys_prompt):
        # Sistemsko navodilo agentu
        print(sys_prompt)
        self.messages.append({"role":"system","content":sys_prompt})

    def new_prompt(self, text):
        # Nadaljna navodila, ki prihajajo od uporabnika
        if not self.active:
            return ""
            
        self.messages.append({"role": "user", "content": text})
        chat = openai.ChatCompletion.create(
            model="gpt-4-0314", messages=self.messages
        )
        reply = chat.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})

        return reply
