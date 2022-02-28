import pickle
import math
from Commons import dictionary_loader
from Commons import nltk_input_list_generator_online_version
from Commons import comment_smoother
from colorama import Fore as color  # This module is used to print a text with different color
from Commons import unique_words_counter

# This function receives a tweet and prints the tweet and its sentiment class
def sentiment_detector(input_tweet, input_positive_dictionary, input_negative_dictionary, number_of_positive_words, number_of_negative_words, number_of_unique_words, input_classifier):
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

        final_result += math.log10((positive_numerator / (number_of_positive_words + number_of_unique_words)) / (negative_numerator / (number_of_negative_words + number_of_unique_words)))

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
        print(color.GREEN + input_tweet)
    if final_label == 0:
        print(color.WHITE + input_tweet)
    if final_label == -1:
        print(color.RED + input_tweet)

    print(color.RESET + "==============================================================================")

# Main part of the code starts here


# Loading saved model
print("Loading saved models...")
positive_comments_dictionary, negative_comments_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words = dictionary_loader()
model_file = open("E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//MaximumEntropy//MaximumEntropyClassifier", "rb")
classifier = pickle.load(model_file)
model_file.close()
unique_words_amount = unique_words_counter(positive_comments_dictionary, negative_comments_dictionary)

while True:
    tweet = input("Enter tweet or enter exit to exit: ")
    if tweet == "exit":
        break
    sentiment_detector(tweet, positive_comments_dictionary, negative_comments_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words, unique_words_amount, classifier)








