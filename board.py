class BoardOutOfBounds(Exception): pass
class BoardReadOutOfBounds(BoardOutOfBounds): pass
class BoardWriteOutOfBounds(BoardOutOfBounds): pass

import piece

class DrMugsBoard:
    # the play area made of 'pieces' (which are just cells really)
    # 0,0 is bottom left
    
    # players curret piece

    def __init__( self, width, height ):
        (self.pX1, self.pY1, self.pX2, self.pY2) = (0, 0, 0, 0)
        self.pieceInPlay = False
        self.width = width
        self.height = height
        self.board = []
        for i in range( 0, self.width * self.height ):
            self.board.append( piece.Piece( piece.EMPTY, piece.NONE ) )

        self.pieceInPlay = False
       
    def setPiece(x, y, p):
        """
            :returns:
                True or False, depending on success
        """
        if (x >= self.width or y >= self.height):
            raise BoardWriteOutOfBounds()

        if (self.board[x + y * self.width].getType() == piece.EMPTY):
            self.board[x + y * self.width] = p
            return True
       
        return False
   
    def getPiece(x, y):
        if (x >= self.width or y >= self.height):
            raise BoardReadOutOfBounds()

        return self.board[x + y * self.width]
   
    
    def addPieceInPlay(type1, type2, x1, y1, x2, y2):
        """
            Place a piece on the self.board!
            :parameters:
                type1 = one end of piece
                type2 = other end of piece
                xn and yn = coords of that end (should be adjacent!)
            :returns:
                True or False, depending on success
        """
        if (x1 >= self.width or y1 >= self.height):
            raise BoardWriteOutOfBounds()

        if (x2 >= self.width or y2 >= self.height):
            raise BoardWriteOutOfBounds()

        if (x1 != x2 and y1 != y2):
            # the piece isn't horiz or vert
            return False
       
        p1 = self.getPiece(x1, y1)
        p2 = self.getPiece(x2, y2)
        if (p1.getType() == piece.EMPTY and p2.getType() == piece.EMPTY):
            # can place piece here ok!
            if (y1 > y2):
                self.setPiece(x1, y1, piece.Piece(type1, piece.TOP_PAIR))
                self.setPiece(x2, y2, piece.Piece(type2, piece.BOTTOM_PAIR))
                self.setPieceInPlay(x1, y1, x2, y2)
                return True
            elif (y2 > y1):
                self.setPiece(x1, y1, piece.Piece(type1, piece.BOTTOM_PAIR))
                self.setPiece(x2, y2, piece.Piece(type2, piece.TOP_PAIR))
                self.setPieceInPlay(x1, y1, x2, y2)
                return True
            elif (x1 > x2):
                self.setPiece(x1, y1, piece.Piece(type1, piece.RIGHT_PAIR))
                self.setPiece(x2, y2, piece.Piece(type2, piece.LEFT_PAIR))
                self.setPieceInPlay(x1, y1, x2, y2)
                return True
            elif (x2 > x1):
                self.setPiece(x1, y1, piece.Piece( type1, piece.LEFT_PAIR ))
                self.setPiece(x2, y2, piece.Piece( type2, piece.RIGHT_PAIR )); 
                self.setPieceInPlay(x1, y1, x2, y2)
                return True
       
        return False
    
    def setPieceInPlay(x1, y1, x2, y2):
        if(x1 >= self.width or y1 >= self.height):
            raise BoardOutOfBounds()
        if(x2 >= self.width or y2 >= self.height):
            raise BoardOutOfBounds()
        self.pX1 = x1
        self.pX2 = x2
        self.pY1 = y1
        self.pY2 = y2
        self.pieceInPlay = True
    
    # scans self.board for orphaned pair halves and converts to piece.SINGLE
    def convertOrphansToSingles():
        for y in range( 0, self.height ):
            for x in range( 0, self.width ):
                if( self.board[ x + y * self.width ].getUnit() == piece.LEFT_PAIR ):
                    if( x < self.width - 1 ):
                        if( self.board[ x + 1 + y * self.width ].getUnit() != piece.RIGHT_PAIR ):
                            self.board[ x + y * self.width ].setUnit( piece.SINGLE )
                       
                    else:
                        # I can't see how this would happen!
                        self.board[ x + y * self.width ].setUnit( piece.SINGLE )
                   
                elif( self.board[ x + y * self.width ].getUnit() == piece.RIGHT_PAIR ):
                    if( x > 0 ):
                        if( self.board[ x - 1 + y * self.width ].getUnit() != piece.LEFT_PAIR ):
                            self.board[ x + y * self.width ].setUnit( piece.SINGLE )
                       
                    else:
                        self.board[ x + y * self.width ].setUnit( piece.SINGLE )
                   
                elif( self.board[ x + y * self.width ].getUnit() == piece.BOTTOM_PAIR ):
                    if( y < self.height - 1 ):
                        if( self.board[ x + ( y + 1 ) * self.width ].getUnit() != piece.TOP_PAIR ):
                            self.board[ x + y * self.width ].setUnit( piece.SINGLE )
                       
                    else:
                        self.board[ x + y * self.width ].setUnit( piece.SINGLE )
                   
                elif( self.board[ x + y * self.width ].getUnit() == piece.TOP_PAIR ):
                    if( y > 0 ):
                        if( self.board[ x + ( y - 1 ) * self.width ].getUnit() != piece.BOTTOM_PAIR ):
                            self.board[ x + y * self.width ].setUnit( piece.SINGLE )
                       
                    else:
                        self.board[ x + y * self.width ].setUnit( piece.SINGLE )
    
    def swapPieces( x1, y1, x2, y2 ):
        if( x1 >= self.width or y1 >= self.height ):
            raise BoardWriteOutOfBounds()
        if( x2 >= self.width or y2 >= self.height ):
            raise BoardWriteOutOfBounds()
        temp = self.board[ x1 + y1 * self.width ]
        self.board[ x1 + y1 * self.width ] = self.board[ x2 + y2 * self.width ]
        self.board[ x2 + y2 * self.width ] = temp
   
    
    # move all pieces down a space if gravity permits 
    def effectGravity():
        # start from bottom so you don't process pieces twice as they fall
        # also start at row 1, not 0, since 0 can't go anywhere!
        moved = False
        for y in range( 1, y < self.height ):
            for x in range( 0, self.width ):
                if(
                    (
                        self.board[ x + y * self.width ].getUnit() == piece.SINGLE or
                        self.board[ x + y * self.width ].getUnit() == piece.BOTTOM_PAIR or
                        self.board[ x + y * self.width ].getUnit() == piece.TOP_PAIR
                    )
                    and self.board[ x + ( y - 1 ) * self.width ].getType() == piece.EMPTY
                ):
                    if( self.pieceInPlay ):
                        if( x == self.pX1 and y == self.pY1 ):
                            self.pY1 -= 1            
                       
                        if( x == self.pX2 and y == self.pY2 ):
                            self.pY2 -= 1
                       
                   
                    self.swapPieces( x, y, x, y - 1 )
                    moved = True
                elif( x < self.width - 1 ):
                    if (
                        self.board[ x + y * self.width ].getUnit() == piece.LEFT_PAIR
                        and self.board[ x + ( y - 1 ) * self.width ].getType() == piece.EMPTY
                        and self.board[ x + 1 + ( y - 1 ) * self.width ].getType() == piece.EMPTY
                    ):
                        self.swapPieces( x, y, x, y - 1 )
                        self.swapPieces( x + 1, y, x + 1, y - 1 )
                        if( self.pieceInPlay ):
                            if( ( x == self.pX1 or x == self.pX2 ) and y == self.pY1 ):
                                self.pY1 -= 1                  
                                self.pY2 -= 1
                           
                       
                        x += 1
                        moved = True

        return moved
    
    # angle -1 for anti, 1, for clockwise
    def rotatePieceInPlay( angle ):
        """
            :returns:
                boolean success
        """
        if( self.pieceInPlay ):
            if( self.pX1 != self.pX2 and self.pY1 == self.height - 1 ):
                return False
           
            if( self.pX1 == self.pX2
                and self.rotationFromVertBlockedOnSide( 1 )
                and self.rotationFromVertBlockedOnSide( -1 ) ):
                # can't turn anywhere cos we're vertical and against walls each side
                return False
           
            if( self.pX1 == self.pX2 and not( self.rotationFromVertBlockedOnSide( - angle ) ) ):
                # we can slide against our angle
                self.swapPieces( self.pX1, min( self.pY1, self.pY2 ), self.pX1 - angle, min( self.pY1, self.pY2 ) )
                self.swapPieces( self.pX1, max( self.pY1, self.pY2 ), self.pX1, min( self.pY1, self.pY2 ) )
                if( self.pY1 > self.pY2 ):
                    self.pY1 -= 1
                    self.pX2 -= angle
                    if( angle == 1 ):
                        # p2 becomes LEFT
                        # p1 becomes RIGHT
                        self.getPiece( self.pX2, self.pY2 ).setUnit( piece.LEFT_PAIR )
                        self.getPiece( self.pX1, self.pY1 ).setUnit( piece.RIGHT_PAIR )
                        
                    else:
                        # p2 -> r
                        # p1 -> l
                        self.getPiece( self.pX2, self.pY2 ).setUnit( piece.RIGHT_PAIR )
                        self.getPiece( self.pX1, self.pY1 ).setUnit( piece.LEFT_PAIR );                        
                   
                else:
                    self.pY2 -= 1
                    self.pX1 -= angle
                    if( angle == 1 ):
                        # p1 becomes LEFT
                        # p2 becomes RIGHT
                        self.getPiece( self.pX2, self.pY2 ).setUnit( piece.RIGHT_PAIR )
                        self.getPiece( self.pX1, self.pY1 ).setUnit( piece.LEFT_PAIR )
                    else:
                        # p1 -> r
                        # p2 -> l
                        self.getPiece( self.pX2, self.pY2 ).setUnit( piece.LEFT_PAIR )
                        self.getPiece( self.pX1, self.pY1 ).setUnit( piece.RIGHT_PAIR )
                   
               
                return True
            else:
                # we must be horizontal
                if( not self.rotationFromHorizBlockedOnSide( angle ) ):
                    if( angle == 1 ):
                        if( self.pX1 > self.pX2 ):
                            #p1 stays same
                            self.swapPieces( self.pX2, self.pY2, self.pX1, self.pY2 + 1 )
                            self.pX2 = self.pX1
                            self.pY2 = self.pY2 + 1
                            # p1 -> bottom
                            # p2 -> top
                            self.getPiece( self.pX2, self.pY2 ).setUnit( piece.TOP_PAIR )
                            self.getPiece( self.pX1, self.pY1 ).setUnit( piece.BOTTOM_PAIR )
                        else:
                            #p2 stays same
                            self.swapPieces( self.pX1, self.pY1, self.pX2, self.pY1 + 1 )
                            self.pX1 = self.pX2
                            self.pY1 = self.pY1 + 1
                            # p1 -> top
                            # p2 -> bottom
                            getPiece( self.pX2, self.pY2 ).setUnit( piece.BOTTOM_PAIR )
                            getPiece( self.pX1, self.pY1 ).setUnit( piece.TOP_PAIR )
                       
                    elif( angle == -1 ):
                        if( self.pX1 < self.pX2 ):
                            #p1 stays same
                            swapPieces( self.pX2, self.pY2, self.pX1, self.pY2 + 1 )
                            self.pX2 = self.pX1
                            self.pY2 = self.pY2 + 1
                            # p1 -> bottom
                            # p2 -> top
                            getPiece( self.pX2, self.pY2 ).setUnit( piece.TOP_PAIR )
                            getPiece( self.pX1, self.pY1 ).setUnit( piece.BOTTOM_PAIR )
                        else:
                            #p2 stays same
                            swapPieces( self.pX1, self.pY1, self.pX2, self.pY1 + 1 )
                            self.pX1 = self.pX2
                            self.pY1 = self.pY1 + 1
                            # p1 -> top
                            # p2 -> bottom
                            getPiece( self.pX2, self.pY2 ).setUnit( piece.BOTTOM_PAIR )
                            getPiece( self.pX1, self.pY1 ).setUnit( piece.TOP_PAIR )
       
        return False
   
    def rotationFromHorizBlockedOnSide( side ):
        if( self.pieceInPlay ):
            minY = min( self.pY1, self.pY2 )
            if( side == 1 ):
                maxX = max( self.pX1, self.pX2 )
                if( getPiece( maxX, minY + 1 ).getType() != piece.EMPTY ):
                    return True
               
            elif( side == -1 ):
                minX = min( self.pX1, self.pX2 )
                if( getPiece( minX, minY + 1 ).getType() != piece.EMPTY ):
                    return True
               
           
       
        return False
   
    def rotationFromVertBlockedOnSide( side ):
        if( self.pieceInPlay ):
            minY = min( self.pY1, self.pY2 )
            if( side == 1 ):
                maxX = max( self.pX1, self.pX2 )
                if( maxX + 1 >= self.width or getPiece( maxX + 1, minY ).getType() != piece.EMPTY ):
                    return True
               
            elif( side == -1 ):
                minX = min( self.pX1, self.pX2 )
                if( minX <= 0 or getPiece( minX - 1, minY ).getType() != piece.EMPTY ):
                    return True
               
           
       
        return False
   
    # x is horiz distance
    def movePieceInPlay( x ):
        if( self.pieceInPlay ):
            if( x == 1 ):
                maxX = max( self.pX1, self.pX2 )
                if( maxX < self.width - 1 ):
                    # can move right unless piece there
                    if( self.pX1 != self.pX2 ):
                        # we're horizontal
                        if( getPiece( maxX + 1, self.pY1 ).getType() == piece.EMPTY ):
                            # we can move right
                            swapPieces( maxX, self.pY1, maxX + 1, self.pY1 )
                            swapPieces( maxX - 1, self.pY1, maxX, self.pY1 )
                            self.pX1 += 1
                            self.pX2 += 1
                            return True
                       
                    else:
                        # we're vertical
                        if( getPiece( self.pX1 + 1,  self.pY1 ).getType() == piece.EMPTY
                            and getPiece( self.pX2 + 1, self.pY2 ).getType() == piece.EMPTY
                        ):
                            # we can move right
                            swapPieces( self.pX1, self.pY1, self.pX1 + 1, self.pY1 )
                            swapPieces( self.pX2, self.pY2, self.pX2 + 1, self.pY2 )
                            self.pX1 += 1
                            self.pX2 += 1
                            return True
                            
            elif( x == -1 ):
                minX = min( self.pX1, self.pX2 )
                if( minX > 0 ):
                    # can move right unless piece there
                    if( self.pX1 != self.pX2 ):
                        # we're horizontal
                        if( getPiece( minX - 1, self.pY1 ).getType() == piece.EMPTY ):
                            # we can move right
                            swapPieces( minX, self.pY1, minX - 1, self.pY1 )
                            swapPieces( minX + 1, self.pY1, minX, self.pY1 )
                            self.pX1 -= 1
                            self.pX2 -= 1
                            return True
                       
                    else:
                        # we're vertical
                        if( getPiece( self.pX1 - 1,  self.pY1 ).getType() == piece.EMPTY
                            and getPiece( self.pX2 - 1, self.pY2 ).getType() == piece.EMPTY
                        ):
                            # we can move right
                            swapPieces( self.pX1, self.pY1, self.pX1 - 1, self.pY1 )
                            swapPieces( self.pX2, self.pY2, self.pX2 - 1, self.pY2 )
                            self.pX1 -= 1
                            self.pX2 -= 1
                            return True
           
       
        return False
   
    
    def testForLine():
        """
            :returns:
                boolean
        """
        same = 1
        last_col = -1
        for y in range( 0, self.height ):
            same = 1
            for x in range( 0, self.width - 1 ):
                if( self.board[ x + y * self.width ].getType() != piece.EMPTY and
                    last_col == self.board[ x + y * self.width ].getType() ):
                    same += 1
                else:
                    if( same >= 4 ):
                        # hooray!
                        return True
                   
                    same = 1
               
                last_col = self.board[ x + y * self.width ].getType()
           
            if( same >= 4 ):
                # hooray!
                return True
           
       
        same = 1
        last_col = -1
        for x in range( 0, self.width ):
            same = 1
            for y in range( 0, self.height - 1 ):
                if( self.board[ x + y * self.width ].getType() != piece.EMPTY and
                    last_col == self.board[ x + y * self.width ].getType() ):
                    same += 1
                else:
                    if( same >= 4 ):
                        return True
                   
                    same = 1
               
                last_col = self.board[ x + y * self.width ].getType()
           
            if( same >= 4 ):
                # hooray!
                return True
           
       
        return False
   
    
    # returns a score (which is prop. to how many blobs deleted)
    def removeLines():
        #check horiz
        same = 1
        cleared = 0
        last_col = -1
        for y in range( 0, self.height ):
            for x in range( 0, self.width ):
                if (
                    self.board[ x + y * self.width ].getType() != piece.EMPTY and
                    last_col == self.board[ x + y * self.width ].getType()
                ):
                    same += 1
                else:
                    if( same >= 4 ):
                        # hooray!
                        for cc in range(x - 1, x - same - 1, -1):
                            self.clearPiece( cc, y )
                       
                        cleared += same
                   
                    same = 1
               
                last_col = self.board[ x + y * self.width ].getType()
           
            if(same >= 4):
                # hooray!
                for cc in range(self.width - 1, self.width - same - 1, -1):
                    self.clearPiece( cc, y )
               
                cleared += same
           
       
        same = 1
        last_col = -1
        for x in range(0, self.width ):
            for y in range(0, self.height):
                if( self.board[ x + y * self.width ].getType() != piece.EMPTY and
                    last_col == self.board[ x + y * self.width ].getType() ):
                    same += 1
                else:
                    if( same >= 4 ):
                        # hooray!
                        for cc in range(y - 1, y - same - 1, -1):
                            self.clearPiece( x, cc )
                       
                        cleared += same
                   
                    same = 1
               
                last_col = self.board[ x + y * self.width ].getType()
           
            if( same >= 4 ):
                # hooray!
                for cc in range(self.height - 1, self.height - same - 1, -1):
                    self.clearPiece( x, cc )
               
                cleared += same
           
        return cleared
   
    def clearPieceInPlay():
        self.pieceInPlay = False
        self.pX1 = self.pY1 = self.pX2 = self.pY2 = 0
   
    def clearPiece( x, y ):
        if( x >= self.width or y >= self.height ):
            raise BoardWriteOutOfBounds()
        self.board[ x + y * self.width ] = piece.Piece()
   
    def countGerms():
        """
            :returns:
                integer
        """
        germ_count = 0
        for cc in range( 0, self.width * self.height):
            if( self.board[ cc ].getUnit() == piece.GERM ):
                germ_count += 1
                      
        return germ_count
   
    def addVertPill( x, y, col1, col2 ):
        """
            :returns:
                True or False, dependant on success
        """
        if( x >= self.width or y + 1 >= self.height ):
            raise BoardWriteOutOfBounds()

        if( self.setPiece( x, y, piece.Piece( col1, piece.BOTTOM_PAIR ) ) ):
            if( self.setPiece( x, y + 1, piece.Piece( col2, piece.TOP_PAIR ) ) ):
                if( self.testForLine() ):
                    self.clearPiece( x, y )
                    self.clearPiece( x + 1, y )
                    return False
                else:
                    return True
               
            else:
                self.clearPiece( x, y )
                return False
       
        return False

    def addHorizPill( x, y, col1, col2 ):
        """
            :returns:
                True or False, dependant on success
        """
        if( x + 1 >= self.width or y >= self.height ):
            raise BoardWriteOutOfBounds()
        if( self.setPiece( x, y, piece.Piece( col1, piece.LEFT_PAIR ) ) ):
            if( self.setPiece( x + 1, y, piece.Piece( col2, piece.RIGHT_PAIR ) ) ):              
                # now test for line
                if( self.testForLine() ):
                    self.clearPiece( x, y )
                    self.clearPiece( x + 1, y )
                    return False
                else:
                    return True
               
            else:
                self.clearPiece( x, y )
                return False
       
        return False
   

if __name__ == "__main__":
    board = DrMugsBoard( 20, 20 )
    print board
