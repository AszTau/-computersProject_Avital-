import file_handling as filehandling
import chi_calculations as fitgui
from matplotlib import pyplot
from matplotlib.mlab import frange
import numpy as np

output_format = \
"a = {a_value} ± {a_error}\n" \
"b = {b_value} ± {b_error}\n" \
"chi2 = {chi_squared}\n" \
"chi2_reduced={chi_reduced}"

def linear_function(x, a):
	return (a[1] + x * a[0])

#BONUS function
def my_function(x, a):
	return (a[0] + x*a[1] + 0.5*a[2]*(x**2))

# Draw the red fitted line
def plot_fitted_graph(min, max, a, func = linear_function, c = "red"):
	x_values = np.array(frange(min, max))
	y_values = [func(x, a) for x in x_values]
	pyplot.plot(x_values, y_values, color = c)

# Plot the crosses on the graph.
def plot_data_points(table):
	# Get the table values
	x_values = table["x"]
	x_errors = table["dx"]
	y_values = table["y"]
	y_errors = table["dy"]

	for i in range(len(x_values)):
		pyplot.errorbar(x_values[i], y_values[i], yerr = y_errors[i], xerr = x_errors[i], ecolor = "b", elinewidth = 1,
						barsabove = True)

# Save the graph as a SVG file.
def save_graph(name):
	pyplot.savefig(name + ".svg", format = "svg")


# This function receives data points and calculates the best linear fit for those data points.
def fit_linear(filename):
	y_title, x_title, table = filehandling.file_handling(filename)

	a, b, da, db, chi, chi_red = fitgui.fit_results(table)

	print(output_format.format(
		a_value = a,
		a_error = da,
		b_value = b,
		b_error = db,
		chi_squared = chi,
		chi_reduced = chi_red
	))

	# Create graph.
	pyplot.figure()
	pyplot.title("Generated linear fit")
	pyplot.ylabel(y_title)
	pyplot.xlabel(x_title)

	# Set data and graph.
	plot_fitted_graph(min(table["x"]), max(table["x"]), (a, b))
	plot_data_points(table)

	save_graph("linear_fit")
	pyplot.show()


# BONUS functions
def search_best_parameter(filename):
	a, b, y_title, x_title, table = filehandling.bonus_file_handling(filename)

	b_range = frange(b[0], b[1], b[2])
	a_range = frange(a[0], a[1], a[2])

	# Calculate chi for each pair of values.
	chi_values = []
	for b_value in b_range:
		for a_value in a_range:
			chi_values.append([b_value, a_value, fitgui.bonus_chi_squared(table, my_function, (0, a_value, b_value))])

	# Minimize chi
	best = chi_values[0]
	for b_value, a_value, chi in chi_values:
		if (chi < best[2]):
			best = (b_value, a_value, chi)

	print(output_format.format(
		a_value = best[1],
		a_error = a[2],
		b_value = best[0],
		b_error = b[2],
		chi_squared = best[2],
		chi_reduced = fitgui._chi_reduced(best[2], len(table["x"]))
	))

	# Create graph.
	pyplot.figure()
	pyplot.title("Generated custom fit")
	pyplot.ylabel("chi2(a,b = {best_b})".format(best_b=best[0]))
	pyplot.xlabel('a')

	# Set data and graph.
	plot_fitted_graph(min(table["x"]), max(table["x"]), (0, best[1], best[0]), my_function, c = "blue")
	plot_data_points(table)

	a_values   = [a for (b, a, chi) in chi_values if b == best[0]]
	chi_values = [chi for (b, a, chi) in chi_values if b == best[0]]
	slope      = (max(chi_values) - min(chi_values)) / (max(a_values) - min(a_values))
	intercept   = max(chi_values) + (slope * max(a_values))

	# save and show bonus function
	save_graph("numeric_sampling")
	pyplot.show()

if __name__ == "__main__":
	print(fit_linear())
	print(fit_linear())
	print(search_best_parameter(r""))