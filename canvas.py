import time
import random
import sys
import pygame
from piece import *
from pygame.locals import *
import logging

class Canvas:
    def __init__(self, screen):
        # load BG image
        self.g = screen
        self.bg = pygame.image.load('resources/gfx/background.png').convert();
        self.logo = pygame.image.load('resources/gfx/dr_mugsy_logo.png').convert()

        # init fonts
        # todo either patch for OTF or use a TTF
        self.main_font = {
            15: pygame.font.SysFont("DejaVu Sans", 15),
            19: pygame.font.SysFont("DejaVu Sans", 19),
        }
        self.bold_font = {
            15: pygame.font.SysFont("DejaVu Sans", 15, bold=True),
            19: pygame.font.SysFont("DejaVu Sans", 19, bold=True),
        }

    def drawText(self, font, text, color, position):
        surf = font.render(text, True, color)
        self.g.blit(surf, position)

    def background(self):
        # we just blit the whole BG because that's fine these days :)
        #background = pygame.Surface(self.g.get_size())
        #background = background.convert()
        #background.fill((0, 0, 0))
        logging.debug("hi")
        self.g.blit(self.bg, (0, 0))

class MenuCanvas(Canvas):
    def __init__(self, screen):
        super(Canvas, self).__init__(self, screen)
    
    def drawInstructions():
        """
            :param g: `pygame.Screen`
            TODO
        """
        self.background()
        self.g.setColor(0x00000000)
        self.g.fillRect( 0, 0, self.getWidth(), self.getHeight() )
        tw.writeTextBox(
            Font.getFont( Font.FACE_PROPORTIONAL, Font.STYLE_PLAIN, Font.SIZE_SMALL ),
            10,
            20, 
            self.getWidth() - 20, self.getHeight() - 30,
            "Get rid of all the germs by making a line of 4 or more of the same colour.  If the germ is part of the line, it will vanish!" 
        )
        self.g.setFont( Font.getFont( Font.FACE_PROPORTIONAL, Font.STYLE_BOLD, Font.SIZE_SMALL ) )
        self.g.drawString( "Instructions", getWidth() / 2, 10, Graphics.TOP | Graphics.HCENTER )
              
    
    def drawTitleScreen():
        """
            :param g: `pygame.Screen`
            TODO
        """
        self.background()

        self.g.setColor( 0x00000000 )
        self.g.fillRect( 0, 0, self.getWidth(), self.getHeight() )
        logo_gfx = Image.createImage( "/drmugs/gfx/dr_mugsy_logo.png" )
        self.g.drawImage( logo_gfx, ( getWidth() - logo_gfx.getWidth() ) / 2, 20, 0 )
        self.g.setFont( Font.getFont( Font.FACE_PROPORTIONAL, Font.STYLE_PLAIN, Font.SIZE_SMALL ) )
        if menu_option_selected == MENU_START:
            self.g.setColor( 0x00ffffff )
        else:
            self.g.setColor( 0x00ff6000 )
        
        self.g.drawString( "Start", getWidth() / 2, 80, Graphics.HCENTER | Graphics.TOP )
        if menu_option_selected == MENU_CONTINUE:
            self.g.setColor( 0x00ffffff )
        else:
            self.g.setColor( 0x00ff6000 )
        
        self.g.drawString( "Continue", getWidth() / 2, 90, Graphics.HCENTER | Graphics.TOP )
        if menu_option_selected == MENU_INSTRUCTIONS:
            self.g.setColor( 0x00ffffff )
        else:
            self.g.setColor( 0x00ff6000 )
        
        self.g.drawString( "Instructions", getWidth() / 2, 100, Graphics.HCENTER | Graphics.TOP )
        
    

class PlayCanvas(Canvas):

    def __init__(self, screen):
        super(Canvas, self).__init__(self, screen)
        self.g = screen;

        self.view_width = screen.get_width()
        self.view_height = screen.get_height()

        # probably pointless
        random.seed()

    def paint():
        self.background()
        if game_state == GAME_PLAYING:
            self.drawPlaying()
        if game_state == GAME_OVER:
            self.g.setColor( 0x00ffffff )
            self.g.setFont( Font.getFont( Font.FACE_PROPORTIONAL, Font.STYLE_BOLD, Font.SIZE_MEDIUM ) )
            self.g.drawString( "GAME OVER", getWidth() / 2, 10, Graphics.TOP | Graphics.HCENTER )
        if game_state == GAME_NEXT_LEVEL:
            self.g.setColor( 0x00ffffff )
            self.g.setFont( Font.getFont( Font.FACE_PROPORTIONAL, Font.STYLE_BOLD, Font.SIZE_MEDIUM ) )
            self.g.drawString( "LEVEL UP!", getWidth() / 2, 10, Graphics.HCENTER | Graphics.TOP )
    
    def drawBoard(offset_left, unit ):
        self.g.setColor( 0x00000000 )
        self.g.fillRoundRect(
            offset_left, self.getHeight() - unit * board.getHeight() - 2,
            unit * board.getWidth(), unit * board.getHeight(),
            unit, unit
        )
    
    def updateScore():
        self.g.setColor( 0x00606060 )
        self.g.fillRect( 0, 0, self.getWidth(), self.getHeight() )
        self.g.setColor( 0x00ffffff )
        #self.g.drawString( "xs: " + board.test, 0, 0, Graphics.TOP | Graphics.LEFT )
        #self.g.drawString( "s: " + score, 0, 20, Graphics.TOP | Graphics.LEFT )
        #self.g.drawString( "ys: " + board.test2, 0, 40, Graphics.TOP | Graphics.LEFT ); 
        #self.g.drawString( "g_c: " + test, 0, 60, Graphics.TOP | Graphics.LEFT )
        self.g.setFont( Font.getFont( Font.FACE_PROPORTIONAL, Font.STYLE_PLAIN, Font.SIZE_SMALL ) )
        self.g.drawString( "" + level, 2, 20, Graphics.TOP | Graphics.LEFT )
        self.g.drawString( "" + score, 2, 45, Graphics.TOP | Graphics.LEFT )
        self.g.drawString( "" + germs_on_board, 2, 70, Graphics.TOP | Graphics.LEFT )
        self.g.setFont( Font.getFont( Font.FACE_PROPORTIONAL, Font.STYLE_BOLD, Font.SIZE_SMALL ) )
        self.g.drawString( "LV", 2, 12, Graphics.TOP | Graphics.LEFT )
        self.g.drawString( "SC", 2, 35, Graphics.TOP | Graphics.LEFT )
        self.g.drawString( "G", 2, 60, Graphics.TOP | Graphics.LEFT )
    
    def drawPlaying():
        flasher = 1 - flasher
        # give us a few pixels to play with
        unit = ( self.getHeight() - 5 ) / board.getHeight()
        if unit * board.getWidth() > self.getWidth():
            unit = self.getWidth() / board.getWidth()
        
        offset_left = ( self.getWidth() - board.getWidth() * unit ) / 2
        if update_score:
            self.updateScore()
               
        self.drawBoard(offset_left, unit)

        for y in range(board.getHeight() - 1, -1, -1):
            for x in range(board.getWidth() - 1, -1, -1):
                p = board.getPiece( x, y )
                if( p.getType() == Piece.EMPTY ):
                    # just leave blank
                    """if( p.getUnit() == Piece.NONE ):
                        self.g.setColor( 0x00303030 )
                        #self.g.drawString( "x", offset_left + x * unit, ( board.getHeight() - ( y ) ) * unit, Graphics.TOP | Graphics.LEFT )
                        self.g.drawLine(
                            offset_left + x * unit, ( board.getHeight() - ( y ) ) * unit,
                            offset_left + ( x + 1 ) * unit - 1, ( board.getHeight() - ( y ) ) * unit
                        )
                        self.g.drawLine(
                            offset_left + x * unit, ( board.getHeight() - ( y ) ) * unit,
                        offset_left + x * unit, ( board.getHeight() - ( y - 1 ) ) * unit - 1
                        )
                    """
                    continue
                
                if p.getUnit() == Piece.GERM:
                    # draw germ
                    self.drawGerm(p, x, y, unit, offset_left )
                else:
                    self.drawPill(p, x, y, unit, offset_left )
                
            
        

    
    
    def drawGerm(p, x, y, unit, offset_left ):
        """
            :param g: `pygame.Screen`
            :param p: `Piece`
        """
        if p.getType() == Piece.BLUE:
            self.g.setColor( 0x003060ff )
        if p.getType() == Piece.RED:
            self.g.setColor( 0x00ff6033 )
        if p.getType() == Piece.YELLOW:
            self.g.setColor( 0x00f0f000 )
        
        self.g.fillRoundRect(
            offset_left + unit * x,
            self.getHeight() - unit * ( y + 1 ) - 2,
            unit,
            unit,
            unit / 4,
            unit / 4
        )
        self.g.setColor( 0x00005000 * ( flasher + 1 ) )
        self.g.fillRoundRect(
            offset_left + unit * x + unit / 4,
            self.getHeight() - unit * ( y + 1 ) + unit / 4 - 2,
            unit / 2,
            unit / 2,
            unit / 4,
            unit / 4
        )
    
    def drawPill(p, x, y, unit, offset_left ):
        """
            :param g: :class:`pygame.Surface`
            :param p: `Piece`
            :param unit: type of piece to draw, taken from `Piece`
        """
        if p.getType() == Piece.BLUE:
            self.g.setColor( 0x003060ff )
        if p.getType() == Piece.RED:
            self.g.setColor( 0x00ff6033 )
        if p.getType() == Piece.YELLOW:
            self.g.setColor( 0x00f0f000 )
        
        self.g.fillRoundRect(
            offset_left + unit * x,
            self.getHeight() - unit * ( y + 1 ) - 2,
            unit,
            unit,
            unit,
            unit
        );  
        if p.getUnit() == Piece.TOP_PAIR:
            self.g.fillRect(
                offset_left + unit * x,
                self.getHeight() - unit * ( y + 1 ) + unit / 2 + 1 - 2, 
                unit,
                unit / 2
            )
        if p.getUnit() == Piece.RIGHT_PAIR:
            self.g.fillRect(
                offset_left + unit * x,
                self.getHeight() - unit * ( y + 1 ) - 2, 
                unit / 2,
                unit
            )
        if p.getUnit() == Piece.BOTTOM_PAIR:
            self.g.fillRect(
                offset_left + unit * x,
                self.getHeight() - unit * ( y + 1 ) - 2, 
                unit,
                unit / 2
            )
        if p.getUnit() == Piece.LEFT_PAIR:
            self.g.fillRect(
                offset_left + unit * x + unit / 2 + 1,
                self.getHeight() - unit * ( y + 1 ) - 2, 
                unit / 2,
                unit
            )
        
        if p.getType() == Piece.BLUE:
            self.g.setColor( 0x00b0e0ff )
        if p.getType() == Piece.RED:
            self.g.setColor( 0x00ffe0b0 )
        if p.getType() == Piece.YELLOW:
            self.g.setColor( 0x00ffffc0 )
        
        if p.getUnit() in ( Piece.LEFT_PAIR, Piece.TOP_PAIR, ):
            self.g.fillRoundRect(
                offset_left + unit * x + unit / 3,
                self.getHeight() - unit * ( y + 1 ) + unit / 3 - 2, 
                unit / 3,
                unit / 3,
                unit / 3,
                unit / 3
            )
    
    def initBoard( level ):
        
        self.board = DrMugsBoard( 10, 15 )
        
        germs_left = 3 + level
        num_germs = 3 + level
        while germs_left > 0:
            col = Piece.getRandomColour()
            if board.setPiece(
                random.randint(0, self.board.getWidth()),
                # restrict to top 2/3
                random.randint(0, board.getHeight() * 2 / 3),
                Piece( col, Piece.GERM )
            ):
                germs_left -= 1
            
        
        germs_on_board = num_germs
        
        # setup board pills
        pills_left = 6 + level
        num_pills = 6 + level
        safety_count = 1000
        while pills_left > 0 and safety_count > 0:
            safety_count -= 1
            if random.randint(0, 1) == 0:
                #vert
                if board.addVertPill( 
                    random.randint(0, board.getWidth() ),
                    random.randint(0, board.getHeight() * 2 / 3 ),
                    Piece.getRandomColour(), 
                    Piece.getRandomColour()
                ):
                    pills_left -= 1
            else:
                #horiz
                if board.addHorizPill(
                    random.randint(0, board.getWidth() - 1 ),
                    random.randint(0, board.getHeight() * 2 / 3 ),
                    Piece.getRandomColour(),
                    Piece.getRandomColour()
                ):
                    pills_left -= 1
            
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    pygame.init()
    screen = pygame.display.set_mode((240, 320))
    pygame.display.set_caption('Canvas test')
    pygame.mouse.set_visible(0)
    c = Canvas(screen)
    clock = pygame.time.Clock()
    while 1:
        clock.tick(2) # 2 fps
        c.background()
        c.drawText(c.main_font[19], "DrMugs by Mark Kennedy", (255, 255, 230), (20, 30))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
    

