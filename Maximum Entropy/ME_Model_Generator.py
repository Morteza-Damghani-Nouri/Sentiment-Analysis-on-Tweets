import nltk
import pickle   # This library is used to save the model on disk

ENGLISH_CHARS = ["a", "b", "c",  "d",  "e",  "f",  "g",  "h",  "i",  "j",  "k",  "l",  "m",  "n",  "o",  "p",  "q",  "r",  "s",  "t",  "u",  "v",  "w",  "x",  "y",  "z",  "A",  "B",  "C",  "D",  "E",  "F",  "G",  "H",  "I",  "J",  "K",  "L",  "M",  "N",  "O",  "P",  "Q",  "R",  "S",  "T",  "U",  "V",  "W",  "X",  "Y",  "Z", "'", "\""]
# This function converts the input list to dictionary format which is accepted in NLTK library
def list_to_dict_converter(input_word_list):
    output_dict = {}
    for word in input_word_list:
        output_dict[word] = True
    return output_dict


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


# This function generates the needed dictionary
def nltk_input_list_generator(input_address, data_tag, main_list):
    input_file = open(input_address, "rt", encoding="utf8")
    line_counter = 0
    while True:
        comment = input_file.readline().lower()
        if comment == "":
            break

        words_list = comment.split(" ")
        temp_list = []
        for word in words_list:
            if word != "." and word != "," and word != "  " and word != ";" and word != "\"" and word != "\'" and word != "*" and word != "(" and word != ")" and word != "--" and word != "-" and word != "?" and word != "!" and word != "&" and word != ":" and word != "_"\
                    and word != "the" and word != "and" and word != "a" and word != "i" and word != "to" and word != "of" and word != "this" and word != "that" and word != "it"\
                    and word != "in" and word != "for" and word != "you" and word != "with" and word != "on" and word != "at" and word != "an" and word != "we" and word != "he" and word != "she"\
                    and word != "they" and word.find("https") == -1 and word.find("http") == -1:
                new_word = smoother_function(word)
                # print(word)
                if new_word != ".":
                    temp_list.append(new_word)
        main_list.append((list_to_dict_converter(temp_list), data_tag))
        line_counter += 1
        print(str(line_counter))
    input_file.close()
    return main_list


# Main part of the code starts here
# Generating the train list
positive_train_tweets_address = "C://Users//user//Desktop//New Dataset 3//Train//positive_train.txt"
negative_train_tweets_address = "C://Users//user//Desktop//New Dataset 3//Train//negative_train.txt"
neutral_train_tweets_address = "C://Users//user//Desktop//New Dataset 3//Train//neutral_train (short version).txt"
train_list = nltk_input_list_generator(positive_train_tweets_address, 1, [])
train_list = nltk_input_list_generator(negative_train_tweets_address, -1, train_list)
train_list = nltk_input_list_generator(neutral_train_tweets_address, 0, train_list)
print("The length of train list is: " + str(len(train_list)))

# Training the model
numIterations = 20
algorithm = nltk.classify.MaxentClassifier.ALGORITHMS[0]
print("Training the model...")
classifier = nltk.MaxentClassifier.train(train_list, algorithm, max_iter=numIterations)
classifier.show_most_informative_features(10)

# Saving the model on disk...
print("Saving the model on disk...")
model_file = open('MaximumEntropyClassifier', 'wb')
pickle.dump(classifier, model_file)
model_file.close()

# Generating the test list for positive test tweets
positive_test_tweets_address = "C://Users//user//Desktop//New Dataset 3//Test//positive_test.txt"
test_list = nltk_input_list_generator(positive_test_tweets_address, 1, [])
print("The length of test list for positive test tweets is: " + str(len(test_list)))

# Evaluating the model for positive tweets
print("Evaluating the model for positive test tweets...")
true_categorization = 0
total_positive_test_tweets = len(test_list)
for tweet_tuple in test_list:
    tweet_word_dictionary = tweet_tuple[0]
    main_label = tweet_tuple[1]
    predicted_label = classifier.classify(tweet_word_dictionary)
    if main_label == predicted_label:
        true_categorization += 1
print("The precision of the model for positive tweets is: " + str(round((true_categorization / total_positive_test_tweets) * 100, 2)) + " %")

# Generating the test list for negative test tweets
negative_test_tweets_address = "C://Users//user//Desktop//New Dataset 3//Test//negative_test.txt"
test_list = nltk_input_list_generator(negative_test_tweets_address, -1, [])
print("The length of test list for negative test tweets is: " + str(len(test_list)))

# Evaluating the model for negative tweets
print("Evaluating the model for negative test tweets...")
true_categorization = 0
total_negative_test_tweets = len(test_list)
for tweet_tuple in test_list:
    tweet_word_dictionary = tweet_tuple[0]
    main_label = tweet_tuple[1]
    predicted_label = classifier.classify(tweet_word_dictionary)
    print("main_label: " + str(main_label) + "    predicted_label: " + str(predicted_label))
    if main_label == predicted_label:
        true_categorization += 1
print("The precision of the model for negative tweets is: " + str(round((true_categorization / total_negative_test_tweets) * 100, 2)) + " %")

# Generating the test list for neutral test tweets
neutral_test_tweets_address = "C://Users//user//Desktop//New Dataset 3//Test//neutral_test.txt"
test_list = nltk_input_list_generator(neutral_test_tweets_address, 0, [])
print("The length of test list for neutral test tweets is: " + str(len(test_list)))

# Evaluating the model for neutral tweets
print("Evaluating the model for neutral test tweets...")
true_categorization = 0
total_neutral_test_tweets = len(test_list)
for tweet_tuple in test_list:
    tweet_word_dictionary = tweet_tuple[0]
    main_label = tweet_tuple[1]
    predicted_label = classifier.classify(tweet_word_dictionary)
    if main_label == predicted_label:
        true_categorization += 1
print("The precision of the model for neutral tweets is: " + str(round((true_categorization / total_neutral_test_tweets) * 100, 2)) + " %")


















