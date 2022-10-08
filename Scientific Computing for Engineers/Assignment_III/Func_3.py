import matplotlib.pyplot as plt
def func(x):
    y = x*x*x - 2*x + 2
    return y
def derivFunc(x):
    y = 3*x*x - 2
    return y
# Bisection Method
def bisection(a,b):
    if (func(a) * func(b) >= 0):
        print("You have not assumed right a and b\n")
        return
    c = a
    while ((b-a) >= 0.000001):
        c = (a+b)/2
        if (func(c) == 0):
            break
        if (func(c)*func(a) < 0):
            b = c
        else:
            a = c
    print("The value of root is : ","%.6f"%c)
# Newton Raphson Method 
def newtonRaphson( x ):
    h = func(x) / derivFunc(x)
    while abs(h) >= 0.000001:
        h = func(x)/derivFunc(x)
        x = x - h
    print("The value of root is : ","%.6f"%x)
# Secant Method
def secant(x1, x2, E):
    xm = 0
    x0 = 0
    c = 0
    if(func(x1) * func(x2) < 0):
        while True:
            x0 = ((x1 * func(x2) - x2 * func(x1)) / (func(x2) - func(x1)))
            c = func(x1) * func(x0)
            x1 = x2
            x2 = x0
            if (c == 0):
                break;
            xm = ((x1 * func(x2) - x2 * func(x1)) / (func(x2) - func(x1)))
            if(abs(xm - x0) < E):
                break;
        print("The value of root is : ","%.6f"%x0)
    else:
        print("You have not assumed correct interval")
# Driver Function
a =-200
b = 300
bisection(a, b)
x0 = -20 
newtonRaphson(x0)
x1 =-200
x2 = 300
E = 0.000001
secant(x1, x2, E)
a =-300
b = 400
bisection(a, b)
x0 = -30 
newtonRaphson(x0)
x1 =-300
x2 = 400
E = 0.000001
secant(x1, x2, E)
