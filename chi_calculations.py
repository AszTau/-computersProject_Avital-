import math

# This function calculates an average  value 'z'
def average_calc(values, y_errors):
    # Square the error of y.
    y_errors_squared = map(lambda y: y ** 2, y_errors)
    # numerator list
    top = []
    # denominator
    bottom = []

    for i in range(len(values)):
        # Calculate the ratio between the average value and the squared value of y error.
        top.append(values[i] / y_errors[i])
        # Calculate the inverse of  y error (1/dy^2).
        bottom.append(1 / y_errors[i])

    # Returns the 'average' calculation.
    return sum(top) / sum(bottom)


def _chi_squared(table):
    # Calculate parameters a and b
    a = _a(table)
    b = _b(table)

    # the table values
    x_values = table["x"]
    x_errors = table["dx"]
    y_values = table["y"]
    y_errors = table["dy"]

    # Calculate chi.
    ratios = []
    for i in range(len(x_values)):
        ratios.append(((y_values[i] - (a * x_values[i] + b)) / y_errors[i]))

    # Square the values.
    chi_squared_values = map(lambda value: value ** 2, ratios)

    # Return the sum of the individual chi squared values.
    return sum(chi_squared_values)

    #Calculate chi squared reduced.
def _chi_reduced(chi_squared, N):
    return chi_squared / (N - 2)


# Calculate the 'a' parameter
def _a(table):
    # Get the values
    x_values = table["x"]
    x_errors = table["dx"]
    y_values = table["y"]
    y_errors = table["dy"]

    # Calculate new values for the formula.
    xy_values = []
    x_values_squared = []
    for i in range(len(x_values)):
        xy_values.append(x_values[i] * y_values[i])
        x_values_squared.append(x_values[i] ** 2)

    # Average values for a
    xy_average = average_calc(xy_values, y_errors)
    x_average = average_calc(x_values, y_errors)
    y_average = average_calc(y_values, y_errors)
    x_squared_average = average_calc(x_values_squared, y_errors)

    return (xy_average - x_average * y_average) / (x_squared_average - x_average ** 2)


# Calculate the 'b' parameter
def _b(table):
    # Get the table values
    x_values = table["x"]
    x_errors = table["dx"]
    y_values = table["y"]
    y_errors = table["dy"]

    a = _a(table)
    x_average = average_calc(x_values, y_errors)
    y_average = average_calc(y_values, y_errors)

    return y_average - x_average * a


# Calculate uncertainty of 'a'
def _da(table):
    # Get the table values
    x_values = table["x"]
    x_errors = table["dx"]
    y_values = table["y"]
    y_errors = table["dy"]

    y_errors_squared = []
    x_values_squared = []
    n = len(x_values)
    for i in range(n):
        y_errors_squared.append(y_errors[i] ** 2)
        x_values_squared.append(x_errors[i] ** 2)

    dy_squared_average = average_calc(y_errors_squared, y_errors)
    x_squared_average = average_calc(x_values_squared, y_errors)
    x_average = average_calc(x_values, y_errors)

    return dy_squared_average / (n * (x_squared_average - x_average ** 2))


# Calculate uncertainty of 'b'.
def _db(table):
    # Get the table values
    x_values = table["x"]
    x_errors = table["dx"]
    y_values = table["y"]
    y_errors = table["dy"]

    y_errors_squared = []
    x_values_squared = []
    n = len(x_values)
    for i in range(n):
        y_errors_squared.append(y_errors[i] ** 2)
        x_values_squared.append(x_errors[i] ** 2)

    dy_squared_average = average_calc(y_errors_squared, y_errors)
    x_squared_average = average_calc(x_values_squared, y_errors)
    x_average = average_calc(x_values, y_errors)

    return (dy_squared_average * (x_average ** 2)) / (n * (x_squared_average - x_average ** 2))


# This function returns the results of the linear fit
def fit_results(table):
    a = _a(table)
    b = _b(table)
    da = _da(table)
    db = _db(table)
    chi_squared = _chi_squared(table)
    chi_squared_reduced = _chi_reduced(chi_squared, len(table["x"]))

    return a, b, da, db, chi_squared, chi_squared_reduced


def bonus_chi_squared(table, func, a):
    # Get the table values
    x_values = table["x"]
    x_errors = table["dx"]
    y_values = table["y"]
    y_errors = table["dy"]

    # Calculate chi values
    ratios = []
    for i in range(len(x_values)):
        temp = y_errors[i] ** 2
        temp += (func(x_values[i] + x_errors[i], a) - func(x_values[i] - x_errors[i], a)) ** 2
        ratios.append((y_values[i] - func(x_values[i], a)) / (temp ** 0.5))

    # Square the values.
    chi_squared_values = map(lambda value: value ** 2, ratios)

    # Return the sum
    return sum(chi_squared_values)
