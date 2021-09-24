w   = 1;     // m
h   = 1;     // m

dx0 = 0.005;  // m
dx1 = 0.05;  // m

hs   = 0.05; // m

Point(1) = {0, 0, 0, dx1};
Point(2) = {w, 0, 0, dx1};
Point(3) = {w, h, 0, dx1};
Point(4) = {0, h, 0, dx1};


Point(5) = {w/2-hs,h/2-hs,0,dx0};
Point(6) = {w/2+hs,h/2-hs,0,dx0};
Point(7) = {w/2+hs,h/2+hs,0,dx0};
Point(8) = {w/2-hs,h/2+hs,0,dx0};
//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 1};
//+
Line(5) = {5, 6};
//+
Line(6) = {6, 7};
//+
Line(7) = {7, 8};
//+
Line(8) = {8, 5};
//+
Curve Loop(1) = {4, 1, 2, 3};
//+
Curve Loop(2) = {8, 5, 6, 7};
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
