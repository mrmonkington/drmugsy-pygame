"""
* All pieces enter a DrMugs board as a left-right pair and are unbreakable
* If line of 4 is matched, and a pair loses its left or right pair, the remainder
* becomes an orphan which does not a attach to anything.  If a column has blank cells
* beneath it, and is contructed only of orphanes or vertically oriented pairs, it will
* fall to fill the space.
*
* Germs are fixed to board and cannot fall.
"""

import random

EMPTY = 0
RED = 1
BLUE = 2
YELLOW = 3

NONE = 0
SINGLE = 1
LEFT_PAIR = 2
RIGHT_PAIR = 3
TOP_PAIR = 4
BOTTOM_PAIR = 5
GERM = 6

class Piece:

    def __init__( self, t = EMPTY, u = NONE ):
        self.type = t
        self.unit = u

    def isVerticallyMobile( self ):
        return ( self.unit == SINGLE or self.unit == TOP_PAIR or self.unit == BOTTOM_PAIR )
    
    @staticmethod
    def getRandomColour():
        return random.choice(( BLUE, RED, YELLOW))

if __name__ == "__main__":
    p = Piece()
    print p.isVerticallyMobile()
    c = Piece.getRandomColour()
    print c
    p.type = c
    print p.isVerticallyMobile()

