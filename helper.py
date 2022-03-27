from stop_words import stop_words
from db import get_ai_dict

def simplify(input):
    punct_list = [".",",","'",":",";","(",")","%"]
    temp = input.lower()
    for word in stop_words:
        temp = temp.replace(" " + word + " ", " ")
    for char in punct_list:
        temp = temp.replace(char, "")
    output = temp
    return output

def get_top_10(inp_dict):
    top_10 = []
    for counter in range(10):
        top_word =  max(inp_dict, key=inp_dict.get)
        if len(top_word) > 1:
            top_10.append(top_word)
        inp_dict.pop(top_word)
    return top_10

def count_most(input):
    words = input.split(" ")
    result = {}
    for word in words:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1
    top_10 = get_top_10(result)
    return top_10


def categorize(top_10_input, input_text):
    prediction = ""
    prediction_dict = {}
    ai_dict = get_ai_dict()
    for item in ai_dict:
        prediction_dict[item] = 0
        key_words = ai_dict[item].split(" ")
        for key_word in key_words:
            if key_word in top_10_input:
                prediction_dict[item] += 5
                print(f"** key word dected in top-10: {key_word}")
            if key_word in input_text:
                prediction_dict[item] += 1
                print(f"** key word dected in text: {key_word}")
    
    prediction = max(prediction_dict, key=prediction_dict.get)

    print()
    print(prediction_dict)
    print()
    print("prediction:", prediction)
    return prediction
    
