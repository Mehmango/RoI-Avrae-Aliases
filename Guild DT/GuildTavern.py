multiline
!embed
<drac2>
args=&ARGS&
title = ":beers: " + name + " visits the guild tavern :beers:"
desc = "﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌\n\n"

guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
tavernDict = None
tavernJson = None

guildInitials = get("guild")
if guildInitials not in guildsDict:
    desc += "**<:kittydotdotdot:770188345187106866> "+name+ " isn't part of a guild** <:kittydotdotdot:770188345187106866>"
elif "tavern" not in guildsDict[guildInitials]:
    desc += "**<:kittydotdotdot:770188345187106866> The " + guildsDict[guildInitials].name + " doesn't have a tavern! <:kittydotdotdot:770188345187106866>**"
else:
    tavernDict = guildsDict[guildInitials].tavern
    level = int(tavernDict.level)
    freeDT = int(tavernDict.freeDT);
    nextWeekFreeDT = int(tavernDict.nextWeekFreeDT);
    maxFreeDT = (2**(level-1))*10;
    pricePerDT = (6-level)*proficiencyBonus + 17

    if len(args)<1:
        desc += "**__The " + guildsDict[guildInitials].name + "'s Tavern is open for business!__**"
        desc += "\n\n\n"
        desc += "<:kittymusic:834292311541809192>" if freeDT>0 else "<:kittyunhappy:770160130301624361>"; 
        desc += " **Free DT Points: `" + freeDT + "`** "
        desc += "<:kittymusic:834292311541809192>" if freeDT>0 else "<:kittyunhappy:770160130301624361>";
        desc += "\n\n"
        for i in range(min(40,freeDT)):
            desc += ":tumbler_glass:"
        if freeDT<1:
            desc += ":cricket:";
        desc += "\n\n*(Run `!GuildTavern Rest` or `!GuildTavern Rest #` to claim # free DT points)*"
        
        desc += "\n\n\n"
        desc += ":tropical_drink: **Free DT Points Next Week: `" + str(nextWeekFreeDT) + " / " + str(maxFreeDT) + "`** :tropical_drink:"
        desc += "\n\n*(Run `!GuildTavern Serve` to spend a DT to generate more free DT points for next week!)*"

        desc += "\n\n\n**:cocktail: Price of Extra DT Points: `(" + str(6-level) + " x proficiency bonus) + 17`gp** :cocktail:"
        desc += "\n\n*(Run `!GuildTavern Patron` or `!GuildTavern Patron #` to buy # DT points!)*"

        desc += "\n\n\nRun `!GuildTavern Help` if you need help"
    elif args[0].lower() == "help":
        desc += "**Need some help in the tavern? <:kittywave:770160454110412800>**\n\n"
        desc += "`!GuildTavern`  ➝  Displays the current status of the guild's tavern :beers:\n\n"
        desc += "`!GuildTavern Help`  ➝  Displays this message <:kittywave:770160454110412800>\n\n"
        desc += "`!GuildTavern Rest` or `!GuildTavern Rest #`  ➝  Rest up and claim # free DT points from the guild tavern :tumbler_glass:\n*(Eg: `!GuildTavern Rest 3`)*\n\n"
        desc += "`!GuildTavern Serve`  ➝  Spend one DT and work in the tavern to generate more free DT points next week :cook: :dancer:\n\n"
        desc += "`!GuildTavern Patron` or `!GuildTavern Patron #`  ➝  Spend gold to gain # DT points :cocktail:\n*(Eg: `!GuildTavern Patron 4`)*"

    elif args[0].lower() == "rest":
        if freeDT<1:
            desc += "**The " + guildsDict[guildInitials].name + "'s tavern doesn't have any more free DT points to claim ** <:kittydotdotdot:770188345187106866>"
        else:
            DTToClaim = 1;
            if len(args)>1 and int(args[1])>1:
                DTToClaim = min(int(args[1]),freeDT);
            
            freeDT -= DTToClaim;
            tavernDict.update(freeDT=freeDT);
            set_cc("DT", get_cc("DT")+DTToClaim);
            desc += "**" + name + " rests up and claims " + str(DTToClaim) + " free DT points!** <:kittymusic:834292311541809192>"
            
            desc += "\n\n\n**" + name + "'s DT points:** "+ cc_str("DT")
            
            desc += "\n\n\n";
            desc += "<:kittymusic:834292311541809192>" if freeDT>0 else "<:kittyunhappy:770160130301624361>"; 
            desc += " **Free DT Points Left: `" + freeDT + "`** "
            desc += "<:kittymusic:834292311541809192>" if freeDT>0 else "<:kittyunhappy:770160130301624361>";
            desc += "\n\n"
            for i in range(min(40,freeDT)):
                desc += ":tumbler_glass:"
            if freeDT<1:
                desc += ":cricket:";
        
    elif args[0].lower() == "patron":
        DTToClaim = 1;
        if len(args)>1 and int(args[1])>1:
            DTToClaim = int(args[1]);
        bags = load_json(bags)
        playerGold=[bags[x][1].get("gp") for x in range(len(bags)) if bags[x][0] == 'Coin Pouch'][0];
        
        if playerGold<pricePerDT*DTToClaim:
            desc += "**" + name + " doesn't have enough gold to buy that many DT points!** <:kittydotdotdot:770188345187106866>"
        else:
            [bags[x][1].update({"gp":bags[x][1].gp-pricePerDT*DTToClaim}) for x in range(len(bags)) if bags[x][0] == 'Coin Pouch'][0]
            set_cvar("bags",dump_json(bags))
            set_cc("DT", get_cc("DT")+DTToClaim);
        
            desc += "**" + name + " pays `" + str(pricePerDT*DTToClaim) + "`gp for some R&R and gets " + str(DTToClaim) + " DT points!** :cocktail:"

            desc += "\n\n\n**" + name + "'s DT points:** "+ cc_str("DT")
            desc += "\n\n**Gold Pieces: **" + str(playerGold) + "gp -> " + str(playerGold-pricePerDT*DTToClaim) + "gp"; 
            
    elif args[0].lower() == "serve":
        if get_cc('DT')==0:
            desc += "**" + name + " does not have the required DT** <:kittydotdotdot:770188345187106866>"
        else:
            if nextWeekFreeDT >= maxFreeDT:
                desc += "**Oop! It seems like the tavern already has enough help!** <:kittyidea:770188542441685002>\n\n"
            else:
                dc = vroll("2d4+6").total
                if character().skills.survival.value == max(character().skills.survival.value,character().skills.charisma.value,character().skills.performance.value):
                    survivalCheck = vroll("2d20kh1+"+(character().skills.survival.value)) if character().skills.survival.adv else vroll("1d20+"+(character().skills.survival.value))
                    desc += "**" + name + " helps out in the kitchen: (DC "+dc+")**\n\n"
                    desc += "**Survival:** "+survivalCheck.full+"\n\n\n"
                    if survivalCheck.total>=dc:
                            desc += "**Success** - The food tastes great! <:kittywonder:770188525353828353>\n\n"
                            nextWeekFreeDT += 2
                    else:
                        desc += "**Failure** - The food taste pretty bland <:kittyunhappy:770160130301624361>\n\n"
                elif character().skills.charisma.value == max(character().skills.survival.value,character().skills.charisma.value,character().skills.performance.value):
                    charismaCheck = vroll("2d20kh1+"+(character().skills.charisma.value)) if character().skills.charisma.adv else vroll("1d20+"+(character().skills.charisma.value))
                    desc += "**" + name + " helps out as a bartender and server: (DC "+dc+")**\n\n"
                    desc += "**Charisma:** "+charismaCheck.full+"\n\n\n"
                    if charismaCheck.total>=dc:
                            desc += "**Success** - The patrons are pleased with the service! <:kittywonder:770188525353828353>\n\n"
                            nextWeekFreeDT += 2
                    else:
                        desc += "**Failure** - Service was... mediocre at best <:kittynotlike:770189258366910475>\n\n"
                else:
                    performanceCheck = vroll("2d20kh1+"+(character().skills.performance.value)) if character().skills.performance.adv else vroll("1d20+"+(character().skills.performance.value))
                    desc += "**" + name + " entertains the patrons: (DC "+dc+")**\n\n"
                    desc += "**Performance:** "+performanceCheck.full+"\n\n\n"
                    if performanceCheck.total>=dc:
                            desc += "**Success** - Everyone cheers loudly! <:kittywonder:770188525353828353>\n\n"
                            nextWeekFreeDT += 2
                    else:
                        desc += "**Failure** - You walk awkwardly off the stage <:kittysweat:770160378201899018>\n\n"
                tavernDict.update(nextWeekFreeDT=nextWeekFreeDT);
                mod_cc("DT", -1)
            
            desc += "\n\n**Free DT Points Next Week: `" + str(nextWeekFreeDT) + " / " + str(maxFreeDT) + "`** :tumbler_glass:"
            
            desc += "\n\n\n\n**DT Remaining:** "+ cc_str("DT")
    
    else:
        desc += "**Invalid option!** <:kittydotdotdot:770188345187106866>\n\n"
        desc += "Run `!GuildTavern Help` to see a list of valid !GuildTavern commands"

guildsJson = dump_json(guildsDict)
desc += "\n\n﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌"
return f""" -title "{title}" -desc "{desc}" -footer "Downtime | GuildTavern | RoI" """
</drac2>
!gvar edit {{guildsGvar}} {{guildsJson}}