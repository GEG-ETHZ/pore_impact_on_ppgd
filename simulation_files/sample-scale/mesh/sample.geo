w   = 1;     // m
h   = 1;     // m

dx0 = 0.05;  // m
dx1 = 0.05;  // m

r   = 0.05784; // m

Point(1) = {0, 0, 0, dx1};
Point(2) = {w, 0, 0, dx1};
Point(3) = {w, h, 0, dx1};
Point(4) = {0.8*w, h, 0, dx1};
Point(5) = {0.7*w, h, 0, dx1};
Point(6) = {0.3*w, h, 0, dx1};
Point(7) = {0.2*w, h, 0, dx1};
Point(8) = {0, h, 0, dx1};
//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 5};
//+
Line(5) = {5, 6};
//+
Line(6) = {6, 7};
//+
Line(7) = {7, 8};
//+
Line(8) = {8, 1};
//+
Point(9)  = {w/2,h/2,0,dx0};
Point(10) = {w/2,h/2-r,0,dx0};
Point(11) = {w/2,h/2+r,0,dx0};
//+
Circle(9) = {11, 9, 10};
//+
Circle(10) = {10, 9, 11};
//+
Curve Loop(1) = {8, 1, 2, 3, 4, 5, 6, 7};
//+
Curve Loop(2) = {9, 10};
//+
Plane Surface(1) = {1, 2};
//+
Plane Surface(2) = {2};
//+
Physical Curve("wall") = {8, 1, 2, 3, 5, 7};
//+
Physical Curve("HV") = {6};
//+
Physical Curve("GE") = {4};
//+
Physical Surface("rock") = {1};
//+
Physical Surface("pore") = {2};
