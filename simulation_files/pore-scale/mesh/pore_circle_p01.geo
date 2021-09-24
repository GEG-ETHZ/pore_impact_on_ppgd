w   = 1;     // m
h   = 1;     // m



r   = 0.056; // m
dx0 = 0.007;  // m
dx1 = 0.05;   // m

Point(1) = {0, 0, 0, dx1};
Point(2) = {w, 0, 0, dx1};
Point(3) = {w, h, 0, dx1};
Point(4) = {0, h, 0, dx1};


Point(5) = {w/2,h/2,0,dx0};
Point(6) = {w/2,h/2-r,0,dx0};
Point(7) = {w/2,h/2+r,0,dx0};
//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 1};
//+
Circle(5) = {7, 5, 6};
//+
Circle(6) = {6, 5, 7};
//+
Curve Loop(1) = {4, 1, 2, 3};
//+
Curve Loop(2) = {5, 6};
//+
Plane Surface(1) = {1, 2};
//+
Plane Surface(2) = {2};
//+
Physical Curve("wall") = {3, 1};
//+
Physical Curve("HV") = {4};
//+
Physical Curve("GE") = {2};
//+
Physical Surface("rock") = {1};
//+
Physical Surface("pore") = {2};
