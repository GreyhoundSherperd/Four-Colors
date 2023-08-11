'''
Each player gets 20 cards of 4 colors, each color has a different objective:
- Red: Attack, 1 red card dealt 1 damage if unblocked or countered, play in a zigzag pattern with green cards to multi-combo,
for example "Red Green Red".
- Blue: Block, 1 blue card defends 1 damage, can multi-block without green cards.
- Green: Bridge, Green cards were played in a zigzag pattern with red or yellow cards to multi-combo or multi-counter.
- Yellow: Counter, A yellow card is a hybrid of red and blue, a yellow card blocks 1 damage and deal 1 damage, play in a zigzag pattern
with green cards to multi-counter. Can only play if a red card was played last turn, and can only play equal or less than the red cards 
played.
'''

colorslst = ["Red", "Blue", "Green", "Yellow"]
playcards = []
botcards = []
playerHP = 10
botHP = 10
damagedealt = 0

for x in range(40):
    playcards.append(colorslst[x % 4])
    botcards.append(colorslst[x % 4])

while playerHP > 0 and botHP > 0:
    print("Player 1: " + str(playcards))
    print("Make a move: ")
    move = input()

    movelst = move.split(" ")
    botmove = ""
    if "Red" in movelst:
        if "Green" in movelst:
            comboHit = movelst.count("Red")
            defend = botcards.count("Blue")
            if defend >= comboHit:
                botmove = ("Blue " * comboHit)
                for v in range(comboHit):
                    botcards.remove("Blue")
            else:
                cOunter = botcards.count("Yellow")
                stackable = botcards.count("Green")
                if cOunter >= comboHit:
                    if stackable >= cOunter:
                        botmove = ""
                        for v in range(comboHit):
                            botmove  += "Yellow "
                            if v == cOunter - 1:
                                break
                            else:
                                botmove += "Green "
                        damagedealt = comboHit
                        for v in range(comboHit):
                            botcards.remove("Yellow")
                        for v in range(comboHit):
                            botcards.remove("Green")
                else:
                    botmove = ("Blue " * movelst.count("Blue"))
                    botHP -= (comboHit - movelst.count("Blue"))
                    for v in range(comboHit):
                        botcards.remove("Blue")
        else:
            defend = botcards.count("Blue")
            cOunter = botcards.count("Yellow")
            if defend != 0 and cOunter != 0:
                if defend >= cOunter:
                    botmove = "Blue"
                else:
                    botmove = "Yellow"
            elif defend == 0 and cOunter != 0:
                botmove = "Yellow"
            elif defend != 0 and cOunter == 0:
                botmove = "Blue"
    elif "Blue" in movelst:
        if len(movelst) == damagedealt:
            pass
        else:
            playerHP -= (damagedealt - len(movelst))
            #FIXME
        botmove = "Blue"
