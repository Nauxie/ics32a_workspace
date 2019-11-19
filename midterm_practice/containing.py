sentence_list = ['I am Boo', ['I wear Boots', [
    'Boo is love'], 'Nothing here'], 'Boo says hi', [['Boo']]]
return_arr = []


def containing_word(slist, target):

    for i in slist:
        if (type(i) == list):
            (containing_word(i, target))
        else:
            if (target in i.split()):
                return_arr.append(i)
    return(return_arr)


print(containing_word(sentence_list, 'Boo'))
