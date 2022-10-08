import matplotlib.pyplot as plt
def func(x):
    y = x*x*x - 2*x + 2
    return y
def derivFunc(x):
    y = 3*x*x - 2
    return y
# Newton Raphson Method 
def newtonRaphson( x ):
    h = func(x) / derivFunc(x)
    while abs(h) >= 0.000001:
        h = func(x)/derivFunc(x)
        x = x - h
    print("The value of root is : ","%.6f"%x)
# Driver Function
x0 = 0 
newtonRaphson(x0)
