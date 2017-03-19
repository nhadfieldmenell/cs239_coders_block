# Calculates the linear regression model and plots the data
# Limitations: only returns the most basic regression outputs

from scipy import stats
import numpy as np
import pylab

# Fit the model
x = np.array([1, 2, 5, 7, 10, 15])
y = np.array([2, 6, 7, 9, 14, 19])
slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x, y)

# Calculate some additional outputs
predict_y = intercept + slope * x
pred_error = y - predict_y