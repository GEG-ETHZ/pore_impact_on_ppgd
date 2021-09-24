w   = 0.13;      // m
h   = 0.03;      // m

dx0 = 0.001;     // m
dx1 = 0.0001;    // m

Point(1) = {0, 0, 0, dx0};
Point(2) = {w, 0, 0, dx0};
Point(3) = {w, h, 0, dx0};
Point(4) = {0.5*w+0.026, h, 0, dx1};
Point(5) = {0.5*w+0.024, h, 0, dx1};
Point(6) = {0.5*w-0.024, h, 0, dx1};
Point(7) = {0.5*w-0.026, h, 0, dx1};
Point(8) = {0, h, 0, dx0};
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
Curve Loop(1) = {8, 1, 2, 3, 4, 5, 6, 7};
//+
Plane Surface(1) = {1};
//+
Physical Curve("wall") = {8, 1, 2, 3, 5, 7};
//+
Physical Curve("HV") = {6};
//+
Physical Curve("GE") = {4};
//+
Physical Surface("rock") = {1};
