from ast import Pass
from cmath import rect
import pygame, random, keyboard, time, sys, enchant
import copy

#Setting up game
pygame.init()
running = True
dictionary = enchant.Dict("en_US")

#Colours
green = (0, 255, 0)
black = (0, 0, 0)
darkergray = (192, 192, 192)
gray = (224, 224, 224)
yellow = (245, 239, 87)

#Initalizing Variables
userEntry = ''
userEntryBox = pygame.Rect(340, 800, 10, 60)
font_size = pygame.font.Font(None, 45)

#Getting random answerWord
words = ['apple', 'beach', 'camel', 'dance', 'eager', 'fairy', 'ghost', 'honey', 'image', 'jolly', 'karma', 'lemon',
             'mango', 'noble', 'olive', 'piano', 'quiet', 'rider', 'saint', 'table', 'uncle', 'vivid', 'witty', 'xenon',
             'young', 'zebra', 'abide', 'brave', 'carry', 'daisy', 'early', 'faith', 'grace', 'happy', 'ideal', 'joker',
             'kings', 'lucky', 'magic', 'noble', 'oasis', 'peace', 'quilt', 'raise', 'sunny', 'tiger', 'unity', 'value',
             'waltz', 'xerox', 'yield', 'zeal', 'alert', 'bliss', 'charm', 'dream', 'evoke', 'fable', 'giant', 'honor',
             'igloo', 'jolly', 'knock', 'lunar', 'medal', 'noble', 'ocean', 'peace', 'quest', 'raise', 'solar', 'trend',
             'urban', 'vivid', 'witty', 'xenon', 'yield', 'zeal', 'angel', 'bliss', 'charm', 'dream', 'enjoy', 'flora',
             'grace', 'happy', 'ideal', 'jolly', 'karma', 'lunar', 'medal', 'noble', 'olive', 'peace', 'quilt', 'raise',
             'sunny', 'tiger', 'unity', 'value', 'waltz', 'xerox', 'yield', 'zeal']

#Getting answer word
answerWord = random.choice(words)

# Setting as first row
turn = 0

# Initializing 5x6 grid
grid = [
    [copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray)],
    [copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray)],
    [copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray)],
    [copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray)],
    [copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray)],
    [copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray), copy.deepcopy(darkergray)],
]

# User guesses list
guesses = []

#Game Speed (FPS)
clock = pygame.time.Clock()   
gameSpeed = 10

#Setting up display
dis = pygame.display.set_mode((800, 900)) 
dis.fill(gray)
pygame.display.set_caption("Wordle By Zain Babar")

font = pygame.font.SysFont('LEMONMILK', 100)
wordle = font.render("WORDLE", black, True)
answerWordScreen = font.render("The word was: " + answerWord, black, True)

# Edit the grid for the row of index 'turn', comparing 'word' to 'answerWord'
def checkWord(word, answerWord, turn):

    #checking for current row
    for index in range(5):

        #Change to green if letter in correct position
        if word[index] == answerWord[index]:
            grid[turn][index] = copy.deepcopy(green)

        #Change to yellow if letter within word, not in correct position
        elif (word[index] in answerWord) and (word[index] != answerWord[index]):
            grid[turn][index] = copy.deepcopy(yellow)

        #If letter not found, change to gray
        else:
            grid[turn][index] = copy.deepcopy(darkergray)

    return grid 


# Game Loop
while running == True:

    #Checking input
    event = pygame.event.poll()

    #If "X" is clicked
    if event.type == pygame.QUIT: 
        running = False

    #Displaying title
    dis.blit(wordle, (255, 20))

    #User Entering a Word
    if event.type == pygame.KEYDOWN:
        
        # Check for backspace
        if event.key == pygame.K_BACKSPACE:
            userEntry = userEntry[:-1] # Splices word to delete last letter
        else:
            userEntry += event.unicode
            userEntry = userEntry[:5] #Max answerWord size of 5

        #Checking to see if valid word is entered
        if len(userEntry) == 5 and event.key == pygame.K_RETURN:
            
            #Checking to see if word exists
            if dictionary.check(userEntry):
                checkWord(userEntry, answerWord, turn)
                guesses.append(userEntry)
            
            

                #Moving to next row
                turn += 1

                # Exit the game loop if user gets word correct or incorrect after all 6 guesses
                if (userEntry == answerWord) or (turn == 6):
                    running = False

    #User Text box  
    pygame.draw.rect(dis, darkergray, userEntryBox)
    textSurface = font_size.render(userEntry, True, (255, 255, 255))
    
    #Render text box
    dis.blit(textSurface, (userEntryBox.x+5, userEntryBox.y+5))

    #Text cannot go outside textbox
    userEntryBox.w = max(130, textSurface.get_width()+10)

    # Go through each turn's row and render its blocks.
    for row in range(6):
        for col in range(5):
            
            blockColor = grid[row][col]
            blockY = 130 + col * 110
            blockX = 100 + row * 110
            blockWidth = 100
            blockHeight = 100

            #Render blocks
            pygame.draw.rect(dis, blockColor, [blockY, blockX, blockWidth, blockHeight])
            
            #Render words
            if (row < len(guesses)):
                dis.blit(font.render(guesses[row][col].upper(), True, black), (blockY+23, blockX+13))


    #Update display
    pygame.display.update()

#If user gets word, display game
if ((turn == 6) and (userEntry == answerWord)) or (userEntry == answerWord):
    time.sleep(1.5)

# Displaying correct word if user did not get it
elif turn == 6:

    time.sleep(2)
    
    dis.fill(gray)
    dis.blit(answerWordScreen, (50, 350))

    pygame.display.update()

    time.sleep(2)

#'Quit'
pygame.quit()