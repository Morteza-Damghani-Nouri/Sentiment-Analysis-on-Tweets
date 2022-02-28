from Commons import nb_smoother_function


# This function receives a list which is sorted by sorted function and produces the output dictionary file
def sorted_dictionary_printer(input_list, output_address, category):
    output_dictionary_file = open(output_address, "wt", encoding="utf8")
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
    input_file = open(input_address, "rt", encoding="utf8")
    line_counter = 0
    while True:
        comment = input_file.readline().lower()
        if comment == "":
            break

        words_list = comment.split(" ")
        for word in words_list:
            if word != "." and word != "," and word != "  " and word != ";" and word != "\"" and word != "\'" and word != "*" and word != "(" and word != ")" and word != "--" and word != "-" and word != "?" and word != "!" and word != "&" and word != ":" and word != "_"\
                    and word != "the" and word != "and" and word != "a" and word != "i" and word != "to" and word != "of" and word != "this" and word != "that" and word != "it"\
                    and word != "in" and word != "for" and word != "you" and word != "with" and word != "on" and word != "at" and word != "an" and word != "we" and word != "he" and word != "she"\
                    and word != "they" and word.find("https") == -1 and word.find("http") == -1:
                new_word = nb_smoother_function(word)
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
positive_train_data_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Train//positive_train.txt"
negative_train_data_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Train//negative_train.txt"

positive_output_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//positive_dictionary.txt"
negative_output_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//negative_dictionary.txt"

positive_words_dictionary = {}
negative_words_dictionary = {}

# Generating the dictionaries
dictionary_generator(negative_words_dictionary, negative_train_data_address, negative_output_dictionary_address, "negative")
dictionary_generator(positive_words_dictionary, positive_train_data_address, positive_output_dictionary_address, "positive")
print("All of the dictionaries generated")




