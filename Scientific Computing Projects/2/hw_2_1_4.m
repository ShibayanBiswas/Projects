clc
clear all
format longG

time_1 = zeros(100, 1);
time_2 = zeros(100, 1);
time_3 = zeros(100, 1);

for n = 2 : 100 % A matrix has order >= 1

  tic();
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
  time_1(n) = toc();

  tic();
  Y = inv(A) * b;
  time_2(n) = toc();

  tic();
  Z = A \ b;
  time_3(n) = toc();

endfor

x = [1 : 100];
hold
plot(x, time_1)
plot(x, time_2)
plot(x, time_3)
xlabel('Matrix size (n)', 'fontsize', 10)
ylabel('Wall Clock Time (t)', 'fontsize', 10)
title('Plot of Wall Clock Time (t) v/s Matrix size (n)', 'fontsize', 14)
legend('Method 1', 'Method 2', 'Method 3')
grid()
