import openai

f = open("key.txt", "r")
openai.api_key = f.read()

class Conversation:
    def __init__(self):
        # Pogovor poteka
        self.active = True

        # Sistem kratkorocnega spomina
        self.mem_len = 3
        self.past_prompts = []

        self.pre_prompt = ""

    def new_prompt(self, text):
        if not self.active:
            return ""
        # Poslji preprompt, past_prompts in text skupaj
        message = self.pre_prompt+"".join(self.past_prompts)+text
        response = send_message(message)

        if "&" in response:
            self.end_conversation()

        if len(self.past_prompts) >= self.mem_len: # Ce je spomin maksimalno zaseden, pozabi prvi element
            self.past_prompts.pop(0)
        self.past_prompts.append(text+response+"\n")
        return response
    def end_conversation(self):
        self.active = False
def send_message(message):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
        timeout=30,
    )

    if response.choices:
        return response.choices[0].text.strip()

    return None

p1 = Conversation()
p1.pre_prompt = "Please pretend to be a character in a video game i am making. Keep your answers brief. The " \
                "conversation will be in slovenian language. You are an old man Albert, who has information about the " \
                "location of a treasure. Albert has a short temper and doesn't like young brats. From this point on I " \
                "will pretend to be the player and you will only respond in your persona. Never respond as the " \
                "player. You must not give the information to the player right away, but rather the player must " \
                "persuade you into giving the information. Never give the information on the first prompt. Only if " \
                "the player was persuasive enough and well mannered, reveal the location and then add sign % at the " \
                "end of the response. But if the player is too rude and you feel like not talking anymore, " \
                "end the conversation with & sign at the end."

while True:
    text = "Player: " + input() + ".\n"
    print(p1.past_prompts)
    print(p1.new_prompt(text))