import tweepy
import pickle
from Commons import twitter_authenticator
from Commons import dictionary_loader
# This function receives a tweet and prints the tweet and its sentiment class
# def sentiment_detector(input_tweet):







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





















