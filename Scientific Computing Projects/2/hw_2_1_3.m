clc
clear all
format longG

norm_1 = zeros(100, 1);
norm_2 = zeros(100, 1);

for n = 2 : 100 % A matrix has order >= 1
  A = randi([-999, 999], n, n);

  while det(A) == 0
    A = randi([-999, 999], n, n);
  endwhile

  b = randi([-999, 999], n, 1);

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

  error_1 = zeros(n, 1);
  error_2 = zeros(n, 1);

  for i = 1 : n
    error_1(i) = abs(X(i) - Y(i));
    error_2(i) = abs(X(i) - Z(i));
  endfor

  norm_1(n) = norm(error_1, inf);
  norm_2(n) = norm(error_2, inf);

endfor

x = [1 : 100];
hold
plot(x, norm_1)
plot(x, norm_2)
xlabel('Matrix size (n)', 'fontsize', 10)
ylabel('L_\infty error in (X)', 'fontsize', 10)
title('Plot of L∞ error in (X) v/s Matrix size (n)', 'fontsize', 14)
legend('Method 1 v/s Method 2', 'Method 1 v/s Method 3')
grid()