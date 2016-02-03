"""
This module contains a function that merges a single row 
or column in 2048.
"""

def merge(line):
    """
    This function merges a single row or column in 2048.
    Takes a list of numbers, sorts them, and merges them
    as according to 2048 rules and returns the list of
    merged numbers the same length as the input line.
    """

    # The sorting step
    # Creates a list of zeros the same length as line
    sorted_list = []
    for dummy_line in line:
        sorted_list.append(0)
        
    # Sorts non-zero elements into the a new intermediate
    # list
    idx = 0
    for dummy_line in line:
        if not dummy_line == 0:
            sorted_list[idx] = dummy_line
            idx += 1
    
    # The merging step
    # Creates a list of zeroes to the new_list the same
    # length as the given line. This will be the list that
    # stores the merged numbers
    new_list = []
    for dummy_line in sorted_list:
        new_list.append(0)
    
    # Merges the sorted non-zero elements to the list
    idx = 0
    for dummy_line in sorted_list:
        if not dummy_line == 0:
            
            # Store the element into the list if the
            # current element of the list is zero
            if new_list[idx] == 0:
                new_list[idx] = dummy_line
            
            # If an element in the sorted list is equal to 
            # the one stored on the list merge them 
            # together and assigns new spot to store the
            # next element by incrementing the index
            elif new_list[idx] == dummy_line:
                new_list[idx] = 2 * dummy_line
                idx += 1
                
            # If sorted element is not equal to the one in
            # the stored list, store elements on the next
            # list
            else:
                idx += 1
                new_list[idx] = dummy_line
                
    return new_list
