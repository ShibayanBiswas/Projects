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
time_1 = zeros(199,1);
time_2 = zeros(199,1);
time_3 = zeros(199,1);
time_4 = zeros(199,1);
for n = 1 : 199;
  dx=(b-a)/n;
  del_x(n)=dx;
  s=cputime;
  for i = 1 : n;
    sum_le(n)=sum_le(n) + (sin(a+(i-1)*dx)*dx);
  end
  e=cputime;
  time_1(n)=e-s;
  s=cputime;
  for i = 1 : n;
    sum_re(n)=sum_re(n) + (sin(a+i*dx)*dx);
  end
  e=cputime;
  time_2(n)=e-s;
  s=cputime;
  for i = 1 : n;
    sum_me(n)=sum_me(n) + (sin((2*a+(2*i-1)*dx)/2)*dx);
  end
  e=cputime;
  time_3(n)=e-s;
  s=cputime;
  for i = 1 : n;
    sum_tz(n)=sum_tz(n) + (((sin(a+(i-1)*dx)+sin(a+i*dx))/2)*dx);
  end
  e=cputime;
  time_4(n)=e-s;
 end
 n=1:199
 hf = figure()
hold
plot(n,time_1)
plot(n,time_2)
plot(n,time_3)
plot(n,time_4)
xlabel('Number of Intervals')
ylabel('Values of Computational Cost')
title('Plot of Values of Computational Cost v/s Number of Intervals')
legend('Left endpoint','Right endpoint','Mid point','Trapezoidal')
grid()
print(hf,'Figure_5.png')
