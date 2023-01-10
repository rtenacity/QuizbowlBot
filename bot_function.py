import qbreader
import re
import nltk
import secrets

def generate_token():
    return secrets.token_hex(16)

def search_list(string_list):
    results = []
    for s in string_list:
        if re.search(r'[-\d]', s):  # check if s contains a hyphen or a digit
            results.append(s)
    return results

def split_difficulty(difficulty_input):
    difficulty_input_str_list = difficulty_input.split("-")
    difficulty_input_list = [int(x) for x in difficulty_input_str_list]
    return difficulty_input_list

def split_categories(categories_input):
    categories_cleaned = categories_input.replace(" ", "")
    categories_input_str_list = categories_cleaned.split(",")
    categories_input_list = [x.capitalize() for x in categories_input_str_list]
    return categories_input_list

def fetch_question(categories=[], difficulty_array=[]):
    l = qbreader.random_question("bonus", difficulty_array, categories)
    question_dict = {}
    question_dict['leadin'] = l[0]['leadin']
    question_dict['parts'] = l[0]['parts']
    question_dict['answers'] = l[0]['answers']
    question_dict['category'] = l[0]['category']
    question_dict['difficulty'] = l[0]['difficulty']
    question_dict['setName'] = l[0]['setName']
    return question_dict

def remove_bracketed(string):
    # Use a regular expression to match and capture items enclosed in brackets or parentheses
    pattern = r'\[[^\]]*\]|\([^\)]*\)'
    return re.sub(pattern, '', string)


#    correct_answer = remove_bracketed(correct_answer)
def is_close_answer(response, correct_answer, threshold=0.1):
    # Tokenize the correct answer and remove stop words
    stop_words = set(nltk.corpus.stopwords.words("english"))
    correct_answer = correct_answer.lower()
    response = response.lower()
    correct_answer_words = [word for word in correct_answer.split() if word.lower() not in stop_words]
    # Split the response into a list of words
    response_words = response.split()
    num_matching_words = 0
    # Calculate the number of words that match between the correct answer and the response
    for correct_answer_word in correct_answer_words:
        # Iterate over the words in the response
        for response_word in response_words:
            # If the words match or are close enough (e.g. differ by one letter), increment the counter
            if correct_answer_word == response_word or nltk.edit_distance(correct_answer_word, response_word) == 2:
                num_matching_words += 1
                break  # Break out of the inner loop so we don't count the same word multiple times
    # Calculate the ratio of matching words to total words in the correct answer
    matching_ratio = num_matching_words / len(correct_answer_words)
    # Return True if the matching ratio is above the threshold, False otherwise
    return matching_ratio >= threshold
#This modified function first removes any stop words from the correct answer using the nltk library, and then compares the remaining words to the words in the response to determine if the response is a "close" answer.

def is_close(response, correct_answer):
    correct_words = correct_answer.split()
    for word in response.split():
        if word not in correct_words:
            return False
    return True
