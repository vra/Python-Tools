# coding: utf-8

import numpy as np
import random
import keras
from keras.models import Sequential
from keras import optimizers
from keras.utils.np_utils import to_categorical
from keras.layers import LSTM, Dense, Dropout
from pyActionRecog.utils.video_funcs import default_aggregation_func

batch_size=32
epochs =  1000
data_dim = 1024
timesteps = 25 
num_classes = 101

def parse_npz_data(npz_file_name):
	#data = np.load('global_pool.npz')
	data = np.load(npz_file_name)
	data = data['arr_0']
	# NOTE: shuffle is run on data itself, return is None!
	np.random.shuffle(data)

	print 'data.shape:', data[:,0].shape
	print 'data.shape:', data[:,0][0].shape
	#agg_score_vect = [default_aggregation_func(x, normalization=False, crop_agg=getattr(np,'mean')) for x in data[:,0]]
#	for x in data[:,0]:
#		new_x = np.mean(x, axis=1)
#		print 'new_x:', new_x
#		new_x = new_x.reshape(tim
	agg_score_vect = [np.mean(x, axis=1).reshape(timesteps,-1) for x in data[:,0]]
	scores = np.array(agg_score_vect)
	print 'scores.shape:', scores.shape
#	scores = scores.reshape(-1, timesteps, data_dim)
	labels = to_categorical(data[:,1])
	print 'labels.shape:', labels.shape
	return scores, labels
#	return scores, data[:,1] 


def  tsn_lstm():
	model = Sequential()	
	#model.add(LSTM(32, dropout=0.2, recurrent_dropout=0.2, batch_input_shape=(1,1024,1)))
	model.add(LSTM(32, dropout=0.2, recurrent_dropout=0.2, batch_input_shape=(batch_size, timesteps, data_dim)))
	#model.add(Dense(1, activation='sigmoid'))
	model.add(Dense(101, activation='softmax'))
#	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	sgd = optimizers.SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
	model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
#	model.compile(loss='mse', optimizer=sgd, metrics=['accuracy'])
	
	x_train, y_train = parse_npz_data('global_pool_train.npz')	
	x_test, y_test = parse_npz_data('global_pool_test.npz')	
	#result = model.fit(x_train[:320*10,:,:], y_train[:320*10], verbose=1, batch_size=batch_size, epochs=epochs, validation_data=(x_test[:320*10,:,:], y_test[:320*10]))
	num_prod  = 29
	result = model.fit(x_train[:320*num_prod,:,:], y_train[:320*num_prod], verbose=1, batch_size=batch_size, epochs=epochs, validation_data=(x_train[:320*num_prod,:,:], y_train[:320*num_prod]))
	print result
#	model.evaluate(x_train[11:21,:,:], y_train[11:21], verbose=0)
	print '***** Begin evaluate'
	score=model.evaluate(x_test[320*9:320*10,:,:], y_test[320*9:320*10], verbose=0)
	print 'score:', score


if __name__ == '__main__':
	tsn_lstm()

