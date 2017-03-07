import logging
from utils import *

def eliminate_twins(values, unit, twin_boxes, twin_value):
    for remove_box in unit:
        if (remove_box not in twin_boxes):
            for i in twin_value:
                assign_value(values, remove_box, values[remove_box].replace(i, ''))

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Get all the units
    digits = '123456789'
    twins = {}

    # Identify twins and values
    for unit in unitlist:
        # Check whether another box has a twin
        twin_boxes = []

        for box in unit:
            if (len(values[box]) == 2):
                twin_found = False
                twin_value = ''
                # Identify the twin and the value
                for twin in unit:
                    if ((box != twin) and (values[box] == values[twin])):
                        twin_boxes = [box, twin]
                        logging.debug(' Twins %s -> %s', box, twin)
                        twin_value = values[box]
                        twin_found = True

                # Remove the digits from the other boxes in unit
                if (twin_found):
                    eliminate_twins(values, unit, twin_boxes, twin_value)


    return values
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    # Check lenght of grid values
    assert len(grid) == 81
    digits = '123456789'
    # Replace empty values with all possible values
    grid = [box.replace('.', digits) for box in grid]
    sudoku_grid = dict(zip(boxes, grid))

    return sudoku_grid



def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    # Iterate over all boxes and dentify the boxes with single digits
    single_digits_boxes = [k for k, v in values.items() if len(v) == 1]

    # Get all the peers
    for box in single_digits_boxes:
        for peer in peers[box]:
            # Remove the value from the peers that do not hold a single digit
            if (len(values[peer]) > 1):
                assign_value(values, peer, values[peer].replace(values[box], ''))

    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # Get all the units
    digits = '123456789'
    for unit in unitlist:
        # Check whether a digit is present in a box
        for digit in digits:
            boxes_with_digit = [box for box in unit if digit in values[box]]
            # Assign the only choice digit to the box value
            if len(boxes_with_digit) == 1:
                assign_value(values, boxes_with_digit[0], digit)

    return values

def reduce_puzzle(values):
    """Reduce the solution using the solution strategies to prune search space.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after applying the solution strategies.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Your code here: Use the Naked Twins Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """Using depth-first search and propagation, create a search tree and solve the sudoku.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after solving the sudoku.
    """

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    # Exit condition. the puzzle is not resolved
    if (False == values):
        return False

    # Check whether the puzzle is resolved
    multiple_digits_boxes = {k : v for k, v in values.items() if len(v) > 1}
    if not multiple_digits_boxes:
        # Puzzle solved
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    fewest_possibilities_square = min(multiple_digits_boxes, key=multiple_digits_boxes.get)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[fewest_possibilities_square]:
        # Make sure the original values are not changed
        new_values = values.copy()
        assign_value(new_values, fewest_possibilities_square, value)
        new_values = search(new_values)
        if new_values:
            return new_values

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # Search return either the solution or False and assign it to values
    values = grid_values(grid)
    values = search(values)

    return values


def main():
    config_log()
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        logging.error(' We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

if __name__ == '__main__':
    main()
