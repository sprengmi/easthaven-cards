#proj07

#This program creates a Solitaire card game called Easthaven, and enforces all of the rules,
#which are shown at http://worldofsolitaire.com. Once at this website, click Solitaire at the left-
#upper corner, click "select game", and choose "Easthaven".

import cards


def setup():
    '''
    paramaters: None
    returns a tuple of:    
    - a foundation (list of 4 empty lists)
    - a tableau (a list of 7 lists, each sublist contains 3 cards, and the first two cards of each list should be set to hidden)
    - a stock contains a list of 31 cards. (after dealing 21 cards to tableau)
    '''
    fdation = [[],[],[],[]]         #Sets foundation, tableau and stock to empty lists
    tableau = []
    stock = []
    Deck = cards.Deck()             #Creates our deck of cards
    Deck.shuffle()                  #Shuffle the deck
    for i in range(7):              #Create 7 lists of 3 cards each, first 2 of each list are hidden
        a = Deck.deal()
        b = Deck.deal()
        c = Deck.deal()
        a.set_hidden()
        b.set_hidden()
        tableau.append([a,b,c])
    for c in range(31):             #"Deal" the remaining cards into the stock list
        c = Deck.deal()
        stock.append(c)
    return fdation,tableau,stock
    

def printGame(fdation,tableau,stock):
    '''
    parameters: a foundation, a tableau and a stock
    returns: Nothing
    prints the game, i.e, print all the info user can see.
    Includes:
        a) print tableau  (Make sure only show those cards which are revealed. For hidden cards, just print "XX".
        b) print foundation
        c) print stock  (only need to show how many cards left in stock)
    '''
    print 'Tableau:'
    for r in range(0,7):                    #We have 7 rows in the tableau
        print 'Row %d: ' %(r+1),            #Print our row number, r+1 since we want 1-7 instead of 0-6
        for c in range(len(tableau[r])):    #Number of cards in each row will vary throughout the game so we check the length of the row and use that as range
            print tableau[r][c],            #Print the card: select the row (r) from the tableau list then the card from the row list
        print ''                            #Breaks the line
        
    print '-'*20
    print 'Foundation:'
    for r in range(0,4):                    #Same as above but only four rows
        print 'Row %d: ' %(r+1),
        for c in range(len(fdation[r])):
            print fdation[r][c],
        print ''
    print '-'*20
    print 'Stock: %d cards left.' %(len(stock))
    

def revealCard(tableau, tRow):
    '''
    parameters: a tableau row and a tableau
    returns: Nothing
    reveal the top card of the indicated row
    '''
    if len(tableau[tRow]) == 0:             #if there are no cards in the row list, nothing to reveal
        pass
    elif tableau[tRow][-1].get_hidden():    #If the top card is hidden
        tableau[tRow][-1].show_card()       #Reveal the top card
    else:
        pass
    
          
def moveToFoundation(tableau,fdation,tRow,fRow):
    '''
    parameters: a tableau, a foundation, row of tableau, row of foundation
    returns: Boolean (True if the move is valid, False otherwise)
    moves a card at the end of a row of tableau to a row of foundation
    reveal the next card in tableau if it is not already revealed.
    '''

    if len(tableau[tRow]) == 0:                             #If the tableau row is empty, no card to move, return False
        return False
    
    c = tableau[tRow][-1]                                   #Get the card we're trying to move
    
    if (len(fdation[fRow]) == 0) and (c.get_rank() == 1):   #If the foundation row is empty and the card is an Ace:
        c = tableau[tRow].pop()                             #Pop that card from its tableau list
        revealCard(tableau,tRow)                            #Run reveal card on that tableau row
        fdation[fRow].append(c)                             #append the card to the foundation list
        return True
    elif len(fdation[fRow]) != 0:                           #Check if there are cards in this foundation row
        fc = fdation[fRow][-1]                              #Get the top card of the foundation row
        if (c.get_suit() == fc.get_suit()) and (c.get_rank() == fc.get_rank()+1):   #If the two cards are the same suit and the foundation card is one less:
            c = tableau[tRow].pop()                         #Pop card from tableau, run revealcard, append to foundation 
            revealCard(tableau,tRow)
            fdation[fRow].append(c)
            return True
        else:
            return False
    else:
        return False
        
    

def canBeConnected(card1, card2):
    '''
    parameters: two cards
    return: Boolean
    ###Can card2 be played on card1...
    if the second card has different color from the first one, and the rank of card2 is one less than that of card1, return True
    Otherwise, return False
    '''
    if (not card1.has_same_color(card2)) and (card1.get_rank() == card2.get_rank()+1):
        #If the cards are opposite colors and the rank of card2 is one less than card1:
        return True
    else:
        return False
    

def moveInTableau(tableau,NumOfCards,tRowSource,tRowDest):
    '''
    parameters: a tableau, number of cards, the source tableau row and the destination tableau row
    returns: Boolean
    moves a certain number of cards from one row to another
    hint: 1. first make sure the cards you are moving are built down by rank and by alternating color
          2. if the dest row is empty, move those cards
             else, make sure the card of tableau[tRowSource][-NumofCards] is one rank lower than the top card of destination row (tableau[tRowDest][-1]),
                     and they should have different color
    '''
    try:                
        n = NumOfCards  #just making it shorter
        moveList = tableau[tRowSource][-n:]                 #Make a list of the cards we have selected to move
        append = []                                         #seperate append list because we'll need to reverse just the items were appending later
        for i in range(len(moveList)-1):                    
            if canBeConnected(moveList[i],moveList[i+1]):   #Check whether each card in the stack we're moving is in the correct order
                #print moveList[i],moveList[i+1],'is good'
                continue
            else:               #If any set of cards fails canBeConnected, return False
                return False
        if len(tableau[tRowDest]) == 0:                     #If the destination row is empty go ahead and move
            for i in range(n):                              
                c = tableau[tRowSource].pop()               #pop and store the card from tableau source row
                revealCard(tableau,tRowSource)
                append.append(c)                            #append card to append list
            append.reverse()                                #reverse append list
            tableau[tRowDest].extend(append)                #extend destination row in tableau with the append list
            return True
        elif canBeConnected(tableau[tRowDest][-1],moveList[0]): #If rows not empty check if top card of move list canBeConnected to last card of dest row
            for i in range(n):                                  #Same as above
                c = tableau[tRowSource].pop()
                revealCard(tableau,tRowSource)
                append.append(c)                            #append card to append list
            append.reverse()                                #reverse append list
            tableau[tRowDest].extend(append)                #extend destination row in tableau with the append list                
            return True
        else:                       # If the move list fails, return False
            return False
    except IndexError:              # Try and except IndexError used to prevent bad NumOfCards input
        return False


def dealMoreCards(stock,tableau):
    '''
    parameters: a stock and a tableau
    returns: Boolean
    deal one card to each row of tableau. For the last deal operation, deal the remaining cards to the first couple rows of tableau.
    returns False if the stock is empty. Otherwise, deal cards, and return True
    '''
    if len(stock) >= 7:
        for i in range(7):          #For each tableau row
            c = stock.pop(0)        #pop and store first card from stock
            tableau[i].append(c)    #Append to appropiate row in tableau
        return True
    elif len(stock) == 3:           #If we've gone through the stock 4 times the length will be three
        for i in range(3):          #pop and append 3 times instead of 7
            c = stock.pop(0)
            tableau[i].append(c)
        return True
    elif len(stock) == 0:           #If stock is empty return False
        print 'There are no cards left in the stock.'
        return False
    else:   #This will never happen (hopefully)
        print 'Well something went wrong. Whoops.'
            
    

def isWinner(fdation):
    '''
    parameters: a fdation
    return: Boolean
    If the fdation contains all 52 cards, return True
    else return False
    '''
    summ = 0                    #initialize sum
    for i in range(4):          #for the 4 rows of fdation
        summ += len(fdation[i]) #add each length
    if summ == 52:              #If all 52 cards are in fdation return True
        return True
    else:
        return False



def printRules():
    '''
    parameters: none
    returns: nothing
    prints the rules
    '''
    print """
Rules of Easthaven
Goal, move all the cards to the foundations
Foundation
	Built up by rank and by suit from Ace to King 
Tableau 
	Built down by rank and by alternating color 
	The top card may be moved 
	Complete or partial correctly ranked piles may be moved 
	An empty spot may be filled with any card or correctly ranked pile 
Stock 
	Dealing from the deck moves 1 card to each Tableau spot.

Responses are: 
	 'f [row A] [foundation F]' to move the top card of row A to foundation F
	 'm [number of cards] [row A] [row B]' to move a certain number of cards from row A to row B
	 'd' to deal cards
	 'q' to quit
	 """

def showHelp():
    '''
    parameters: none
    returns: nothing
    prints the supported commands
    '''
    print """
Responses are: 
	 'f [row A] [foundation F]' to move the top card of row A to foundation F
	 'm [number of cards] [row A] [row B]' to move a certain number of cards from row A to row B
	 'd' to deal cards
	 'q' to quit
	 """

def playagain(command):
    '''
    parameters: a command given after winning game in play Fn
    returns: nothing
    User is prompted to see if they would like to play again (Y/N).
    '''
    if command in "Yy":
        play()
    elif command in "Nn":
        print 'Thanks for playing!'

    
def play():
    ''' 
    main program. Does error checking on the user input. 
    '''
    printRules()                                                #Print the rules, only print once at beginning
    fdation,tableau,stock = setup()                             #Setup fdation,tableau and stock
    
    while not isWinner(fdation):                                #As long as the user hasn't won (all 52 cards in fdation) we'll ask for commands and run them
        printGame(fdation,tableau,stock)                        #Print Game each time through
        print''
        print''
        command = raw_input("Command (type 'h' for help): ")    #Ask for the command
        command = command.split()                               #Split the command into a list so it can be easily indexed
        
        if len(command) == 0:               #If command is left blank:
            print 'Please enter a command.'
            print ''
            continue
        
        if not command[0] in 'FfMmDdQqHh':                      #Check that the first item of the command list is a valid alpha command
            print 'Unknown Command:',command[0]
            print ''
            continue

        if (command[0] in 'DdQqHh') and (len(command) > 1): #Make sure a d q or h command isn't followed by gibberish, we want clean commands and dag-nab-it we'll get them
            print 'The command',command[0],'should not be followed by any other characters.'
            print ''
            continue
        elif command[0] in 'Dd':                            #If we've got a d command, deal some cards, pronto!
            dealMoreCards(stock,tableau)
            continue
        elif command[0] in 'Qq':                            #If we've got a q command, end the game, they've obviously got places to go and people to see!
            print 'Thanks for playing.'                     
            break                                           #Break to exit game loop
        elif command[0] in 'Hh':                            #Well if they've forgotten the valid responses already we'll give em a hand
            showHelp()                                      #showHelp() for h command
            continue
            
        try:
            if (command[0] in 'Ff'):
                    #If we have a foundation command make sure the command list is of the correct format.
                if (len(command) == 3) and (int(command[1]) in range(1,8)) and (int(command[2]) in range(1,5)):
                    tRow = int(command[1]) - 1                           #Set tRow and fRow, -1 due to indexing
                    fRow = int(command[2]) - 1
                    if moveToFoundation(tableau,fdation,tRow,fRow):     #If move is valid, move is executed
                        continue
                    else:                                               #If not, tells user and continues
                        print 'Invalid move'
                        print ''
                        continue
                else:   #command is f but failed the format test
                    print 'move to foundation command should have the format of:  f [row A] [foundation F]. \
[row A] should be a number between 1 and 7, inclusively. [foundation F] should be a number between 1 and 4, inclusively.'
                    print ''
                continue
            
            elif (command[0] in 'Mm'):
                    #If we have a move command, mke sure that the entire command list is in the correct format.
                if (len(command) == 4) and (int(command[2]) in range(1,8)) and (int(command[3]) in range(1,8)):
                    if int(command[1]) <= len(tableau[int(command[2])-1]):                  #Check if its a valid move based on number of cards we want to move and the length of the row wer're moving from
                        NumOfCards,tRowSource,tRowDest = int(command[1]),int(command[2])-1,int(command[3])-1   #Set the values for the move function to our commands (-1 for the row nums)
                        if moveInTableau(tableau,NumOfCards,tRowSource,tRowDest):           #If move is valid, move is executed
                            continue
                        else:                                                               #Else, prints invalid and continues
                            print 'Invalid move'
                            print ''
                            continue
                    else:
                        print 'Invalid move'
                        print ''
                        continue
                else:   #command is m but faild the format test
                    print 'The command of moving cards within tableau should have the format of: m [number of cards] [row A] [row B].\
[number of cards],[row A],[row B] should all be integers.'
                    print ''
                    continue                                                                                         

        except ValueError:    #If we ran into a ValueError from the command
            if command[0] in 'Ff':          #If it was an f command, describe format of f and continue
                print 'move to foundation command should have the format of:  f [row A] [foundation F]. \
[row A] should be a number between 1 and 7, inclusively. [foundation F] should be a number between 1 and 4, inclusively.'
                print ''
                continue
            elif command[0] in 'Mm':        #If it was an m command, describe format of m and continue
                print 'The command of moving cards within tableau should have the format of: m [number of cards] [row A] [row B].\
[number of cards],[row A],[row B] should all be integers.'
                print ''
                continue
        except IndexError:    #If we ran into an IndexError from the command
            if command[0] in 'Ff':          #If it was an f command, describe format of f and continue
                print 'move to foundation command should have the format of:  f [row A] [foundation F]. \
[row A] should be a number between 1 and 7, inclusively. [foundation F] should be a number between 1 and 4, inclusively.'
                print ''
                continue
            elif command[0] in 'Mm':        #If it was an m command, describe format of m and continue
                print 'The command of moving cards within tableau should have the format of: m [number of cards] [row A] [row B].\
[number of cards],[row A],[row B] should all be integers.'
                print ''
                continue
            else:
                continue
            
    if isWinner(fdation):                       #If isWinner is True
        print ''
        printGame(fdation,tableau,stock)        #Print their game one last time
        print''
        print''
        for i in range(4):                      #Print the classic cascading solitaire cards
            for c in range(13):
                print ' '*c,fdation[i][c]
        print 'Congratulations!!!! You WON!'    #Print winning message

        while True:                             #Prompt to play again
            command = raw_input('Insert token to play again? (Y/N): ')
            if command in 'YyNn':
                playagain(command)
                break
            else:
                continue
        
play()
