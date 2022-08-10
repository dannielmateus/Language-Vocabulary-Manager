# Vocabulary builder

import random
import json
import os

open("WORDS.txt", "a+")
with open("WORDS.txt", "r", encoding="utf-8") as f:
    words = f.read().splitlines()
    f.close()

f = open("stats.json")
json_stats = json.load(f)
if json_stats["language1"] == "" or json_stats["language2"] == "":
    lang1 = input("To start, choose your primary language: ")
    lang2 = input("Now choose your secondary language you wanna learn: ")
    json_stats["language1"] = lang1
    json_stats["language2"] = lang2
    with open('stats.json', 'w') as f:
        json.dump(json_stats, f)
        f.close()

lang1 = json_stats["language1"]
lang2 = json_stats["language2"]

def reset():
    os.remove("WORDS.txt")  
    open("WORDS.txt", "a+")
    with open('stats.json', 'w') as f:
        for stat in json_stats:
            print(stat)
            if stat == ("language1" or "language2"):
                json_stats[stat] = ""
            else:
                json_stats[stat] = 0
        json.dump(json_stats, f)

def change_language():
        new_lang1 = input("Choose the new primary language: ")
        new_lang2 = input("Choose the new secundary language: ")
        json_stats["language1"] = new_lang1
        json_stats["language2"] = new_lang2

def show_stats():
    print("\nLanguages: ", json_stats["language1"], "/", json_stats["language2"])
    print("Questions done: ", json_stats["questions_count"])
    print("Correct answers: ", json_stats["correct_count"])
    print("Wrong answers: ", json_stats["wrong_count"])
    print("Words learned: ", json_stats["word_count"])

def separate_words(words):  # words = "word1 word2"
    space = words.find(" ")
    word1 = words[:space]
    word2 = words[space+1:]
    return [word1, word2]

while True:
    with open("WORDS.txt", "rt", encoding="utf-8") as f:
        words = f.read().splitlines()

    choice = input("\nWhat do you want to do? \n[add word, exam, see stats, see words learned, reset, exit]\n")
    
    if choice == "exit":
        exit()

    if choice == "reset":
        done = 0
        while done == 0:
            yn = input("Are you sure you want to reset? That will delete your stats and learned words. [Yes/No]\n")
            if yn == "Yes":
                reset()
                done += 1
            if yn == "No":
                done += 1
            if yn != ("Yes" or "No"):
                print("Can not compute answer ", yn, ", try again")
                
    if choice == "see stats":
        json_stats["word_count"] = len(words)
        show_stats()

    if choice == "add word":
        def add_word():
            new_word = lambda lang : "Write the word in " + lang + ":"
            print(new_word(lang1))
            word_lang1 = input()
            print(new_word(lang2))
            word_lang2 = input()
            with open("WORDS.txt", "a+", encoding="utf-8") as f:
                f.write(word_lang1 + " " + word_lang2 + "\n")
            print("New words added: ", word_lang1, ", ", word_lang2)
        add_word()
        with open('stats.json', 'w') as f:
            json.dump(json_stats, f)

    if choice == "exam":
        # Check if there are enough words
        if len(words) < 4:
            print("\nYou need to add more words first!")
        else:
            # Select number of questions
            num_questions = input("Choose the number of questions: ")
            # Start correct questions counter   
            exam_correct_count = 0
            # Do "num_questions" questions
            for exam_question in range(int(num_questions)):
                # Update questions counter for every question
                json_stats["questions_count"] += 1
                print("\nQuestion ", exam_question+1)
                # Function to pick random options
                def pick_random():
                    idx_question = random.randint(0, len(words)-1)
                    question_word = separate_words(words[idx_question])
                    random_words = []
                    idxs = []
                    i = 0
                    while i <= 2:
                        idx_rdn = random.randint(0, len(words)-1)
                        if idx_rdn != idx_question and idxs.count(idx_rdn) == 0:
                            random_words.append(separate_words(words[idx_rdn]))
                            i += 1
                    return [question_word, random_words]
                
                # Choose either to translate lang1 -> lang2 or lang2 -> lang1
                methods = [1, 2] # lang1 -> lang2, lang2 -> lang1
                method = methods[random.randint(0, 1)] # Choose random method
                if method == methods[0]:
                    # Generate exam question and options
                    exam = pick_random()
                    print("\nWhat is the translation of: " + exam[0][0] + " ?")
                    # Print options
                    options = []
                    for i in range(len(exam[1])):
                        options.append(exam[1][i][1])
                    correct_answer = exam[0][1]
                    options.append(correct_answer)
                    random.shuffle(options)
                    q = 1
                    for option in options:
                        print(q, "-", option)
                        q += 1
                    # Check answer
                    answer = input("\n=> ")
                    if answer in ["1", "2", "3", "4"]:
                        print("Please write the complete word instead of the number: ")
                        answer = input("\n=> ")
                    if answer == correct_answer:
                        print("Correct answer! :D")
                        json_stats["correct_count"] += 1
                        exam_correct_count +=1
                    else:
                        print("Wrong answer! :(\nCorrect answer is: " + correct_answer)
                        json_stats["wrong_count"] += 1
                    with open('stats.json', 'w') as f:
                        json.dump(json_stats, f)

                if method == methods[1]:
                    exam = pick_random()
                    print("\nWhat is the translation of: " + exam[0][1] + " ?")
                    options = []
                    for i in range(len(exam[1])):
                        options.append(exam[1][i][0])
                    correct_answer = exam[0][0]
                    options.append(correct_answer)
                    random.shuffle(options)
                    q = 1
                    for option in options:
                        print(q, "-", option)
                        q += 1
                    answer = input("\n=> ")
                    answer = input("\n=> ")
                    if answer in ["1", "2", "3", "4"]:
                        print("Please write the complete word instead of the number: ")
                        answer = input("\n=> ")
                    if answer == correct_answer:
                        print("Correct answer! :D")
                        json_stats["correct_count"] += 1
                        exam_correct_count +=1
                    else:
                        print("Wrong answer! :(\nCorrect answer is: " + correct_answer)
                        json_stats["wrong_count"] += 1
                    with open('stats.json', 'w') as f:
                        json.dump(json_stats, f)
            print("Exam done. Your score: ", exam_correct_count, "/", num_questions)

    if choice == "see words learned":
        print("\nWords learned:")
        if words == []:
            print("\nNo words were added yet.")
        i = 0
        for word_list in words:
            i += 1
            print(i, "-", separate_words(word_list)[0], "/", separate_words(word_list)[1])
