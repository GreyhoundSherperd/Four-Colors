'''
Each player gets 20 cards of 4 colors, each color has a different objective:
- Red: Attack, 1 red card dealt 1 damage if unblocked or countered, play in a zigzag pattern with green cards to multi-combo,
for example "Red Green Red".
- Blue: Block, 1 blue card defends 1 damage, can multi-block without green cards.
- Green: Bridge, Green cards were played in a zigzag pattern with red or yellow cards to multi-combo or multi-counter.
- Yellow: Counter, A yellow card is a hybrid of red and blue, a yellow card blocks 1 damage and deal 1 damage, can multi-counter without green cards.
Can only play if a red card was played last turn, and can only play equal or less than the red cards 
played.
'''

from random import randint
from math import floor

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

    # Defend logic
    movelst = move.split(" ")
    botmove = ""
    if "Red" in movelst:
        if "Green" in movelst:
            comboHit = movelst.count("Red")
            defend = botcards.count("Blue")

            # Defendable?
            if defend >= comboHit:
                botmove = ("Blue " * comboHit)
                for v in range(comboHit):
                    botcards.remove("Blue")
            
            # Counterable?
            else:
                cOunter = botcards.count("Yellow")
                stackable = botcards.count("Green")
                if cOunter >= comboHit:
                    # Stackable?
                    if stackable >= cOunter or stackable == (cOunter - 1):
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
                        for v in range(comboHit - 1):
                            botcards.remove("Green")
                # Back to defend
                else:
                    if defend != 0 and cOunter != 0:
                        if cOunter > defend:
                            botmove = "Yellow" * cOunter
                            for v in range(cOunter):
                                botcards.remove("Yellow")
                            botHP -= (comboHit - cOunter)
                            damagedealt = cOunter
                        else:
                            botmove = "Blue" * defend
                            for v in range(defend):
                                botcards.remove("Blue")
                            botHP -= (comboHit - defend)
        
        # Single attack logic
        else:
            defend = botcards.count("Blue")
            cOunter = botcards.count("Yellow")
            if defend != 0 and cOunter != 0:
                if defend >= cOunter:
                    botmove = "Blue"
                else:
                    botmove = "Yellow"
                    damagedealt = 1
            elif defend == 0 and cOunter != 0:
                botmove = "Yellow"
                damagedealt = 1
            elif defend != 0 and cOunter == 0:
                botmove = "Blue"
            else:
                attack = botcards.count("Red")
                if attack == 0:
                    # GAME OVER
                    pass
                else:
                    botmove = "Red"
                    damagedealt = 1
                    botHP -= 1
    elif "Blue" in movelst:
        # Dealing damage
        if len(movelst) == 1 and damagedealt == 0:
            pass
        elif damagedealt != 0:
            if len(movelst) == damagedealt:
                damagedealt = 0
            else:
                playerHP -= (damagedealt - len(movelst))
                damagedealt = 0

        # Attacking Logic
        attack = botcards.count("Red")
        chance = randint(1, 3)
        if chance == 1:
            lipchance = randint(2, 3)
            if floor((attack / lipchance)) == 0:
                if attack == 0:
                    defend = movelst.count("Blue")
                    if defend == 0:
                        # GAME OVER
                        pass
                    else:
                        botmove = "Blue"
                else:
                    botmove == "Red" * attack
                    for v in range(attack):
                        botcards.remove("Red")
                    damagedealt = attack
            else:
                botmove = "Red" * floor((attack / lipchance))
                for v in range(floor(attack / lipchance)):
                    botcards.remove("Red")
                damagedealt = floor(attack / lipchance)
        elif chance == 2:
            lipchance = randint(3, 4)
            if floor((attack / lipchance)) == 0:
                if attack == 0:
                    defend = botcards.count("Blue")
                    if defend == 0:
                        # GAME OVER
                        pass
                    else:
                        botmove = "Blue"
                else:
                    botmove == "Red" * attack
                    for v in range(attack):
                        botcards.remove("Red")
                    damagedealt = attack
            else:
                botmove = "Red" * floor((attack / lipchance))
                for v in range(floor(attack / lipchance)):
                    botcards.remove("Red")
                damagedealt = floor(attack / lipchance)
        elif chance == 3:
            defend = botcards.count("Blue")
            if defend == 0:
                if attack != 0:
                    botmove = "Red" * attack
                    for v in range(attack):
                        botcards.remove("Red")
                    damagedealt = attack
                else:
                    # GAME OVER
                    pass
            else:
                botmove = "Blue"
                botcards.remove("Blue")
    elif "Yellow" in movelst:
        if (len(movelst)+1)/2 == damagedealt:
            damagedealt = 0
        else:
            playerHP -= damagedealt - (len(movelst)+1)/2
            damagedealt = 0
        if "Green" in movelst:
            defend = botcards.count("Blue")
            cOunter = botcards.count("Yellow")
            if defend >= cOunter:
                if defend >= (len(movelst)+1)/2:
                    botmove = "Blue" * int(((len(movelst)+1)/2))
                else:
                    botmove = "Blue" * defend
            else:
                if cOunter >= (len(movelst)+1)/2:
                    botmove = "Yellow" * int(((len(movelst)+1)/2))
                    damagedealt = (len(movelst)+1)/2
                else:
                    botmove = "Yellow" * cOunter
                    damagedealt = cOunter
        else:
            defend = botcards.count("Blue")
            cOunter = botcards.count("Yellow")
            if defend != 0 and cOunter != 0:
                if defend >= cOunter:
                    botmove = "Blue"
                else:
                    botmove = "Yellow"
                    damagedealt = 1
            elif defend != 0 and cOunter == 0:
                botmove = "Blue"
            elif defend == 0 and cOunter != 0:
                botmove = "Yellow"
                damagedealt = 1

    print(botmove)
    
