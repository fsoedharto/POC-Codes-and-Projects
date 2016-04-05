"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import math
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"

codeskulptor.set_timeout(100)

# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    non_duplicates = []
    # Good for non sorted list
    # for dummy_list in list1:
    #    if dummy_list not in non_duplicates:
    #        non_duplicates.append(dummy_list)
    
    # Alternate implementation (Maybe the fastest)
    index = 0
    for dummy_list in list1:
        if non_duplicates == []:
            non_duplicates.append(dummy_list)
        elif non_duplicates[index] != dummy_list:
            non_duplicates.append(dummy_list)
            index += 1
    return non_duplicates

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    intersections = []
    
    # This is a binary search algorithm
    # Searches exhaustively through list1 while
    # using binary search to list 2
    # Compare the lengths to make it more efficient
    
    for dummy_idx in range(len(list1)):
        position = len(list2) / 2
        increment = len(list2) / 2
        for dummy_half in range(len(list2)):
            # Increment
            increment = increment / 2
            
            # If the increment is zero, then change
            # increment by just one.
            if increment == 0:
                increment = 1
            # print position, list2[position], dummy_idx, list1[dummy_idx]
            if list1[dummy_idx] > list2[position]:
                position = position + increment
                if position >= len(list2):
                    break
            elif list1[dummy_idx] < list2[position]:
                position = position - increment
                if position < 0:
                    break
            else:
                intersections.append(list2[position])
                break
                
    return intersections

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merges two sorted list.
    """
    # Create copies of the two lists
    list1_copy = list(list1)
    list2_copy = list(list2)
    answer = []
    
    # Reiterates over the list until one of them is empty
    while list1_copy != [] and list2_copy != []:
        
        if list1_copy[0] > list2_copy[0]:
            answer.append(list2_copy.pop(0))
        else:
            answer.append(list1_copy.pop(0))
    
    # Adds up the remaining list
    if list1_copy == []:
        answer += list2_copy
    elif list2_copy == []:
        answer += list1_copy
    
    return answer
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    
    full_range = len(list1)
    half_range = int(math.ceil(full_range / 2.0))
    # Split the list into two
    # then recursively call sort to get the sorted list
    # and then call merge on the sorted list
    if len(list1) < 2:
        # base case
        # if less than two length then just return the list
        return list1
    else:
        # recursive case
        # call the merge sort method by dividing the list into
        # two
        return merge(merge_sort(list1[0:half_range]), merge_sort(list1[half_range:full_range]))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    # Split the input words into two parts first and last
    # Generate rest strings by inserting the first character
    # to every possible position
    #
    if word == '':
        # base case
        # returns an empty string if the word is an empty
        # string
        return [word]
    else:
        # Separate the word into first characters and the
        # rest, generate the rest of the strings recursively
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        
        # Add generate series of strings by adding the first
        # character into the each of the generated string
        # if it is an empty string, just add the character
        new_strings = []
        for dummy_strings in rest_strings:
            if dummy_strings == '':
                new_strings.append(first)
            else:
                for dummy_idx in range(len(dummy_strings)+1):
                    new_strings.append(dummy_strings[0:dummy_idx] + first + dummy_strings[dummy_idx:])
        return rest_strings + new_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    strings = []
    
    # Load the url
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    huge_strings = netfile.read()
    
    # Reiterates through the strings and store each words
    # into a list everytime it sees a newline
    temp_string = ''
    for dummy_strings in huge_strings:
        if dummy_strings == '\n':
            strings += [temp_string]
            temp_string = ''
        else:
            temp_string += dummy_strings
    
    return strings

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

# print intersect([8, 10, 12, 13], [1, 2, 3, 8])
# print intersect([0, 4, 6, 10], [10])
