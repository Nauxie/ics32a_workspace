from pathlib import Path
import os
eligible_paths = [] # store eligible paths
interesting_paths = [] # store interesting paths


def sort_iterdir(input_path_list: [list]) -> list: 
    ''' Turns the list casted iterdir generator Into a sorted list of Paths '''
    string_list = [] 
    for path in input_path_list:
        string_list.append(path.as_posix()) # turns list of Paths into list of strings
    string_list.sort() # sorts that list of strings
    path_list = []
    for string in string_list:
        path_list.append(Path(string)) # turns list of strings back into (sorted) list of Paths
    return path_list

def regularDirect(inpt: [str]) -> None:
    '''Prints out all the files in a  directory'''
    if (inpt.startswith('D ')):  # path starts with D (directory)
        inpt = inpt[2:] # gets rid of the D 
        my_path = Path(inpt) 
        if (my_path.exists()): # only make path eligible if it exists
            for subpath in sort_iterdir(list(my_path.iterdir())):
                if(subpath.is_file()): # if subpath is file, print and make eligible
                    print(subpath)
                    eligible_paths.append(subpath)
        else:
            print('ERROR')
            regularDirect(input()) # restart input
        

    else:
        print('ERROR')
        regularDirect(input())


def specialDirect(inpt: [str]) -> None:
    '''Prints out all files in directory including subdirectories'''
    if (inpt.startswith('R ')):  # path starts with R (directory) 
        inpt = inpt[2:] # removes R 
        my_path = Path(inpt)
        if (my_path.exists()): # makes file path eligible if exists
            for subpath in sort_iterdir(list(my_path.iterdir())):
                if(subpath.is_file()): # if file, make eligible
                    print(subpath)
                    eligible_paths.append(subpath)

            for subpath in sort_iterdir(my_path.iterdir()): # if directory, recurisvely call method on new subdirectory
                if(subpath.is_dir()):
                    specialDirect('R ' + subpath.as_posix())
        else:
            print('ERROR')
            specialDirect(input())

    elif (inpt.startswith('D ')): # redirects to D method (regularDirect())
        regularDirect(inpt)
    else:
        print('ERROR')
        specialDirect(input())


def narrow_interesting(interest: [str]) -> None:
    '''narrows the interesting files based off of input'''
    if (interest == 'A'):
        for path in eligible_paths: # adds all elgible paths to interesting paths
            print(path)
            interesting_paths.append(path) 
    elif (interest.startswith('N ')): 
        interest = interest[2:]
        for path in eligible_paths: # if filename matches input, make interesting
            if (path.as_posix()[path.as_posix().rfind('/')+1:] == interest): #checks if the string after the last '/' matches the file
                print(path)
                interesting_paths.append(path)
    elif (interest.startswith('E ')):
        interest = interest[2:]
        for path in eligible_paths: # if extension matches input, make interesting
            if (path[path.find('.'):] == interest or path[path.find('.')+1:] == interest): #checks if the text after or including and after the dot in the path matches
                print(path)
                interesting_paths.append(path) 
    elif (interest.startswith('T ')): 
        interest = interest[2:]
        uniquefiles = [] # keep track of which files have been printed so even if there are multiple occurences of text, it will only be printed once
        for path in eligible_paths:
            try:
                my_file = open(path, 'r')
                for line in my_file:
                    if (interest in line): # if input is on any line
                        if (path not in uniquefiles): #only if this file hasn't been counted as having the input text, then print and make interesting
                            print(path)
                            interesting_paths.append(path)
                            uniquefiles.append(path)
                my_file.close()
            except UnicodeDecodeError: # if file cannot be opened, then ignore it (pass it)
                pass
    elif (interest.startswith('< ')):
        interest = interest[2:]
        for path in eligible_paths:
            size = path.stat().st_size # size of file
            if (size < interest): 
                print(path)
                interesting_paths.append(path)
    elif (interest.startswith('> ')):
        interest = int(interest[2:])
        for path in eligible_paths:
            size = path.stat().st_size
            if (size > interest):
                print(path)
                interesting_paths.append(path)
    else:
        print('ERROR')
        narrow_interesting(input())

def take_action(action: [str]) -> None:
    '''Acts upon interesting directories based off of input'''
    if (action == 'F'):
        for path in interesting_paths:
            try:
                my_file = open(path, 'r')
                print(my_file.readline().rstrip()) # prints first line of file
                my_file.close()

            except UnicodeDecodeError: # prints NOT TEXT if file cannot be opened
                print('NOT TEXT')
    elif(action == 'D'):
        for path in interesting_paths:
            my_file = open(path.as_posix()+'.dup', 'w+') # writes new file with .dup extension
            my_file.close()

    elif(action == 'T'):
        for path in interesting_paths:
            path.touch() # update timestamp on file
    else:
        print('ERROR')
        take_action(input()) 

#begin main running sequence
path_input = input()
specialDirect(path_input) 
interesting = input()
narrow_interesting(interesting)
if (len(interesting_paths) != 0):
    change = input()
    take_action(change)
# end main sequence

