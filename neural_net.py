from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json

import numpy as np 

class Snake_nn:

	def __init__(self, load = False):

		self.model = None

		self.dataset = np.loadtxt("data/snake_data_10.txt", delimiter = ",")

		self.X = self.dataset[:,0:10]
		self.Y = self.dataset[:,10:14]

		if load:
			self.load_model()
		else:
			self.init_model()
			self.save_model()

	def init_model(self):
		
		self.model = Sequential()
		self.model.add(Dense(64, input_dim=10, activation='relu'))
		self.model.add(Dense(4, activation='sigmoid'))

		self.model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

		self.model.fit(self.X, self.Y, epochs=400, batch_size=10)


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

	def predict_direction(self, input):

		scores = self.model.predict(input)
		print(scores)
		return scores.argmax()


