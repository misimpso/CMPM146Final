% tile at most one named sprite
% vp, hp - veritcal portal, horizontal portal
% vw, hw - vertical wall, horizontal wall
% tlc, trc, brc, blc - top left corner, top right corner, bottom right corner, bottom left corner
% te, be, re, le - top end, bottom end, right end, left end
% isl - island
% bt, tt, rt, lt, x - bottom T, top T, right T, left T, four-way
% gd - ghost door
% pmsp, bsp, psp, isp, csp - pacman start pos, blinky start pos, pinky start pos, inky start pos, clyde start pos
% f, sf - food, super food

sprite(vw;hw).
sprite(tlc;trc;brc;blc).
sprite(te;be;re;le).
sprite(isl).
sprite(bt;tt;rt;lt;x).
sprite(gd).
sprite(pmsp;bsp;psp;isp;csp).
sprite(f;sf).
sprite(blank).

wall_sprite(vw;hw;tlc;trc;brc;blc;te;be;re;le;isl;bt;tt;rt;lt;x).
ghost_sprite(bsp;psp;isp;csp).

unique_sprite(pmsp).
unique_sprite(G) :- ghost_sprite(G).

#const width=5.
#const height=5.
cell((0..width-1, 0..height-1)).

1 { place(S, C):sprite(S) } 1 :- cell(C).


:- unique_sprite(S); not 1 { place(S, C):cell(C) } 1.

%:- not place(pmsp, (0,0)).
%:- not place(bsp, (0,1)).
%:- not place(isp, (0,2)).
%:- not place(csp, (1,0)).
%:- not place(psp, (1, 1)).
%:- not place(blank, (1, 2)).
%:- not place(blank, (2,0)).
%:- not place(blank, (2, 1)).
%:- not place(blank, (2, 2)).

border((0, Y)) :- cell((0, Y)).
border((width-1, Y)) :- cell((width-1, Y)).
border((X, 0)) :- cell((X, 0)).
border((X, height-1)) :- cell((X, height-1)).

:- border(C); place(S, C); not wall_sprite(S).

:- not 1 { place(f, C):cell(C) }.


#show place/2.
#show msg/1.