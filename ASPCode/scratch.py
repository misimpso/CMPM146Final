import subprocess
import json
import collections
import random
import sys
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
    print "Sprites: {}".format(sprite)
    #param = dict(design['param'])
    #native width, height - 21, 25
    #native center - (11, 13)
    glyph = dict(blank='0', vp='21', hp='20', vw='101', hw='100', tlc='107', trc='108', brc='106', blc='105', te='113', be='110', re='112', le='111', isl='120', bt='130', tt='133', rt='132', lt='131', x='140', gd='1', pmsp='4', bsp='10', psp='11', isp='12', csp='13', f='2', sf='3')
    level_block = ''
    
    for h in range(0, height):
        for w in range(0, width):
            if((w, h) in sprite):
                if w == width - 1:
                    level_block += glyph[sprite[(w,h)]] + '\n'
                else:
                    level_block += glyph[sprite[(w,h)]] + ' '
            else:
                if w == width - 1:
                    level_block += ' 0\n'
                else:
                    level_block += '0 '
    return level_block       

if __name__ == '__main__':
    lvlWidth = 11
    lvlHeight = 11
    design = solve("./ASPCode/scratch.lp", "-c", "width=%d"%lvlWidth, "-c", "height=%d"%lvlHeight)
    print design
    params = '# lvlwidth ' + str(lvlWidth) + '\n# lvlheight ' + str(lvlHeight) + '\n# bgcolor 0 0 0\n# edgecolor 0 0 255\n# fillcolor 0 0 0\n# pelletcolor 255 255 255\n# fruittype 1\n# startleveldata\n'
    params += render_level(design, lvlWidth, lvlHeight) + '# endleveldata\n\n# sprites'
    print params
    
    f = open("./pacman-python-master/pacman/res/levels/1.txt", 'w')
    f.write(params)
    f.close()

    