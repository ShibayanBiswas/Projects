import matplotlib.pyplot as plt
import datetime
import math
def func(x):
    y = (math.exp(x))*(x*x*x - 3*x*x - x + 9)
    return y
def derivFunc(x):
    y = (math.exp(x))*(3*x*x - 7*x + 8)
    return y
# Bisection Method
def bisection(a,b):
    x1 = list()
    y1 = list()
    t1 = list()
    i = 0
    if (func(a) * func(b) >= 0):
        print("You have not assumed right a and b\n")
        return
    c = a
    while ((b - a) >= 0.000001):
        dt_started = datetime.datetime.utcnow()
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
        dt_ended = datetime.datetime.utcnow()
        t1.append((dt_ended - dt_started).total_seconds())
    print("The value of root is : ","%.6f"%c)
    return x1, y1, t1
# Newton Raphson Method 
def newtonRaphson(x):
    x2 = list()
    y2 = list()
    t2 = list()
    i = 0
    h = func(x) / derivFunc(x)
    while abs(h) >= 0.000001:
        dt_started = datetime.datetime.utcnow()
        h = func(x)/derivFunc(x)
        x = x - h
        x2.append(x)
        y2.append(i)
        i = i + 1
        dt_ended = datetime.datetime.utcnow()
        t2.append((dt_ended - dt_started).total_seconds())
    print("The value of root is : ","%.6f"%x)
    return x2, y2, t2
# Secant Method
def secant(x1, x2, E):
    x3 = list()
    y3 = list()
    t3 = list()
    i = 0
    xm = 0
    x0 = 0
    c = 0
    if(func(x1) * func(x2) < 0):
        while True:
            dt_started = datetime.datetime.utcnow()
            x0 = ((x1 * func(x2) - x2 * func(x1)) / (func(x2) - func(x1)))
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
            x3.append(func(x0))
            dt_ended = datetime.datetime.utcnow()
            t3.append((dt_ended - dt_started).total_seconds())
        print("The value of root is : ","%.6f"%x0)
    else:
        print("You have not assumed correct interval")
    return x3, y3, t3
# Driver Function
a = float(input('Enter the value of a : ')) 
b = float(input('Enter the value of b : '))
a1,b1,t1=bisection(a, b)
x0 = float(input('Enter the value of x0 : ')) 
a2,b2,t2=newtonRaphson(x0)
x1 = float(input('Enter the value of x1 : '))
x2 = float(input('Enter the value of x2 : '))
E = 0.000001
a3,b3,t3=secant(x1, x2, E)
plt.scatter(t1,a1,label='Bisection Method')
plt.scatter(t2,a2,label='Newton-Raphson Method')
plt.scatter(t3,a3,label='Secant Method')
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('Plot of $f_1$(x) v/s Wall Clock time using all the methods')
plt.grid()
plt.legend()
plt.show()
