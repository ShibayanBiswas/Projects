%Taking dataset as input from user
dataset = input('input your dataset (.txt) : ',"s");
%Storing it in data
data = dlmread(dataset);
%column 1 of data
x = data(:,1);
%column 2 of data
y = data(:,2);
%regress of (y,x) would give the slope of the approximated linear curve y= m*x +c
regmat = regress(y,x)

