
data_1 = dlmread('data1.txt');
x_1 = data_1(1 : 50, 1);
y_1 = data_1(1 : 50, 2);
p = polyfit(x_1, y_1, 1);

fig = figure();
hold
plot(x_1, (p(2) + x_1 * p(1)))
scatter(x_1, y_1, '.')
title('Best Fit Curve For Data-Set 1', "fontsize", 16)
xlabel('(X)-  Axis')
ylabel('(Y)-  Axis')
legend('Best Fit Curve', 'Scattered Data')
grid()


data_2 = dlmread('data2.txt');
x_2 = data_2(1 : 100, 1);
y_2 = data_2(1 : 100, 2);
p= polyfit(x_2, y_2, 1);

fig_1 = figure();
hold
plot(x_2, (p(2) + x_2 * p(1)))
scatter(x_2, y_2, '.')
title('Best Fit Curve For Data-Set 2', "fontsize", 16)
xlabel('(X)-  Axis')
ylabel('(Y)-  Axis')
legend('Best Fit Curve', 'Scattered Data')
grid()


data_3 = dlmread('data3.txt');
x_3 = data_3(1 : 200, 1);
y_3 = data_3(1 : 200, 2);
p = polyfit(x_3, y_3, 1);

fig_2 = figure();
hold
plot(x_3, (p(2) + x_3 * p(1)))
scatter(x_3, y_3, '.')
title('Best Fit Curve For Data-Set 3', "fontsize", 16)
xlabel('(X)-  Axis')
ylabel('(Y)-  Axis')
legend('Best Fit Curve', 'Scattered Data')
grid()
