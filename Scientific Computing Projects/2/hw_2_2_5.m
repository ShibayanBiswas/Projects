clc
clear all
format longG
pkg load symbolic

data = load('data1.txt');
x = data(:, 1);
y = data(:, 2);

n = 100;

for i = 1 : n
  y_1 = zeros(i, (i + 1));
  y_1 = polyfit(x, y, i);
endfor

fig = figure()
hold
x_1 = linspace(min(x), max(x));
y_1 = polyval(y_1, x_1);
plot(x_1, y_1)
scatter(x, y, '.')
title("Best Fit Curve For Data-Set 1")
xlabel('(X)-  Axis')
ylabel('(Y)-  Axis')
legend('Best Fit Curve', 'Scattered Data')
grid()
