pkg load symbolic
data=load('data1.txt')
x=data(:,1)
y=data(:,2)
val=5;
imp=zeros(1,val+1);
for z = 1:val
	imp=zeros(z,z+1);
	imp=polyfit(x,y,z);
end
fig=figure();
x1=linspace(min(x),max(x));
y1=polyval(imp,x1);
plot(x,y,'+',x1,y1,'r-')
title('Best fit curve');
xlabel('x-axis')
ylabel('yaxis')
