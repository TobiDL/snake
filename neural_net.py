from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json

import numpy as np 

np.random.seed(420)

class Snake_nn:

	def __init__(self, load = False):

		self.model = None

		self.dataset = np.loadtxt("data/snake_data_10.txt", delimiter = ",")

		self.X = self.dataset[:,0:13]
		self.Y = self.dataset[:,13:17]

		if load:
			self.load_model()
		else:
			self.init_model()
			self.save_model()

	def init_model(self):
		
		self.model = Sequential()
		self.model.add(Dense(24, input_dim=13, activation='relu'))
		self.model.add(Dense(4, activation='softmax'))

		self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

		self.model.fit(self.X, self.Y, epochs=200, batch_size=50)


	def load_model(self):

		with open('model/model_10.json', 'r') as file:
			model_json = file.read()

		self.model = model_from_json(model_json)
		self.model.load_weights("model/model_10.h5")
		self.model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['accuracy'])


	def save_model(self):
		model_json = self.model.to_json()

		with open('model/model_10.json', 'w') as file:
			file.write(model_json)

		self.model.save_weights("model/model_10.h5")

	def predict_direction(self, input):
		print(input)
		scores = self.model.predict(input)
		print(scores)
		return scores.argmax()


