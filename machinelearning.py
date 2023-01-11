import json
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, GRU

# Load the JSON data into a Pandas DataFrame
with open("data.csv", "r") as f:
    data = json.load(f)
df = pd.DataFrame(data)

# Extract the "response", "answer" and "answer" fields 
responses = df['response'].tolist()
answers = df['answer'].tolist()
labels = df['correct'].tolist()

# tokenizing the data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(responses+answers)
questions_tok = tokenizer.texts_to_sequences(responses)
answers_tok = tokenizer.texts_to_sequences(answers)

# Padding the data
max_len = max(len(questions_tok[i]) for i in range(len(questions_tok)))
questions_tok = pad_sequences(questions_tok, maxlen=max_len)
answers_tok = pad_sequences(answers_tok, maxlen=max_len)

# Splitting the data into training and testing
X_train, X_test, y_train, y_test = train_test_split(questions_tok, labels, test_size=0.2)

# Building the model
model = Sequential()
model.add(Embedding(len(tokenizer.word_index)+1, 128))
model.add(GRU(64, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fitting the model
model.fit(X_train, y_train, epochs=5, batch_size=32, validation_data=(X_test, y_test))
