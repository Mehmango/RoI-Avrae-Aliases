multiline
!embed
<drac2>
args = &ARGS&
title = "📚 " + name + " studies in the guild library 📚"
desc = "﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌\n\n"

guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
libraryDict = None
libraryJson = None
unknowns = ["a","b","c","d","e","f","g","h",'i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','y','z']

guildInitials = get("guild")
if guildInitials not in guildsDict:
    desc += "**<:kittydotdotdot:770188345187106866> " + name + " isn't part of a guild** <:kittydotdotdot:770188345187106866>"
elif "library" not in guildsDict[guildInitials]:
    desc += "**<:kittydotdotdot:770188345187106866> The " + guildsDict[
        guildInitials].name + " doesn't have a library! <:kittydotdotdot:770188345187106866>**"
else:
    libraryDict = guildsDict[guildInitials].library
    level = int(libraryDict.level)
    solved = libraryDict.solved
    numbers = libraryDict.numbers
    equation = libraryDict.equation
    equationWithBlanks = libraryDict.equationWithBlanks
    spellLevel = libraryDict.spellLevel
    maxSpellLevel = 1 + 2*level

    if len(args) < 1:
        desc += "**__The " + guildsDict[guildInitials].name + "'s Library is bursting with knowledge!__**\n\n\n"
        if solved:
            desc += "║<:pandawizard:841013412524064808> **Researching Level " + spellLevel + " Spell: Complete! <:pandawizard:841013412524064808>** ║\n\n\n"
            desc += "*Take the rest of the week off! <:kittycelebrate:835505972952432680>*\n"
            desc += "*(Claim your spell scroll at the end of the week)* :scroll:"
        elif spellLevel == "":
            desc += "║ **No spell is currently being researched** <:kittysleep:834292416269778944>║\n\n\n"
            desc += "*Run `!GuildLibrary Research <spell level>` to start researching a spell!* :scroll:"
        else:
            desc += "║<:kittythink:834292466571411507> **Researching Level " + spellLevel + " Spell: In Progress <:kittythink:834292466571411507>** ║\n\n\n"
            desc += "**The equation:**\n"
            desc += "*`" + equationWithBlanks + "`*"
            desc += "\n\n*(Run `GuildLibrary Research` to spend a DT to reveal a clue for the equation)*"
            desc += "\n\n*(Run `!GuildLibrary Solve <equation>` to spend a DT to try and solve the equation. Enter the correct full equation in quotes \n(Eg: `!GuildLibrary Solve '(24 x 12) + (42 x 82) + (14 x 24) + (41 x 91) + (43 x 42) = 9605'`))*"
        desc += "\n\n\nRun `!GuildLibrary Help` if you need help"
    elif args[0].lower() == "help":
        desc += "**Need some help with your research? <:kittywave:770160454110412800>**\n\n"
        desc += "`!GuildLibrary`  ➝  Displays the current status of the guild's library :potted_plant:\n\n"
        desc += "`!GuildLibrary Help`  ➝  Displays this message <:kittywave:770160454110412800>\n\n"
        desc += "`!GuildLibrary Research #` or `!GuildLibrary Research`  ➝  Begin research on a spell with level #, or spend a DT to help with a research in progress\n*(Eg: `!GuildLibrary 2`)* :book:\n\n"
        desc += "`!GuildLibrary Solve <equation>`  ➝  Spend a DT to try to solve the equation. Enter the correct full equation in quotes to finish your research!\n*(Eg: `!GuildLibrary Solve '(24 x 12) + (42 x 82) + (14 x 24) + (41 x 91) + (43 x 42) = 9605'`)* :scroll:"

    elif args[0].lower() == "research":
        if solved:
            desc += "**The equation has already been solved!** <:kittysmug:834292430467104768>\n\n"
            desc += "*Take the rest of the week off and claim your spell scroll at the end of the week!* <:kittysleep:834292416269778944>"
        elif len(args)>1:
            if spellLevel:
                desc += "**A spell is already being researched! Run `!GuildLibrary` to check its progress, or `!GuildLibrary research` to help with the research!** 📚"
            elif not args[1].lower().isnumeric() or int(args[1]) < 0:
                desc += "**Incorrect number format. Please use `!GuildLibrary #`, where # is the level of the spell you want to research** <:kittydotdotdot:770188345187106866>\n"
                desc += "*(Eg: `!GuildLibrary 2`)*"
            elif int(args[1]) > maxSpellLevel:
                desc += "**Your library isn't equipped to research a spell of that level yet!** <:kittyunhappy:770160130301624361>\n\n"
                desc += "*Upgrade your library to research more powerful spells!*"
            else:
                spellLevel = int(args[1])
                randNums = [randint(2, 100) for i in range(3**spellLevel)]
                numbers = [randint(2, 100) for i in range(3**spellLevel)]
                equation = "+".join(randNums[i]+"*"+numbers[i] for i in range(len(numbers)))
                result = roll(equation)
                equation = " + ".join(["(" + randNums[i] + " x " + numbers[i] + ")" for i in range(len(randNums))]) + " = " + result
                equationWithBlanks = " + ".join(["(" + randNums[i] + " x " + unknowns[i] + ")" for i in range(len(randNums))]) + " = " + result
                libraryDict.update(spellLevel=spellLevel, numbers=numbers,equation=equation,equationWithBlanks=equationWithBlanks)
                desc += "**The " + guildsDict[guildInitials].name + " start to research a level " + spellLevel + " spell!** <:pandawizard:841013412524064808>\n\n"
                desc += "**The equation:**\n"
                desc += "*`"+equationWithBlanks+"`*\n\n"
                desc += "**Good Luck!** <:kittyposh:834292368785014804>"
        elif spellLevel == "":
            desc += "**No spell is currently being researched** <:kittydotdotdot:770188345187106866>\n"
            desc += "*Run `!GuildLibrary Research #` to Begin research on a spell with level #! :scroll:*"
        elif len(numbers)<1:
            desc += "**There is nothing left to discover** <:kittydead:834292798429724724>\n\n"
            desc += "**The equation:**\n"
            desc += "*`" + equationWithBlanks + "`*\n\n"
        elif get_cc('DT') == 0:
            desc += "**" + name + " does not have the required DT** <:kittydotdotdot:770188345187106866>"
        else:
            intCheck = vroll("2d20kh1+" + (character().skills.intelligence.value)) if character().skills.intelligence.adv else vroll("1d20+" + (character().skills.intelligence.value))
            dc = vroll("2d4+6"+"-"+(level-1)*2).total

            desc += "**" + name + " does research on the spell: (DC " + dc + ")**\n\n"
            desc += "**Intelligence:** " + intCheck.full + "\n\n\n"

            if intCheck.total >= dc:
                num1, num2 = randint(1,10), randint(1,10)
                unknownIndex1, unknownIndex2 = randint(0,len(numbers)), randint(0,len(numbers))
                while unknownIndex2 == unknownIndex1:
                    unknownIndex2 = randint(0,len(numbers))
                reveal = num1 + unknowns[unknownIndex1] + " + " + num2 + unknowns[unknownIndex2] + " = " + (num1*int(numbers[unknownIndex1])+num2*int(numbers[unknownIndex2])) 
                desc += "**Success** - "+name+"'s research reveals this equation:\n "
                desc += "**`"+ reveal +"`**\n\n"
            else:
                desc += "**Failure** - "+name+" couldn't find anything useful <:kittyunhappy:770160130301624361>\n\n"
            mod_cc("DT", -1)
            desc += "**The equation:**\n"
            desc += "*`" + equationWithBlanks + "`*"
            desc += "\n\n\n\n**DT Remaining:** " + cc_str("DT")

    elif args[0].lower() == "solve":
        if solved:
            desc += "**The equation has already been solved!** <:kittysmug:834292430467104768>\n\n"
            desc += "*Take the rest of the week off and claim your spell scroll at the end of the week!* <:kittysleep:834292416269778944>"
        elif get_cc('DT') == 0:
            desc += "**" + name + " does not have the required DT** <:kittydotdotdot:770188345187106866>"
        elif len(args)<2:
            desc += "**Please enter the whole solved equation as an argument** <:kittydotdotdot:770188345187106866>\n"
            desc += "*(Eg: `!GuildLibrary Solve '(24 x 12) + (42 x 82) + (14 x 24) + (41 x 91) + (43 x 42) = 9605'`)*\n\n"
            desc += "**The spaces are important!!!**"
        else:
            desc += "**" + name + " attempts to solve the equation!** <:kittythink:834292466571411507>\n\n"
            desc += "**" + name + "'s answer:**\n"
            desc += args[1] + "\n\n\n"
            if args[1] == equation:
                desc += "**It's correct! The equation is solved!** <:pandawizard:841013412524064808>\n"
                desc += "Now take a break while the scroll is being scribed <:kittysleep:834292416269778944>"
                solved = True
                libraryDict.update({"solved":solved})
            else:
                desc += "**It's wrong!** <:kittyscream:834292391212482630>\n\n"
                desc += "*Run `!GuildLibrary Research` to search for some clues and try again!* <:pandawizard:841013412524064808>\n\n"
                desc += "**The equation:**\n"
                desc += "*`" + equationWithBlanks + "`*"
            mod_cc("DT", -1)
            desc += "\n\n\n\n**DT Remaining:** " + cc_str("DT")
    else:
        desc += "**Invalid option!** <:kittydotdotdot:770188345187106866>\n\n"
        desc += "Run `!GuildLibrary Help` to see a list of valid !GuildLibrary commands"

guildsJson = dump_json(guildsDict)
desc += "\n\n﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌"
return f""" -title "{title}" -desc "{desc}" -footer "Downtime | GuildLibrary | RoI" """
</drac2>
!gvar edit {{guildsGvar}} {{guildsJson}}