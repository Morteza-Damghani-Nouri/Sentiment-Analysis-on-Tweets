import tweepy
import pickle
import math
from Commons import twitter_authenticator
from Commons import dictionary_loader
from Commons import nltk_input_list_generator_online_version
from Commons import comment_smoother


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









# Main part of the code starts here
# Twitter Authentication
api = twitter_authenticator()

# Loading saved model
print("Loading saved models...")
positive_comments_dictionary, negative_comments_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words = dictionary_loader()
model_file = open("E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//MaximumEntropy//MaximumEntropyClassifier", "rb")
classifier = pickle.load(model_file)
model_file.close()



# WOEID of Washington
woeid = 2514815

# Storing received tweets in a file
my_dataset = open("My Dataset.txt", "at", encoding="utf8")
my_dataset.write("==============================================================================\n")

# fetching the top 50 trends topics in Washington
trends = api.get_place_trends(id=woeid)
trend_topics_names = []
for value in trends:
    for trend in value['trends']:
        trend_topics_names.append(trend['name'])
print("Top 50 trend topics are: ")
for name in trend_topics_names:
    print(name)
print("==============================================================================")
print("Receiving tweets...")
received_tweets = []
i = 0
while i < 4:
    results = tweepy.Cursor(api.search_tweets, q=trend_topics_names[i], tweet_mode = "extended").items(10)
    for result in results:
       if result.lang == "en":
        received_tweets.append(result.full_text)
        my_dataset.write(result.full_text + "\n")
    i += 1
print("len: " + str(len(received_tweets)))
for tweet in received_tweets:
    print(tweet)









my_dataset.close()





















