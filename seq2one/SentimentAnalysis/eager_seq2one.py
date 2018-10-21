import tensorflow as tf
import tensorflow.contrib.eager as tfe
from tensorflow.keras.layers import Dense, Embedding, Flatten
from tensorflow.keras.models import Sequential
import numpy as np
import argparse

tfe.enable_eager_execution()


def get_batch(batch_size =32):
    r = np.random.randint(0, N-batch_size)
    return x_train[r:r+batch_size], y_train[r:r+batch_size]


def loss(model, x, y):
    prediction = model(x)
    return tf.losses.softmax_cross_entropy(y, logits=prediction)


def grad(model, x, y):
    with tf.GradientTape() as tape :
        loss_value = loss(model, x, y)
    return tape.gradient(loss_value, model.variables)


def accuracy(model, x, y):
    yhat = model(x)
    yhat = tf.argmax(yhat, 1).numpy()
    y = tf.argmax(y,1).numpy()
    return np.sum(y == yhat)/len(y)


def create_model(embedding_length_size=32, top_words=1, input_length=100):
    model = Sequential()
    model.add(Embedding(top_words, embedding_length_size, input_length=input_length))
    # model.add(BatchNormalization)
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    return model


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument()
    # args = parser.parse_args()
    model = create_model()
    print(model.summary())
    N = 100
    batch_size = 64
    epoch_length = N // batch_size
    epoch = 0
    epochs = 5

    optimizer = tf.train.AdadeltaOptimizer()
    loss_history = tfe.metrics.Mean("loss")
    accuracy_history = tfe.metrics.Mean("accuracy")

    while epocs < epochs :
        # get next batch
        x, y = get_batch(batch_size=batch_size)

        grads = grad(model, x, y)

        optimizer.apply_gradients(zip(grads, model.variables), global_step=tf.train.get_or_create_global_step())

        loss_history(loss(model, x, y))
        accuracy_history(accuracy(model, x, y))

        if i % epoch_length == 0:
            print(
                "epoch: {:d} Loss: {:.3f}, Acc: {:.3f}".format(epoch, loss_history.result(), accuracy_history.result()))

            # clear the history
            loss_history.init_variables()
            accuracy_history.init_variables()

            epoch += 1

        i += 1
        print("train complete")





