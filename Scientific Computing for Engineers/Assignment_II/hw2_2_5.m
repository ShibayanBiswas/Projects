data1=dlmread('data1.txt');
x1 = data1(1:50,1);
y1 = data1(1:50,2);
p1= polyfit(x1,y1,1);

x2 = data1(1:100,1);
y2 = data1(1:100,2);
p2= polyfit(x2,y2,1);

x3 = data1(1:200,1);
y3 = data1(1:200,2);
p3= polyfit(x3,y3,1);

data2=dlmread('data2.txt');
x4 = data2(1:50,1);
y4 = data2(1:50,2);
p4= polyfit(x4,y4,1);

x5 = data2(1:100,1);
y5 = data2(1:100,2);
p5= polyfit(x5,y5,1);

x6 = data2(1:200,1);
y6 = data2(1:200,2);
p6= polyfit(x6,y6,1);

data3=dlmread('data3.txt');
x7 = data3(1:50,1);
y7 = data3(1:50,2);
p7= polyfit(x7,y7,1);

x8 = data3(1:100,1);
y8 = data3(1:100,2);
p8= polyfit(x8,y8,1);

x9 = data3(1:200,1);
y9 = data3(1:200,2);
p9= polyfit(x9,y9,1);

m = zeros(9,1);
c = zeros(9,1);

m(1)= p1(1);
m(2)= p2(1);
m(3)= p3(1);
m(4)= p4(1);
m(5)= p5(1);
m(6)= p6(1);
m(7)= p7(1);
m(8)= p8(1);
m(9)= p9(1);

c(1)= p1(2);
c(2)= p2(2);
c(3)= p3(2);
c(4)= p4(2);
c(5)= p5(2);
c(6)= p6(2);
c(7)= p7(2);
c(8)= p8(2);
c(9)= p9(2);

z=[m c] ;


