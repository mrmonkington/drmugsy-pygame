from exceptions import *

import os, sys
import pygame
# import constants, such as keys, into global namespace
from pygame.locals import *

# import key mapping
from defaults import *
# TODO import user mapping

GAME_TITLE_SCREEN = 1
GAME_INTRO = 2
GAME_PLAYING = 3
GAME_OVER = 4
GAME_SCORES = 5
GAME_NEXT_LEVEL = 6
GAME_INSTRUCTIONS = 7

MENU_START = 0
MENU_CONTINUE = 1
MENU_INSTRUCTIONS = 2

class DrMugs:
    def __init__(self):
        self.time_now = 0
        self.next_time = 0
        
        self.flasher = 1
        self.level = 1
        self.germs_on_board = 0
        
        # test count
        self.test = 0
        self.board = False
        # ms required for a piece to fall one board square (lower == more difficult)
        self.gravity = 1000
        // count of game ticks
        self.gravity_clock = 0
        
        self.game_state = 0
        
        self.menu_option_selected = MENU_START
        
        self.update_score = False
        
        self.score = 0
        pass

    def main(self):
        pygame.init()
        self.screen = pygame.display.set_mode((320,240))
        self.screen.fill((0,0,0))

    def init_menu(self):
        pass

    def run_menu(self):
        pass

    def init_game(self)
        self.board = DrMugsBoard( 10, 20
        pass

    def run_game(game):
        while not exit
            exit = True
            try:
                # limit to 60fps
                self.clock.tick(60)
                exit = False
            except GameError:
                # I guess just return to menu
                pass
    

"""
 * The controls:
 * (all are non-repeating if held)
 *   command   key   action                                      reset grav clock
 *   -----------------------------------------------------------------------------
 *   left            move piece left                             no
 *   right           move piece right                            no
 *   clockwise       rotate piece clockwise
 *                   if vert: sliding left and rotating about
 *                            lowest point
 *                   if horiz: rotating about rightmost point    no
 *   anticlockwise   rotate piece anticlockwise
 *                   if vert: sliding right and rotating
 *                            about lowest point
 *                   if horiz: rotating about leftmost point
 *   down            move to next gravity period                 yes
 *
"""
    def do_game_keys(self):
        repaint = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pass
                # quit!
            else if event.type == KEYDOWN:
                if event.key == KEY_LEFT:
                    self.board.movePieceInPlay( -1 )
                    repaint = True
                elif event.key == KEY_RIGHT
                    self.board.movePieceInPlay( 1 )
                    repaint = True
                elif event.key == KEY_CLOCK:
                    self.board.rotatePieceInPlay( 1 )
                    repaint = True
                elif event.key == KEY_ANTI:
                    self.board.rotatePieceInPlay( -1 )
                    repaint = True
                elif event.key == KEY_DOWN
                    # advance to next gravity tick
                    self.gravity_clock = self.gravity
                    repaint = True
                         
                    break
    def do_intruction_keys(self):
                case GAME_INSTRUCTIONS:
                    game_state = GAME_TITLE_SCREEN
                    break
    def do_gameover_keys(self):
                    game_state = GAME_TITLE_SCREEN
                    break
    def do_title_keys(self):
                    //game_state = GAME_INTRO
                    if( ( key_state & MY_UP_PRESSED ) != 0 ):
                        menu_option_selected --
                        if( menu_option_selected <  MENU_START ):
                            menu_option_selected = MENU_START
                        elif( menu_option_selected > MENU_INSTRUCTIONS ):
                            menu_option_selected = MENU_INSTRUCTIONS
                        
                    
                    if( ( key_state & MY_DOWN_PRESSED ) != 0 ):
                        menu_option_selected ++
                        if( menu_option_selected <  MENU_START ):
                            menu_option_selected = MENU_START
                        elif( menu_option_selected > MENU_INSTRUCTIONS ):
                            menu_option_selected = MENU_INSTRUCTIONS

                    if( ( key_state & MY_PRIMARY_PRESSED ) != 0 ):
                        if menu_option_selected == MENU_START:
                            level = 1
                            game_state = GAME_INTRO
                        elif menu_option_selected == MENU_CONTINUE:
                            // load
                            game_state = GAME_INTRO
                        elif menu_option_selected == MENU_INSTRUCTIONS:
                            game_state = GAME_INSTRUCTIONS

    def run():
        next_time = System.currentTimeMillis()
        boolean exit = False
        int step_test = 0;    
        game_rate = 20; #50Hz
        gravity_clock = 0; # count of 
        gravity = 5; # 10 tick per second
        #game_state = GAME_PLAYING
        game_state = GAME_TITLE_SCREEN
 
        int paint_refresh = 5
        int paint_clock = 0
        
        
        while( !exit ):
            switch( game_state ):
                case GAME_PLAYING:
                case GAME_INTRO:
                    initBoard( level )
                    settleBoard()
                    board.addPieceInPlay(
                        Piece.getRandomColour( rand ),
                        Piece.getRandomColour( rand ),
                        board.getWidth() / 2 - 1,
                        board.getHeight() - 1, board.getWidth() / 2,
                        board.getHeight() - 1
                    );  
                    gravity = 40 - ( paint_refresh * (int)( level / paint_refresh ) ); # 1 tick per half second  
                    gravity_clock = 0
                    update_score = True
                    game_state = GAME_PLAYING
                    repaint()
                    while( game_state == GAME_PLAYING ):
                        time_now = System.currentTimeMillis()
                        if( time_now > next_time ):
                            gravity_clock += 1
                            if( paint_clock ++ >= paint_refresh ):
                                repaint();        
                                paint_clock = 0
                            
                            if( gravity_clock >= gravity ):
                                gravity_clock = 0
                                # advance app timer (not same as game timer?)
                                int points = 0
                                test ++
                                update_score = False
                                if( ! board.effectGravity() ):
                                    # piece now static
                                    board.clearPieceInPlay()
                                    points = board.removeLines()
                                    if( points > 0 ):
                                        update_score = True
                                        gravity = 5
                                        # recalc germs
                                        germs_on_board = board.countGerms()
                                        # a line must have been cleared -- process falling stuff
                                        board.convertOrphansToSingles()
                                        repaint()
                                        score += points
                                    else:
                                        # create new play piece
                                        gravity = 25
                                        # test exit conditions
                                        if( germs_on_board == 0 ):
                                            game_state = GAME_NEXT_LEVEL
                                        else if( ! board.addPieceInPlay(
                                                Piece.getRandomColour( rand ),
                                                Piece.getRandomColour( rand ),
                                                board.getWidth() / 2 - 1,
                                                board.getHeight() - 1, board.getWidth() / 2,
                                                board.getHeight() - 1
                                            )
                                        ):
                                            game_state = GAME_OVER
                                        
                                    
                                                    
                            
                            next_time = time_now + game_rate
                        
                        # some sort of thread sleep?
                    
                    break
                case GAME_OVER:
                    # delete save game
                    pass
                            
                        
                    
                    #make sure game_over screen is shown
                    repaint()
:
                        long go_timer = time_now + 2000
                        while( time_now < go_timer && game_state == GAME_OVER ):
                            time_now = System.currentTimeMillis()
                            if( time_now > next_time ):
                                gravity_clock += 1
                                if( paint_clock ++ >= paint_refresh ):
                                    repaint();        
                                    paint_clock = 0
                                
                                next_time = time_now + game_rate
                                     
                         
                        game_state = GAME_TITLE_SCREEN
                    
                    break
                case GAME_NEXT_LEVEL:
                    #make sure game_over screen is shown
                    repaint()
:
                        long go_timer = time_now + 1000
                        while( time_now < go_timer ):
                            time_now = System.currentTimeMillis()
                            if( time_now > next_time ):
                                gravity_clock += 1
                                if( paint_clock ++ >= paint_refresh ):
                                    repaint();        
                                    paint_clock = 0
                                
                                next_time = time_now + game_rate
                                     
                         
                        level ++
                        saveLevel()
                        initBoard( level )
                        settleBoard()
                        game_state = GAME_PLAYING
                        update_score = True
                        repaint()
                    
                    break
                case GAME_TITLE_SCREEN:
                    repaint()
                    while( game_state == GAME_TITLE_SCREEN ):
                        time_now = System.currentTimeMillis()
                        if( time_now > next_time ):
                            gravity_clock += 1
                            if( paint_clock ++ >= paint_refresh ):
                                repaint();        
                                paint_clock = 0
                            
                            next_time = time_now + game_rate
                    
                    break
                case GAME_INSTRUCTIONS:
                    repaint()
                    while( game_state == GAME_INSTRUCTIONS ):
                        time_now = System.currentTimeMillis()
                        if( time_now > next_time ):
                            gravity_clock += 1
                            if( paint_clock ++ >= paint_refresh ):
                                repaint();        
                                paint_clock = 0
                            
                            next_time = time_now + game_rate
                    
                    break
                default:
                    return
    
    def saveLevel():
        #byte[] monk =: (byte)level 
        pass

    def settleBoard():
        boolean gravityAffected = True
        while( gravityAffected ):
            gravityAffected = board.effectGravity()
