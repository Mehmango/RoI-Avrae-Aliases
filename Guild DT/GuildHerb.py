multiline
!embed
<drac2>
args=&ARGS&
title = ":herb: " + name + " tends to the guild's herb garden :herb:"
desc = "﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌\n\n"

guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
herbDict = None
herbJson = None

guildInitials = get("guild")
if guildInitials not in guildsDict:
    desc += "**<:kittydotdotdot:770188345187106866> "+name+ " isn't part of a guild** <:kittydotdotdot:770188345187106866>"
elif "herb" not in guildsDict[guildInitials]:
    desc += "**<:kittydotdotdot:770188345187106866> The " + guildsDict[guildInitials].name + " doesn't have a herb garden! <:kittydotdotdot:770188345187106866>**"
else:
    herbDict = guildsDict[guildInitials].herb
    level = int(herbDict.level)
    herbsStored = int(herbDict.herbsStored)
    herbsInGarden = int(herbDict.herbsInGarden)
    maxHerbsInGarden = level*5 + 5
    commonPotions = int(herbDict.commonPotions)
    uncommonPotions = int(herbDict.uncommonPotions)
    rarePotions = int(herbDict.rarePotions)
    veryRarePotions = int(herbDict.veryRarePotions)
    currentPotionRarity = herbDict.currentPotionRarity
    currentPotionTarget = herbDict.currentPotionTarget
    potionTargetFloor = int(currentPotionTarget[0])
    potionTargetCeil = int(currentPotionTarget[1])
    currentPotionSaturation = int(herbDict.currentPotionSaturation)
    maxPotionRange = 30

    if len(args)<1:
        desc += "**__The " + guildsDict[guildInitials].name + "'s Herb Garden is ready for planting!__**\n\n\n"
        desc += "║ **Total Herbs In Storage:** `" + herbsStored + "` "
        desc += ":herb:" if herbsStored else "<:kittythink:834292466571411507>"
        desc += " ║\n\n\n"
        desc += ":test_tube: **Potions Made** :test_tube:\n\n"
        desc += "__Common__: `" + commonPotions + "`\n"
        desc += "__Uncommon__: `" + uncommonPotions + "`\n"
        desc += "__Rare__: `" + rarePotions + "`\n"
        desc += "__Very Rare__: `" + veryRarePotions + "`\n"

        desc += "\n\n:potted_plant: **The Garden** :potted_plant:\n\n"
        plotsLeftover = maxHerbsInGarden - herbsInGarden
        desc += "".join([":seedling:" for i in range(0,herbsInGarden)])
        desc += "".join(["︵" for i in range(0,plotsLeftover)])
        desc += "\n\n*(Run `!GuildHerb Garden` to plant a herb!)*"

        desc += "\n\n\n:scientist: **Current Brewing Status** :scientist:\n\n"
        if potionTargetCeil == 0:
            desc += "There are currently no potions being brewed <:kittysleep:834292416269778944>\n\n"
            desc += "*Run `!GuildHerb Brew <rarity>` to start brewing a potion! (Uses up a stored herb)*"
        else:
            desc += "**Rarity:** `" + currentPotionRarity.title() + "`\n\n"
            desc += "**Current Saturation:** `" + currentPotionSaturation + "` / " + maxPotionRange + "\n"
            desc += "".join(["▰" if i < currentPotionSaturation else "▱" for i in range(0,potionTargetFloor)])
            desc += "|"
            desc += "".join(["▱" for i in range(potionTargetFloor,potionTargetCeil+1)])
            desc += "|"
            desc += "".join(["▱" for i in range(potionTargetCeil+1,maxPotionRange)])
            desc += "\n\n*(Run `!GuildHerb Brew` or `!GuildHerb Brew #` to help brew the potion!)*"

        desc += "\n\n\nRun `!GuildHerb Help` if you need help"
    elif args[0].lower() == "help":
        desc += "**Need some help with the garden? <:kittywave:770160454110412800>**\n\n"
        desc += "`!GuildHerb`  ➝  Displays the current status of the guild's herb garden :potted_plant:\n\n"
        desc += "`!GuildHerb Help`  ➝  Displays this message <:kittywave:770160454110412800>\n\n"
        desc += "`!GuildHerb Garden`  ➝  Spend one DT and roll a nature check to plant and grow a herb! :seedling:\n\n"
        desc += "`!GuildHerb Brew <rarity>`  ➝  Begin brewing a potion of the specified rarity :test_tube:\n*(Eg: `!GuildHerb Brew Uncommon`)*\n\n"
        desc += "`!GuildHerb Brew` or `!GuildHerb Brew #`  ➝  Roll a d10 to add the rolled amount to the current potion's saturation. Add or subtract the specified # to the roll (up to your Arcana bonus) :test_tube:\n*(Eg: `!GuildHerb Brew +4`, `!GuildHerb Brew -2`)*"

    elif args[0].lower() == "garden":
        if get_cc('DT')==0:
            desc += "**" + name + " does not have the required DT** <:kittydotdotdot:770188345187106866>"
        else:
            if herbsInGarden >= maxHerbsInGarden:
                desc += "**Oop! It seems like the garden is already at maximum capacity!** <:kittyidea:770188542441685002>\n\n"
            else:
                natureCheck = vroll("2d20kh1+"+(character().skills.nature.value)) if character().skills.nature.adv else vroll("1d20+"+(character().skills.nature.value))
                dc = vroll("2d4+6").total

                desc += "**" + name + " attempts to plant a herb: (DC "+dc+")**\n\n"
                desc += "**Nature:** "+natureCheck.full+"\n\n\n"
                
                if natureCheck.total>=dc:
                    desc += "**Success** - The herb looks strong and healthy! <:kittywonder:770188525353828353>\n\n"
                    herbsInGarden += 1
                    herbDict.update({"herbsInGarden": herbsInGarden})
                else:
                    desc += "**Failure** - The herb withers away <:kittyscream:834292391212482630>\n\n"
                mod_cc("DT", -1)

            desc += "\n:potted_plant: **The Garden** :potted_plant:\n\n"
            plotsLeftover = maxHerbsInGarden - herbsInGarden
            desc += "".join([":seedling:" for i in range(0,herbsInGarden)])
            desc += "".join(["︵" for i in range(0,plotsLeftover)])
            desc += "\n\n\n\n**DT Remaining:** "+ cc_str("DT")
            
    elif args[0].lower() == "brew":
        title = ":test_tube: " + name + " brews a potion in the herb garden :test_tube:"
        if potionTargetCeil == 0: # No potion currently brewing
            if herbsStored < 1:
                desc += "**There aren't enough herbs in storage to brew a potion** <:kittyunhappy:770160130301624361>\n"
                desc += "*(Run `!GuildHerb Garden` to grow herbs for future use!)*"
            elif len(args)<2 or (len(args)>1 and args[1].lower() not in ["common", "uncommon", "rare", "very rare"]):
                desc += "**Specify the rarity of the potion you'd like to start brewing :test_tube:**\n"
                desc += "*(Eg: `!GuildHerb Brew Uncommon`)*"
            else:
                currentPotionRarity = args[1].lower()
                herbDict.update({"currentPotionRarity":currentPotionRarity})
                potionRange = 0
                if currentPotionRarity == "common":
                    potionRange = 10
                elif currentPotionRarity == "uncommon":
                    potionRange = 6
                elif currentPotionRarity == "rare":
                    potionRange = 2
                elif currentPotionRarity == "very rare":
                    potionRange = 1
                potionRange = int(potionRange*(1 + 0.5 * (level-1)))
                if potionRange > maxPotionRange:
                    potionRange = maxPotionRange
                
                potionTargetCeil = randint(potionRange, 30, 1)
                potionTargetFloor = potionTargetCeil - potionRange + 1
                herbDict.update({"currentPotionTarget":[potionTargetFloor,potionTargetCeil]})
                herbsStored -= 1
                herbDict.update({"herbsStored": herbsStored})

                desc += "**The " + guildsDict[guildInitials].name + " starts brewing a " + currentPotionRarity + " potion! **:scientist:\n\n\n"
                desc += "**Current Saturation:** `" + currentPotionSaturation + "` / " + maxPotionRange + "\n"
                desc += "".join(["▱" for i in range(0,potionTargetFloor)])
                desc += "|"
                desc += "".join(["▱" for i in range(potionTargetFloor,potionTargetCeil+1)])
                desc += "|"
                desc += "".join(["▱" for i in range(potionTargetCeil,maxPotionRange)])
                desc += "\n\n**Try to get the potion's saturation within the target range 🎯**"
                desc += "\n\n*(Run `!GuildHerb Brew` or `!GuildHerb Brew #` to help brew the potion!)*"
        else:
            if len(args)>1 and not (args[1].isnumeric() or (args[1][0] in ["+", "-"] and args[1][1:].isnumeric())):
                desc += "**Incorrect number format. Please use either `+#`, `-#` or `#`, where # is an integer up to your arcana bonus** <:kittydotdotdot:770188345187106866>\n"
                desc += "*(Eg: `!GuildHerb Brew +2`, `!GuildHerb Brew -3`, `!GuildHerb Brew 5`)*\n"
            else:
                mod = 0
                if len(args)>1:
                    mod = int(args[1])
                    if abs(mod) > character().skills.arcana.value:
                        mod = character().skills.arcana.value if mod > 0 else -character().skills.arcana.value
                saturationRoll = vroll("1d10+"+mod)
                currentPotionSaturation += saturationRoll.total
                if currentPotionSaturation < 0:
                    currentPotionSaturation = 0
                desc += "**" + name + " helps brew the potion!**\n\n\n"
                desc += "**<:kittygrimace:834292284006334475> Adding saturation...... : **" + saturationRoll.full + "\n\n"
                desc += "".join(["▰" if i < currentPotionSaturation else "▱" for i in range(0,potionTargetFloor)])
                desc += "|"
                desc += "".join(["▰" if i < currentPotionSaturation else "▱" for i in range(potionTargetFloor,potionTargetCeil+1)])
                desc += "|"
                desc += "".join(["▰" if i < currentPotionSaturation else "▱" for i in range(potionTargetCeil+1,maxPotionRange)])
                desc += "\n\n"
                if currentPotionSaturation < potionTargetFloor:
                    desc += "***Hmm, seems like we need a little more... <:kittythink:834292466571411507>***"
                else:
                    if currentPotionSaturation in range(potionTargetFloor, potionTargetCeil+1):
                        desc += "***Hurray! The potion is done! <:kittyamazed:770160347881275393>***"
                        if currentPotionRarity == "common":
                            commonPotions += 1
                            herbDict.update({"commonPotions":commonPotions})
                            desc += "\n\n:test_tube: __Common potions:__ `" + commonPotions + "`"
                        elif currentPotionRarity == "uncommon":
                            uncommonPotions += 1
                            herbDict.update({"uncommonPotions":uncommonPotions})
                            desc += "\n\n:test_tube: __Uncommon potions:__ `" + uncommonPotions + "`"
                        elif currentPotionRarity == "rare":
                            rarePotions += 1
                            herbDict.update({"rarePotions":rarePotions})
                            desc += "\n\n:test_tube: __Rare potions:__ `" + rarePotions + "`"
                        elif currentPotionRarity == "very rare":
                            veryRarePotions += 1
                            herbDict.update({"veryRarePotions":veryRarePotions})
                            desc += "\n\n:test_tube: __Very Rare potions:__ `" + veryRarePotions + "`"
                    else:
                        desc += "***Oh no! The potion is ruined! <:kittyscream:834292391212482630>***"
                    
                    currentPotionRarity = None
                    currentPotionTarget = [0,0]
                    currentPotionSaturation = 0
                    herbDict.update({"currentPotionRarity":currentPotionRarity})
                    herbDict.update({"currentPotionTarget":currentPotionTarget})

                herbDict.update({"currentPotionSaturation":currentPotionSaturation})
    
    else:
        desc += "**Invalid option!** <:kittydotdotdot:770188345187106866>\n\n"
        desc += "Run `!GuildHerb Help` to see a list of valid !GuildHerb commands"

guildsJson = dump_json(guildsDict)
desc += "\n\n﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌"
return f""" -title "{title}" -desc "{desc}" -footer "Downtime | GuildHerb | RoI" """
</drac2>
!gvar edit {{guildsGvar}} {{guildsJson}}