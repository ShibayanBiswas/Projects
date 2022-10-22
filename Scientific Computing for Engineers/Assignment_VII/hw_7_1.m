clc
clear all
format longG

A = input('Enter the Square Matrix : A = ')
b = input('Enter the Vector : b = ')

n = size(A,1);
Q = zeros(n,n);
R = zeros(n,n);
q = zeros(n,1);
v = zeros(n,1);

for j = 1:n
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

Q
R

b = b';
y = Q'*b;
x = zeros(n,1);

for j = n:-1:1
    if (R(j,j) == 0)
      error('Matrix is singular!');
    end
    x(j) = y(j)/R(j,j);
    y(1:j-1) = y(1:j-1)-R(1:j-1,j)*x(j);
end

x
