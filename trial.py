import openai

openai.api_key = "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"

def detect_adult_content(message):
    # Using OpenAI's content filter model to detect adult content
    response = openai.Completion.create(
        engine="content-filter-alpha-c4",
        prompt=message,
        max_tokens=1
    )
    # Check the model's output for adult content
    if "2" in response.choices[0].text:
        return True
    else:
        return False

messages = []
system_msg = input("Hii How are you?\n")
messages.append({"role": "system", "content": system_msg})

print("Your new assistant is ready!")

while True:
    message = input()
    messages.append({"role": "user", "content": message})
    
    # Check if the user input contains adult content
    if detect_adult_content(message):
        print("Assistant: Flagged Message")
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        print("Assistant:", reply)

    if message.lower() == "quit()":
        break
