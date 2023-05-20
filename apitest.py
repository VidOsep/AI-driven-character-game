import openai

# Set up your OpenAI API credentials
openai.api_key = ''

# Define a function to send a message to the chat model
def send_message(message):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None,
        timeout=30,
    )

    if response.choices:
        return response.choices[0].text.strip()

    return None

# Main chat loop
while True:
    user_input = input("User: ")

    # Send user message to the chat model
    response = send_message(user_input)

    if response:
        print("ChatGPT: " + response)
    else:
        print("ChatGPT: Sorry, I didn't understand that.")
