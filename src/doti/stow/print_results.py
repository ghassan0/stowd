"""
Print [un]stow[-root] results.
"""


def print_results(counter):
    """Print results."""
    if counter[0] > 0:
        print("Total added to home directory: " + str(counter[0]))
    if counter[1] > 0:
        print("Total removed from home directory: " + str(counter[1]))
    if counter[2] > 0:
        print("Total added to root directory: " + str(counter[2]))
    if counter[3] > 0:
        print("Total removed from root directory: " + str(counter[3]))
    if counter[4] > 0:
        print("Total ignored: " + str(counter[4]))
    if counter[5] > 0:
        print("Total errors: " + str(counter[5]))
    if sum(counter) == 0:
        print("Nothing done")
