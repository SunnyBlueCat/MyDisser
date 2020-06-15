import csv

def csv_reader(file_obj):
    reader = csv.reader(file_obj, delimiter=';')
    my_dict = {rows[0]: rows[1] for rows in reader}
    return my_dict

def findMelody(words):
    csv_path = "word.csv"

    with open(csv_path, "r") as f_obj:
        dict = csv_reader(f_obj)

    melody = []
    found_words = []
    for i in range(len(words)):
        if words[i] in dict:
            melody.append(dict.get(words[i]))
            if words[i] not in found_words:
                found_words.append(words[i])

    return melody, found_words
