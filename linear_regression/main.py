import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from tabulate import tabulate
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import mean_absolute_error

# Linear regression
lin_reg = LinearRegression()
stats = pd.read_csv('results_1.csv', sep=',')

# Sort by Time
stats = stats.sort_values(by='Time')

# Set values
x = np.array(pd.to_timedelta(stats['Time']).dt.total_seconds()).reshape(-1, 1)
y = np.array(stats['Score'])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.05, random_state=0, shuffle=True)

# Train
lin_reg.fit(x_train, y_train)

# Graphic
plt.scatter(x_train, y_train, color='wheat')
plt.plot(x_test, lin_reg.predict(x_test), color='red')
plt.scatter(x_test, y_test, color='blue')
plt.title("Linear regression")
plt.xlabel('Total seconds')
plt.ylabel('Score')
plt.show()

# Print results
for i in range(len(x_test)):
    print("Test score: " + str(y_test[i]) + ", Predicted score: " + str(lin_reg.predict(x_test)[i]))

a1 = lin_reg.coef_
print("Influence coefficient = " + str(a1))

y_train_pred = lin_reg.predict(x_train)
y_test_pred = lin_reg.predict(x_test)

print('MSE train: ' +
      str(mean_squared_error(y_train, y_train_pred)) + ', test: ' +
      str(mean_squared_error(y_test, y_test_pred)))
print('R^2 train: ' +
      str(r2_score(y_train, y_train_pred)) + ', test: ' +
      str(r2_score(y_test, y_test_pred)))