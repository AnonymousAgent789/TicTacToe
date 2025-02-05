'''
TicTacToe

    Gamemodes:
        PvP:
            Each player inputs name
            Each player places their piece until win
            Output player that won
        
        PvC:
            Computer has multiple difficulties
            Player should be given ratings depending on these games
            Record win_counter and losses for these games
            Same layout as PvP
    
    Logic:
        Checks all win conditions without using 8 different if statements by looping through blocks
        Computer difficulties:
            Easy:
                Computer randomly places squares everywhere until game ends
            Medium:
                Computer randomly places squares everywhere until it can place 3 in a row or block the player's 3 in a row
                Detects 2 in a row by looping through all blocks and checking horizontal and vertical 2 in a row for each block
            Hard:
                First utilises finishing logic from medium
                Then uses that same logic to block player if they can place 3
                Then places blocks in corners and then in varying places so that it is impossible for computer to lose
    
    Extra:
        Must have buttons for back and quit
        Must be able to change themes through theme button
        All themes are stored in a single list
        Must have 'computer thinking' screen with balls that rotate mathematically
'''

#Imports
import pygame
from random import randint as random
from math import sin as sin

'''Resets the  variables for user to play again'''
def setup_vars():
    global playing #Whether in game screen or not
    playing = True
    
    global names_of_players #Names of players
    names_of_players = ["", ""]
    
    global current_selected_player #Used for the text box when inputting player names_of_players
    current_selected_player = 0
    
    global current_screen #Stores which screen the user is on
    current_screen = 0
    
    global current_turn #Current player turn
    current_turn = 1
    
    global board #Values for the board
    board = ["", "", "", "", "", "", "", "", ""]
    
    global difficulty #Computer difficulty for PvC games
    difficulty = 0
    
    global current_computer_move #Which move the computer is on
    current_computer_move = 1
    
    global game_loop_counter #Counts the number of game loops while runnning, also used as a timer of sorts
    game_loop_counter = 0
    
    global computer_think_counter #Delays the computer moving by a certain amount of time
    computer_think_counter = 0
    
    global win_data #Data about winning
    win_data = [] #First is id of start of horizontal line, second is (1 -> horizontal; 2 -> vertical; 3 -> negative diagonal; 4 -> positive diagonal; 5-> draw)

'''Start of game'''
pygame.init()
pygame.display.set_caption("Tictactoe")
global screen
screen = pygame.display.set_mode((600, 700))
global win_counter
win_counter = [[0, 0, 0], [0, 0, 0], [0, 0, 0]] #Wins, draws, losses and (easy, medium, hard) inside each one
global themes
themes = [ #Name, [Text colour, Background colour, Button colour, Pressed button colour, Win text colour, Win line colour, Back button colour, Quit button colour, Button separator line colour, Text box colour]
        ["Classic", [
                    "black",
                    (200, 255, 200),
                    (150, 255, 100),
                    (150, 200, 150),
                    "red",
                    (100, 100, 100),
                    (255, 180, 100),
                    (255, 130, 100),
                    (100, 150, 100),
                    (225, 255, 225)
                ]
        ],
        ["Dark", [
                    (200, 200, 200),
                    (50, 50, 50),
                    (125, 125, 125),
                    (100, 100, 100),
                    (200, 50, 50),
                    (75, 75, 75),
                    (150, 100, 45),
                    (150, 40, 20),
                    (20, 20, 20),
                    (60, 60, 60)
                ]
        ], 
        ["Light", [
                    "black",
                    "white",
                    (200, 200, 200),
                    (175, 175, 175),
                    "red",
                    (100, 100, 100),
                    (255, 100, 50),
                    (255, 150, 150),
                    (150, 150, 150),
                    (150, 150, 150)
                ]
        ],
        ]
global current_theme
current_theme = 0
running = True
setup_vars()
mouse = [0, 0]

'''Calculates the block to its right and the block below it'''
def block_right(index):
    return index - 2 if index % 3 == 2 else index + 1
def block_down(index):
    return index - 6 if index // 3 == 2 else index + 3

'''Logic for the computer for easy difficulty'''
def easy_computer_logic():
    global board
    index = random(0, 8)
    while board[index] != "":
        index = random(0, 8)
    board[index] = "X"

'''Logic for the computer for medium difficulty'''
def medium_computer_logic(hard, letter_to_check):
    global board
    vals = ""
    
    for i in board: #Remove blanks
        vals += "." if i == "" else i
    
    for i in range(0, 9): #Straight lines
        if vals[i] == letter_to_check and vals[block_right(i)] == letter_to_check and vals[block_right(block_right(i))] == ".": #Horizontal
            board[block_right(block_right(i))] = "X"
            return True
        if vals[i] == letter_to_check and vals[block_down(i)] == letter_to_check and vals[block_down(block_down(i))] == ".": #Vertical
            board[block_down(block_down(i))] = "X"
            return True
    
    for i in range(0, 9, 4): #Diagonals
        if vals[i] == letter_to_check and vals[block_right(block_down(i))] == letter_to_check and vals[block_right(block_right(block_down(block_down(i))))] == ".": #Negative diagonal
            board[block_right(block_right(block_down(block_down(i))))] = "X"
            return True
        j = ((i // 3) * 3) + (2 - (i % 3)) #Reflection in the y-axis down the middle
        if vals[j] == letter_to_check and vals[block_right(block_right(block_down(j)))] == letter_to_check and vals[block_right(block_down(block_down(j)))] == ".": #Positive diagonal
            board[block_right(block_down(block_down(j)))] = "X"
            return True
    
    if not hard and letter_to_check == "O":
        easy_computer_logic() #Otherwise, random
        return
    
    return False

'''Logic for the computer for hard difficulty'''
def hard_computer_logic():
    global current_computer_move
    
    if medium_computer_logic(True, "X"): #Complete 3
        return
    if medium_computer_logic(True, "O"): #Block player 3
        current_computer_move += 1
        return
    
    vals = ""
    for i in board: #Remove blanks
        vals += "." if i == "" else i
    
    #First move
    if current_computer_move == 1:
        board[0] = "X"
        current_computer_move += 1
        return

    #Second move
    if current_computer_move == 2:
        if board[4] == "" and board[2] == "" and board[1] == "":
            board[2] = "X"
            current_computer_move += 1
            return
        elif board[4] == "" and board[6] == "" and board[3] == "":
            board[6] = "X"
            current_computer_move += 1
            return
        else:
            board[8] = "X"
            current_computer_move += 1
            return
    
    #Third move
    if current_computer_move == 3:
        if board[2] == "X":
            if board[5] == "" and board[8] == "":
                board[8] = "X"
                current_computer_move += 1
                return
            elif board[3] == "" and board[6] == "":
                board[6] = "X"
                current_computer_move += 1
                return
        if board[6] == "X":
            if board[7] == "" and board[8] == "":
                board[8] = "X"
                current_computer_move += 1
                return
            elif board[1] == "" and board[2] == "":
                board[2] = "X"
                current_computer_move += 1
                return
        elif board[6] == "":
            board[6] = "X"
            current_computer_move += 1
            return
    
    #Otherwise
    easy_computer_logic()
    current_computer_move += 1
    return

'''Base function for when it is computer's turn'''
def computer_logic():
    global difficulty
    global current_turn
    
    if difficulty == 1: #Easy
        easy_computer_logic()
    elif difficulty == 2: #Medium
        if not medium_computer_logic(False, "X"): #Places
            medium_computer_logic(False, "O") #Blocks
        
    elif difficulty == 3: #Hard
        hard_computer_logic()
    
    current_turn = 2 #Changes turn to be player's turn
    
    generate_board()
    if not calculate_win("X"):
        calculate_win("O")

'''Checks all win conditions'''
def calculate_win(letter):
    global win_data
    vals = ""
    
    for i in board: #Remove blanks
        vals += "." if i == "" else i
    
    for i in range(0, 9, 4):
        if vals[i] == letter and vals[block_right(i)] == letter and vals[block_right(block_right(i))] == letter: #Horizontal
            win_data = [(i // 3) * 3, 1]
        if vals[i] == letter and vals[block_down(i)] == letter and vals[block_down(block_down(i))] == letter: #Vertical
            win_data = [i % 3, 2]
    
    if vals[0] == letter and vals[4] == letter and vals[8] == letter: #Negative diagonal
        win_data = [0, 3]
    if vals[2] == letter and vals[4] == letter and vals[6] == letter: #Positive diagonal
        win_data = [2, 4]    
    if not vals.__contains__(".") and win_data == []: #Tie
        win_data = [0, 5]

    if win_data == []: #Game has not ended
        return False
    
    end_game()
    return True

'''Displays end-of-game overlay in the case of the game ending'''
def end_game():
    global win_data
    global playing
    global current_screen
    global win_counter
    global themes
    global current_theme
    global difficulty
    playing = False
    
    if win_data[1] == 5: #Tie
        screen.blit(pygame.font.SysFont(None, 100).render("Tie!", True, themes[current_theme][1][4]), (250, 250))
        if current_screen == 3: #Stores tie if PvC
            win_counter[1][difficulty - 1] += 1
    else:
        #Winning line
        if win_data[1] == 1: #Horizontal
            pygame.draw.line(screen, themes[current_theme][1][5], (0, ((win_data[0] // 3) * 200) + 100), (600, ((win_data[0] // 3) * 200) + 100), 30)
        if win_data[1] == 2: #Vertical
            pygame.draw.line(screen, themes[current_theme][1][5], (((win_data[0] % 3) * 200) + 100, 0), (((win_data[0] % 3) * 200) + 100, 600), 30)
        if win_data[1] == 3: #Negative diagonal
            pygame.draw.line(screen, themes[current_theme][1][5], (0, 0), (600, 600), 30)
        if win_data[1] == 4: #Positive diagonal
            pygame.draw.line(screen, themes[current_theme][1][5], (0, 600), (600, 0), 30)
        
        #Player that won
        if current_screen == 1: #PvP
            if board[win_data[0]] == "X":
                screen.blit(pygame.font.SysFont(None, 75).render(names_of_players[0] + " has won!", True, themes[current_theme][1][4]), (50, 275))
            else:
                screen.blit(pygame.font.SysFont(None, 75).render(names_of_players[1] + " has won!", True, themes[current_theme][1][4]), (50, 275))
        else: #PvC
            if board[win_data[0]] == "X":
                screen.blit(pygame.font.SysFont(None, 75).render("The computer has won!", True, themes[current_theme][1][4]), (10, 275))
                win_counter[2][difficulty - 1] += 1
            else:
                screen.blit(pygame.font.SysFont(None, 75).render("You have won!", True, themes[current_theme][1][4]), (100, 275))
                win_counter[0][difficulty - 1] += 1
    
    pygame.display.flip()

'''Base function for when a button is pressed inside games'''
def button_clicked():
    global current_turn
    global board
    global win_data
    button_num = (mouse[0] // 200) + (mouse[1] // 200) * 3 #Calculates the button currently being pressed
    if button_num < 0 or button_num > 8:
        return
    
    #If player presses button
    if board[button_num] == "":
        if current_turn == 1:
            board[button_num] = "X"
            current_turn = 2
        else:
            board[button_num] = "O"
            current_turn = 1
    else:
        return

    generate_board()
    if not calculate_win("X"):
        calculate_win("O")

'''Base function for when the mouse is clicked on the screen'''
def mouse_functions():
    global current_screen
    global current_turn
    global current_selected_player
    global themes
    global current_theme
    global difficulty
    
    if current_screen == 0: #Main menu
        if mouse[0] >= 150 and mouse[0] <= 450 and mouse[1] >= 250 and mouse[1] <= 350: #PvP name selector
            current_screen = 5
        elif mouse[0] >= 150 and mouse[0] <= 450 and mouse[1] >= 375 and mouse[1] <= 475: #PvC
            current_screen = 2
        elif mouse[0] >= 550 and mouse[1] <= 50: #Info
            current_screen = 4
    elif current_screen == 1 and playing: #Player vs player
        button_clicked()
    elif current_screen == 2 and mouse[0] >= 150 and mouse[0] <= 450: #Difficulty selector screen
        if mouse[1] >= 100 and mouse[1] <= 200: #Easy
            difficulty = 1
        elif mouse[1] >= 250 and mouse[1] <= 350: #Medium
            difficulty = 2
        elif mouse[1] >= 400 and mouse[1] <= 500: #Hard
            difficulty = 3
        else:
            return
        current_screen = 3
    elif current_screen == 3 and playing and current_turn == 2: #PvC game
        button_clicked()
    elif current_screen == 4 and mouse[0] >= 10 and mouse[0] <= 350 and mouse[1] >= 390 and mouse[1] <= 440: #Change themes
        if current_theme == len(themes) - 1:
            current_theme = 0
        else:
            current_theme += 1
    elif current_screen == 5 and mouse[0] >= 150 and mouse[0] <= 450:
        if mouse[1] >= 100 and mouse[1] <= 200: #Player 1 name
            current_selected_player = 1
        elif mouse[1] >= 250 and mouse[1] <= 350: #Player 2 name
            current_selected_player = 2
        elif mouse[1] >= 400 and mouse[1] <= 500: #Play
            current_screen = 1
        else:
            current_selected_player = 0
    else:
        current_selected_player = 0 #Deselect player
    
    if mouse[0] >= 250 and mouse[0] <= 350 and mouse[1] >= 625 and mouse[1] <= 675: #Quit button
        running = False
        quit()
    
    if mouse[0] <= 50 and mouse[1] >= 675: #Back
        setup_vars()
    
'''Generates the playing board'''
def generate_board():
    global themes
    global current_theme
    #Buttons
    for i in range(0, 9):
        if board[i] == "": #Blank
            pygame.draw.rect(screen, themes[current_theme][1][1], [(i % 3) * 200, (i // 3) * 200, 200, 200])
        else: #Pressed
            pygame.draw.rect(screen, themes[current_theme][1][3], [(i % 3) * 200, (i // 3) * 200, 200, 200])
        screen.blit(pygame.font.SysFont(None, 200).render(board[i], True, themes[current_theme][1][0]), (200 * (i % 3) + 50, 200 * (i // 3) + 50))
            
    #Lines
    pygame.draw.line(screen, themes[current_theme][1][8], (200, 0), (200, 600), 5)
    pygame.draw.line(screen, themes[current_theme][1][8], (400, 0), (400, 600), 5)
    pygame.draw.line(screen, themes[current_theme][1][8], (0, 200), (600, 200), 5)
    pygame.draw.line(screen, themes[current_theme][1][8], (0, 400), (600, 400), 5)
    pygame.draw.line(screen, themes[current_theme][1][8], (0, 600), (600, 600), 5)

'''Renders the 'computer thinking' screen'''
def computer_thinking():
    global game_loop_counter
    global themes
    global current_theme
    
    screen.blit(pygame.font.SysFont(None, 70).render("Computer is thinking", True, themes[current_theme][1][0]), (10, 275))
    
    for i in range(0, 3): #Dots
        pygame.draw.circle(screen, themes[current_theme][1][0], (520 - (150 * (0.1 * (sin(2 * ((game_loop_counter / 100) - i))) - 0.2)), 315 - (30 * (sin((game_loop_counter / 100) - i) ** 6))), 5) #Mathematical formula for position of dots
        
'''Calculates the rating of the player for PvC games'''
def calculate_rating():
    global win_counter
    rating = 100
    
    #Easy
    rating = rating * (1.025 ** win_counter[0][0]) #Easy win
    rating = rating * (0.9 ** win_counter[1][0]) #Easy draw
    rating = rating * (0.75 ** win_counter[2][0]) #Easy loss
    
    #Medium
    rating = rating * (1.075 ** win_counter[0][1]) #Medium win
    rating = rating * (1.01 ** win_counter[1][1]) #Medium draw
    rating = rating * (0.95 ** win_counter[2][1]) #Medium loss
    
    #Medium
    rating = rating * (1.5 ** win_counter[0][2]) #Hard win
    rating = rating * (1.1 ** win_counter[1][2]) #Hard draw
    rating = rating * (0.975 ** win_counter[2][2]) #Hard loss
    
    return int(rating)

'''Base game'''
while running:
    mouse = pygame.mouse.get_pos()
    game_loop_counter = game_loop_counter + 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Exiting
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: #Clicking mouse
            mouse_functions()
        elif event.type == pygame.KEYDOWN and current_selected_player != 0 and current_screen == 5: #Inputting names_of_players
            if event.key == pygame.K_BACKSPACE: #Delete character
                names_of_players[current_selected_player - 1] = names_of_players[current_selected_player - 1][:-1]
            elif event.key == pygame.K_RETURN: #Enter:
                if current_selected_player == 1:
                    current_selected_player = 2
                else:
                    current_screen = 1
            elif len(names_of_players[current_selected_player - 1]) < 10:
                names_of_players[current_selected_player - 1] += event.unicode
    
    if current_screen == 0: #Main menu
        screen.fill(themes[current_theme][1][1])
        screen.blit(pygame.font.SysFont(None, 100).render("TicTacToe", True, themes[current_theme][1][0]), (150, 100)) #Title text
        
        #PvP
        pygame.draw.rect(screen, themes[current_theme][1][2], [150, 250, 300, 100])
        screen.blit(pygame.font.SysFont(None, 45).render("Player vs Player", True, themes[current_theme][1][0]), (180, 285))
        
        #PvC
        pygame.draw.rect(screen, themes[current_theme][1][2], [150, 375, 300, 100])
        screen.blit(pygame.font.SysFont(None, 40).render("Player vs Computer", True, themes[current_theme][1][0]), (170, 410))
        
        #Info
        pygame.draw.rect(screen, themes[current_theme][1][2], [550, 0, 50, 50])
        screen.blit(pygame.font.SysFont("webdings", 40, False, False).render("i", True, themes[current_theme][1][0]), (555, 5))
        
    elif current_screen == 1 and playing: #2 player
        generate_board()
    
    elif current_screen == 2: #Difficulty selector screen
        screen.fill(themes[current_theme][1][1])
        screen.blit(pygame.font.SysFont(None, 75).render("Select Difficulty", True, themes[current_theme][1][0]), (100, 25)) #Title text
        
        #Easy
        pygame.draw.rect(screen, themes[current_theme][1][2], [150, 100, 300, 100])
        screen.blit(pygame.font.SysFont(None, 75).render("Easy", True, themes[current_theme][1][0]), (240, 130))
        
        #Medium
        pygame.draw.rect(screen, themes[current_theme][1][2], [150, 250, 300, 100])
        screen.blit(pygame.font.SysFont(None, 75).render("Medium", True, themes[current_theme][1][0]), (215, 280))
        
        #Hard
        pygame.draw.rect(screen, themes[current_theme][1][2], [150, 400, 300, 100])
        screen.blit(pygame.font.SysFont(None, 75).render("Hard", True, themes[current_theme][1][0]), (240, 425))
    
    elif current_screen == 3 and playing: #Player vs computer
        generate_board()
        if current_turn == 1:
            #COmputer thinking timer
            if computer_think_counter == 0:
                computer_think_counter = game_loop_counter
            elif game_loop_counter == computer_think_counter + (difficulty * 250):
                computer_think_counter = 0
                computer_logic()
            else:
                computer_thinking()
    
    elif current_screen == 4: #Info
        screen.fill(themes[current_theme][1][1])
        screen.blit(pygame.font.SysFont(None, 100).render("Info", True, themes[current_theme][1][0]), (235, 100)) #Title text
        
        #Stats
        screen.blit(pygame.font.SysFont(None, 50).render("Games won: " + str(win_counter[0][0] + win_counter[0][1] + win_counter[0][2]), True, themes[current_theme][1][0]), (10, 200)) #WIn
        screen.blit(pygame.font.SysFont(None, 50).render("Games drawn: " + str(win_counter[1][0] + win_counter[1][1] + win_counter[1][2]), True, themes[current_theme][1][0]), (10, 240)) #Draw
        screen.blit(pygame.font.SysFont(None, 50).render("Games lost: " + str(win_counter[2][0] + win_counter[2][1] + win_counter[2][2]), True, themes[current_theme][1][0]), (10, 280)) #Loss
        screen.blit(pygame.font.SysFont(None, 50).render("Rating: " + str(calculate_rating()), True, themes[current_theme][1][0]), (10, 320)) #Rating
        screen.blit(pygame.font.SysFont(None, 25).render("*Statistics are available for PvC games only*", True, themes[current_theme][1][0]), (10, 355))
        
        #Theme
        pygame.draw.rect(screen, themes[current_theme][1][2], [10, 390, 340, 50])
        screen.blit(pygame.font.SysFont(None, 40).render("Current theme: " + themes[current_theme][0], True, themes[current_theme][1][0]), (20, 400))
    
    elif current_screen == 5: #PvP name selector screen
        screen.fill(themes[current_theme][1][1])
        screen.blit(pygame.font.SysFont(None, 75).render("Enter names of players", True, themes[current_theme][1][0]), (5, 25)) #Title text
        
        #PLayer 1
        pygame.draw.rect(screen, themes[current_theme][1][9], [150, 100, 300, 100])
        if (game_loop_counter // 200) % 2 == 0 and current_selected_player == 1:
            screen.blit(pygame.font.SysFont(None, 75).render(names_of_players[0] + "|", True, themes[current_theme][1][0]), (160, 130))
        else:
            screen.blit(pygame.font.SysFont(None, 75).render(names_of_players[0], True, themes[current_theme][1][0]), (160, 130))
        
        #Player 2
        pygame.draw.rect(screen, themes[current_theme][1][9], [150, 250, 300, 100])
        if (game_loop_counter // 200) % 2 == 0 and current_selected_player == 2:
            screen.blit(pygame.font.SysFont(None, 75).render(names_of_players[1] + "|", True, themes[current_theme][1][0]), (160, 280))
        else:
            screen.blit(pygame.font.SysFont(None, 75).render(names_of_players[1], True, themes[current_theme][1][0]), (160, 280))
        
        #Start
        pygame.draw.rect(screen, themes[current_theme][1][2], [150, 400, 300, 100])
        screen.blit(pygame.font.SysFont(None, 75).render("Play", True, themes[current_theme][1][0]), (240, 425))
    
    #Quit
    pygame.draw.rect(screen, themes[current_theme][1][7], [250, 625, 100, 50])
    screen.blit(pygame.font.SysFont(None, 40).render("Quit", True, themes[current_theme][1][0]), (270, 637))
    
    #Back
    if current_screen != 0:
        pygame.draw.rect(screen, themes[current_theme][1][6], [0, 675, 50, 25])
        screen.blit(pygame.font.SysFont(None, 20).render("Back", True, themes[current_theme][1][0]), (5, 680))
    
    pygame.display.flip()

pygame.quit()
