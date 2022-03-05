import pickle   # This library is used to load the trained model from disk
from Commons import nltk_input_list_generator


# Main part of the code starts here
# Loading the saved trained model
model_file = open("MaximumEntropyClassifier", "rb")
classifier = pickle.load(model_file)
model_file.close()

# Generating the test list for positive test tweets
positive_test_tweets_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//positive_test.txt"
test_list = nltk_input_list_generator(positive_test_tweets_address, 1, [])
print("Number of positive test tweets: " + str(len(test_list)))

# Evaluating the model for positive tweets
true_categorization = 0
total_positive_test_tweets = len(test_list)
for tweet_tuple in test_list:
    tweet_word_dictionary = tweet_tuple[0]
    main_label = tweet_tuple[1]
    predicted_label = classifier.classify(tweet_word_dictionary)
    if main_label == predicted_label:
        true_categorization += 1
print("The precision of the model for positive tweets is: " + str(round((true_categorization / total_positive_test_tweets) * 100, 2)) + " %")
print("================================================================================================================")

# Generating the test list for negative test tweets
negative_test_tweets_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//negative_test.txt"
test_list = nltk_input_list_generator(negative_test_tweets_address, -1, [])
print("Number of negative test tweets: " + str(len(test_list)))

# Evaluating the model for negative tweets
true_categorization = 0
total_negative_test_tweets = len(test_list)
for tweet_tuple in test_list:
    tweet_word_dictionary = tweet_tuple[0]
    main_label = tweet_tuple[1]
    predicted_label = classifier.classify(tweet_word_dictionary)
    if main_label == predicted_label:
        true_categorization += 1
print("The precision of the model for negative tweets is: " + str(round((true_categorization / total_negative_test_tweets) * 100, 2)) + " %")
print("================================================================================================================")

# Generating the test list for neutral test tweets
neutral_test_tweets_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//neutral_test.txt"
test_list = nltk_input_list_generator(neutral_test_tweets_address, 0, [])
print("Number of neutral test tweets: " + str(len(test_list)))

# Evaluating the model for neutral tweets
true_categorization = 0
total_neutral_test_tweets = len(test_list)
for tweet_tuple in test_list:
    tweet_word_dictionary = tweet_tuple[0]
    main_label = tweet_tuple[1]
    predicted_label = classifier.classify(tweet_word_dictionary)
    if main_label == predicted_label:
        true_categorization += 1
print("The precision of the model for neutral tweets is: " + str(round((true_categorization / total_neutral_test_tweets) * 100, 2)) + " %")
