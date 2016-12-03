%------------------- Ideas -------------------------
% Put power pills at each corner, make sure there are multiple paths to each from pacman start pos
% For larger maps (15x15 and up) generate a quadrant, or half than mirror
% Keep pacman, ghost pos, and door pos hardcoded, so we have a constant position and proximity from each other
% ---------------------------------------------------

% tile at most one named sprite

% sprite(vp;hp). % vp, hp - veritcal portal, horizontal portal
sprite(vw;hw). % vw, hw - vertical wall, horizontal wall
sprite(tlc;trc;brc;blc). % tlc, trc, brc, blc - top left corner, top right corner, bottom right corner, bottom left corner
sprite(te;be;re;le). % te, be, re, le - top end, bottom end, right end, left end
sprite(isl). % isl - island
sprite(bt;tt;rt;lt;x). % bt, tt, rt, lt, x - bottom T, top T, right T, left T, four-way
sprite(gd). % gd - ghost door
sprite(pmsp;bsp;psp;isp;csp). % pmsp, bsp, psp, isp, csp - pacman start pos, blinky start pos, pinky start pos, inky start pos, clyde start pos
sprite(f;sf). % f, sf - food, super food
sprite(blank). % blank - blank space

% Differentiate the wall sprites
wall_sprite(vw;hw;tlc;trc;brc;blc;te;be;re;le;isl;bt;tt;rt;lt;x).

% Differentiate the ghost sprites
ghost_sprite(bsp;psp;isp;csp).

% Make Pacman, the ghost door, all of the ghosts a unique sprite
unique_sprite(pmsp).
unique_sprite(gd).
unique_sprite(G) :- ghost_sprite(G).

% Dimensions of the level
#const width=5.
#const height=5.
#const wall_amount = 5.

% Coordinates between 0, width-1 and 0, height-1 are cells
cell((0..width-1, 0..height-1)).

1 { place(S, C):sprite(S) } 1 :- cell(C).

% Fail if a unique sprite is not in a cell
:- unique_sprite(S); not 1 { place(S, C):cell(C) } 1.

% Hardcode: Fail if specific sprite is not in its designated cell
%:- not place(pmsp, (0,0)).
%:- not place(bsp, (0,1)).
%:- not place(isp, (0,2)).
%:- not place(csp, (1,0)).
%:- not place(psp, (1, 1)).
%:- not place(blank, (1, 2)).
%:- not place(blank, (2,0)).
%:- not place(blank, (2, 1)).
%:- not place(blank, (2, 2)).

% Creating border cell set
border((X, 0)) :- cell((X, 0)). % Cells along the top wall
%border((X, height-1)) :- cell((X, height-1)). % Cells along the bottom wall
border((0, Y)) :- cell((0, Y)). % Cells along the left wall
%border((width-1, Y)) :- cell((width-1, Y)). % Cells along the right wall

% Fail if border cell doesnt contain a wall_sprite
:- border(C); place(S, C); not wall_sprite(S).

% Fail if less than 1 food in level
:- not 1 { place(f, C):cell(C) }.

% Fail if amount of wall sprites is less than the constant wall amount
%:- { place(S, C):wall_sprite(S) } wall_amount.

% Create adjacent set that is true for every cell that is one away from the current cell 
adj((X1,Y1),(X2,Y2)) :- cell((X1,Y1)); cell((X2,Y2)); |X1-X2| + |Y1-Y2| == 1.

% Create individual adjacent sets for each direction
left_adj((X1, Y1), (X2, Y2)) :- cell((X1, Y1)); cell((X2, Y2)); Y1 == Y2; X1 - X2 == 1.
right_adj((X1, Y1), (X2, Y2)) :- cell((X1, Y1)); cell((X2, Y2)); Y1 == Y2; X2 - X1 == 1.
top_adj((X1, Y1), (X2, Y2)) :- cell((X1, Y1)); cell((X2, Y2)); X1 == X2; Y1 - Y2 == 1.
bottom_adj((X1, Y1), (X2, Y2)) :- cell((X1, Y1)); cell((X2, Y2)); X1 == X2; Y2 - Y1 == 1.

% Create individual diagonal sets for each direction
tr_diag((X1, Y1), (X2, Y2)) :- cell((X1, Y1)); cell((X2, Y2)); X2 - X1 == 1; Y1 - Y2 == 1.
tl_diag((X1, Y1), (X2, Y2)) :- cell((X1, Y1)); cell((X2, Y2)); X1 - X2 == 1; Y1 - Y2 == 1.
br_diag((X1, Y1), (X2, Y2)) :- cell((X1, Y1)); cell((X2, Y2)); X2 - X1 == 1; Y2 - Y1 == 1.
bl_diag((X1, Y1), (X2, Y2)) :- cell((X1, Y1)); cell((X2, Y2)); X1 - X2 == 1; Y2 - Y1 == 1.

% Set of all wall locations
blocked(C) :- place(S, C); wall_sprite(S).

% Set of all food locations
food(C) :- place(f, C); cell(C).
food(C) :- place(sf, C); cell(C).

% Set of all blank space locations
blank(C) :- place(blank, C); cell(C).

% Set of all reachable cells by pacman
reach(C) :- place(pmsp, C); cell(C).
reach(C2) :- reach(C1); adj(C1,C2); not blocked(C2).

% Fail if a food cell isn't reachable
:- cell(C); not reach(C); food(C).

% Fail if ghost position isn't reachable by pacman
:- unique_sprite(G); place(G, C); not reach(C).

% Fail if a blank cell is reachable
:- blank(C); reach(C).

% Fail if: (B = wall, C1, C2 = food)
% B C2
% C1 B 
:- food(C1); food(C2); C1 != C2; blocked(B); tr_diag(C1, C2); top_adj(C1, B); right_adj(C1, B).

% Fail if:
% C2 B
% B C1
:- food(C1); food(C2); C1 != C2; blocked(B); tl_diag(C1, C2); top_adj(C1, B); left_adj(C1, B).

% Fail if:
% C1 B
% B C2
:- food(C1); food(C2); C1 != C2; blocked(B); br_diag(C1, C2); bottom_adj(C1, B); right_adj(C1, B).

% Fail if:
% B C1
% C2 B
:- food(C1); food(C2); C1 != C2; blocked(B); bl_diag(C1, C2); bottom_adj(C1, B); left_adj(C1, B).

tube(C1) :- food(C1); 2 { blocked(C2); adj(C1,C2)} 3.
:- 10 { tube(C1) }.

#show place/2.
#show reach/1.
%#show food/1.
%#show blank/1.
%#show left_adj/2.