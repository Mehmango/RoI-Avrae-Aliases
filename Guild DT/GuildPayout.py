multiline
!embed
<drac2>
args = &ARGS&
title = ":coin: Accessing the coffers...... :coin:"
desc = "﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌\n\n"
helpMessage = "**Coffers a little stuck? <:kittywave:770160454110412800>**\n\n"
helpMessage += "`!GuildPayout` or `!GuildPayout Help`  ➝  Displays this message <:kittywave:770160454110412800>\n\n"
helpMessage += "`!GuildPayout All`  ➝  Reap the rewards from all your guild modules at once <:kittygift:834292253803020313>\n\n"
helpMessage += "`!GuildPayout Market`  ➝  Claim the profits from the market 💰\n\n"
helpMessage += "`!GuildPayout Herb`  ➝  Harvest the herbs and claim the potions from the herb garden :herb:\n\n"
helpMessage += "`!GuildPayout Library`  ➝  Collect your spellscrolls after a long week's study and research :scroll:\n\n"
helpMessage += "`!GuildPayout SE`  ➝  Claim your loot from a week of crime :spy:\n\n"
helpMessage += "`!GuildPayout Tavern`  ➝  Redeem free DT points from this week's work :tumbler_glass:\n\n"

validArguments = ["all", "market", "herb", "library", "se", "tavern"];

guildInitials = get("guild")
guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
if guildInitials not in guildsDict:
    desc += "**<:kittydotdotdot:770188345187106866> "+name+ " isn't part of a guild** <:kittydotdotdot:770188345187106866>\n\n"
else:
    title = ":coin: Accessing the " + guildsDict[guildInitials].name + "'s coffers...... :coin:"
    if len(args)<1:
        desc += helpMessage
    elif args[0].lower() == "help":
        desc += helpMessage
    elif args[0].lower() in validArguments:
        if args[0].lower() == "all" or args[0].lower() == "market":
            if "market" not in guildsDict[guildInitials] and args[0].lower() == "market":
                desc += "**The " + guildsDict[guildInitials]['name'] +" does not have a market** <:kittyunhappy:770160130301624361>\n\n"
            elif "market" in guildsDict[guildInitials]:
                marketDict = guildsDict[guildInitials].market
                marketSway = randchoice([0.8, 0.9, 1.0, 1.1, 1.2])
                totalEarnings = marketDict.projectedEarnings
                totalEarnings = int(totalEarnings * marketSway)
                desc += ":convenience_store: __**The " + guildsDict[guildInitials].name + "'s Market Earnings**__ :convenience_store:\n\n"
                if marketSway < 1:
                    desc += "*The market trends weren't very favourable this week. The total earnings are slightly lower than projected* <:kittysweat:770160378201899018>\n\n"
                elif marketSway > 1:
                    desc += "*The market trends were favourable this week. The total earnings are slightly higher than projected* <:kittycelebrate:835505972952432680>\n\n"
                else:
                    desc += "*The market trends were stable this week. The total earnings are exactly as projected* <:kittycomfy:834292211041435688>\n\n"
                desc += "💰 **Total Earnings:** `" + totalEarnings + "gp`"
                desc += "\n\n*(After a player gets their share, it is then multiplied by `proficiencyBonus/2`. This calculation is done separately from the total profits, so nothing extra is taken out)*"
                marketDict.update(invested = 0, salesCounter = 0, supplyRunsCounter = 0, projectedEarnings = 0)
                
                desc += "\n\n\n"

        if args[0].lower() == "all" or args[0].lower() == "herb":
            if "herb" not in guildsDict[guildInitials] and args[0].lower() == "herb":
                desc += "**The " + guildsDict[guildInitials]['name'] +" does not have a herb garden** <:kittyunhappy:770160130301624361>\n\n"
            elif "herb" in guildsDict[guildInitials]:
                herbDict = guildsDict[guildInitials].herb
                herbsStored = int(herbDict.herbsStored)
                herbsInGarden = int(herbDict.herbsInGarden)
                commonPotions = int(herbDict.commonPotions)
                uncommonPotions = int(herbDict.uncommonPotions)
                rarePotions = int(herbDict.rarePotions)
                veryRarePotions = int(herbDict.veryRarePotions)

                desc += ":potted_plant: __**The " + guildsDict[guildInitials].name + "'s Herb Garden Produce**__ :potted_plant:\n\n"
                desc += ":herb: **Herbs** :herb:\n\n"
                desc += "__Herbs harvested:__ `" + herbsInGarden + "`\n"
                desc += "__Herbs in storage:__ `" + herbsStored + "` ➝ `" + (herbsStored+herbsInGarden) + "`\n\n"
                desc += ":test_tube: **Potions** :test_tube:\n\n"
                desc += "__Common:__    `" + commonPotions + "`\n"
                desc += "__Uncomomon:__ `" + uncommonPotions + "`\n"
                desc += "__Rare:__      `" + rarePotions + "`\n"
                desc += "__Very Rare:__ `" + veryRarePotions + "`"

                herbDict.update(herbsStored=herbsStored+herbsInGarden, herbsInGarden=0, commonPotions=0, uncommonPotions=0, rarePotions=0, veryRarePotions=0)

                desc += "\n\n\n"

        if args[0].lower() == "all" or args[0].lower() == "library":
            if "library" not in guildsDict[guildInitials] and args[0].lower() == "library":
                desc += "**The " + guildsDict[guildInitials]['name'] +" does not have a library** <:kittyunhappy:770160130301624361>\n\n"
            elif "library" in guildsDict[guildInitials]:
                libraryDict = guildsDict[guildInitials].library
                spellLevel = libraryDict.spellLevel
                desc += ":books: __**The " + guildsDict[guildInitials].name + "'s Library Research Results**__ :books:\n\n"
                if spellLevel == "":
                    desc += "**There are no spellscrolls to claim from the library this week** <:kittyunhappy:770160130301624361>"
                else:
                    desc += "**The " + guildsDict[guildInitials].name + "'s research yields a level `" + spellLevel + "` spellscroll for everyone!** <:pandawizard:841013412524064808>"
                libraryDict.update(spellLevel="", numbers=[], equation = "", equationWithBlanks = "", solved=False)

                desc += "\n\n\n"
                
        if args[0].lower() == "all" or args[0].lower() == "se":
            if "secretEntrance" not in guildsDict[guildInitials] and args[0].lower() == "se":
                desc += "**The " + guildsDict[guildInitials]['name'] +" does not have a secret entrance** <:kittyunhappy:770160130301624361>\n\n"
            elif "secretEntrance" in guildsDict[guildInitials]:
                seDict = guildsDict[guildInitials].secretEntrance
                loot = int(seDict.loot);
                
                desc += ":spy: __**The " + guildsDict[guildInitials].name + "'s Criminal Rewards**__ :spy:\n\n"
                if loot <= 0:
                    desc += "**Crime didn't pay off this week. Maybe next week <:kittysweat:770160378201899018>**"
                else:
                    desc += "**This Week's Loot: ** `" + loot + "gp` <:kittyrich:834292404629536768>"
                    desc += "\n\n*(After a player gets their share, it is then multiplied by `proficiencyBonus/2`. This calculation is done separately from the total profits, so nothing extra is taken out)*"
                seDict.update(loot=0, crime="", crew=[], rolls=[]);
                
                desc += "\n\n\n"
                
        if args[0].lower() == "all" or args[0].lower() == "tavern":
            if "tavern" not in guildsDict[guildInitials] and args[0].lower() == "tavern":
                desc += "**The " + guildsDict[guildInitials]['name'] +" does not have a tavern** <:kittyunhappy:770160130301624361>\n\n"
            elif "tavern" in guildsDict[guildInitials]:
                tavernDict = guildsDict[guildInitials].tavern
                level = int(tavernDict.level)
                maxFreeDT = (2**(level-1))*10;
                freeDT = min(maxFreeDT, int(tavernDict.freeDT) + int(tavernDict.nextWeekFreeDT));
                
                desc += ":beers: __**The " + guildsDict[guildInitials].name + "'s Tavern Turnouts**__ :beers:\n\n"
                desc += "**Free DT This Week: `" + str(freeDT) + "`**"
                desc += "<:kittymusic:834292311541809192>" if freeDT>0 else "<:kittyunhappy:770160130301624361>";
                tavernDict.update(freeDT=freeDT, nextWeekFreeDT=0)
                
                desc += "\n\n\n"

    else:
        desc += "**Invalid option!** <:kittydotdotdot:770188345187106866>\n\n"
        desc += "Run `!GuildPayout` or `!GuildPayout Help` to see a list of valid !GuildMarket commands\n\n"

desc += "﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌"

guildsJson = dump_json(guildsDict)

return f""" -title "{title}" -desc "{desc}" -footer "Downtime | GuildPayout | RoI" """
</drac2>
!gvar edit {{guildsGvar}} {{guildsJson}}