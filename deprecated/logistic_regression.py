import numpy as np

def linear_function(x, w, b):
    return (np.dot(w, x) + b)

def cost_function(predictive_function ,w, b, y, X):
    m = X.shape[0]
    total_cost = 0
    for i in range(m):
        predicted_value = predictive_function(X[i], w, b)
        total_cost += (predicted_value - y[i]) ** 2
    return total_cost/(2*m)



def computeGradient(predictive_function, w, b, y, X):
    m = X.shape[0]
    n = w.shape[0]

    dj_dw = np.zeros(n)
    dj_db = 0

    for i in range(m):
        f_wb = predictive_function(X[i], w, b)
        dj_db += f_wb - y[i]
        for j in range(n):
            if n == 1:
                dj_dw[j] += X[i] * (f_wb - y[i])    
            else:
                dj_dw[j] += X[i][j] * (f_wb - y[i])
    
    dj_dw = dj_dw/m
    dj_db = dj_db/m

    return dj_dw, dj_db

def gradientDescent(X, y, alpha, iter = 10000):
    Xshape = X.shape
    if len(Xshape) == 1:
        n = 1
    else:
        n = X.shape[1]
    b = 0
    w = np.zeros(n)

    for i in range(iter):
        b_prev = b
        w_prev = w

        gradient_w, gradient_b = computeGradient(linear_function, w_prev, b_prev, y, X)

        w = w - alpha*gradient_w
        b = b - alpha*gradient_b

        if i % 100 == 0:
            print(f"Iteration: {i}, Cost: {cost_function(linear_function, w, b, y, X)}, Gradient_w: {gradient_w}, Gradient_b: {gradient_b}")
    
    print(w, b)
    return w, b

def predict(X, w, b):
    m = X.shape[0]
    y = []
    for i in range(m):
        y.append(linear_function(X[i], w, b))
    
    return y

