# Function to compute the power of the number recursively
def power(x, n):
    if (n == 0):
        return 1
    if (x == 0):
        return 0
    return x * power(x, n - 1) 
# Driver Code
x = int(input("Enter the number : "))
n = int(input("Enter the power : "))
print("The result is : ", power(x, n))
