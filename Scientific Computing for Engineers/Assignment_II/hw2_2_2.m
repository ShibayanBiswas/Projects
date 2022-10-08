%Performing Linear regression on dataset1
data1=dlmread('data1.txt');
x1 = data1(1:50,1);
y1 = data1(1:50,2);
p= polyfit(x1,y1,1);
 %Plotting graph for dataset1
hf = figure();
hold
plot(x1,(p(2) + x1*p(1)),'r')
scatter(x1,y1,'b')
title('Best Fit Line For Dataset-1',"fontsize",16);
xlabel('X-Axis');
ylabel('Y-Axis');
legend('LR-Line','Scattered data');
print(hf,'lrd1.png');
%Performing Linear regression on dataset2
data2=dlmread('data2.txt');
x2 = data2(1:100,1);
y2 = data2(1:100,2);
p= polyfit(x2,y2,1);
 %Plotting graph for dataset2
hf1 = figure();
hold
plot(x2,(p(2) + x2*p(1)),'r')
title('Best Fit Line For Dataset-2',"fontsize",16);
xlabel('X-Axis');
ylabel('Y-Axis');
scatter (x2,y2,'b');
legend('LR-Line','Scattered data');
print(hf1,'lrd2.png')
%Performing Linear regression on dataset3
data3=dlmread('data3.txt');
x3 = data3(1:200,1);
y3 = data3(1:200,2);
p= polyfit(x3,y3,1);
 %Plotting graph for dataset3
hf2 = figure();
hold
plot(x3,(p(2) + x3*p(1)),'r')
scatter(x3,y3,'b')
title('Best Fit Line For Dataset-3');
xlabel('X-Axis');
ylabel('Y-Axis');
legend('LR-Line','Scattered data');
print(hf2,'lrd3.png');

