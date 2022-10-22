clc
clear all
format longG

norm_inf = zeros(1000,1);

for num = 1:1000
  A = randi([-1000,1000],num,num);
  b = randi([-1000,1000],num,1);

  while det(A) == 0
    A = randi([-1000,1000],num,num);
  endwhile

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

  y = Q'*b;
  x = zeros(num,1);

  for j = num:-1:1
      if (R(j,j) == 0)
        error('Matrix is singular!');
      end
      x(j) = y(j)/R(j,j);
      y(1:j-1) = y(1:j-1)-R(1:j-1,j)*x(j);
  end

  Y = A\b;
  error = zeros(num,1);

  for k = 1:num
    error(k) = abs(x(k)-Y(k));
  endfor

  norm_inf(num) = norm(error,inf);
endfor

x = [1:1000];
hold
plot(x,norm_inf)
xlabel('Matrix size n')
ylabel('L_\infty error in x')
title('Plot of L∞ error in x v/s Matrix size n')
legend('L∞ error in x v/s Matrix size')
grid()
