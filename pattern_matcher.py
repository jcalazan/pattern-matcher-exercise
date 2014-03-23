__author__ = 'Jonathan Calazan (jonathan@calazan.com)'

"""
Pattern-Matching Paths - Coding Exercise

Requirements:
    - Ignore leading and trailing slashes.
    - Inputs must be read from stdin and output to stdout.
    - If a wildcard exists, find the best match by fewest wildcard.
    - If more than 1 possible match and the patterns have the same number of
      wildcards, go with the pattern where the leftmost wildcard is furthest
      to the right.
    - If match is not found, output 'NO MATCH'.

Assumptions:
    - Each pattern is unique (we can break the search as soon as an exact
      match is found).
    - Each path may appear more than once (we can't remove patterns in the
      pattern list when exact matches are found).
    - Fields in the pattern can't be empty.
    - Input contains ASCII characters only.
    - First line of the input is an integer specifying the number of patterns,
      and the following lines contains one pattern per line. The paths then
      follow the patterns starting with an integer specifying the number of
      paths.
"""

import sys
from itertools import islice
from operator import eq


WILDCARD = '*'
PATTERN_DELIMITER = ','
PATH_DELIMITER = '/'


def main():
    """
    Read the standard input and print to the standard output (print adds a
    newline character by default, so it's preferred in this case as per
    requirement instead of sys.stdout.write()).
    """
    # Remove the newline character and create a generator object.
    inputs = (line.rstrip('\n') for line in sys.stdin)

    # Retrieve the patterns. We're assuming that the first line is an integer
    # specifying the number of patterns. Note that after slicing, the elements
    # will be removed from the generator ('inputs'). The patterns will be
    # stored in a list as we'll need to reuse them.
    pattern_size = int(list((islice(inputs, 1)))[0])
    patterns = list(islice(inputs, pattern_size))

    # Retrieve the paths.
    path_size = int(list((islice(inputs, 1)))[0])
    paths = islice(inputs, path_size)

    for path in paths:
        print find_match(path, patterns)


def find_match(path, patterns):
    """
    Find a match for a given path in a list of patterns.

    Steps:
        1. Convert the path and patterns to lists.
        2. If the two lists match exactly, then a match is found and no need
           to look further.
        3. If the two lists have the same number of fields and contains a
           wildcard, check for a potential match.
        4. If there's only one potential match, return that.
        5. If there's more than one potential match, then get the best one
           by fewest number of wildcards.
        6. If number of wildcards are the same, resolve the tie by choosing
           the pattern whose leftmost wildcard is furthest to the right.
    """
    # Remove leading and trailing slashes.
    path_fields = path.strip(PATH_DELIMITER).split(PATH_DELIMITER)

    exact_match = None
    potential_matches = []
    for pattern in patterns:
        # Remove leading and trailing commas.
        pattern_fields = pattern.strip(PATTERN_DELIMITER)\
            .split(PATTERN_DELIMITER)

        # Exact match found, break the loop.
        if path_fields == pattern_fields:
            exact_match = pattern_fields
            break
        # List sizes match and wildcard character in the pattern,
        # could be a possible match.
        elif len(path_fields) == len(pattern_fields) \
            and WILDCARD in pattern_fields:
            if is_potential_match(path_fields, pattern_fields):
                potential_matches.append(pattern_fields)

    if exact_match:
        return to_string(exact_match)
    elif potential_matches:
        if len(potential_matches) == 1:
            return to_string(potential_matches[0])
        else:
            best_match = get_best_potential_match(potential_matches)
            return to_string(best_match)
    else:
        return 'NO MATCH'


def is_potential_match(path_fields, pattern_fields):
    """
    Check whether the given pattern is a potential match.

    Steps:
        1. Count the number of wildcards in pattern_fields.
        2. Compare the path_fields and pattern_fields and count the fields that
           are equal.
        3. Check whether the size of path_fields equals the the number of
           matched fields plus the number of wildcards.
    """
    num_wildcards = pattern_fields.count(WILDCARD)
    num_field_matches = map(eq, path_fields, pattern_fields).count(True)

    if (num_field_matches + num_wildcards) == len(path_fields):
        return True
    else:
        return False


def get_best_potential_match(potential_matches):
    """
    Find the best matching pattern.

    Steps:
        1. The pattern with the fewest wildcards wins.
        2. If there's a tie, resolve it by taking the sum of the indexes
           of the wildcard elements. Highest sum wins.
    """
    fewest_wildcards = []
    wildcard_counter = None

    for match in potential_matches:
        num_wildcards = match.count(WILDCARD)

        # First entry.
        if not wildcard_counter:
            wildcard_counter = num_wildcards
            fewest_wildcards.append(match)
        else:
            # If fewer wildcards than the last element, empty the list and
            # insert the new element.
            if num_wildcards < wildcard_counter:
                wildcard_counter = num_wildcards
                fewest_wildcards[:] = []
                fewest_wildcards.append(match)
            # If the same number of wildcards as the last element, simply
            # append.
            elif num_wildcards == wildcard_counter:
                fewest_wildcards.append(match)

    if len(fewest_wildcards) == 1:
        return fewest_wildcards[0]
    else:
        return resolve_tie(fewest_wildcards)


def resolve_tie(pattern_fields):
    """
    Return the pattern whose leftmost wildcard is furthest to the right.

    Since the patterns have the same number of wildcards at this point, we can
    just get the sum of the index of the wildcard elements.  Whichever has
    the highest value wins.

    Each pattern is unique, so no need to check for duplicates.
    """
    winner = None
    highest_score = None

    for pattern in pattern_fields:
        index_sum = sum([i for i, v in enumerate(pattern) if v == WILDCARD])

        # First entry.
        if highest_score is None:
            highest_score = index_sum
            winner = pattern
        elif index_sum > highest_score:
            highest_score = index_sum
            winner = pattern

    return winner


def to_string(list_value):
    """
    Converts a list to a comma separated string.
    """
    return ','.join(list_value)


if __name__ == '__main__':
    main()