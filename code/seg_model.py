import tensorflow as tf
from tensorflow.contrib.rnn import BasicLSTMCell
from tensorflow.python.ops.rnn import dynamic_rnn

class Model:

	def __init__(self):
		self.cats=10

		self.fsize=1500

		self.x = tf.placeholder(tf.float32, [None, self.fsize])
		self.y = tf.placeholder(tf.float32, [None, self.cats])
		self.seq_length = tf.placeholder(tf.int32)

		self.keep_prob = tf.placeholder(tf.float32)
		self.n_hidden=25
		self.n_classes=self.cats

		self.learning_rate = 0.1
		self.dropout = 0.75 

		self.weights = {
			'out': tf.Variable(tf.random_normal([self.n_hidden, self.cats])),
			'out_bw': tf.Variable(tf.random_normal([self.n_hidden, self.cats]))
		}

		self.biases = {
			'out': tf.Variable(tf.random_normal([self.cats]))
		}

		self.number_of_layers=1

		self.pred = self.network(self.x, self.weights, self.biases, self.keep_prob, self.seq_length)

		self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.pred, labels=self.y))
		self.optimizer = tf.train.FtrlOptimizer(learning_rate=self.learning_rate, l2_regularization_strength=1.0).minimize(self.cost)

		self.prediction=tf.argmax(self.pred,1)
		self.correct_pred = tf.equal(tf.argmax(self.pred, 1), tf.argmax(self.y, 1))
		self.accuracy = tf.reduce_mean(tf.cast(self.correct_pred, tf.float32))


	def network(self, x, weightss, biases, dropout, seq_length):
		
		fc1 = tf.reshape(x, [1, -1, self.fsize])

		lstm_fw_cell = BasicLSTMCell(self.n_hidden, forget_bias=1.0, state_is_tuple=True)
		lstm_fw_multicell = tf.contrib.rnn.MultiRNNCell([lstm_fw_cell] * self.number_of_layers, state_is_tuple=True)

		lstm_bw_cell = BasicLSTMCell(self.n_hidden, forget_bias=1.0, state_is_tuple=True)
		lstm_bw_multicell = tf.contrib.rnn.MultiRNNCell([lstm_bw_cell] * self.number_of_layers, state_is_tuple=True)

		(output_fw, output_bw), (state_fw, state_bw) = tf.nn.bidirectional_dynamic_rnn(lstm_fw_multicell, lstm_bw_multicell, fc1, dtype='float32', sequence_length=tf.reshape(seq_length, [1]))

		outputs_fw = tf.reshape(output_fw, [seq_length, self.n_hidden])
		outputs_bw = tf.reshape(output_bw, [seq_length, self.n_hidden])

		out = tf.matmul(outputs_fw, weightss['out']) + tf.matmul(outputs_bw, self.weights['out_bw']) + self.biases['out']
		return out

