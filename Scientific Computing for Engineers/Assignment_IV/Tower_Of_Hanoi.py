import matplotlib.pyplot as plt
import math
def Tower_Of_Hanoi(N, from_rod, to_rod, aux_rod):
    if N == 0:
        return
    Tower_Of_Hanoi((N - 1), from_rod, aux_rod, to_rod)
    print("Move disk", N, "from rod", from_rod, "to rod", to_rod)
    Tower_Of_Hanoi((N - 1), aux_rod, to_rod, from_rod)
N = int(input("Enter the number of disks : "))
Tower_Of_Hanoi(N, 'A', 'C', 'B')
# Defining the lists
x = list()
y = list()
# Finding the list of Number of Initial Disks
for iterator in range(1, N + 1):
    x.append(iterator)
# Finding the list of Minimal Number of Moves
for iterator in x:
    y.append(math.pow(2, iterator) - 1)
# Plotting the curve
plt.plot(x, y,label='Normal Fit Curve')
plt.title('Plot of Minimum number of moves v/s Number of disks')
plt.xlabel('Number of disks')
plt.ylabel('Minimum number of moves')
plt.grid()
plt.legend()
plt.show()
