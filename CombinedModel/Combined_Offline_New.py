import math
import pickle
from tensorflow import keras
from Commons import comment_smoother
from Commons import dictionary_loader
from Commons import nltk_input_list_generator
from Commons import unique_words_counter
from Commons import x_file_reader


# This function returns the final classification of combined model
def final_evaluator(input_nb_results, input_me_results, final_results, expected_tag):
    true_classification = 0
    i = 0
    while i < len(input_me_results):
        if input_nb_results[i] == 1 and input_me_results[i] == 1:
            final_results.append(1)
            if expected_tag == 1:
                true_classification += 1
        if input_nb_results[i] == -1 and input_me_results[i] == -1:
            final_results.append(-1)
            if expected_tag == -1:
                true_classification += 1
        if input_nb_results[i] == 1 and input_me_results[i] == 0:
            final_results.append(0)
            if expected_tag == 0:
                true_classification += 1
        if input_nb_results[i] == -1 and input_me_results[i] == 0:
            final_results.append(0)
            if expected_tag == 0:
                true_classification += 1
        if input_nb_results[i] == -1 and input_me_results[i] == 1:
            final_results.append(-1)
            if expected_tag == -1:
                true_classification += 1
        if input_nb_results[i] == 1 and input_me_results[i] == -1:
            final_results.append(1)
            if expected_tag == 1:
                true_classification += 1
        if input_nb_results[i] == 0 and input_me_results[i] == 1:
            final_results.append(1)
            if expected_tag == 1:
                true_classification += 1
        if input_nb_results[i] == 0 and input_me_results[i] == -1:
            final_results.append(-1)
            if expected_tag == -1:
                true_classification += 1
        if input_nb_results[i] == 0 and input_me_results[i] == 0:
            final_results.append(0)
            if expected_tag == 0:
                true_classification += 1
        i += 1
    return true_classification


# This function creates the neural network model for testing
def create_model():
    output_model = keras.Sequential()
    output_model.add(keras.layers.Dense(64, activation="relu", input_shape=(47, )))
    output_model.add(keras.layers.Dense(32, activation="relu"))
    output_model.add(keras.layers.Dense(3, activation="softmax"))
    output_model.summary()
    output_model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return output_model


# This function generates Naive Bayes model results for the input test file
def nb_predictor(input_test_file_address, input_positive_dictionary, input_negative_dictionary, input_positive_words_count, input_negative_words_count, input_unique_words_count):
    output_results = []
    test_tweets_file = open(input_test_file_address, "rt", encoding="utf8")
    while True:
        tweet = test_tweets_file.readline().lower()
        if tweet == "":
            break

        tweet = comment_smoother(tweet)
        words_list = tweet.split(" ")
        final_result = 0
        for word in words_list:
            if word in input_positive_dictionary:
                positive_numerator = input_positive_dictionary[word] + 1
            else:
                positive_numerator = 1

            if word in input_negative_dictionary:
                negative_numerator = input_negative_dictionary[word] + 1
            else:
                negative_numerator = 1

            final_result += math.log10((positive_numerator / (input_positive_words_count + input_unique_words_count)) / (negative_numerator / (input_negative_words_count + input_unique_words_count)))
        if final_result > 0:
            output_results.append(1)
        if final_result == 0:
            output_results.append(0)
        if final_result < 0:
            output_results.append(-1)

    return output_results


def precision_printer(input_results, input_desired_label, input_method_name):
    counter = 0
    for result in input_results:
        if result == input_desired_label:
            counter += 1
    if input_desired_label == 1:
        print(input_method_name + " positive precision: " + str(round((counter / len(input_results)), 2)) + " %")
    if input_desired_label == 0:
        print(input_method_name + " neutral precision: " + str(round((counter / len(input_results)), 2)) + " %")
    if input_desired_label == -1:
        print(input_method_name + " negative precision: " + str(round((counter / len(input_results)), 2)) + " %")
    print("===========================================================================================================")


# This function generates Maximum Entropy model results for the input test file
def me_predictor(input_test_file_address, input_desired_label, input_classifier):
    output_results = []
    test_tweets_list = nltk_input_list_generator(input_test_file_address, input_desired_label, [])
    for tweet_tuple in test_tweets_list:
        tweet_word_dictionary = tweet_tuple[0]
        main_label = tweet_tuple[1]
        predicted_label = input_classifier.classify(tweet_word_dictionary)
        output_results.append(predicted_label)
    return output_results


# This function generates FCNN model results for the input test file
def fcnn_predictor(input_test_x_file_address, input_fcnn_model):
    output_results = []
    test_x = x_file_reader(input_test_x_file_address)
    model_predictions = input_fcnn_model.predict(test_x)
    for prediction in model_predictions:
        maximum = max(prediction[0], prediction[1], prediction[2])
        if maximum == prediction[0]:
            output_results.append(1)
        if maximum == prediction[1]:
            output_results.append(0)
        if maximum == prediction[2]:
            output_results.append(-1)
    return output_results







# Main part of the code starts here
# Loading saved models
print("Loading saved models...")
positive_tweets_dictionary, negative_tweets_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words = dictionary_loader()
me_model_file = open("E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//MaximumEntropy//MaximumEntropyClassifier", "rb")
me_classifier = pickle.load(me_model_file)
me_model_file.close()
fcnn_model = create_model()
fcnn_model.load_weights("E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//FCNN//Checkpoints//Main Trained Model//my_checkpoint1")
number_of_unique_words = unique_words_counter(positive_tweets_dictionary, negative_tweets_dictionary)

# Evaluating the positive test tweets
positive_test_tweets_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//positive_test.txt"
nb_positive_test_results = nb_predictor(positive_test_tweets_file_address, positive_tweets_dictionary, negative_tweets_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words, number_of_unique_words)
print("The length of nb_positive_test_results: " + str(len(nb_positive_test_results)))
precision_printer(nb_positive_test_results, 1, "nb")
me_positive_test_results = me_predictor(positive_test_tweets_file_address, 1, me_classifier)
print("The length of me_positive_test_results: " + str(len(me_positive_test_results)))
precision_printer(me_positive_test_results, 1, "me")
fcnn_positive_test_tweets_file_address = "E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//FCNN//Test_X//positive_test_x_complete.txt"
fcnn_positive_test_results = fcnn_predictor(fcnn_positive_test_tweets_file_address, fcnn_model)
print("The length of fcnn_positive_test_results: " + str(len(fcnn_positive_test_results)))
precision_printer(fcnn_positive_test_results, 1, "fcnn")








# Evaluating the negative test tweets
me_results = []
nb_results = []
final_negative_results = []
negative_test_comments_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//negative_test.txt"
negative_test_comments_file = open(negative_test_comments_file_address, "rt", encoding="utf8")
comments_counter = 0
true_categorization = 0
while True:
    comment = negative_test_comments_file.readline().lower()
    if comment == "":
        break


    comment = comment_smoother(comment)
    words_list = comment.split(" ")
    final_result = 0
    for word in words_list:
        if word in positive_comments_dictionary:
            positive_numerator = positive_comments_dictionary[word] + 1
        else:
            positive_numerator = 1

        if word in negative_comments_dictionary:
            negative_numerator = negative_comments_dictionary[word] + 1
        else:
            negative_numerator = 1

        final_result += math.log10((positive_numerator / (total_number_of_positive_dictionary_words + number_of_unique_words)) / (negative_numerator / (total_number_of_negative_dictionary_words + number_of_unique_words)))
    if final_result < 0:
        nb_results.append(-1)
    if final_result > 0:
        nb_results.append(1)
    if final_result == 0:
        nb_results.append(0)
    comments_counter += 1


# Generating the test list for negative test tweets
test_list = nltk_input_list_generator(negative_test_comments_file_address, -1, [])

# Evaluating the model for negative tweets by Maximum Entropy model
for tweet_tuple in test_list:
    tweet_word_dictionary = tweet_tuple[0]
    main_label = tweet_tuple[1]
    predicted_label = classifier.classify(tweet_word_dictionary)
    me_results.append(predicted_label)

negative_precision = round((final_evaluator(nb_results, me_results, final_negative_results, -1) / comments_counter) * 100, 2)

# Evaluating the neutral test tweets
me_results = []
nb_results = []
final_neutral_results = []
neutral_test_comments_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//neutral_test.txt"
neutral_test_comments_file = open(neutral_test_comments_file_address, "rt", encoding="utf8")
comments_counter = 0
true_categorization = 0
while True:
    comment = neutral_test_comments_file.readline().lower()
    if comment == "":
        break
    comment = comment_smoother(comment)
    words_list = comment.split(" ")
    final_result = 0
    for word in words_list:
        if word in positive_comments_dictionary:
            positive_numerator = positive_comments_dictionary[word] + 1
        else:
            positive_numerator = 1

        if word in negative_comments_dictionary:
            negative_numerator = negative_comments_dictionary[word] + 1
        else:
            negative_numerator = 1

        final_result += math.log10((positive_numerator / (total_number_of_positive_dictionary_words + number_of_unique_words)) / (negative_numerator / (total_number_of_negative_dictionary_words + number_of_unique_words)))
    if final_result < 0:
        nb_results.append(-1)
    if final_result > 0:
        nb_results.append(1)
    if final_result == 0:
        nb_results.append(0)
    comments_counter += 1


# Generating the test list for neutral test tweets
test_list = nltk_input_list_generator(neutral_test_comments_file_address, 0, [])

# Evaluating the model for neutral tweets by Maximum Entropy model
for tweet_tuple in test_list:
    tweet_word_dictionary = tweet_tuple[0]
    main_label = tweet_tuple[1]
    predicted_label = classifier.classify(tweet_word_dictionary)
    me_results.append(predicted_label)
neutral_precision = round((final_evaluator(nb_results, me_results, final_neutral_results, 0) / comments_counter) * 100, 2)

print("The model precision for positive tweets: " + str(positive_precision) + " %")
print("The model precision for negative tweets: " + str(negative_precision) + " %")
print("The model precision for neutral tweets: " + str(neutral_precision) + " %")











