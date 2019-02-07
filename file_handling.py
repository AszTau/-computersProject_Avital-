import os.path

# Error prints.
length_error = "Input file error: Data lists are not the same length."
non_positive_uncertainty_error = "Input file error: Not all uncertainties are positive."
path_invalid_error = "Input file error: path invalid."

def is_filename_valid(filename):
    # Check if  path is valid.
    if not (os.path.exists(filename)):
        return (False)

    # Everything is valid
    return True


def fix_table(lines):
    table = {"x": [], "dx": [], "y": [], "dy": []}

    # Check that all the rows are the same length.
    if (len(set([len(line.split(" ")) for line in lines])) != 1):
        print(length_error)
        exit()

    # Check if the file is in column format.
    if all([part in ['x', 'y', 'dx', 'dy'] for part in lines[0].lower().split(" ")]):
        # finds the original order of the columns.
        order_of_columns = lines[0].lower().split(" ")

        # Insert the values into the relevant keys.
        for line in lines[1:]:
            for col in range(len(order_of_columns)):
                table[order_of_columns[col]].append(float(line.split(" ")[col]))
    else:
        for line in lines:
            table[line.lower().split(" ")[0]] = list(map(float, line.split(" ")[1:]))

    return table


def check_data(table):
    # Check dx.
    for value in table["dx"]:
        if (value <= 0):
            print(non_positive_uncertainty_error)
            return None

    # Check dy
    for value in table["dy"]:
        if (value <= 0):
            print(non_positive_uncertainty_error)
            return None

    # The table is valid.
    return (table)


def get_content(filename):
    with open(filename, "r") as file_handling:
        lines = file_handling.readlines()

        # Remove empty lines.
        new_lines = []
        for line in lines:
            if line.strip("\n") != "":
                new_lines.append(line.strip("\n"))

        # Get graph titles.
        y_title = new_lines.pop(len(new_lines) - 1)[8:]
        x_title = new_lines.pop(len(new_lines) - 1)[8:]

        # Correct the table.
        table = fix_table(new_lines)

        return (y_title, x_title, check_data(table))

    # Default return value (Error with file).
    return "", "", None


# This function receives a file and returns a table of data points.
def file_handling(filename):
    if (False == is_filename_valid(filename)):
        print(path_invalid_error)
        exit()

    return get_content(filename)


def bonus_file_handling(filename):
    with open(filename, "r") as file_handling:
        lines = file_handling.readlines()

        # Remove empty spaces.
        new_lines = []
        for line in lines:
            if line.strip("\n") != "":
                new_lines.append(line.strip("\n"))

        # Convert values to float.
        b = new_lines.pop(len(new_lines) - 1).split(" ")
        a = new_lines.pop(len(new_lines) - 1).split(" ")

        #  range of a and b.
        a = (float(a[1]), float(a[2]), float(a[3]))
        b = (float(b[1]), float(b[2]), float(b[3]))

        # Get graph titles.
        y_title = new_lines.pop(len(new_lines) - 1)[8:]
        x_title = new_lines.pop(len(new_lines) - 1)[8:]

        # Correct the table.
        table = fix_table(new_lines)

        return a, b, y_title, x_title, check_data(table)

    # Default return value in case of error
    return None, None, "", "", None
