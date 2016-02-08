#!/usr/bin/env python
#--------------------------------------------------------------------------
# Tic Tac Toe game in Python
# Author: Mawuli Adzaku <mawuli@mawuli.me>
#
# Date: 20-05-2013
# Tested with Python 2.7
#
# Contributor: Stepan.lenevich <stepan.lenevich@gmail.com>
# (Improved AI of TBot, polished invalid imput handling)
# Date: 02-08-2016
#
# TO RUN:
#         sudo chmod a+x tictactoe.py
#         ./tictactoe.py
# OR JUST RUN : python tictactoe.py
#
# @todo:  log user names and game scores
# OR delete todo and comments to make it look like a completed project o_O
# 
# ---------------------------------------------------------------------------


# import modules
import random
import sys
import copy
from random import randint

class Game:
    "Tic-Tac-Toe class. This class holds the user interaction, and game logic"
    def __init__(self):
        self.board = [' '] * 9
        self.player_name = ''
        self.player_marker = ''
        self.bot_name = 'TBot'
        self.bot_marker = ''
        self.winning_combos = (
        [6, 7, 8], [3, 4, 5], [0, 1, 2], [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6],
    )
        self.lastmove = 0
        self.corners = [0,2,6,8]
        self.sides = [1,3,5,7]
        self.middle = 4
        self.move_count = 0
        self.markers=['X', 'O']
        self.randomside = 1
        self.form = '''
           \t| %s | %s | %s |
           \t-------------
           \t| %s | %s | %s |
           \t-------------
           \t| %s | %s | %s |
           '''                    

    def print_board(self,board = None):
        "Display board on screen"
        if board is None:
            print self.form % tuple(self.board[6:9] + self.board[3:6] + self.board[0:3])
        else:
            # when the game starts, display numbers on all the grids
            print self.form % tuple(board[6:9] + board[3:6] + board[0:3])

    def get_marker(self):
        marker = raw_input("Would you like your marker to be play X or O?: ").upper()
        if marker not in ["X","O"]:
			self.randomside=randint(0,1)
			marker=self.markers[self.randomside]

        if marker == "X":
            return ('X', 'O')
        else:
            return ('O','X')
    

    def help(self):
        print '''
\n\t The game board has 9 sqaures(3X3).
\n\t Two players take turns in marking the spots/grids on the board.
\n\t The first player to have 3 pieces in a horizontal, vertical or diagonal row wins the game.
\n\t To place your mark in the desired square, simply type the number corresponding with the square on the grid 
 
\n\t Press Ctrl + C to quit
'''

    def quit_game(self):
        "exits game"
        self.print_board
        print "\n\t Thanks for playing :-) \n\t Come play again soon!\n"
        sys.exit()

    def is_winner(self, board, marker):
        "check if this marker will win the game"
        # order of checks:
        #   1. across the horizontal top
        #   2. across the horizontal middle
        #   3. across the horizontal bottom
        #   4. across the vertical left
        #   5. across the vertical middle
        #   6. across the vertical right
        #   7. across first diagonal
        #   8. across second diagonal
        for combo in self.winning_combos:
            if (board[combo[0]] == board[combo[1]] == board[combo[2]] == marker):
                return True
        return False

    def get_bot_move(self):
        '''
        find the best space on the board for the bot. Objective
        is to find a winning move, a blocking move or an equalizer move. 
        Bot must always win
        '''


        """Added random first move weighted towards center and corner moves"""
# ---------------------------------------------------------------------------
# <Author: "Stepan">                                                          
# If bot plays X, then it chooses a move randomly.                            
# Corner moves are prefered, sides are disfavored.                            
# ---------------------------------------------------------------------------
          
        if self.move_count < 1:
            
            first_move_choice = randint(1,7)
                        
            if first_move_choice == 1:
                return self.choose_random_move(self.sides)
                
            elif first_move_choice > 6:
                return self.middle
                
            else:
                return self.choose_random_move(self.corners)

# ---------------------------------------------------------------------------
# </Author>                                                                   
# ---------------------------------------------------------------------------


        # check if bot can win in the next move
        for i in range(0,len(self.board)):
            board_copy = copy.deepcopy(self.board)
            if self.is_space_free(board_copy, i):
                self.make_move(board_copy,i,self.bot_marker)
                if self.is_winner(board_copy, self.bot_marker):
                    return i
                
        # check if player could win on his next move
        for i in range(0,len(self.board)):
            board_copy = copy.deepcopy(self.board)
            if self.is_space_free(board_copy, i):
                self.make_move(board_copy,i,self.player_marker)
                if self.is_winner(board_copy, self.player_marker):
                    return i
 
# ---------------------------------------------------------------------------
# <Author: "Stepan">                                                          
#
# Handling XOX along a diagonal case. Two distinct forks are possible.        
# Cleaner implementation is outlined in the pseodocode below: 
#
#
# make an array of all_forking_moves_for_human
#     if array all_forking_moves_for_human is not empty:
#         for legal_move in self.board:                                
#             if legal_move is a check:
#                 calculate blocking_move
#                 if blocking_move not in all_forking_moves_for_human:
#                     return legal_move
#        
#         print "how is this even possible? Have I (bot) skipped some moves? "
#             return
#
#   
# This double fork is unique, so a fast patch was used instead
# ---------------------------------------------------------------------------

        if self.move_count == 3:
            if ((self.board[0] == 'X' and self.board[8] == 'X') or (self.board[2] == 'X' and self.board[6] == 'X')) and self.board[4] == 'O':
                return self.choose_random_move(self.sides)


        #New branch starts here. Check for possible forks. first for the bot then for the player"""
        for i in range(0,len(self.board)):                                 
            board_copy1 = copy.deepcopy(self.board)                       
            fork_count=0
            if self.is_space_free(board_copy1, i):                          
                self.make_move(board_copy1,i,self.bot_marker)               


                for j in range(0,len(self.board)):                                            
                    if self.is_space_free(board_copy1, j):                      
                        board_copy2 = copy.deepcopy(self.board)
                        self.make_move(board_copy2,i,self.bot_marker)
                        self.make_move(board_copy2,j,self.bot_marker)
                        if self.is_winner(board_copy2, self.bot_marker):
                            fork_count+=1

            if fork_count > 1:
                return i
                                                        
                                                   
        for i in range(0,len(self.board)):                                 
            board_copy1 = copy.deepcopy(self.board)                       
            fork_count=0
            if self.is_space_free(board_copy1, i):                          
                self.make_move(board_copy1,i,self.player_marker)               


                for j in range(0,len(self.board)):                                            
                    if self.is_space_free(board_copy1, j):                      
                        board_copy2 = copy.deepcopy(self.board)
                        self.make_move(board_copy2,i,self.player_marker)
                        self.make_move(board_copy2,j,self.player_marker)
                        if self.is_winner(board_copy2, self.player_marker):
                            fork_count+=1

            if fork_count > 1:
                return i 
        
        # Middle is preferred over corners, so I changed the order
        
        # If the middle is free, take it
        if self.is_space_free(self.board,self.middle):
            return self.middle

        # check for space in the corners, and take it
        move = self.choose_random_move(self.corners)
        if move != None:
            return move                

# ---------------------------------------------------------------------------
# </Author>                                                                   
# ---------------------------------------------------------------------------


        # else, take one free space on the sides
        return self.choose_random_move(self.sides)

    def is_space_free(self, board, index):
        "checks for free space of the board"
        # print "SPACE %s is taken" % index
        return board[index] == ' '

    def is_board_full(self):
        "checks if the board is full"
        for i in range(1,9):
            if self.is_space_free(self.board, i):
                return False
        return True

    def make_move(self,board,index,move):
        board[index] =  move

    def choose_random_move(self, move_list):
        possible_winning_moves = []
        for index in move_list:
            if self.is_space_free(self.board, index):
                possible_winning_moves.append(index)
                if len(possible_winning_moves) != 0:
                    return random.choice(possible_winning_moves)
                else:
                    return None
       
    def start_game(self):
       "welcomes user, prints help message and hands over to the main game loop"
       # welcome user 
       print '''\n\t-----------------------------------
                \n\t   TIC-TAC-TOE by Mawuli Adzaku, AI strengthened by Stepan Lenevich
                \n\t------------------------------------
             '''
       self.print_board(range(1,10))
       self.help()
       self.player_name = self.get_player_name()

       # get user's preferred marker 
       self.player_marker, self.bot_marker = self.get_marker()
       print "Your marker is " + self.player_marker
        
       # randomly decide who can play first
       if self.player_marker == 'O':
           print "I will go first"

           #self.print_board()
           self.move_count=0
           self.enter_game_loop('b')
       else:
           print "You will go first"          
           # now, enter the main game loop
           self.print_board()
           self.enter_game_loop('h')


# ---------------------------------------------------------------------------
# <Author: "Stepan">                                                          
#    
# Fixed handling of invalid input
# ---------------------------------------------------------------------------


    def get_player_move(self):
        move = None
        while move is None:
            input_value = raw_input("Pick a spot to move: (1-9) ")
            try:
                move = int(input_value)
                if move not in [1,2,3,4,5,6,7,8,9] or not self.is_space_free(self.board,move-1):	
                    move = None                    
            except ValueError:
				pass
            
        return move - 1
        
# ---------------------------------------------------------------------------
# </Author>                                                                   
# ---------------------------------------------------------------------------
        
    def get_player_name(self):
        return raw_input("Hi, i am %s" % self.bot_name + ". What is your name? ") 


    def enter_game_loop(self,turn):
       "starts the main game loop"
       is_running = True
       player = turn #h for human, b for bot
       while is_running:
           if player == 'h':
               user_input = self.get_player_move()
               self.make_move(self.board,user_input, self.player_marker)
               self.move_count+=1
               
               if(self.is_winner(self.board, self.player_marker)):
                   self.print_board()
                   print "\n\tCONGRATULATIONS %s, YOU HAVE WON THE GAME!!! \\tn" % self.player_name
                   #self.incr_score(self.player_name)
                   is_running = False
                   #break
               else:
                   if self.is_board_full():
                       self.print_board()
                       print "\n\t-- Match Draw --\t\n"
                       is_running = False
                       #break
                   else:
                       self.print_board()
                       player = 'b'
           # bot's turn to play
           else:
              bot_move =  self.get_bot_move()
              self.make_move(self.board, bot_move, self.bot_marker)
              self.move_count+=1                                                   #got on self.bot
              if (self.is_winner(self.board, self.bot_marker)):
                  self.print_board()
                  print "\n\t%s HAS WON!!!!\t\n" % self.bot_name
                  #self.incr_score(self.bot_name)
                  is_running = False
                  break
              else:
                  if self.is_board_full():
                      self.print_board()
                      print "\n\t -- Match Draw -- \n\t"
                      is_running = False
                      #break
                  else:
                      self.print_board()
                      player = 'h'

       # when you break out of the loop, end the game
       self.end_game()

    def end_game(self):
       play_again = raw_input("Would you like to play again? (y/n): ").lower()
       if play_again != 'n':
           self.__init__() # necessary for re-initialization of the board etc
           self.start_game()
       else:
           print "\n\t-- GAME OVER!!!--\n\t"
           self.quit_game()



if __name__ == "__main__":   
     TicTacToe = Game()
     TicTacToe.start_game()
