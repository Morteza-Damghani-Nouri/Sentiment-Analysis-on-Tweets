import tweepy
import math
from PIL import Image   # This library is used to resize the background image used in GUI
from tensorflow import keras
ENGLISH_CHARS = ["a", "b", "c",  "d",  "e",  "f",  "g",  "h",  "i",  "j",  "k",  "l",  "m",  "n",  "o",  "p",  "q",  "r",  "s",  "t",  "u",  "v",  "w",  "x",  "y",  "z",  "A",  "B",  "C",  "D",  "E",  "F",  "G",  "H",  "I",  "J",  "K",  "L",  "M",  "N",  "O",  "P",  "Q",  "R",  "S",  "T",  "U",  "V",  "W",  "X",  "Y",  "Z", "'", "\""]


# This function removes redundant characters of an input comment
def comment_smoother(input_comment):
    input_comment = input_comment.replace(".", "")
    input_comment = input_comment.replace(";", "")
    input_comment = input_comment.replace("[", "")
    input_comment = input_comment.replace("]", "")
    input_comment = input_comment.replace(":", "")
    input_comment = input_comment.replace("!", "")
    input_comment = input_comment.replace("?", "")
    input_comment = input_comment.replace(",", "")
    input_comment = input_comment.replace(")", "")
    input_comment = input_comment.replace("(", "")
    input_comment = input_comment.replace("\n", " ")
    return input_comment


# This function loads the negative and positive dictionaries
def dictionary_loader():
    print("Loading dictionaries...")
    positive_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//positive_dictionary.txt"
    negative_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//negative_dictionary.txt"
    positive_dictionary_file = open(positive_dictionary_address, "rt", encoding="utf8")
    negative_dictionary_file = open(negative_dictionary_address, "rt", encoding="utf8")
    positive_dictionary = {}
    negative_dictionary = {}
    total_number_of_negative_words = 0
    total_number_of_positive_words = 0

    # Loading positive dictionary
    while True:
        line = positive_dictionary_file.readline()
        if line == "":
            break
        index = line.find(" ")
        line_list = list(line)
        i = 0
        word = ""
        while i < index:
            word += line_list[i]
            i += 1
        i = 1
        while i <= 30:
            line_list.pop(0)
            i += 1
        count = ""
        i = 0
        while i < len(line_list):
            count += line_list[i]
            i += 1
        count = int(count)
        positive_dictionary[word] = count
        total_number_of_positive_words += count

    # Loading negative dictionary
    while True:
        line = negative_dictionary_file.readline()
        if line == "":
            break
        index = line.find(" ")
        line_list = list(line)
        i = 0
        word = ""
        while i < index:
            word += line_list[i]
            i += 1
        i = 1
        while i <= 30:
            line_list.pop(0)
            i += 1
        count = ""
        i = 0
        while i < len(line_list):
            count += line_list[i]
            i += 1
        count = int(count)
        negative_dictionary[word] = count
        total_number_of_negative_words += count

    # print("The length of positive tweets dictionary is: " + str(len(positive_dictionary)))
    # print("Total number of words in positive words dictionary is: " + str(total_number_of_positive_words))
    # print("The length of negative tweets dictionary is: " + str(len(negative_dictionary)))
    # print("Total number of words in negative words dictionary is: " + str(total_number_of_negative_words))
    # print("==============================================================================")
    return positive_dictionary, negative_dictionary, total_number_of_positive_words, total_number_of_negative_words


# This function counts unique words in both positive and negative dictionaries
def unique_words_counter(input_positive_dictionary, input_negative_dictionary):
    sorted_positive_list = sorted(input_positive_dictionary.items(), key=lambda x: x[1], reverse=True)
    sorted_negative_list = sorted(input_negative_dictionary.items(), key=lambda x: x[1], reverse=True)
    counter = 0
    for word in sorted_positive_list:
        if word[1] == 1:
            counter += 1
    for word in sorted_negative_list:
        if word[1] == 1:
            counter += 1
    return counter


# This function removes the redundant last characters of words like ?? in that?? and removes numbers and the name of seasons
def smoother_function(input_word):
    if input_word.find("0") != -1 or input_word.find("1") != -1 or input_word.find("2") != -1 or input_word.find("3") != -1 or input_word.find("4") != -1 or input_word.find("5") != -1 or input_word.find("6") != -1 or input_word.find("7") != -1 or input_word.find("8") != -1 or input_word.find("9") != -1:
        return "."
    if input_word == "january" or input_word == "february" or input_word == "march" or input_word == "april" or input_word == "may" or input_word == "june" or input_word == "july" or input_word == "august" or input_word == "september" or input_word == "october" or input_word == "november" or input_word == "december":
        return "."
    if input_word.find("/") != -1 or input_word.find("\\") != -1:
        return "."
    input_word_list = list(input_word)
    while len(input_word_list) != 0 and (input_word_list[len(input_word_list) - 1] == "." or input_word_list[len(input_word_list) - 1] == "-" or input_word_list[len(input_word_list) - 1] == ";" or input_word_list[len(input_word_list) - 1] == "[" or input_word_list[len(input_word_list) - 1] == "]" or input_word_list[len(input_word_list) - 1] == ":" or input_word_list[len(input_word_list) - 1] == "*" or input_word_list[len(input_word_list) - 1] == "!" or input_word_list[len(input_word_list) - 1] == "?" or input_word_list[len(input_word_list) - 1] == "," or input_word_list[len(input_word_list) - 1] == ")" or input_word_list[len(input_word_list) - 1] == "\"" or input_word_list[len(input_word_list) - 1] == "\'"):
        input_word_list.pop(len(input_word_list) - 1)
    while len(input_word_list) != 0 and (input_word_list[0] == "(" or input_word_list[0] == "-" or input_word_list[0] == "*" or input_word_list[0] == "\'" or input_word_list[0] == "\"" or input_word_list[0] == "." or input_word_list[0] == "?" or input_word_list[0] == "[" or input_word_list[0] == "]" or input_word_list[0] == "!"):
        input_word_list.pop(0)
    output_word = ""
    for char in input_word_list:
        if char not in ENGLISH_CHARS:
            return "."
        output_word += char
    if output_word.find(",") != -1 or output_word.find(".") != -1 or output_word.find("(") != -1 or output_word.find(")") != -1 or output_word.find("!") != -1 or output_word.find("?") != -1 or output_word.find(":") != -1 or output_word.find("+") != -1 or output_word.find("@") != -1 or output_word.find("?") != -1 or output_word.find("]") != -1 or output_word.find("[") != -1 or output_word.find("$") != -1 or output_word.find("{") != -1 or output_word.find("}") != -1 or output_word.find("~") != -1 or output_word.find("|") != -1 or output_word.find("#") != -1 or output_word.find("&") != -1 or output_word.find("%") != -1 or output_word.find("=") != -1 or output_word.find(">") != -1 or output_word.find("<") != -1 or output_word.find("+") != -1 or output_word.find("_") != -1 or output_word.find("^") != -1:
        return "."
    if output_word == "january" or output_word == "february" or output_word == "march" or output_word == "april" or output_word == "may" or output_word == "june" or output_word == "july" or output_word == "august" or output_word == "september" or output_word == "october" or output_word == "november" or output_word == "december":
        return "."
    if output_word != "" and output_word != "\n" and len(output_word) != 1:
        return output_word.replace("\n", "")
    else:
        return "."


# This function converts the input list to dictionary format which is accepted in NLTK library
def list_to_dict_converter(input_word_list):
    output_dict = {}
    for word in input_word_list:
        output_dict[word] = True
    return output_dict


# This function generates the needed dictionary as an input for nltk library
def nltk_input_list_generator(input_address, data_tag, main_list):
    input_file = open(input_address, "rt", encoding="utf8")
    line_counter = 0
    while True:
        comment = input_file.readline().lower()
        comment = comment_smoother(comment)
        if comment == "":
            break
        words_list = comment.split(" ")
        temp_list = []
        for word in words_list:
            if word != "." and word != "," and word != "  " and word != ";" and word != "\"" and word != "\'" and word != "*" and word != "(" and word != ")" and word != "--" and word != "-" and word != "?" and word != "!" and word != "&" and word != ":" and word != "_"\
                    and word != "the" and word != "and" and word != "a" and word != "i" and word != "to" and word != "of" and word != "this" and word != "that" and word != "it"\
                    and word != "in" and word != "for" and word != "you" and word != "with" and word != "on" and word != "at" and word != "an" and word != "we" and word != "he" and word != "she"\
                    and word != "they" and word.find("https") == -1 and word.find("http") == -1 and word != "rt" and word != "david" and word != "scotland":
                new_word = smoother_function(word)
                # print(word)
                if new_word != ".":
                    temp_list.append(new_word)
        main_list.append((list_to_dict_converter(temp_list), data_tag))
        line_counter += 1
        # print(str(line_counter))
    input_file.close()
    return main_list


# This function generates the needed dictionary as an input for nltk library and it is used for online tests
def nltk_input_list_generator_online_version(input_tweet):
    comment = input_tweet.lower()
    comment = comment_smoother(comment)
    words_list = comment.split(" ")
    temp_list = []
    for word in words_list:
        if word != "." and word != "," and word != "  " and word != ";" and word != "\"" and word != "\'" and word != "*" and word != "(" and word != ")" and word != "--" and word != "-" and word != "?" and word != "!" and word != "&" and word != ":" and word != "_" \
                and word != "the" and word != "and" and word != "a" and word != "i" and word != "to" and word != "of" and word != "this" and word != "that" and word != "it" \
                and word != "in" and word != "for" and word != "you" and word != "with" and word != "on" and word != "at" and word != "an" and word != "we" and word != "he" and word != "she" \
                and word != "they" and word.find("https") == -1 and word.find("http") == -1 and word != "rt" and word != "david" and word != "scotland":
            new_word = smoother_function(word)
            # print(word)
            if new_word != ".":
                temp_list.append(new_word)
    return list_to_dict_converter(temp_list)


# This function connects to my developer Twitter acount and returns the API
def twitter_authenticator():
    consumer_key_file = open("E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//My Final Project Twitter API Keys//Consumer Key.txt", "rt")
    consumer_key = consumer_key_file.readline().rstrip("\n")
    consumer_key_file.close()
    consumer_secret_file = open("E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//My Final Project Twitter API Keys//Consumer Secret.txt", "rt")
    consumer_secret = consumer_secret_file.readline().rstrip("\n")
    consumer_secret_file.close()
    access_token_file = open("E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//My Final Project Twitter API Keys//Access Token.txt", "rt")
    access_token = access_token_file.readline().rstrip("\n")
    access_token_file.close()
    access_token_secret_file = open("E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//My Final Project Twitter API Keys//Access Token Secret.txt", "rt")
    access_token_secret = access_token_secret_file.readline().rstrip("\n")
    access_token_secret_file.close()
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


# This function resizes the background image according to screen width and height
def background_image_resize(input_width, input_height, input_image_address, output_image_address):
    image = Image.open(input_image_address)
    new_image = image.resize((input_width, input_height))
    new_image.save(output_image_address)


# This function loads the negative and positive dictionaries and it is used in FCNN code
def dictionary_loader_fcnn():
    positive_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//positive_dictionary.txt"
    negative_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//negative_dictionary.txt"
    positive_dictionary_file = open(positive_dictionary_address, "rt", encoding="utf8")
    negative_dictionary_file = open(negative_dictionary_address, "rt", encoding="utf8")
    positive_dictionary = {}
    negative_dictionary = {}

    # Loading positive dictionary
    while True:
        line = positive_dictionary_file.readline()
        if line == "":
            break
        index = line.find(" ")
        line_list = list(line)
        i = 0
        word = ""
        while i < index:
            word += line_list[i]
            i += 1
        i = 1
        while i <= 30:
            line_list.pop(0)
            i += 1
        count = ""
        i = 0
        while i < len(line_list):
            count += line_list[i]
            i += 1
        count = int(count)
        positive_dictionary[word] = count

    # Loading negative dictionary
    while True:
        line = negative_dictionary_file.readline()
        if line == "":
            break
        index = line.find(" ")
        line_list = list(line)
        i = 0
        word = ""
        while i < index:
            word += line_list[i]
            i += 1
        i = 1
        while i <= 30:
            line_list.pop(0)
            i += 1
        count = ""
        i = 0
        while i < len(line_list):
            count += line_list[i]
            i += 1
        count = int(count)
        negative_dictionary[word] = count

    return positive_dictionary, negative_dictionary


# This function generates the dictionary which is used in the neural network
def model_dictionary_generator():
    output_model_dictionary = {"": 0}
    positive_comments_dictionary, negative_comments_dictionary = dictionary_loader_fcnn()
    i = 0
    positive_words_list = list(positive_comments_dictionary.keys())
    while i < len(positive_words_list):
        if positive_words_list[i] not in output_model_dictionary:
            output_model_dictionary[positive_words_list[i]] = len(output_model_dictionary)
        i += 1
    negative_words_list = list(negative_comments_dictionary.keys())
    for word in negative_words_list:
        if word not in positive_comments_dictionary:
            output_model_dictionary[word] = len(output_model_dictionary)

    return output_model_dictionary


# This function generates lists like train_y or test_y
def y_list_generator(input_size, input_tag):
    output_list = []
    i = 1
    while i <= input_size:
        output_list.append(input_tag)
        i += 1
    return output_list


# This function converts an input string list to a list
def string_to_list_converter(input_string):
    output_list = []
    primary_list = input_string.split(" ")
    for element in primary_list:
        element = element.replace(",", "")
        element = element.replace("[", "")
        element = element.replace("]", "")
        output_list.append(int(element))

    return output_list


# This function reads the train_x or test_x lists from a file and stores them in a list
def x_file_reader(file_address):
    output_list = []
    file = open(file_address, "rt")
    counter = 1
    while True:
        temp = file.readline()
        if temp == "":
            break
        temp = temp.replace("\n", "")
        output_list.append(string_to_list_converter(temp))
        # print(counter)
        counter += 1
    file.close()
    return output_list


# This function receives a list of data and the desired tag and returns the accuracy. if a data is exactly 1/2 then the related element in the list will be -1
def evaluate(input_data, desired_tag):
    data_tag_list = []
    i = 0
    while i < len(input_data):
        maximum = max(input_data[i][0], input_data[i][1], input_data[i][2])
        if maximum == input_data[i][0]:
            data_tag_list.append("positive")
        if maximum == input_data[i][1]:
            data_tag_list.append("neutral")
        if maximum == input_data[i][2]:
            data_tag_list.append("negative")
        i += 1
    correct_counter = 0
    i = 0
    while i < len(data_tag_list):
        if data_tag_list[i] == desired_tag:
            correct_counter += 1
        i += 1
    # print("The data tag list length is: " + str(len(data_tag_list)))
    return round((correct_counter / len(data_tag_list)) * 100, 2)


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


# This function generates Naive Bayes model results for the input test tweet and this function is used in online version code
def nb_predictor_online_version(input_tweet, input_positive_dictionary, input_negative_dictionary, input_positive_words_count, input_negative_words_count, input_unique_words_count):
    output_results = []
    tweet = input_tweet.lower()
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

        final_result += math.log10((positive_numerator / (input_positive_words_count + input_unique_words_count)) / (
                    negative_numerator / (input_negative_words_count + input_unique_words_count)))
    if final_result > 0:
        output_results.append(1)
    if final_result == 0:
        output_results.append(0)
    if final_result < 0:
        output_results.append(-1)
    return output_results


# This function generates Maximum Entropy model results for the input test file
def me_predictor(input_test_file_address, input_desired_label, input_classifier):
    output_results = []
    test_tweets_list = nltk_input_list_generator(input_test_file_address, input_desired_label, [])
    for tweet_tuple in test_tweets_list:
        tweet_word_dictionary = tweet_tuple[0]
        predicted_label = input_classifier.classify(tweet_word_dictionary)
        output_results.append(predicted_label)
    return output_results


# This function generates Maximum Entropy model results for the input tweet and this function is used in online version code
def me_predictor_online_version(input_tweet, input_classifier):
    output_results = []
    tweet_word_dictionary = nltk_input_list_generator_online_version(input_tweet)
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


# This function generates FCNN model results for the input tweet and this function is used in online version code
def fcnn_predictor_online_version(input_tweet, input_fcnn_model):
    output_results = []
    model_predictions = input_fcnn_model.predict(input_tweet)
    for prediction in model_predictions:
        maximum = max(prediction[0], prediction[1], prediction[2])
        if maximum == prediction[0]:
            output_results.append(1)
        if maximum == prediction[1]:
            output_results.append(0)
        if maximum == prediction[2]:
            output_results.append(-1)
    return output_results


# This function calculates the precision of different models on different test data and initializes related variable
def precision_calculator(input_results, input_desired_label):
    counter = 0
    for result in input_results:
        if result == input_desired_label:
            counter += 1
    return round((counter / len(input_results)) * 100, 2)


# This function generates data with proper format to be fed to the fully connected neural network
def data_loader_online_version(input_tweet, input_model_dictionary):
    output_list = []
    comment = input_tweet
    words_list = comment.split(" ")
    temp_list = []
    for word in words_list:
        if word != "." and word != "," and word != "  " and word != ";" and word != "\"" and word != "\'" and word != "*" and word != "(" and word != ")" and word != "--" and word != "-" and word != "?" and word != "!" and word != "&" and word != ":" and word != "_" \
                and word != "the" and word != "and" and word != "a" and word != "i" and word != "to" and word != "of" and word != "this" and word != "that" and word != "it" \
                and word != "in" and word != "for" and word != "you" and word != "with" and word != "on" and word != "at" and word != "an" and word != "we" and word != "he" and word != "she" \
                and word != "they" and word.find("https") == -1 and word.find("http") == -1 and word != "rt" and word != "david" and word != "scotland":
            new_word = smoother_function(word)
            if new_word != ".":
                if new_word in input_model_dictionary:
                    temp_list.append(input_model_dictionary[new_word])

    i = 47 - len(temp_list)
    if i < 0:
        new_temp_list = []
        m = 0
        while m <= 46:
            new_temp_list.append(temp_list[m])
            m += 1
        output_list.append(new_temp_list)
    else:
        j = 1
        while j <= i:
            temp_list.append(0)
            j += 1
        output_list.append(temp_list)
    return output_list












