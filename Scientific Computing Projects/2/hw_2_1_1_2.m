clc
clear all
format longG

n = input("Enter the order of the Matrix : ");  % A matrix has order >= 1

A = randi([-999, 999], n, n);
A

while det(A) == 0
   A = randi([-999, 999], n, n);
endwhile

b = randi([-999, 999], n, 1);
b

for j = 1 : (n - 1)
  for i = n : -1 : (j + 1)
    mul = A(i, j) / A(j, j);
    A(i, : ) = A(i, : ) - mul * A(j, : );
    b(i) = b(i) - mul * b(j);
  endfor
endfor

X = zeros(n, 1);

X(n) = b(n) / A(n, n);
for i = (n - 1) : -1 : 1
  sum = 0;
  for j = n : -1 : (i + 1)
    sum = sum + A(i, j) * X(j);
  endfor
  X(i) = (b(i) - sum) / A(i, i);
endfor

Y = inv(A) * b;

Z = A \ b;

X
Y
Z

