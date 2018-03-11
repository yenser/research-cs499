#!/usr/bin/env python3

# imports
import tensorflow as tf
import numpy as np
from create_test_data import get_data_and_create_test_set


'''
input > weight > hidden layer 1 (activation function) > 
weights > hidden l2 (activation function) > weights > output layer

compare output to intended output > cost function (cross entropy)
optimization function (optimizer) > minimize cost (AdamOptimizer ... SGD, AdaGrad)


Backpropagation

feed forward + backprop = epoch
'''


# code

# 10 classes, 0-9

filename='./models/4in_model.ckpt'

n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

batch_size = 3392 # adjust this for batchsize

train_x, train_y, test_x, test_y, batch_size = get_data_and_create_test_set('AAPL', 'MSFT', 'GOOGL', 'AMZN', 'ADBE', 'ORCL')

n_classes = len(train_y[0]) # how many outputs

# height x width

input_size = 5
print("Input Size: ", input_size)
print('Batch Size: ', batch_size)
x = tf.placeholder('float') # input data
y = tf.placeholder('float')

hidden_1_layer = {'f_fum':n_nodes_hl1,'weights': tf.Variable(tf.random_normal([input_size, n_nodes_hl1])), 'biases':tf.Variable(tf.random_normal([n_nodes_hl1]))}

hidden_2_layer = {'f_fum':n_nodes_hl2,'weights': tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])), 'biases':tf.Variable(tf.random_normal([n_nodes_hl2]))}

hidden_3_layer = {'f_fum':n_nodes_hl3,'weights': tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])), 'biases':tf.Variable(tf.random_normal([n_nodes_hl3]))}

output_layer = {'f_fum':None,'weights': tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])), 'biases':tf.Variable(tf.random_normal([n_classes]))}

def neural_network_model(data):

	# (input_data * weights) + biases

	l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']), hidden_1_layer['biases'])
	l1 = tf.nn.relu(l1)

	l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']), hidden_2_layer['biases'])
	l2 = tf.nn.relu(l2)

	l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']), hidden_3_layer['biases'])
	l3 = tf.nn.relu(l3)

	output = tf.matmul(l3, output_layer['weights']) + output_layer['biases']

	return output



### IMPORTANT:
saver = tf.train.Saver()
# saver.recover('/models/4in_model.ckpt')

def train_neural_network(x, hm_epochs=50):
	prediction = neural_network_model(x)
	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=prediction, labels=y))

	#								learning rate = 0.001
	optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(cost)

	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())
		saver.restore(sess,filename)


		for epoch in range(hm_epochs):
			epoch_loss = 0

			i = 0
			while i < len(train_x):
				start = i
				end = i + batch_size

				batch_x = np.array(train_x[start:end])
				batch_y = np.array(train_y[start:end])

				_, c = sess.run([optimizer, cost], feed_dict={x: batch_x, y: batch_y})
				epoch_loss += c
				i+=batch_size
				# print(tf.equal(tf.argmax(prediction, 1), tf.argmax(y,1)))

			saver.save(sess, filename)
			print('Epoch', epoch+1, 'completed out of', hm_epochs, 'loss', epoch_loss)


		correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y,1))
		accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
		print('Accuracy:', accuracy.eval({x:test_x, y:test_y}))


train_neural_network(x)