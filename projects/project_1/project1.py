from pathlib import Path
import os
path_input = input()
eligible_paths = []
interesting_paths = []


def sort_iterdir(gen: [list]) -> list:
    ''' Turns the list casted iterdir generator Into a sorted list of Paths '''
    list2 = []
    for path in gen:
        list2.append(path.as_posix())
    list2.sort()
    list3 = []
    for string in list2:
        list3.append(Path(string))
    return list3

def regularDirect(inpt: [str]) -> None:
    '''Prints out all the files in a  directory'''
    if (inpt.startswith('D ')):  # path starts with D (directory)
        inpt = inpt[2:]
        my_path = Path(inpt)
        if (my_path.exists()):
            for subpath in sort_iterdir(list(my_path.iterdir())):
                if(subpath.is_file()):
                    print(subpath)
                    eligible_paths.append(subpath.as_posix())
        else:
            print('ERROR')
            regularDirect(input())
        

    else:
        print('ERROR')
        regularDirect(input())


def specialDirect(inpt: [str]) -> None:
    '''Prints out all files in directory including subdirectories'''
    if (inpt.startswith('R ')):  # path starts with R (directory)
        inpt = inpt[2:]
        my_path = Path(inpt)
        if (my_path.exists()):
            for subpath in sort_iterdir(list(my_path.iterdir())):
                if(subpath.is_file()):
                    print(subpath)
                    eligible_paths.append(subpath.as_posix())

            for subpath in sort_iterdir(my_path.iterdir()):
                if(subpath.is_dir()):
                    specialDirect('R ' + subpath.as_posix())
        else:
            print('ERROR')
            specialDirect(input())

    elif (inpt.startswith('D ')):
        regularDirect(inpt)
    else:
        print('ERROR')
        specialDirect(input())


def narrow_interesting(interest: [str]) -> None:
    '''narrows the interesting files based off of letter'''
    if (interest == 'A'):
        for string in eligible_paths:
            print(string)
            interesting_paths.append(string)
    elif (interest.startswith('N ')):
        interest = interest[2:]
        for string in eligible_paths:
            if (string.endswith(interest)):
                print(string)
                interesting_paths.append(string)
    elif (interest.startswith('E ')):
        interest = interest[2:]
        for string in eligible_paths:
            if (string[string.find('.'):] == interest or string[string.find('.')+1:] == interest):
                print(string)
                interesting_paths.append(string)
    elif (interest.startswith('T ')):
        interest = interest[2:]
        uniquefiles = []
        for string in eligible_paths:
            try:
                my_file = open(string, 'r')
                # print(my_file)
                for line in my_file:
                    if (interest in line):
                        if (string not in uniquefiles):
                            print(string)
                            interesting_paths.append(string)
                            uniquefiles.append(string)

            except UnicodeDecodeError:
                pass
    elif (interest.startswith('< ')):
        interest = interest[2:]
        interest = int(interest)
        for string in eligible_paths:
            size = Path(string).stat().st_size
            if (size < interest):
                print(string)
                interesting_paths.append(string)
    elif (interest.startswith('> ')):
        interest = interest[2:]
        interest = int(interest)
        for string in eligible_paths:
            size = Path(string).stat().st_size
            if (size > interest):
                print(string)
                interesting_paths.append(string)
    else:
        print('ERROR')
        narrow_interesting(input())

def take_action(action: [str]) -> None:
    '''Acts upon interesting directories based off of input'''
    if (action == 'F'):
        for string in interesting_paths:
            try:
                my_file = open(string, 'r')
                print(my_file.readline().rstrip())

            except UnicodeDecodeError:
                print('NOT TEXT')
    elif(action == 'D'):
        for string in interesting_paths:
            my_file = open(string+'.dup', 'w+')

    elif(action == 'T'):
        for string in interesting_paths:
            Path(string).touch()
    else:
        print('ERROR')
        take_action(input())

#begin main sequence
specialDirect(path_input) 
interesting = input()
narrow_interesting(interesting)
if (len(interesting_paths) != 0):
    change = input()
    take_action(change)
# end main sequence

if __name__ == '__main__':
    print('hello')
