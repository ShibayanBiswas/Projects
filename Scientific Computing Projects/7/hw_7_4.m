clc
clear all
format longG

time_1 = zeros(1000,1);
time_2 = zeros(1000,1);
time_3 = zeros(1000,1);

for num = 1:1000
  s = cputime;
  A = randi([-1000,1000],num,num);
  b = randi([-1000,1000],num,1);

  while det(A) == 0
    A = randi([-1000,1000],num,num);
  endwhile

  s1 = cputime;
  Q = zeros(num,num);
  R = zeros(num,num);
  q = zeros(num,1);
  v = zeros(num,1);

  for j = 1:num
    v = A(:,j);
    for i = 1:j-1
      q = Q(:,i);
      R(i,j) = dot(q,v);
      v = v - R(i,j) * q;
    end
    no = norm(v);
    Q(:,j) = v/no;
    R(j,j) = no;
  end
  e1 = cputime;
  time_2(num) = e1-s1;

  s2 = cputime;
  y = Q'*b;
  x = zeros(num,1);

  for j = num:-1:1
      if (R(j,j) == 0)
        error('Matrix is singular!');
      end
      x(j) = y(j)/R(j,j);
      y(1:j-1) = y(1:j-1)-R(1:j-1,j)*x(j);
  end
  e2 = cputime;
  time_3(num) = e2-s2;
  e = cputime;
  time_1(num) = e-s;
endfor

x = [1:1000];
hold
plot(x, time_1)
plot(x, time_2)
plot(x, time_3)
xlabel('Matrix size n')
ylabel('Computational Cost')
title('Computational Cost v/s Matrix size n')
legend('Total computational time', 'Time for generating Q and R', 'Time for back-substitution and solving for x')
grid()
