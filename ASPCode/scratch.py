import subprocess
import json
import collections
import sys
import math
import random
import pdb

def solve(*args):
    # Run clingo with the provided argument list and return the parsed JSON result.
    
    CLINGO = './clingo-4.5.0-win64/clingo'
    
    clingo = subprocess.Popen(
        [CLINGO, '--outf=2'] + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    out, err = clingo.communicate()
    if err:
        print err
        
    return parse_result(out)
    
def parse_result(out):
    # Take in the JSON output from clingo and 
    # return a dictionary of all of the predicates
    # expressed at the end of scratch.lp
    
    result = json.loads(out)
    
    assert len(result['Call']) > 0
    assert len(result['Call'][0]['Witnesses']) > 0
    
    witness = result['Call'][0]['Witnesses'][0]['Value']
    
    class identitydefaultdict(collections.defaultdict):
        def __missing__(self, key):
            return key
    
    preds = collections.defaultdict(set)
    env = identitydefaultdict()
    
    for atom in witness:
        if '(' in atom:
            left = atom.index('(')
            functor = atom[:left]
            arg_string = atom[left:]
            try:
                preds[functor].add( eval(arg_string, env) )
            except TypeError:
                pass # at least we tried...
            
        else:
            preds[atom] = True
    
    return dict(preds)
    
def cleanup_walls(level):
    # Clean up Walls changes walls so they fit together
    
    # Level_walls holds every walls coordinates
    level_walls = {}
    
    # Lookup table for all of the wall sprites
    walls_lookup = ['100', '101', '105', '106', '107', '108', '110', '111', '112', '113', '120', '130', '131', '132', '133', '140']
    
    # Populate level_walls
    for h in range(0, len(level)):
        for w in range(0, len(level[h])):
            if level[h][w] in walls_lookup:
                level_walls[(w, h)] = level[h][w]
    
    # Checks each wall if it has and adjacent walls and changes it accordingly
    for coor in level_walls:
        # List of all directions from current coordinate
        #               Right                   Bottom                   Left                     Top
        dirs = [(1 + coor[0], coor[1]), (coor[0], 1 + coor[1]), (coor[0] - 1, coor[1]), (coor[0], coor[1] - 1)]
        
        # Changes walls based off of neighbouring walls
        # Check ./pacman-python-master/pacman/res/crossref.txt to find sprite values
        if (dirs[0] in level_walls) and (dirs[1] in level_walls) and (dirs[2] in level_walls) and (dirs[3] in level_walls):
            level[coor[1]][coor[0]] = '140'
            
        elif (dirs[0] in level_walls) and (dirs[1] not in level_walls) and (dirs[2] in level_walls) and (dirs[3] in level_walls):
            level[coor[1]][coor[0]] = '130'
        elif (dirs[0] in level_walls) and (dirs[1] in level_walls) and (dirs[2] not in level_walls) and (dirs[3] in level_walls):
            level[coor[1]][coor[0]] = '131'
        elif (dirs[0] not in level_walls) and (dirs[1] in level_walls) and (dirs[2] in level_walls) and (dirs[3] in level_walls):
            level[coor[1]][coor[0]] = '132'
        elif (dirs[0] in level_walls) and (dirs[1] in level_walls) and (dirs[2] in level_walls) and (dirs[3] not in level_walls):
            level[coor[1]][coor[0]] = '133'
            
        elif (dirs[0] in level_walls) and (dirs[1] not in level_walls) and (dirs[2] in level_walls) and (dirs[3] not in level_walls):
            level[coor[1]][coor[0]] = '100'
        elif (dirs[0] not in level_walls) and (dirs[1] in level_walls) and (dirs[2] not in level_walls) and (dirs[3] in level_walls):
            level[coor[1]][coor[0]] = '101'
            
        elif (dirs[0] in level_walls) and (dirs[1] not in level_walls) and (dirs[2] not in level_walls) and (dirs[3] in level_walls):
            level[coor[1]][coor[0]] = '105'
        elif (dirs[0] not in level_walls) and (dirs[1] not in level_walls) and (dirs[2] in level_walls) and (dirs[3] in level_walls):
            level[coor[1]][coor[0]] = '106'
        elif (dirs[0] in level_walls) and (dirs[1] in level_walls) and (dirs[2] not in level_walls) and (dirs[3] not in level_walls):
            level[coor[1]][coor[0]] = '107'
        elif (dirs[0] not in level_walls) and (dirs[1] in level_walls) and (dirs[2] in level_walls) and (dirs[3] not in level_walls):
            level[coor[1]][coor[0]] = '108'
            
        elif (dirs[0] not in level_walls) and (dirs[1] not in level_walls) and (dirs[2] not in level_walls) and (dirs[3] in level_walls):
            level[coor[1]][coor[0]] = '110'
        elif (dirs[0] in level_walls) and (dirs[1] not in level_walls) and (dirs[2] not in level_walls) and (dirs[3] not in level_walls):
            level[coor[1]][coor[0]] = '111'
        elif (dirs[0] not in level_walls) and (dirs[1] not in level_walls) and (dirs[2] in level_walls) and (dirs[3] not in level_walls):
            level[coor[1]][coor[0]] = '112'
        elif (dirs[0] not in level_walls) and (dirs[1] in level_walls) and (dirs[2] not in level_walls) and (dirs[3] not in level_walls):
            level[coor[1]][coor[0]] = '113'
            
        elif (dirs[0] not in level_walls) and (dirs[1] not in level_walls) and (dirs[2] not in level_walls) and (dirs[3] not in level_walls):
            level[coor[1]][coor[0]] = '120'
            
    return level

def render_level(design, width, height):
    # Create sprite dict holds every cell coordinate and its corresponding sprite
    sprite = {cell:sprite for (sprite, cell) in design['place'] }
    
    # Glyph dict maps each sprite's character code to its numerical code
    glyph = dict(blank='0', vp='21', hp='20', vw='101', hw='100', tlc='107', trc='108', brc='106', blc='105', te='113', be='110', re='112', le='111', isl='120', bt='130', tt='133', rt='132', lt='131', x='140', gd='1', pmsp='4', bsp='10', psp='11', isp='12', csp='13', f='2', sf='3')
    
    # Lists containing each quadrant's sprites
    level_block_0 = [] # Top left
    level_block_1 = [] # Top right
    level_block_2 = [] # Bottom left
    level_block_3 = [] # Bottom right
    
    # Decides where to put the vertical portals along the top wall of top left quadrant
    if(random.random() < .5):
        choices = [i for i in range(1, 11)]
        rand_cell = random.choice(choices)
        choices.remove(rand_cell)
        while(sprite[(rand_cell, 1)] != 'f' and len(choices)):
            rand_cell = random.choice(choices)
            choices.remove(rand_cell)
        sprite[(rand_cell, 0)] = 'vp'
        
    # Decides where to put the horizontal portals along the left wall of top left quadrant
    if(random.random() < .5):
        choices = [i for i in range(1, 11)]
        rand_cell = random.choice(choices)
        choices.remove(rand_cell)
        while(sprite[(1, rand_cell)] != 'f' and len(choices)):
            rand_cell = random.choice(choices)
            choices.remove(rand_cell)
        sprite[(0, rand_cell)] = 'hp'
    
    # Check if power pill is within the column or row that will get cut off
    # Replaces it randomly in the quadrant if it is
    for coor in sprite:
        if sprite[coor] == 'sf' and (coor[0] == width-1 or coor[1] == height-1):
            new_coor = coor
            while sprite[new_coor] != 'f':
                new_coor = (random.randint(1, width-2), random.randint(1, height-2))
            sprite[coor] = 'f'
            sprite[new_coor] = 'sf'
            break
    
    # Populate the top left quadrant with the sprites in normal order
    for h in range(0, height):
        level_block_0.append([])
        for w in range(0, width):
            if(w, h) in sprite:
                level_block_0[h].append((glyph[sprite[(w,h)]]))
    
    # Populate the top right quadrant with the sprites in reverse width order
    for h in range(0, height):
        level_block_1.append([])
        for w in range(width - 1, -1, -1):
            if (w, h) in sprite:
                level_block_1[h].append(glyph[sprite[(w, h)]])
    
    # Populate the bottom left quadrant with the sprites in reverse height order
    for h in range(height - 1, -1, -1):
        level_block_2.append([])
        for w in range(0, width):
            if(w, h) in sprite:
                level_block_2[height - h-1].append((glyph[sprite[(w,h)]]))
        
    # Populate the top right quadrant with the sprites in reverse width and height order
    for h in range(height - 1, -1, -1):
        level_block_3.append([])
        for w in range(width - 1, -1, -1):
            if(w, h) in sprite:
                level_block_3[height - h-1].append((glyph[sprite[(w,h)]]))
    
    # Combine top right quadrant to top left quadrant
    # Combine bottom right quadrant to bottom left quadrant
    for i in range(0,len(level_block_0)):
        for j in range(0,len(level_block_1)):
            level_block_0[i].append(level_block_1[i][j])
            level_block_2[i].append(level_block_3[i][j])
    
    # Combine bottom half to top half
    for i in range(0,len(level_block_0)):
        level_block_0.append(level_block_2[i])
    
    # Cut out the middle column
    for i in range(0, len(level_block_0)):
        level_block_0[i][width] = 666
        level_block_0[i].remove(level_block_0[i][width])

    # Cut out the middle row
    level_block_0[height] = []
    level_block_0.remove([])
    
    # Remove unique sprites for later replacement
    unique = ['1','4','10','11','12','13']
    for i in range(0, len(level_block_0)):
        for j in range(0, len(level_block_0[i])):
            if level_block_0[i][j] in unique:
                level_block_0[i][j] = '2'
    
    # Carve out center for ghost pen placement
    for i in range(height -3 , height +2):
        for j in range(width - 4, width+3):
            level_block_0[i][j] = '0'
    
    # Hardcode pacman, ghost, and ghost door location
    level_block_0[height-1][width-2] = '10'
    level_block_0[height-1][width-1] = '11'
    level_block_0[height-1][width] = '12'
    level_block_0[height-2][width-1] = '1'
    level_block_0[height-3][width-1] = '13'
    level_block_0[height+1][width-1] = '4'
    
    # Place walls around the unique sprites
    for i in range(height - 2, height + 1):
        for j in range(width - 3, width + 2):
            if level_block_0[i][j] not in unique:
                level_block_0[i][j] = '120'
    
    return level_block_0      

if __name__ == '__main__':
    # Width and Height of top left quadrant
    # Top right quadrant is width-1 x height
    # Bottom left quadrant is width x height-1
    # Bottom right quadrant is width-1 x height-1
    lvlWidth = 11
    lvlHeight = 11
    
    # Constants to be sent to clingo
    wall_amount = math.floor((lvlWidth * lvlHeight)*(0.43))
    blank_amount = math.floor((lvlWidth * lvlHeight)*(.1))
    
    # Get back design from clingo with our provided constants
    design = solve("./ASPCode/scratch.lp", "-c", "width=%d"%lvlWidth, "-c", "height=%d"%lvlHeight, "-c", "wall_amount=%d"%wall_amount, "-c", "blank_amount=%d"%blank_amount, '--sign-def=3','--seed='+str(random.randint(0,1<<30)))
    
    # Start creating text to be saved to 1.txt
    level = '# lvlwidth ' + str(lvlWidth*2-1) + '\n# lvlheight ' + str(lvlHeight*2-1) + '\n# bgcolor 0 0 0\n# edgecolor 0 0 255\n# fillcolor 0 0 0\n# pelletcolor 255 255 255\n# fruittype 1\n# startleveldata\n'
    
    # Convert clingo output to usable output
    x = render_level(design, lvlWidth, lvlHeight)
    
    # Fill wall orientation
    x = cleanup_walls(x)
    
    # Output the list as each individual sprite and add it to the current level text
    for i in range(0,len(x)):
        #level += str(x[i]).replace("]","").replace("[","").replace(",","").replace("'", "") + "\n"
        level += " ".join(x[i]) + '\n'
    
    # Add final text
    level += '# endleveldata\n\n# sprites'
    
    # Open 1.txt and save our generated level
    f = open("./pacman-python-master/pacman/res/levels/1.txt", 'w')
    f.write(level)
    f.close()
