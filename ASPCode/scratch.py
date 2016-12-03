import subprocess
import json
import collections
import sys
import math
import random
import pdb

def solve(*args):
    '''Run clingo with the provided argument list and return the parsed JSON result.'''
    
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
    '''Parse the provided JSON text and extract a dict
    representing the predicates described in the first solver result.'''

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
    
def render_level(design, width, height):
    '''Given a dict of predicates, return an ASCII-art depiction of the a dungeon.'''
    sprite = {cell:sprite for (sprite, cell) in design['place'] }
    #print '{}\n'.format(design['left_adj'])
    #print '{}\n'.format(design['food'])
    #print design['place']
    #native width, height - 21, 25
    #native center - (11, 13)
    glyph = dict(blank='0', vp='21', hp='20', vw='101', hw='100', tlc='107', trc='108', brc='106', blc='105', te='113', be='110', re='112', le='111', isl='120', bt='130', tt='133', rt='132', lt='131', x='140', gd='1', pmsp='4', bsp='10', psp='11', isp='12', csp='13', f='2', sf='3')
    level_block_0 = [] #Top left
    level_block_1 = [] #Top right
    level_block_2 = [] #Bottom left
    level_block_3 = [] # Bottom right
    
    for h in range(0, height):
        level_block_0.append([])
        for w in range(0, width):
            if(w, h) in sprite:
                level_block_0[h].append((glyph[sprite[(w,h)]]))
        
                
    for h in range(0, height):
        level_block_1.append([])
        for w in range(width - 1, -1, -1):
            if (w, h) in sprite:
                level_block_1[h].append(glyph[sprite[(w, h)]])
        
    for h in range(height - 1, -1, -1):
        level_block_2.append([])
        for w in range(0, width):
            if(w, h) in sprite:
                level_block_2[height - h-1].append((glyph[sprite[(w,h)]]))
        
    for h in range(height - 1, -1, -1):
        level_block_3.append([])
        for w in range(width - 1, -1, -1):
            if(w, h) in sprite:
                level_block_3[height - h-1].append((glyph[sprite[(w,h)]]))
    
    for i in range(0,len(level_block_0)):
        for j in range(0,len(level_block_1)):
        
            level_block_0[i].append(level_block_1[i][j])
            level_block_2[i].append(level_block_3[i][j])
    
    for i in range(0,len(level_block_0)):
        level_block_0.append(level_block_2[i])
            
    
        
        
    for i in level_block_0:
        print i
    print "\n"
    
    return level_block_0      

if __name__ == '__main__':
    #print(sys.argv[1])
    lvlWidth = 11
    lvlHeight = 11
    wall_amount = math.floor((lvlWidth * lvlHeight)*(0.43))
    design = solve("./ASPCode/scratch.lp", "-c", "width=%d"%lvlWidth, "-c", "height=%d"%lvlHeight, "-c", "wall_amount=%d"%wall_amount, '--sign-def=3','--seed='+str(random.randint(0,1<<30)))
    #print design
    
    level = '# lvlwidth ' + str(lvlWidth*2) + '\n# lvlheight ' + str(lvlHeight*2) + '\n# bgcolor 0 0 0\n# edgecolor 0 0 255\n# fillcolor 0 0 0\n# pelletcolor 255 255 255\n# fruittype 1\n# startleveldata\n'
    
    x = render_level(design, lvlWidth, lvlHeight)
    for i in range(0,len(x)):
        level += str(x[i]).replace("]","").replace("[","").replace(",","").replace("'", "") + "\n"
    
    #level += render_level(design, lvlWidth, lvlHeight) + '# endleveldata\n\n# sprites'
    render_level(design, lvlWidth, lvlHeight)
    #print level
    
    f = open("./pacman-python-master/pacman/res/levels/1.txt", 'w')
    f.write(level)
    f.close()
