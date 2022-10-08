%Here we define thr range for the norms
norm1 = zeros(100,1);
norm2 = zeros(100,1);

%Here we define the range for the order of the matrix as 'n'
for n=[2:100]
  %Here we define a random matrix of order n
  A = randi([-1111,1111],n,n);
  %Here we define a random vector of constants
  B = randi([-1111,1111],n,1);
%Method_1
  %This is the Augmented matrix of 'A' and 'B'
  C = [A B];
  %Here we find the pivot entries
  for j = 0:n-2
    k = j+1;
    for i = k:n-1
      mul = C(i+1,j+1)/C(j+1,j+1);  %Here we find the multipliers
      C(i+1,:) = (C(i+1,:) - mul*C(j+1,:));
    endfor
  endfor
  X = zeros(n,1);
  %Finding elements of the resultant matrix
  for a = n:-1:1
    X(a) = ((C(a,n+1) - C(a,a+1:n)*X(a+1:n))/C(a,a));
  endfor
%Method_2
  Y = inv(A)*B;
%Method_3
  Z = A\B ;

  e1 = zeros(n,1);
  e2 = zeros(n,1);

  for k = 1:n
    e1(k) = abs(X(k)-Y(k));
    e2(k) = abs(X(k)-Z(k));
  endfor
  %Here we find the L∞ norm of error
  norm1(n) = norm(e1,inf);
  norm2(n) = norm(e2,inf);
endfor

x=[1:100]';
f = figure()
hold on
plot(x,norm1);
plot(x,norm2);
title('Plot of Linf v/s n',"fontsize",16);
xlabel('n');
ylabel('Linf(n)')
legend('Linf of m1 and m2','Linf of m1 and m3');
print(f,'Linf.png')
hold off

