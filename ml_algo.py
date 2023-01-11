from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import numpy as np

# Load the trained model
model = load_model('model.h5')

# Prepare the tokenizer
# This will be the set of responses and answers used to train the model
response = input("Enter a response: ")
correct_answer = input("Enter the correct answer: ")

tokenizer = Tokenizer()
tokenizer.fit_on_texts(response + correct_answer)

# Tokenize and pad the response and correct answer
response_sequence = tokenizer.texts_to_sequences([response])
correct_answer_sequence = tokenizer.texts_to_sequences([correct_answer])
max_len = max(len(r) for r in response_sequence + correct_answer_sequence)
response_padded = pad_sequences(response_sequence, 100)
correct_answer_padded = pad_sequences(correct_answer_sequence, 100)

# Concatenate the response and correct answer
X = np.concatenate([response_padded, correct_answer_padded], axis=1)

# Make the prediction
prediction = model.predict(X)

# Print the result
if prediction >= 0.5:
    print("The response is similar to the correct answer.")
else:
    print("The response is not similar to the correct answer.")
