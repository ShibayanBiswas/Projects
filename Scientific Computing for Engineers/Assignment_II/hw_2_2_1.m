clc
clear all
format longG

dataset = input('Dataset in (.txt) : ', 's');
data = dlmread(dataset);
x = data(:,1);
y = data(:,2);
regmat = regress(y, x)

