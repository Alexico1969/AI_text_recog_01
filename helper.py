todo = "todo"

def simplify(input):
    strip_list = ["the", "a", "to", "from", "it", "in", "not", "are", "is", "have", "has", "was", "she", "he", "of", "by"]
    temp = input.lower()
    for word in strip_list:
        temp = temp.replace(word + " ", "")
    output = temp
    print(output)
    return output

def get_top_10(inp_dict):
    max_nr =  max(inp_dict, key=inp_dict.get)
    print("max:", max_nr)
    return max_nr

def count_most(input):
    words = input.split(" ")
    result = {}
    for word in words:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1
    print("result: ", result)
    print("max:", get_top_10(result))
    return result

def count_most_weighed(input):
    print(todo)

def categorize(input):
    print(todo)
    
