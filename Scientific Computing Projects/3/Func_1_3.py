import matplotlib.pyplot as plt
def func(x):
    y = x*x*x - 3*x*x - x + 9
    return y
def derivFunc(x):
    y = 3*x*x - 6*x  - 1
    return y
# Bisection Method
def bisection(a,b):
    x1 = list()
    y1 = list()
    i = 0
    if (func(a) * func(b) >= 0):
        print("You have not assumed right a and b\n")
        return
    c = a
    while ((b - a) >= 0.000001):
        c = (a + b)/2
        x1.append(c)
        y1.append(i)
        if (func(c) == 0):
            break
        if (func(c)*func(a) < 0):
            b = c
        else:
            a = c
        i = i + 1
    print("The value of root is : ","%.6f"%c)
    return x1, y1
# Newton Raphson Method 
def newtonRaphson(x):
    x2 = list()
    y2 = list()
    i = 0
    h = func(x) / derivFunc(x)
    while abs(h) >= 0.000001:
        h = func(x)/derivFunc(x)
        x = x - h
        x2.append(x)
        y2.append(i)
        i = i + 1
    print("The value of root is : ","%.6f"%x)
    return x2, y2
# Secant Method
def secant(x1, x2, E):
    x3 = list()
    y3 = list()
    i = 0
    xm = 0
    x0 = 0
    c = 0
    if(func(x1) * func(x2) < 0):
        while True:
            x0 = ((x1 * func(x2) - x2 * func(x1)) / (func(x2) - func(x1)))
            x3.append(func(x0))
            y3.append(i)
            c = func(x1) * func(x0)
            x1 = x2
            x2 = x0
            if (c == 0):
                break;
            xm = ((x1 * func(x2) - x2 * func(x1)) / (func(x2) - func(x1)))
            if(abs(xm - x0) < E):
                break;
            i = i + 1
        print("The value of root is : ","%.6f"%x0)
    else:
        print("You have not assumed correct interval")
    return x3, y3
# Driver Function
a = float(input('Enter the value of a : ')) 
b = float(input('Enter the value of b : '))
a1,b1=bisection(a, b)
x0 = float(input('Enter the value of x0 : ')) 
a2,b2=newtonRaphson(x0)
x1 = float(input('Enter the value of x1 : '))
x2 = float(input('Enter the value of x2 : '))
E = 0.000001
a3,b3=secant(x1, x2, E)
plt.plot(b3,a3,label='Secant Method')
plt.plot(b1,a1,label='Bisection Method')
plt.plot(b2,a2,label='Newton-Raphson Method')
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('Plot of $f_1$(x) v/s number of iterations using all the methods')
plt.grid()
plt.legend()
plt.show()
