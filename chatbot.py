import re
import respond as long
import wikipedia

# Function to check for adult content using regular expressions
def check_for_adult_content(message):
    # Define regular expression patterns for adult content
    adult_patterns = [
        r"\bsex\b",
        r"\badult\b",
        r"\bNSFW\b",
        r"\bporn\b",
        r"\bxxx\b",
        # Add more patterns as needed
    ]
    
    # Check if any of the patterns match the message
    for pattern in adult_patterns:
        if re.search(pattern, message):
            return True
    return False

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])

    # Longer responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    # Check for Wikipedia search
    if 'tell me about' in ' '.join(message):
        query = ' '.join(message).replace('tell me about', '').strip()
        try:
            summary = wikipedia.summary(query, sentences=2)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options
            return f"Can you be more specific? I found multiple options: {', '.join(options)}"
        except wikipedia.exceptions.PageError:
            return "Sorry, I couldn't find any information on that topic."

    # Check for adult content
    if check_for_adult_content(' '.join(message)):
        return "The flagged message received"

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match

# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

# Initialize Wikipedia
wikipedia.set_lang("en")

# Testing the response system
while True:
    user_input = input('You: ')
    response = get_response(user_input)
    print('Bot:', response)








