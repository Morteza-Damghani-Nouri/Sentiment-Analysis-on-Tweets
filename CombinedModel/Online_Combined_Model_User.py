import tkinter as tk    # This library is used for GUI implementation
from tkinter import *
import pickle
import math
from Commons import dictionary_loader
from Commons import nltk_input_list_generator_online_version
from Commons import comment_smoother
from Commons import unique_words_counter
from Commons import background_image_resize
from Commons import create_model
from Commons import precision_calculator
from Commons import nb_predictor_online_version
from Commons import me_predictor_online_version
from Commons import fcnn_predictor_online_version


# This function finds the most accurate method among avalaible methods according to precision
def best_method_finder():
    nb_average_precision = (NB_POSITIVE_PRECISION + NB_NEGATIVE_PRECISION + NB_NEUTRAL_PRECISION) / 3
    me_average_precision = (ME_POSITIVE_PRECISION + ME_NEGATIVE_PRECISION + ME_NEUTRAL_PRECISION) / 3
    fcnn_average_precision = (FCNN_POSITIVE_PRECISION + FCNN_NEGATIVE_PRECISION + FCNN_NEUTRAL_PRECISION) / 3
    if nb_average_precision == me_average_precision:
        print("The precision of Naive Bayes method and Maximum Entropy method are equal. Unable to find the best method according to average precision.")
        exit(1)
    if nb_average_precision == fcnn_average_precision:
        print("The precision of Naive Bayes method and Fully Connected Neural Network method are equal. Unable to find the best method according to average precision.")
        exit(1)
    if me_average_precision == fcnn_average_precision:
        print("The precision of Maximum Entropy method and Fully Connected Neural Network method are equal. Unable to find the best method according to average precision.")
        exit(1)
    maximum_precision = max(nb_average_precision, me_average_precision, fcnn_average_precision)
    if maximum_precision == nb_average_precision:
        return maximum_precision, "nb"
    if maximum_precision == me_average_precision:
        return maximum_precision, "me"
    if maximum_precision == fcnn_average_precision:
        return maximum_precision, "fcnn"


# This function returns the final classification of combined model
def final_evaluator(, , ,):
    input_nb_results =
    input_me_results =
    input_fcnn_results =
    best_method_precision, best_method_name = best_method_finder()
    final_results = []
    i = 0
    while i < len(input_nb_results):
        if input_nb_results[i] == 1 and input_me_results[i] == 1 and input_fcnn_results[i] == 1:
            final_results.append(1)
        if input_nb_results[i] == -1 and input_me_results[i] == -1 and input_fcnn_results[i] == -1:
            final_results.append(-1)
        if input_nb_results[i] == 0 and input_me_results[i] == 0 and input_fcnn_results[i] == 0:
            final_results.append(0)
        if input_nb_results[i] == 1 and input_me_results[i] == 1 and input_fcnn_results[i] == -1:
            maximum_positive = max(NB_POSITIVE_PRECISION, ME_POSITIVE_PRECISION)
            minimum_positive = min(NB_POSITIVE_PRECISION, ME_POSITIVE_PRECISION)
            final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
            if final_positive_precision >= FCNN_NEGATIVE_PRECISION:
                final_results.append(1)
            else:
                final_results.append(-1)
        if input_nb_results[i] == 1 and input_me_results[i] == -1 and input_fcnn_results[i] == 1:
            maximum_positive = max(NB_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
            minimum_positive = min(NB_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
            final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
            if final_positive_precision >= ME_NEGATIVE_PRECISION:
                final_results.append(1)
            else:
                final_results.append(-1)
        if input_nb_results[i] == -1 and input_me_results[i] == 1 and input_fcnn_results[i] == 1:
            maximum_positive = max(ME_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
            minimum_positive = min(ME_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
            final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
            if final_positive_precision >= NB_NEGATIVE_PRECISION:
                final_results.append(1)
            else:
                final_results.append(-1)
        if input_nb_results[i] == 1 and input_me_results[i] == 1 and input_fcnn_results[i] == 0:
            maximum_positive = max(NB_POSITIVE_PRECISION, ME_POSITIVE_PRECISION)
            minimum_positive = min(NB_POSITIVE_PRECISION, ME_POSITIVE_PRECISION)
            final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
            if final_positive_precision >= FCNN_NEUTRAL_PRECISION:
                final_results.append(1)
            else:
                final_results.append(0)
        if input_nb_results[i] == 1 and input_me_results[i] == 0 and input_fcnn_results[i] == 1:
            maximum_positive = max(NB_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
            minimum_positive = min(NB_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
            final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
            if final_positive_precision >= ME_NEUTRAL_PRECISION:
                final_results.append(1)
            else:
                final_results.append(0)
        if input_nb_results[i] == 0 and input_me_results[i] == 1 and input_fcnn_results[i] == 1:
            maximum_positive = max(ME_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
            minimum_positive = min(ME_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
            final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
            if final_positive_precision >= NB_NEUTRAL_PRECISION:
                final_results.append(1)
            else:
                final_results.append(0)
        if input_nb_results[i] == 1 and input_me_results[i] == -1 and input_fcnn_results[i] == 0:
            if best_method_name == "nb":
                maximum_precision = max(NB_POSITIVE_PRECISION + (best_method_precision / 5), ME_NEGATIVE_PRECISION, FCNN_NEUTRAL_PRECISION)
                if maximum_precision == (NB_POSITIVE_PRECISION + (best_method_precision / 5)):
                    final_results.append(1)
                if maximum_precision == ME_NEGATIVE_PRECISION:
                    final_results.append(-1)
                if maximum_precision == FCNN_NEUTRAL_PRECISION:
                    final_results.append(0)
            if best_method_name == "me":
                maximum_precision = max(NB_POSITIVE_PRECISION, ME_NEGATIVE_PRECISION + (best_method_precision / 5), FCNN_NEUTRAL_PRECISION)
                if maximum_precision == NB_POSITIVE_PRECISION:
                    final_results.append(1)
                if maximum_precision == (ME_NEGATIVE_PRECISION + (best_method_precision / 5)):
                    final_results.append(-1)
                if maximum_precision == FCNN_NEUTRAL_PRECISION:
                    final_results.append(0)
            if best_method_name == "fcnn":
                maximum_precision = max(NB_POSITIVE_PRECISION, ME_NEGATIVE_PRECISION, FCNN_NEUTRAL_PRECISION + (best_method_precision / 5))
                if maximum_precision == NB_POSITIVE_PRECISION:
                    final_results.append(1)
                if maximum_precision == ME_NEGATIVE_PRECISION:
                    final_results.append(-1)
                if maximum_precision == (FCNN_NEUTRAL_PRECISION + (best_method_precision / 5)):
                    final_results.append(0)
        if input_nb_results[i] == -1 and input_me_results[i] == 1 and input_fcnn_results[i] == 0:
            if best_method_name == "nb":
                maximum_precision = max(NB_NEGATIVE_PRECISION + (best_method_precision / 5), ME_POSITIVE_PRECISION, FCNN_NEUTRAL_PRECISION)
                if maximum_precision == (NB_NEGATIVE_PRECISION + (best_method_precision / 5)):
                    final_results.append(-1)
                if maximum_precision == ME_POSITIVE_PRECISION:
                    final_results.append(1)
                if maximum_precision == FCNN_NEUTRAL_PRECISION:
                    final_results.append(0)
            if best_method_name == "me":
                maximum_precision = max(NB_NEGATIVE_PRECISION, ME_POSITIVE_PRECISION + (best_method_precision / 5), FCNN_NEUTRAL_PRECISION)
                if maximum_precision == NB_NEGATIVE_PRECISION:
                    final_results.append(-1)
                if maximum_precision == (ME_POSITIVE_PRECISION + (best_method_precision / 5)):
                    final_results.append(1)
                if maximum_precision == FCNN_NEUTRAL_PRECISION:
                    final_results.append(0)
            if best_method_name == "fcnn":
                maximum_precision = max(NB_NEGATIVE_PRECISION, ME_POSITIVE_PRECISION, FCNN_NEUTRAL_PRECISION + (best_method_precision / 5))
                if maximum_precision == NB_NEGATIVE_PRECISION:
                    final_results.append(-1)
                if maximum_precision == ME_POSITIVE_PRECISION:
                    final_results.append(1)
                if maximum_precision == (FCNN_NEUTRAL_PRECISION + (best_method_precision / 5)):
                    final_results.append(0)
        if input_nb_results[i] == -1 and input_me_results[i] == 0 and input_fcnn_results[i] == 1:
            if best_method_name == "nb":
                maximum_precision = max(NB_NEGATIVE_PRECISION + (best_method_precision / 5), ME_NEUTRAL_PRECISION, FCNN_POSITIVE_PRECISION)
                if maximum_precision == (NB_NEGATIVE_PRECISION + (best_method_precision / 5)):
                    final_results.append(-1)
                if maximum_precision == ME_NEUTRAL_PRECISION:
                    final_results.append(0)
                if maximum_precision == FCNN_POSITIVE_PRECISION:
                    final_results.append(1)
            if best_method_name == "me":
                maximum_precision = max(NB_NEGATIVE_PRECISION, ME_NEUTRAL_PRECISION + (best_method_precision / 5), FCNN_POSITIVE_PRECISION)
                if maximum_precision == NB_NEGATIVE_PRECISION:
                    final_results.append(-1)
                if maximum_precision == (ME_NEUTRAL_PRECISION + (best_method_precision / 5)):
                    final_results.append(0)
                if maximum_precision == FCNN_POSITIVE_PRECISION:
                    final_results.append(1)
            if best_method_name == "fcnn":
                maximum_precision = max(NB_NEGATIVE_PRECISION, ME_NEUTRAL_PRECISION, FCNN_POSITIVE_PRECISION + (best_method_precision / 5))
                if maximum_precision == NB_NEGATIVE_PRECISION:
                    final_results.append(-1)
                if maximum_precision == ME_NEUTRAL_PRECISION:
                    final_results.append(0)
                if maximum_precision == (FCNN_POSITIVE_PRECISION + (best_method_precision / 5)):
                    final_results.append(1)
        if input_nb_results[i] == 1 and input_me_results[i] == 0 and input_fcnn_results[i] == -1:
            if best_method_name == "nb":
                maximum_precision = max(NB_POSITIVE_PRECISION + (best_method_precision / 5), ME_NEUTRAL_PRECISION, FCNN_NEGATIVE_PRECISION)
                if maximum_precision == (NB_POSITIVE_PRECISION + (best_method_precision / 5)):
                    final_results.append(1)
                if maximum_precision == ME_NEUTRAL_PRECISION:
                    final_results.append(0)
                if maximum_precision == FCNN_NEGATIVE_PRECISION:
                    final_results.append(-1)
            if best_method_name == "me":
                maximum_precision = max(NB_POSITIVE_PRECISION, ME_NEUTRAL_PRECISION + (best_method_precision / 5), FCNN_NEGATIVE_PRECISION)
                if maximum_precision == NB_POSITIVE_PRECISION:
                    final_results.append(1)
                if maximum_precision == (ME_NEUTRAL_PRECISION + (best_method_precision / 5)):
                    final_results.append(0)
                if maximum_precision == FCNN_NEGATIVE_PRECISION:
                    final_results.append(-1)
            if best_method_name == "fcnn":
                maximum_precision = max(NB_POSITIVE_PRECISION, ME_NEUTRAL_PRECISION, FCNN_NEGATIVE_PRECISION + (best_method_precision / 5))
                if maximum_precision == NB_POSITIVE_PRECISION:
                    final_results.append(1)
                if maximum_precision == ME_NEUTRAL_PRECISION:
                    final_results.append(0)
                if maximum_precision == (FCNN_NEGATIVE_PRECISION + (best_method_precision / 5)):
                    final_results.append(-1)
        if input_nb_results[i] == 0 and input_me_results[i] == 1 and input_fcnn_results[i] == -1:
            if best_method_name == "nb":
                maximum_precision = max(NB_NEUTRAL_PRECISION + (best_method_precision / 5), ME_POSITIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                if maximum_precision == (NB_NEUTRAL_PRECISION + (best_method_precision / 5)):
                    final_results.append(0)
                if maximum_precision == ME_POSITIVE_PRECISION:
                    final_results.append(1)
                if maximum_precision == FCNN_NEGATIVE_PRECISION:
                    final_results.append(-1)
            if best_method_name == "me":
                maximum_precision = max(NB_NEUTRAL_PRECISION, ME_POSITIVE_PRECISION + (best_method_precision / 5), FCNN_NEGATIVE_PRECISION)
                if maximum_precision == NB_NEUTRAL_PRECISION:
                    final_results.append(0)
                if maximum_precision == (ME_POSITIVE_PRECISION + (best_method_precision / 5)):
                    final_results.append(1)
                if maximum_precision == FCNN_NEGATIVE_PRECISION:
                    final_results.append(-1)
            if best_method_name == "fcnn":
                maximum_precision = max(NB_NEUTRAL_PRECISION, ME_POSITIVE_PRECISION, FCNN_NEGATIVE_PRECISION + (best_method_precision / 5))
                if maximum_precision == NB_NEUTRAL_PRECISION:
                    final_results.append(0)
                if maximum_precision == ME_POSITIVE_PRECISION:
                    final_results.append(1)
                if maximum_precision == (FCNN_NEGATIVE_PRECISION + (best_method_precision / 5)):
                    final_results.append(-1)
        if input_nb_results[i] == 0 and input_me_results[i] == -1 and input_fcnn_results[i] == 1:
            if best_method_name == "nb":
                maximum_precision = max(NB_NEUTRAL_PRECISION + (best_method_precision / 5), ME_NEGATIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                if maximum_precision == (NB_NEUTRAL_PRECISION + (best_method_precision / 5)):
                    final_results.append(0)
                if maximum_precision == ME_NEGATIVE_PRECISION:
                    final_results.append(-1)
                if maximum_precision == FCNN_POSITIVE_PRECISION:
                    final_results.append(1)
            if best_method_name == "me":
                maximum_precision = max(NB_NEUTRAL_PRECISION, ME_NEGATIVE_PRECISION + (best_method_precision / 5), FCNN_POSITIVE_PRECISION)
                if maximum_precision == NB_NEUTRAL_PRECISION:
                    final_results.append(0)
                if maximum_precision == (ME_NEGATIVE_PRECISION + (best_method_precision / 5)):
                    final_results.append(-1)
                if maximum_precision == FCNN_POSITIVE_PRECISION:
                    final_results.append(1)
            if best_method_name == "fcnn":
                maximum_precision = max(NB_NEUTRAL_PRECISION, ME_NEGATIVE_PRECISION, FCNN_POSITIVE_PRECISION + (best_method_precision / 5))
                if maximum_precision == NB_NEUTRAL_PRECISION:
                    final_results.append(0)
                if maximum_precision == ME_NEGATIVE_PRECISION:
                    final_results.append(-1)
                if maximum_precision == (FCNN_POSITIVE_PRECISION + (best_method_precision / 5)):
                    final_results.append(1)
        if input_nb_results[i] == -1 and input_me_results[i] == -1 and input_fcnn_results[i] == 1:
            maximum_negative = max(NB_NEGATIVE_PRECISION, ME_NEGATIVE_PRECISION)
            minimum_negative = min(NB_NEGATIVE_PRECISION, ME_NEGATIVE_PRECISION)
            final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
            if final_negative_precision >= FCNN_POSITIVE_PRECISION:
                final_results.append(-1)
            else:
                final_results.append(1)
        if input_nb_results[i] == -1 and input_me_results[i] == 1 and input_fcnn_results[i] == -1:
            maximum_negative = max(NB_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
            minimum_negative = min(NB_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
            final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
            if final_negative_precision >= ME_POSITIVE_PRECISION:
                final_results.append(-1)
            else:
                final_results.append(1)
        if input_nb_results[i] == 1 and input_me_results[i] == -1 and input_fcnn_results[i] == -1:
            maximum_negative = max(ME_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
            minimum_negative = min(ME_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
            final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
            if final_negative_precision >= NB_POSITIVE_PRECISION:
                final_results.append(-1)
            else:
                final_results.append(1)
        if input_nb_results[i] == 1 and input_me_results[i] == 0 and input_fcnn_results[i] == 0:
            maximum_neutral = max(ME_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
            minimum_neutral = min(ME_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
            final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
            if final_neutral_precision >= NB_POSITIVE_PRECISION:
                final_results.append(0)
            else:
                final_results.append(1)
        if input_nb_results[i] == 0 and input_me_results[i] == 1 and input_fcnn_results[i] == 0:
            maximum_neutral = max(NB_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
            minimum_neutral = min(NB_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
            final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
            if final_neutral_precision >= ME_POSITIVE_PRECISION:
                final_results.append(0)
            else:
                final_results.append(1)
        if input_nb_results[i] == 0 and input_me_results[i] == 0 and input_fcnn_results[i] == 1:
            maximum_neutral = max(NB_NEUTRAL_PRECISION, ME_NEUTRAL_PRECISION)
            minimum_neutral = min(NB_NEUTRAL_PRECISION, ME_NEUTRAL_PRECISION)
            final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
            if final_neutral_precision >= FCNN_POSITIVE_PRECISION:
                final_results.append(0)
            else:
                final_results.append(1)
        if input_nb_results[i] == 0 and input_me_results[i] == -1 and input_fcnn_results[i] == -1:
            maximum_negative = max(ME_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
            minimum_negative = min(ME_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
            final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
            if final_negative_precision >= NB_NEUTRAL_PRECISION:
                final_results.append(-1)
            else:
                final_results.append(0)
        if input_nb_results[i] == -1 and input_me_results[i] == 0 and input_fcnn_results[i] == -1:
            maximum_negative = max(NB_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
            minimum_negative = min(NB_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
            final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
            if final_negative_precision >= ME_NEUTRAL_PRECISION:
                final_results.append(-1)
            else:
                final_results.append(0)
        if input_nb_results[i] == -1 and input_me_results[i] == -1 and input_fcnn_results[i] == 0:
            maximum_negative = max(NB_NEGATIVE_PRECISION, ME_NEGATIVE_PRECISION)
            minimum_negative = min(NB_NEGATIVE_PRECISION, ME_NEGATIVE_PRECISION)
            final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
            if final_negative_precision >= FCNN_NEUTRAL_PRECISION:
                final_results.append(-1)
            else:
                final_results.append(0)
        if input_nb_results[i] == -1 and input_me_results[i] == 0 and input_fcnn_results[i] == 0:
            maximum_neutral = max(ME_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
            minimum_neutral = min(ME_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
            final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
            if final_neutral_precision >= NB_NEGATIVE_PRECISION:
                final_results.append(0)
            else:
                final_results.append(-1)
        if input_nb_results[i] == 0 and input_me_results[i] == -1 and input_fcnn_results[i] == 0:
            maximum_neutral = max(NB_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
            minimum_neutral = min(NB_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
            final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
            if final_neutral_precision >= ME_NEGATIVE_PRECISION:
                final_results.append(0)
            else:
                final_results.append(-1)
        if input_nb_results[i] == 0 and input_me_results[i] == 0 and input_fcnn_results[i] == -1:
            maximum_neutral = max(NB_NEUTRAL_PRECISION, ME_NEUTRAL_PRECISION)
            minimum_neutral = min(NB_NEUTRAL_PRECISION, ME_NEUTRAL_PRECISION)
            final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
            if final_neutral_precision >= FCNN_NEGATIVE_PRECISION:
                final_results.append(0)
            else:
                final_results.append(-1)
        i += 1

    counter = 0
    for result in final_results:
        if result == expected_tag:
            counter += 1
    if expected_tag == 1:
        print("The combined model precision for positive tweets: " + str(round((counter / len(input_nb_results)) * 100, 2)) + " %")
    if expected_tag == -1:
        print("The combined model precision for negative tweets: " + str(round((counter / len(input_nb_results)) * 100, 2)) + " %")
    if expected_tag == 0:
        print("The combined model precision for neutral tweets: " + str(round((counter / len(input_nb_results)) * 100, 2)) + " %")


# This function receives a tweet and prints the tweet and its sentiment class
def sentiment_detector():
    input_tweet = T.get("1.0", "end")
    if input_tweet != "" and input_tweet != " " and input_tweet != " \n" and input_tweet != "\n\n":
        input_positive_dictionary = positive_comments_dictionary
        input_negative_dictionary = negative_comments_dictionary
        number_of_positive_words = total_number_of_positive_dictionary_words
        number_of_negative_words = total_number_of_negative_dictionary_words
        number_of_unique_words = unique_words_amount
        input_classifier = classifier
        lower_input_tweet = input_tweet.lower()
        me_predicted_label = input_classifier.classify(nltk_input_list_generator_online_version(lower_input_tweet))
        new_input_tweet = comment_smoother(lower_input_tweet)
        words_list = new_input_tweet.split(" ")
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

            final_result += math.log10((positive_numerator / (number_of_positive_words + number_of_unique_words)) / (
                        negative_numerator / (number_of_negative_words + number_of_unique_words)))

        if final_result > 0:
            nb_predicted_label = 1
        if final_result == 0:
            nb_predicted_label = 0
        if final_result < 0:
            nb_predicted_label = -1

        if nb_predicted_label == 1 and me_predicted_label == 1:
            final_label = 1
        if nb_predicted_label == -1 and me_predicted_label == -1:
            final_label = -1
        if nb_predicted_label == 1 and me_predicted_label == 0:
            final_label = 0
        if nb_predicted_label == -1 and me_predicted_label == 0:
            final_label = 0
        if nb_predicted_label == -1 and me_predicted_label == 1:
            final_label = -1
        if nb_predicted_label == 1 and me_predicted_label == -1:
            final_label = 1
        if nb_predicted_label == 0 and me_predicted_label == 1:
            final_label = 1
        if nb_predicted_label == 0 and me_predicted_label == -1:
            final_label = -1
        if nb_predicted_label == 0 and me_predicted_label == 0:
            final_label = 0

        if final_label == 1:
            tweets_text_box.config(state=NORMAL)
            tweets_text_box.insert(END, input_tweet.rstrip("\n") + "\n", "positive")
        if final_label == 0:
            tweets_text_box.config(state=NORMAL)
            tweets_text_box.insert(END, input_tweet.rstrip("\n") + "\n", "neutral")
        if final_label == -1:
            tweets_text_box.config(state=NORMAL)
            tweets_text_box.insert(END, input_tweet.rstrip("\n") + "\n", "negative")
        tweets_text_box.insert(END, "================================================================================\n", "separator")
        tweets_text_box.config(state=DISABLED)
        T.delete("1.0", "end")
    else:
        T.delete("1.0", "end")


# This function removes the foreground text in text box
def text_box_foreground_eraser(event):
    T.delete("1.0", "end")


# Main part of the code starts here
# Loading saved model
print("Loading saved models...")
positive_tweets_dictionary, negative_tweets_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words = dictionary_loader()
me_model_file = open("E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//MaximumEntropy//MaximumEntropyClassifier", "rb")
me_classifier = pickle.load(me_model_file)
me_model_file.close()
fcnn_model = create_model()
fcnn_model.load_weights("E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//FCNN//Checkpoints//Main Trained Model//my_checkpoint1")
number_of_unique_words = unique_words_counter(positive_tweets_dictionary, negative_tweets_dictionary)

# Initializing precision variables
# Evaluating the positive test tweets
positive_test_tweets_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//positive_test.txt"
nb_positive_test_results = nb_predictor(positive_test_tweets_file_address, positive_tweets_dictionary, negative_tweets_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words, number_of_unique_words)
me_positive_test_results = me_predictor(positive_test_tweets_file_address, 1, me_classifier)
fcnn_positive_test_tweets_file_address = "E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//FCNN//Test_X//positive_test_x_complete.txt"
fcnn_positive_test_results = fcnn_predictor(fcnn_positive_test_tweets_file_address, fcnn_model)

# Evaluating the negative test tweets
negative_test_tweets_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//negative_test.txt"
nb_negative_test_results = nb_predictor(negative_test_tweets_file_address, positive_tweets_dictionary, negative_tweets_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words, number_of_unique_words)
me_negative_test_results = me_predictor(negative_test_tweets_file_address, -1, me_classifier)
fcnn_negative_test_tweets_file_address = "E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//FCNN//Test_X//negative_test_x_complete.txt"
fcnn_negative_test_results = fcnn_predictor(fcnn_negative_test_tweets_file_address, fcnn_model)

# Evaluating the neutral test tweets
neutral_test_tweets_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//neutral_test.txt"
nb_neutral_test_results = nb_predictor(neutral_test_tweets_file_address, positive_tweets_dictionary, negative_tweets_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words, number_of_unique_words)
me_neutral_test_results = me_predictor(neutral_test_tweets_file_address, 0, me_classifier)
fcnn_neutral_test_tweets_file_address = "E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//FCNN//Test_X//neutral_test_x_complete.txt"
fcnn_neutral_test_results = fcnn_predictor(fcnn_neutral_test_tweets_file_address, fcnn_model)

NB_POSITIVE_PRECISION = precision_calculator(nb_positive_test_results, 1)
NB_NEGATIVE_PRECISION = precision_calculator(nb_negative_test_results, -1)
NB_NEUTRAL_PRECISION = precision_calculator(nb_neutral_test_results, 0)
ME_POSITIVE_PRECISION = precision_calculator(me_positive_test_results, 1)
ME_NEGATIVE_PRECISION = precision_calculator(me_negative_test_results, -1)
ME_NEUTRAL_PRECISION = precision_calculator(me_neutral_test_results, 0)
FCNN_POSITIVE_PRECISION = precision_calculator(fcnn_positive_test_results, 1)
FCNN_NEGATIVE_PRECISION = precision_calculator(fcnn_negative_test_results, -1)
FCNN_NEUTRAL_PRECISION = precision_calculator(fcnn_neutral_test_results, 0)


# Loading graphics
window = Tk()
window.title("Sentiment Analyzer")

# Adjusting window size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(str(screen_width) + "x" + str(screen_height))
background_image_resize(screen_width, screen_height, "Background_Image.png", "Background_Image_Resized.png")

# Setting GUI background image
img = PhotoImage(file="Background_Image_Resized.png")
label = Label(window, image=img, border=0)
label.place(x=0, y=0)

# Creating tweets frame
tweets_frame = tk.Frame(window)
tweets_frame_scrollbar = Scrollbar(tweets_frame)
tweets_text_box = Text(tweets_frame, height=25, width=80, relief=RIDGE, borderwidth=5, yscrollcommand=tweets_frame_scrollbar.set, bg="grey", font="calibry 12")
tweets_frame_scrollbar.pack(side=RIGHT, fill=Y)
tweets_text_box.insert(INSERT, "Recent Analyzed Tweets:\n")
tweets_text_box.config(state=DISABLED)
tweets_text_box.tag_config("positive", foreground="green")
tweets_text_box.tag_config("negative", foreground="red")
tweets_text_box.tag_config("neutral", foreground="blue")
tweets_text_box.tag_config("separator", foreground="black")

# Creating text widget and specify size
input_text_box_frame = tk.Frame(window)
T_scrollbar = Scrollbar(input_text_box_frame)
T = Text(input_text_box_frame, height=5, width=70, relief=RIDGE, borderwidth=5, yscrollcommand=T_scrollbar.set, bg="grey", font="calibry 14")
T.insert(INSERT, "Type tweet here...")
T.bind("<Button-1>", text_box_foreground_eraser)
T_scrollbar.config(command=T.yview)
T_scrollbar.pack(side=RIGHT, fill=Y)

# Creating button for receiving new tweets
b1 = Button(window, text ="Analyze Text", command=sentiment_detector, relief=RIDGE, borderwidth=3, font="calibri 12")

# Creating an Exit button
b2 = Button(window, text ="Exit", command = window.destroy, relief=RIDGE, borderwidth=3, font="calibri 12")

tweets_frame.pack(pady=(20, 20))
tweets_text_box.pack()
input_text_box_frame.pack(pady=(10, 20))
T.pack()
b1.pack(pady=(0, 10))
b2.pack()
tk.mainloop()








