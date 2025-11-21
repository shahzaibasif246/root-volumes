import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np

df = pd.read_excel('final_volumes.xlsx')

#print(df)

x = np.array(df['total_volume_light_microscopy'].tolist())
y = np.array(df['dinoline_volumes'].tolist())

x = x.reshape(-1, 1)

model = LinearRegression()
model.fit(x, y)

# Predicted values
y_pred = model.predict(x)

r2 = r2_score(y, y_pred)
print("R² value:", r2)

plt.scatter(x, y, color='blue', label='Data')
plt.plot(x, y_pred, color='red', label='Fit')
plt.text(max(x), max(y), f'R² = {r2:.2f}', fontsize=12)  # Display R² on the plot
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Linear Regression with R²')
plt.legend()
plt.show()
