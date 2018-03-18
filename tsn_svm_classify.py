# coding: utf-8
import numpy as np
import random
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC


def parse_npz_data(npz_file_name):
	data = np.load(npz_file_name)
	data = data['arr_0']
	# NOTE: shuffle is run on data itself, return is None!
	np.random.shuffle(data)
	label = data[:,1].astype('float32')
	data = np.array([np.max(d, axis=0).flatten().astype('float32') for d in data[:,0]])
	return data, label

def svm_classifier(x_train, y_train, x_test, y_test):
	clf = OneVsRestClassifier(LinearSVC(C=0.1))
	clf.fit(x_train, y_train)
	accu = clf.score(x_test, y_test)
	print 'accu: ', accu
	

if __name__ == '__main__':
	print 'loading training data...'
	x_train, y_train = parse_npz_data('global_pool_train.npz')	
	print 'loading test data...'
	x_test, y_test = parse_npz_data('global_pool_test.npz')	
	print 'run svm...'
	svm_classifier(x_train, y_train, x_test, y_test)

