t1 = zeros(100,1);
t2 = zeros(100,1);
t3 = zeros(100,1);

for n=[2:100]
  tic()
  A = randi([-1111,1111],n,n);
  B = randi([-1111,1111],n,1);
  C = [A B];
  for j=0:n-2
    k=j+1;
    for i=k:n-1
      mul= C(i+1,j+1)/C(j+1,j+1);
      C(i+1,:) = (C(i+1,:) - mul*C(j+1,:));
    endfor
  endfor

  X = zeros(n,1);
  for a=n:-1:1
    X(a) = ((C(a,n+1) - C(a,a+1:n)*X(a+1:n))/C(a,a));
  endfor
  t1(n) = toc();  %Time taken for method_1

  tic()
  Y= inv(A)*B;
  t2(n)= toc();  %Time taken for method_2

  tic()
  Z= A \ B ;
  t3(n)= toc();  %Time taken for method_3
endfor
x=[1:100]';
f = figure();
hold on
plot(x,t1);
plot(x,t2);
plot(x,t3);
title('Plot of Wall Clock Time',"fontsize",14);
xlabel('n');
ylabel('WallClockTime(n)');
legend('Method1','Method2','Method3');
hold off
print(f,'WLC.png')