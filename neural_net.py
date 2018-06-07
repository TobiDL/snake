from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json

import numpy as np 

class Snake_nn:

	def __init__(self, load = False):

		self.model = None

		self.dataset = np.loadtxt("data/snake_data_10.txt", delimiter = ",")

		self.X = self.dataset[:,0:100]
		self.Y = self.dataset[:,100]

		if load:
			self.load_model()
		else:
			self.init_model()
			self.save_model()

	def init_model(self):
		
		self.model = Sequential()
		self.model.add(Dense(8, input_dim=100, activation='relu'))
		self.model.add(Dense(1, activation='sigmoid'))

		self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

		self.model.fit(self.X, self.Y, epochs=150, batch_size=10)


	def load_model(self):

		with open('model/model_10.json', 'r') as file:
			model_json = file.read()

		self.model = model_from_json(model_json)
		self.model.load_weights("model/model_10.h5")
		self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


	def save_model(self):
		model_json = self.model.to_json()

		with open('model/model_10.json', 'w') as file:
			file.write(model_json)

		self.model.save_weights("model/model_10.h5")

	def predict_direction(self, board):

		scores = self.model.predict(board)
		
		return int(scores[0])


