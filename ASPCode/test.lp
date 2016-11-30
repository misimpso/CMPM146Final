#const width=9.
#const height=11.

%param('width',width).

dimw(0..width-1).
dimh(0..height-1).

tile((X,Y)) :- dimw(X); dimh(Y).
    
adj((X1,Y1),(X2,Y2)) :- 
    tile((X1,Y1));
    tile((X2,Y2));
    |X1-X2| + |Y1-Y2| == 1.
    
<<<<<<< HEAD
pacman((10, 16)).
blinky((10, 10)).
pinky((9, 12)).
inky((10, 12)).
clyde((11, 12)).
=======
pacman((4, 8)).
blinky((4, 2)).
pinky((4, 4)).
inky((4, 5)).
clyde((4, 6)).
door((4, 3)).
>>>>>>> 32fb5169cf381851e77f2afd7c155a1ad3c1db0b

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
   
% there is exactly one pacman, one of each ghost, and one ghost door
:- not 1 { sprite(T,pmsp) } 1.
:- not 1 { sprite(T,bsp) } 1.
:- not 1 { sprite(T,psp) } 1.
:- not 1 { sprite(T,isp) } 1.
:- not 1 { sprite(T,csp) } 1.
:- not 1 { sprite(T,gd) } 1.
    
% there are between 2 and 5 traps in the level
:- not 2 { sprite(T,sf) } 5.
    
% the pacman and ghost locations are not taken by any other sprite
sprite(T, pmsp) :- pacman(T).
sprite(T, bsp) :- blinky(T).
sprite(T, psp) :- pinky(T).
sprite(T, isp) :- inky(T).
sprite(T, csp) :- clyde(T).


#show tile/1.
#show sprite/2.