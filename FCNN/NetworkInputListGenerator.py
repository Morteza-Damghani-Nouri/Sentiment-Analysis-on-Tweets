from Commons import smoother_function
from Commons import model_dictionary_generator


# This function generates data with proper format to be fed to the network
def data_loader(file_address, input_model_dictionary):
    input_file = open(file_address, "rt", encoding="utf8")
    output_list = []
    counter = 1
    while True:
        comment = input_file.readline()
        if comment == "":
            break

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
        print(counter)
        counter += 1

    input_file.close()
    return output_list


# This function receives a list and saves the list into a file
def file_generator(input_list, input_file_name):
    file = open(input_file_name, "wt")
    for element in input_list:
        file.write(str(element) + "\n")
    file.close()



# Main part of the code starts here
# Generating train lists
model_dictionary = model_dictionary_generator()
positive_train_x = data_loader("E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Train//positive_train.txt", model_dictionary)
print("Saving the data on positive_train_x.txt...")
file_generator(positive_train_x, "Train_X//positive_train_x.txt")
print("positive_train_x file generated")
negative_train_x = data_loader("E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Train//negative_train.txt", model_dictionary)
print("Saving the data on negative_train_x.txt...")
file_generator(negative_train_x, "Train_X//negative_train_x.txt")
print("negative_train_x file generated")
neutral_train_x = data_loader("E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Train//neutral_train.txt", model_dictionary)
print("Saving the data on neutral_train_x.txt...")
file_generator(neutral_train_x, "Train_X//neutral_train_x.txt")
print("neutral_train_x file generated")
print("All train_x files generated")

# Generating test lists
positive_test_x = data_loader("E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//positive_test.txt", model_dictionary)
print("Saving the data on positive_test_x_complete.txt...")
file_generator(positive_test_x, "Test_X//positive_test_x_complete.txt")
print("positive_test_x_complete file generated")
negative_test_x = data_loader("E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//negative_test.txt", model_dictionary)
print("Saving the data on negative_test_x_complete.txt...")
file_generator(negative_test_x, "Test_X//negative_test_x_complete.txt")
print("negative_test_x_complete file generated")
neutral_test_x = data_loader("E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//neutral_test.txt", model_dictionary)
print("Saving the data on neutral_test_x_complete.txt...")
file_generator(neutral_test_x, "Test_X//neutral_test_x_complete.txt")
print("neutral_test_x_complete file generated")
print("All test_x files generated")

