"""
Support for pipe-separated values (PSV) format.
"""

__author__ = "Nassib Nassar"
__copyright__ = "Copyright (C) 2013 Nassib Nassar"
__license__ = "MIT"

def align(psv):
    """
    Given a string containing PSV, return an equivalent PSV with the columns
    aligned.
    """
    # Split the given PSV into a table (list of lists)
    table = [ [field.strip() for field in line.split('|')]
              for line in psv.splitlines() ]
    # Look at the first row to determine the number of columns
    num_columns = len(table[0]) if len(table) > 0 else 0
    # Initialize a list that will store the maximum width of each column
    width = [0 for x in range(num_columns)]
    # Scan all fields to find the maximum width of each column
    for row in table:
        for f, field in enumerate(row):
            w = len(field)
            if w > width[f]:
                width[f] = w
    # Append spaces to each field to pad it to a uniform width
    for row in table:
        for f, field in enumerate(row):
            pad = width[f] - len(field)
            row[f] = field + (' ' * pad)
    # Convert the table back to PSV
    aligned = '\n'.join([' | '.join(row) for row in table])
    return aligned

if __name__ == '__main__':
    pass
