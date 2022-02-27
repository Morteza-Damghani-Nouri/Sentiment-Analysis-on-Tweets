import math
import pickle
from Commons import comment_smoother
from Commons import dictionary_loader
from Commons import nltk_input_list_generator
from Commons import unique_words_counter
from Commons import final_evaluator


# Main part of the code starts here
# Loading saved models
print("Loading saved models...")
positive_comments_dictionary, negative_comments_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words = dictionary_loader()
model_file = open("E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//MaximumEntropy//MaximumEntropyClassifier", "rb")
classifier = pickle.load(model_file)
model_file.close()

# Evaluating the positive test tweets
positive_test_comments_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//positive_test.txt"
positive_test_comments_file = open(positive_test_comments_file_address, "rt", encoding="utf8")
me_results = []
nb_results = []
comments_counter = 0
true_categorization = 0
number_of_unique_words = unique_words_counter(positive_comments_dictionary, negative_comments_dictionary)
while True:
    comment = positive_test_comments_file.readline()
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
    if final_result > 0:
        nb_results.append(1)
    if final_result == 0:
        nb_results.append(0)
    if final_result < 0:
        nb_results.append(-1)
    comments_counter += 1


# Generating the test list for positive test tweets
test_list = nltk_input_list_generator(positive_test_comments_file_address, 1, [])

# Evaluating the model for positive tweets by Maximum Entropy model
total_positive_test_tweets = len(test_list)
for tweet_tuple in test_list:
    tweet_word_dictionary = tweet_tuple[0]
    main_label = tweet_tuple[1]
    predicted_label = classifier.classify(tweet_word_dictionary)
    me_results.append(predicted_label)
final_positive_results = []
positive_precision = round((final_evaluator(nb_results, me_results, final_positive_results, 1) / comments_counter) * 100, 2)

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
