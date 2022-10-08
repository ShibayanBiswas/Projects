%Define x and y
hf = figure();
x=y=linspace(-11,11,200);
[x,y]=meshgrid(x,y);
r = (x.^2 + y.^2).^0.5;
z = log(r);

mesh(x,y,z,"linewidth",1)

xlabel('X-axis');
ylabel('Y-axis');
zlabel('Z-axis');

xh = get(gca,'XLabel');
set(xh, 'Units', 'Normalized')
pos = get(xh, 'Position');
set(xh, 'Position',pos.*[1,1,1])

yh = get(gca,'YLabel');
set(yh, 'Units', 'Normalized')
pos = get(yh, 'Position');
set(yh, 'Position',pos.*[1,1,1])

zh = get(gca,'ZLabel');
set(zh, 'Units', 'Normalized')
pos = get(zh, 'Position');


