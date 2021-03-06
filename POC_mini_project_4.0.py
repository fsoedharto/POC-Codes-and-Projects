"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
Lower level might be needed
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand


    Returns an integer score 
    """
    # Only works when sorted
    
    max_score = 0
    
    # Algorithm for finding the maximum score
    for dummy_hand in hand:
        if max_score <= (hand.count(dummy_hand) * dummy_hand):
            max_score = dummy_hand * hand.count(dummy_hand)
    
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    # Copies the held dice in another variable
    held_dice_lst = tuple(held_dice)
    
    # Generates the number of possible dice list based on the
    # number of free dice and dice sides
    possible_dice_list = gen_all_sequences(range(1, num_die_sides+1), num_free_dice)
    
    # Reiterates over the list of possible dice list and
    # combines them with the held dice
    held_possible_combo = list([])
    for dummy_dice_list in possible_dice_list:
        empty_dice_list = held_dice_lst
        empty_dice_list += dummy_dice_list
        empty_dice_list = tuple(sorted(empty_dice_list))
        held_possible_combo.append(empty_dice_list)
    
    sum_possible_values = 0.0
    for dummy_dice_hand in held_possible_combo:
        sum_possible_values += float(score(dummy_dice_hand))
    sum_possible_values /= (num_die_sides ** num_free_dice)
    
    return sum_possible_values

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    
    # The first thing to do is to enumerate the indices
    # of the hand with [0, 1, 2, ...] which will be used
    # when retreving the cards from the list
    generate_all_indices = gen_all_sequences(range(0, len(hand)), len(hand))
    generate_unique_indices = set([()])
    for dummy_indices in generate_all_indices:
        generate_unique_indices.add(tuple(sorted(set(dummy_indices))))
    
    all_holds = set([()])
    for dummy_all_holds in generate_unique_indices:
        temp = list([])
        for dummy_indices in dummy_all_holds:
            temp.append(hand[dummy_indices])
        temp = tuple(temp)
        all_holds.add(temp)
    
    return all_holds

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds_value = gen_all_holds(hand)
    max_expected_val = 0.0
    max_val_hold = tuple()
    for dummy_all_holds in all_holds_value:
        expect_val = expected_value(dummy_all_holds, num_die_sides, len(hand)-len(dummy_all_holds))
        if (expect_val >= max_expected_val):
            max_val_hold = tuple(dummy_all_holds)
            max_expected_val = expect_val
        
    return (max_expected_val, max_val_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = ((1,))
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
run_example()

# import poc_holds_testsuite
# poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



