import seaborn as sns
iris = sns.load_dataset('iris')
iris.head()

import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
sns.pairplot(iris, hue='species', size=1.5)


X_iris = iris.drop('species', axis=1)
X_iris.shape

y_iris = iris['species']
y_iris.shape

import numpy as np
rng = np.random.RandomState(42)
x = 10 * rng.rand(50)
y = 2 * x - 1 + rng.randn(50)
plt.scatter(x, y);


from sklearn.linear_model import LinearRegression
model = LinearRegression(fit_intercept=True)
model

X = x[:, np.newaxis]
X.shape
model.fit(X, y)
model.coef_
model.intercept_

xfit = np.linspace(-1, 11)
Xfit = xfit[:, np.newaxis]
yfit = model.predict(Xfit)
plt.plot(xfit, yfit);

plt.show()
