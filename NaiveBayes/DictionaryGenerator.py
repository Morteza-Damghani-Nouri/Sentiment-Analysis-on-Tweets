
ENGLISH_CHARS = ["a", "b", "c",  "d",  "e",  "f",  "g",  "h",  "i",  "j",  "k",  "l",  "m",  "n",  "o",  "p",  "q",  "r",  "s",  "t",  "u",  "v",  "w",  "x",  "y",  "z",  "A",  "B",  "C",  "D",  "E",  "F",  "G",  "H",  "I",  "J",  "K",  "L",  "M",  "N",  "O",  "P",  "Q",  "R",  "S",  "T",  "U",  "V",  "W",  "X",  "Y",  "Z", "'", "\""]
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


# This function receives a list which is sorted by sorted function and produces the output dictionary file
def sorted_dictionary_printer(input_list, output_address, category):
    output_dictionary_file = open(output_address, "wt")
    if category == "positive":
        for word in input_list:
            if word[1] > 0 and len(word[0]) < 30:
                output_dictionary_file.write(word[0] + " " * (30 - len(word[0])) + str(word[1]) + "\n")
    else:
        for word in input_list:
            if word[1] > 0 and 30 > len(word[0]):
                output_dictionary_file.write(word[0] + " " * (30 - len(word[0])) + str(word[1]) + "\n")
    output_dictionary_file.close()


# This function generates the needed dictionary
def dictionary_generator(input_dictionary, input_address, output_address, category):
    input_file = open(input_address, "rt", encoding="cp850")
    line_counter = 0
    while True:
        comment = input_file.readline()
        if comment == "":
            break

        words_list = comment.split(" ")
        for word in words_list:
            if word != "." and word != "," and word != "  " and word != ";" and word != "\"" and word != "\'" and word != "*" and word != "(" and word != ")" and word != "--" and word != "-" and word != "?" and word != "!" and word != "&" and word != ":" and word != "_"\
                    and word != "the" and word != "and" and word != "a" and word != "i" and word != "to" and word != "of" and word != "this" and word != "that" and word != "it"\
                    and word != "in" and word != "for" and word != "you" and word != "with" and word != "on" and word != "at" and word != "an" and word != "we" and word != "he" and word != "she"\
                    and word != "they" and word.find("https") == -1 and word.find("http") == -1:
                new_word = smoother_function(word)
                # print(word)
                if new_word != ".":
                    if new_word in input_dictionary:
                        input_dictionary[new_word] += 1
                    else:
                        input_dictionary[new_word] = 1

        line_counter += 1
        print(str(line_counter))
    input_file.close()

    # Sorting the dictionary (sorted function returns a list)
    print("Sorting...")
    sorted_list = sorted(input_dictionary.items(), key=lambda x: x[1], reverse=True)
    print("Printing output dictionary to the file...")
    sorted_dictionary_printer(sorted_list, output_address, category)


# Main part of the code starts here
positive_train_data_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Train Dataset for Twitter//Dataset//Complete Dataset//Train//positive_train_tweets.txt"
negative_train_data_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Train Dataset for Twitter//Dataset//Complete Dataset//Train//negative_train_tweets (short version3).txt"

positive_output_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Naive Bayes//Unigram//Dictionaries//unigram_positive_dictionary.txt"
negative_output_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Naive Bayes//Unigram//Dictionaries//unigram_negative_dictionary.txt"

positive_words_dictionary = {}
negative_words_dictionary = {}
neutral_words_dictionary = {}

# Generating the dictionaries
dictionary_generator(negative_words_dictionary, negative_train_data_address, negative_output_dictionary_address, "negative")
# dictionary_generator(neutral_words_dictionary, neutral_train_data_address, neutral_output_dictionary_address, "neutral")
dictionary_generator(positive_words_dictionary, positive_train_data_address, positive_output_dictionary_address, "positive")
print("All of the dictionaries generated")




