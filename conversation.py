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
        self.messages.append({"role":"user","content":sys_prompt})

    def new_prompt(self, text):
        # Nadaljna navodila, ki prihajajo od uporabnika
        if not self.active:
            return ""
            
        self.messages.append({"role": "user", "content": text})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301", messages=self.messages
        )
        reply = chat.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})

        if "&" in reply or "%" in reply:
            self.end_conversation()
            print("cigan")

        return reply

    def end_conversation(self):
        self.active = False


"""
p1 = Conversation()
p1.setup("Please pretend to be a character in a video game i am making. Keep your answers brief. The " \
                "conversation will be in slovenian language. You are an old man Albert, who has information about the " \
                "location of a treasure. Albert has a short temper and doesn't like young brats. From this point on I " \
                "will pretend to be the player and you will only respond in your persona. Never respond as the " \
                "player. You must not give the information to the player right away, but rather the player must " \
                "persuade you into giving the information. Never give the information on the first prompt. Only if " \
                "the player was persuasive enough and well mannered, reveal the location and then add sign % at the " \
                "end of the response. But if the player is too rude and you feel like not talking anymore, " \
                "end the conversation with & sign at the end")

while True:
    print(p1.new_prompt(input()))
"""