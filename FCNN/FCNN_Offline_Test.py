from tensorflow import keras
from Commons import y_list_generator
from Commons import x_file_reader
from Commons import evaluate


# This function creates the neural network model for testing by reading the saved weights
def create_model():
    output_model = keras.Sequential()
    output_model.add(keras.layers.Dense(64, activation="relu", input_shape=(47, )))
    output_model.add(keras.layers.Dense(32, activation="relu"))
    output_model.add(keras.layers.Dense(3, activation="softmax"))
    output_model.summary()
    output_model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return output_model


# Main part of the code starts here
model = create_model()
model.load_weights('Checkpoints//Main Trained Model//my_checkpoint1')
positive_test_x = x_file_reader("Test_X//positive_test_x_complete.txt")
negative_test_x = x_file_reader("Test_X//negative_test_x_complete.txt")
neutral_test_x = x_file_reader("Test_X//neutral_test_x_complete.txt")
positive_test_y = y_list_generator(len(positive_test_x), [1, 0, 0])
negative_test_y = y_list_generator(len(negative_test_x), [0, 0, 1])
neutral_test_y = y_list_generator(len(neutral_test_x), [0, 1, 0])
print("The length of positive_test_y: " + str(len(positive_test_y)))
print("The length of negative_test_y: " + str(len(negative_test_y)))
print("The length of neutral_test_y: " + str(len(neutral_test_y)))

# Predicting the model test data output
print("Predicting the neural network output of test data...")
positive_pred = model.predict(positive_test_x)
print("Positive test data prediction finished")
negative_pred = model.predict(negative_test_x)
print("Negative test data prediction finished")
neutral_pred = model.predict(neutral_test_x)
print("Neutral test data prediction finished")

# Evaluating the model by positive and negative test data
print("Evaluating the model...")
positive_accuracy = evaluate(positive_pred, "positive")
negative_accuracy = evaluate(negative_pred, "negative")
neutral_accuracy = evaluate(neutral_pred, "neutral")
print("Positive test data accuracy: " + str(positive_accuracy) + str(" %"))
print("Negative test data accuracy: " + str(negative_accuracy) + str(" %"))
print("Neutral test data accuracy: " + str(neutral_accuracy) + str(" %"))



