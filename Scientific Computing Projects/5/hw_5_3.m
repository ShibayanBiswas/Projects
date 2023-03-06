clc
clear all
format longG
a= 0;
b = pi/2;
del_x=zeros(199,1);
sum_le = zeros(199,1);
sum_re = zeros(199,1);
sum_me = zeros(199,1);
sum_tz = zeros(199,1);
err_1 = zeros(199,1);
err_2 = zeros(199,1);
err_3 = zeros(199,1);
err_4 = zeros(199,1);
for n = 1 : 199;
  dx=(b-a)/n;
  del_x(n)=dx;
  for i = 1 : n;
    sum_le(n)=sum_le(n) + (sin(a+(i-1)*dx)*dx);
    err_1(n)=abs(sum_le(n) - 1);
  end
  for i = 1 : n;
    sum_re(n)=sum_re(n) + (sin(a+i*dx)*dx);
    err_2(n)=abs(sum_re(n) - 1);
  end
  for i = 1 : n;
    sum_me(n)=sum_me(n) + (sin((2*a+(2*i-1)*dx)/2)*dx);
    err_3(n)=abs(sum_me(n) - 1);
  end
  for i = 1 : n;
    sum_tz(n)=sum_tz(n) + (((sin(a+(i-1)*dx)+sin(a+i*dx))/2)*dx);
    err_4(n)=abs(sum_tz(n) - 1);
  end
 end
 hf=figure()
best_fit_1=polyfit(del_x,err_1,1);
best_fit_2=polyfit(del_x,err_2,1);
best_fit_3=polyfit(del_x,err_3,1);
best_fit_4=polyfit(del_x,err_4,1);
hold
scatter(del_x,err_1,'.')
scatter(del_x,err_2,'.')
scatter(del_x,err_3,'.')
scatter(del_x,err_4,'.')
plot(del_x,((best_fit_1(1)*del_x)+best_fit_1(2)))
plot(del_x,((best_fit_2(1)*del_x)+best_fit_2(2)))
plot(del_x,((best_fit_3(1)*del_x)+best_fit_3(2)))
plot(del_x,((best_fit_4(1)*del_x)+best_fit_4(2)))
xlabel('Values of (\Deltax)')
ylabel('Values of error')
title('Plot of Values of error v/s Values of (\Deltax)')
legend('Left endpoint','Right endpoint','Mid point','Trapezoidal','Best Fit Line(Left endpoint)','Best Fit Line(Left endpoint)','Best Fit Line(Right endpoint)','Best Fit Line(Trapezoidal)')
grid()
print(hf,'Figure_3.png')
