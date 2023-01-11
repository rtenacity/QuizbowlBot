import numpy as np
import tensorflow as tf
import json
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Define the dataset
data = [
    {"response": "mars", "answer": "Mars", "correct": True}, 
    {"response": "posidion", "answer": "Neptune (do NOT accept Poseidon)", "correct": False}, 
    {"response": "juno", "answer": "Juno (do NOT accept Hera)", "correct": True}, 
    {"response": "defense of the dark arts", "answer": "Hogwarts Professor of Defense Against the Dark Arts [accept any answer describing a Hogwarts teacher of Defense Against the Dark Arts or equivalents; prompt on answers like Hogwarts Professor]", "correct": True}, 
    {"response": "Candide", "answer": "Mr. Wickham", "correct": False}, 
    {"response": "Mr Darcy", "answer": "Mr. Darcy", "correct": True}, 
    {"response": "Pride and prejudice", "answer": "Pride and Prejudice", "correct": True}, 
    {"response": "n", "answer": "Matsuo Bash\u014d [or S\u014db\u014d; or T\u014ds\u0113; or Matsuo Ch\u016bemon Munefusa]", "correct": False}, 
    {"response": "Haiku", "answer": "haiku", "correct": True}, 
]
response_data = [d["response"] for d in data]
answer_data = [d["answer"] for d in data]
labels = [d["correct"] for d in data]

# Tokenize and pad the response and answer data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(response_data + answer_data)
response_sequence = tokenizer.texts_to_sequences(response_data)
answer_sequence = tokenizer.texts_to_sequences(answer_data)
max_len = max(len(r) for r in response_sequence + answer_sequence)
response_padded = pad_sequences(response_sequence, 100)
answer_padded = pad_sequences(answer_sequence, 100)

# Concatenate the response and answer
X = np.concatenate([response_padded, answer_padded], axis=1)

# Convert the labels to a numpy array
y = np.array(labels)

# Define the model
embedding_size = 50
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=embedding_size, input_shape=(X.shape[1],)))
model.add(LSTM(32))
model.add(Dense(1, activation='sigmoid'))

# Compile and train the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
model.fit(X, y, epochs=10, batch_size=32)

model.save("model.h5")