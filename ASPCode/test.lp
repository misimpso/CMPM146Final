#const width=21.
#const height=25.

%param('width',width).

dimw(0..width-1).
dimh(0..height-1).

tile((X,Y)) :- dimw(X); dimh(Y).
    
adj((X1,Y1),(X2,Y2)) :- 
    tile((X1,Y1));
    tile((X2,Y2));
    |X1-X2| + |Y1-Y2| == 1.
    
pacman((10, 16)).
blinky((10, 10)).
pinky((9, 12)).
inky((9, 13)).
clyde((9, 14)).

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

0 { sprite(T,(vp;hp;vw;hw;tlc;trc;brc;blc;te;be;re;le;isl;bt;tt;rt;lt;x;gd;pmsp;bsp;psp;isp;csp;f;sf)) } 1 :- tile(T).
   
% there is exactly one gem and one altar in the whole level
:- not 1 { sprite(T,pmsp) } 1.
:- not 1 { sprite(T,bsp) } 1.
:- not 1 { sprite(T,psp) } 1.
:- not 1 { sprite(T,isp) } 1.
:- not 1 { sprite(T,csp) } 1.
:- not 1 { sprite(T,gd) } 1.
    
% there are between 2 and 5 traps in the level
%:- not 2 { sprite(T,trap) } 5.
    
% the start and finish are clear
sprite(T, pmsp) :- pacman(T).
sprite(T, bsp) :- blinky(T).
sprite(T, psp) :- pinky(T).
sprite(T, isp) :- inky(T).
sprite(T, csp) :- clyde(T).

#show tile/1.
#show sprite/2.