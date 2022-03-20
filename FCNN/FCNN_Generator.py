from tensorflow import keras
from matplotlib import pyplot as plt
from keras import callbacks
from Commons import y_list_generator
from Commons import x_file_reader
from Commons import evaluate
import time    # This library is used to measure train time


# Main part of the code starts here
# Combining the positive_train_x and negative_train_x and neutral_train_x
start_time = time.time()
positive_train_x = x_file_reader("Train_X//positive_train_x.txt")
negative_train_x = x_file_reader("Train_X//negative_train_x.txt")
neutral_train_x = x_file_reader("Train_X//neutral_train_x.txt")
train_x = []
for i in positive_train_x:
    train_x.append(i)
for i in negative_train_x:
    train_x.append(i)
for i in neutral_train_x:
    train_x.append(i)

positive_train_y = y_list_generator(len(positive_train_x), [1, 0, 0])
neutral_train_y = y_list_generator(len(neutral_train_x), [0, 1, 0])
negative_train_y = y_list_generator(len(negative_train_x), [0, 0, 1])

# Combining the positive_train_y and negative_train_y and neutral_train_y
train_y = []
for i in positive_train_y:
    train_y.append(i)
for i in negative_train_y:
    train_y.append(i)
for i in neutral_train_y:
    train_y.append(i)

# Loading validation data
positive_validation_x = x_file_reader("Test_X//positive_validation_x.txt")
negative_validation_x = x_file_reader("Test_X//negative_validation_x.txt")
neutral_validation_x = x_file_reader("Test_X//neutral_validation_x.txt")
validation_x = []
for i in positive_validation_x:
    validation_x.append(i)
for i in negative_validation_x:
    validation_x.append(i)
for i in neutral_validation_x:
    validation_x.append(i)

positive_validation_y = y_list_generator(len(positive_validation_x), [1, 0, 0])
negative_validation_y = y_list_generator(len(negative_validation_x), [0, 0, 1])
neutral_validation_y = y_list_generator(len(neutral_validation_x), [0, 1, 0])
validation_y = []
for i in positive_validation_y:
    validation_y.append(i)
for i in negative_validation_y:
    validation_y.append(i)
for i in neutral_validation_y:
    validation_y.append(i)


# Neural network implementation
print("Training the fully connected neural network...")
fcnn_model = keras.Sequential()
fcnn_model.add(keras.layers.Dense(64, activation="relu", input_shape=(47, )))
fcnn_model.add(keras.layers.Dense(32, activation="relu"))
fcnn_model.add(keras.layers.Dense(3, activation="softmax"))
fcnn_model.summary()
fcnn_model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
early_stopping = callbacks.EarlyStopping(monitor="val_accuracy", mode="max", restore_best_weights=True, patience=500)
history = fcnn_model.fit(train_x, train_y, epochs=500, verbose=2, batch_size=100, validation_data=(validation_x, validation_y), callbacks=[early_stopping])
fig, axis = plt.subplots(2)
axis[0].plot(history.history["accuracy"], label="Train Accuracy")
axis[0].plot(history.history["val_accuracy"], label="Validation Accuracy")
axis[1].plot(history.history["loss"], label="Train Loss")
axis[1].plot(history.history["val_loss"], label="Validation Loss")
plt.legend()
plt.show()

# Saving the weights and biases of the model in a file
fcnn_model.save_weights('Checkpoints//Other Trained Models//my_checkpoint1')
finish_time = time.time()

# Loading test data
positive_test_x = x_file_reader("Test_X//positive_test_x.txt")
negative_test_x = x_file_reader("Test_X//negative_test_x.txt")
neutral_test_x = x_file_reader("Test_X//neutral_test_x.txt")
positive_test_y = y_list_generator(len(positive_test_x), [1, 0, 0])
negative_test_y = y_list_generator(len(negative_test_x), [0, 0, 1])
neutral_test_y = y_list_generator(len(neutral_test_x), [0, 1, 0])

# Predicting the model test data output
print("Predicting the neural network output of test data...")
positive_pred = fcnn_model.predict(positive_test_x)
print("Positive test data prediction finished")
negative_pred = fcnn_model.predict(negative_test_x)
print("Negative test data prediction finished")
neutral_pred = fcnn_model.predict(neutral_test_x)
print("Neutral test data prediction finished\n")

# Evaluating the model by positive and negative and neutral test data
print("Evaluating the model...")
positive_accuracy = evaluate(positive_pred, "positive")
negative_accuracy = evaluate(negative_pred, "negative")
neutral_accuracy = evaluate(neutral_pred, "neutral")

print("Positive test data accuracy: " + str(positive_accuracy) + str(" %"))
print("Negative test data accuracy: " + str(negative_accuracy) + str(" %"))
print("Neutral test data accuracy: " + str(neutral_accuracy) + str(" %"))
print("Train time is: " + str(round(finish_time - start_time, 2)) + " seconds")























