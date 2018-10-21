import tensorflow as tf


class EncoderRNN(object):
    def __init__(self, num_units = 150):
        self.num_units = num_units
        self.encoder_cell = tf.nn.rnn_cell.BasicLSTMCell(self.num_units)

    def forward(self, x):
        state = self.encoder_cell.zero_state(len(x), dtype=tf.float32)
        timestep_x = tf.unstack(x, axis=1)
        outputs, cell_states = [], []
        for input_step in timestep_x:
            output, state = self.encoder_cell(input_step, state)
            outputs.append(output)
            cell_states.append(state[0])

        outputs = tf.stack(outputs, axis=1)
        cell_states = tf.stack(cell_states, axis=1)
        return outputs, cell_states
