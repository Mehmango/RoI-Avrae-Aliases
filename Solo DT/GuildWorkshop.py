multiline
!embed
<drac2>
args=&ARGS&
title = ":tools: " + name + " checks out the guild workshop :tools:"
desc = "﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌\n\n"

guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
workshopDict = None
workshopJson = None

guildInitials = get("guild")
magicItemAdept = False;

if get("ArtificerLevel") and int(get("ArtificerLevel")) >= 10:
    magicItemAdept = True
if len(args) > 0 and args[-1] == "MIA":
    magicItemAdept = True;
    args = args[:len(args)-1];

if guildInitials not in guildsDict:
    desc += "**<:kittydotdotdot:770188345187106866> "+name+ " isn't part of a guild** <:kittydotdotdot:770188345187106866>"
elif "workshop" not in guildsDict[guildInitials]:
    desc += "**<:kittydotdotdot:770188345187106866> The " + guildsDict[guildInitials].name + " doesn't have a workshop! <:kittydotdotdot:770188345187106866>**"
else:
    workshopDict = guildsDict[guildInitials].workshop
    guildExtraFailures = workshopDict.level;
    if len(args)<1:
        if workshopDict.currentlyCrafting == "":
            desc += ":cricket: **Currently Crafting:** *Nothing*  :cricket:"
            desc += "\n\n*(Run `!GuildWorkshop Craft <item name> <'original item cost> [quantity]` to start crafting an item in the guild workshop with your guildmates!)*";
        else:
            craftingDict = workshopDict.currentlyCrafting;
            itemName = craftingDict.name;
            quantity = craftingDict.quantity;
            successesNeeded = int(craftingDict.successesNeeded);
            successes = int(craftingDict.successes);
            failures = int(craftingDict.failures);
            runNumber = int(craftingDict.runs) + 1;
            craftingDone = False;
            maxFailures = 4+guildExtraFailures;
            if quantity == 1:
                desc += ":tools: **Currently Crafting:** *" + itemName + "*  :tools:"
            else:
                desc += ":tools: **Currently Crafting:** *" + quantity + "x " + itemName + "*  :tools:"
                
            desc += "\n\n**Progress:** " + successes + "/" + successesNeeded;
            desc += "\n\n"
            for success in range(round((successes/successesNeeded)*min(30,successesNeeded))):
                desc += "▰";
            for nonSuccess in range(round(((successesNeeded-successes)/successesNeeded)*min(30,successesNeeded))):
                desc += "▱";
            desc += "\n\n**Mistakes:** ";
            for failure in range(failures):
                desc += " :broken_heart: ";
            for nonFailure in range(maxFailures-failures):
                desc += " :heart: ";
                
            desc += "\n\n**Next Check: **";
            if workshopDict.currentlyCrafting.runs%3==0:
                desc += "__*Dexterity*__"
            elif workshopDict.currentlyCrafting.runs%3==1:
                desc += "__*Intelligence*__"
            else:
                desc += "__*Wisdom*__"
            desc += "\n\n*(Run `!GuildWorkshop Craft` to continue crafting the " + workshopDict.currentlyCrafting.name + " in the guild workshop with your guildmates!)*";
        desc += "\n\n\n**Items Crafted by Guild Members: `" + len(workshopDict.crafted) + "`**"
        desc += "\n\n*(Run `!GuildWorkshop List` to see all the list of items crafted by guild members and their bonuses)*"
        
    elif args[0].lower() == "help":
        desc += "**Need some help in the workshop? <:kittywave:770160454110412800>**\n\n"
        desc += "`!GuildWorkshop`  ➝  Displays the current status of the guild's workshop :tools:\n\n"
        desc += "`!GuildWorkshop Help`  ➝  Displays this message <:kittywave:770160454110412800>\n\n"
        desc += "`!GuildWorkshop List`  ➝  Lists all the items that guild members have crafted and their bonuses :gem:\n\n"
        desc += "`!GuildWorkshop Craft`  ➝  Start or continue crafting an item in the guild workshop :hammer:\n*(Eg: `!GuildWorkshop Craft 'Bag of Holding' 4000 3`, `!GuildWorkshop Craft`)*"

    elif args[0].lower() == "list":
        desc += ":hammer_pick: **Items Crafted in the Workshop:** :hammer_pick:\n"
        for item, bonus in workshopDict.crafted.items():
            if item != "level":
                desc += "\n\n:gem: **" + item + "**";
                desc += "\n     Times Crafted/DC Cut: `" + bonus + "`";
                
    elif args[0].lower() == "craft":
        if workshopDict.currentlyCrafting == "":
            if len(args)<=1:
                desc += "**The " + guildsDict[guildInitials].name + " is not currently crafting anything.** \nUse `!GuildWorkshop Craft <item name> <'original item cost> [quantity]` to begin crafting an item <:kittydotdotdot:770188345187106866>"
            elif len(args)!=3 and len(args)!=4:
                desc += "**Invalid number of arguments provided.** \nPlease use the format `!GuildWorkshop Craft <item name> <'original item cost> [quantity]`. <:kittydotdotdot:770188345187106866>\n*(Eg: `!GuildWorkshop Craft 'Bag of Holding' 4000 3`)*"
            elif not args[2].isnumeric() or args[1].isnumeric() or not (args[3].isnumeric() if len(args)==4 else True):
                desc += "**Invalid argument format.** \nPlease use the format `!GuildWorkshop Craft <item name> <'original item cost> [quantity]`. <:kittydotdotdot:770188345187106866>\n*(Eg: `!GuildWorkshop Craft 'Bag of Holding' 4000 3`)*"
            else:
                quantity = 1 if len(args)!=4 else int(args[3]);
                cost = int(args[2])*quantity;
                materialsCost = round(cost/4,2);

                if magicItemAdept:
                    materialsCost /= 2;
                
                bags = load_json(bags)
                playerGold=[bags[x][1].get("gp") for x in range(len(bags)) if bags[x][0] == 'Coin Pouch'][0];
                
                if playerGold<materialsCost:
                    desc += "**" + name + " does not have the required gold** <:kittydotdotdot:770188345187106866>\n Gold Required: `" + materialsCost + "gp`";
                else:
                    itemName = args[1];
                    successes = 0;
                    failures = 0;
                    successesNeeded = max(1, round(float(cost)/160));

                    if magicItemAdept:
                        successesNeeded = max(1,round(successesNeeded/4))

                    maxFailures = 4+guildExtraFailures;
                    guildDCCut = 0
                    
                    craftingDict = {
                        "name":itemName,
                        "quantity":quantity,
                        "successesNeeded": successesNeeded,
                        "successes":successes,
                        "failures":failures,
                        "runs":0
                    }
                    workshopDict.update(currentlyCrafting = craftingDict)
                    
                    if quantity == 1:
                        desc += ":tools: **" + name + " begins crafting a(n) " + itemName + "!** :tools:"
                    else:
                        desc += ":tools: **" + name + " begins crafting " + str(quantity) + "x " + itemName + "!** :tools:"
                    
                    if itemName in workshopDict.crafted:
                        guildDCCut = int(workshopDict.crafted[itemName])
                    desc += "\n\n**The " + guildsDict[guildInitials]['name'] + " Workshop Bonus: "
                    desc += "DC `-" + guildDCCut + "`, " if guildDCCut>0 else ""
                    desc += "Max Failures `+" + guildExtraFailures + "`** <:kittysmug:834292430467104768>"

                    if magicItemAdept:
                        desc += "\n\n**<:pandawizard:841013412524064808> " + name + " is a Magic Item Adept (Cost/2, Time/4) <:pandawizard:841013412524064808>**"
                    
                    desc += "\n\n**Materials Cost: `" + materialsCost + "gp`**"
                    [bags[x][1].update({"gp":bags[x][1].gp-materialsCost}) for x in range(len(bags)) if bags[x][0] == 'Coin Pouch'][0]
                    character().set_cvar("bags",dump_json(bags))
                    desc += "\n\n**Gold Pieces: **" + str(playerGold) + "gp -> " + str(playerGold-materialsCost) + "gp"; 
                    
                    desc += "\n\n**Progress:** " + successes + "/" + successesNeeded;
                    desc += "\n\n"
                    for success in range(round((successes/successesNeeded)*min(30,successesNeeded))):
                        desc += "▰";
                    for nonSuccess in range(round(((successesNeeded-successes)/successesNeeded)*min(30,successesNeeded))):
                        desc += "▱";
                    desc += "\n\n**Mistakes:** ";
                    for failure in range(failures):
                        desc += " :broken_heart: ";
                    for nonFailure in range(maxFailures-failures):
                        desc += " :heart: ";
                    
                    desc += "\n\n**Next Check:** __*Dexterity*__";
                    
        else:
            if len(args)>1:
                if workshopDict.currentlyCrafting.quantity == 1:
                    desc += "**The " + guildsDict[guildInitials].name + " is currently crafting a(n) " + workshopDict.currentlyCrafting.name + "**. \nUse `!GuildWorkshop Craft` to continue crafting it. <:kittydotdotdot:770188345187106866>"
                else:
                    desc += "**The " + guildsDict[guildInitials].name + " is currently crafting " + workshopDict.currentlyCrafting.quantity + "x " + workshopDict.currentlyCrafting.name + "**. \nUse `!GuildWorkshop Craft` to continue crafting them. <:kittydotdotdot:770188345187106866>"
            elif get_cc('DT')==0:
                desc += "**" + name + " does not have the required DT** <:kittydotdotdot:770188345187106866>";
            else:
                craftingDict = workshopDict.currentlyCrafting;
                itemName = craftingDict.name;
                quantity = craftingDict.quantity;
                successesNeeded = int(craftingDict.successesNeeded);
                successes = int(craftingDict.successes);
                failures = int(craftingDict.failures);
                runNumber = int(craftingDict.runs) + 1;
                craftingDone = False;
                maxFailures = 4+guildExtraFailures;
                guildDCCut = 0
                
                if quantity == 1:
                    title = ":tools: " + name + " crafts a(n) " + itemName + " :tools:"
                else:
                    title = ":tools: " + name + " crafts " + quantity + "x " + itemName + " :tools:"
                
                if itemName in workshopDict.crafted:
                    guildDCCut = int(workshopDict.crafted[itemName])
                desc += "**The " + guildsDict[guildInitials]['name'] + " Workshop Bonus: "
                desc += "DC `-" + guildDCCut + "`, " if guildDCCut>0 else ""
                desc += "Max Failures `+" + guildExtraFailures + "` ** <:kittysmug:834292430467104768>"
                
                dc = max(0, vroll("2d4+6").total - guildDCCut)
                check = 0;
                skill = ""
                
                if runNumber%3==1:
                    check = vroll("2d20kh1+"+(character().skills.dexterity.value)) if character().skills.dexterity.adv else vroll("1d20+"+(character().skills.dexterity.value))
                    skill = "Dexterity";
                elif runNumber%3==2:
                    check = vroll("2d20kh1+"+(character().skills.intelligence.value)) if character().skills.intelligence.adv else vroll("1d20+"+(character().skills.intelligence.value))
                    skill = "Intelligence"
                else:
                    check = vroll("2d20kh1+"+(character().skills.wisdom.value)) if character().skills.wisdom.adv else vroll("1d20+"+(character().skills.wisdom.value))
                    skill = "Wisdom"
                
                desc += "\n\n**" + name + " continues crafting a(n) " + itemName + ": (DC "+dc+")**\n\n"
                desc += "**" + skill + ":** "+check.full+"\n\n\n"

                if check.total>=dc:
                    desc += "**Success** - You gain one progress point <:kittywonder:770188525353828353>\n\n"
                    successes += 1;
                else:
                    desc += "**Failure** - You mess up a step <:kittysweat:770160378201899018>\n\n"
                    failures += 1;
                
                desc += "﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏"
                desc += "\n\n**Progress:** " + successes + "/" + successesNeeded;
                desc += "\n\n"
                for success in range(round((successes/successesNeeded)*min(30,successesNeeded))):
                    desc += "▰";
                for nonSuccess in range(round(((successesNeeded-successes)/successesNeeded)*min(30,successesNeeded))):
                    desc += "▱";
                desc += "\n\n**Mistakes:** ";
                for failure in range(failures):
                    desc += " :broken_heart: ";
                for nonFailure in range(maxFailures-failures):
                    desc += " :heart: ";
                
                if successes==successesNeeded:
                    if quantity == 1:
                        desc += "\n\n<:kittycelebrate:835505972952432680> **Hooray! The " + itemName + " is finished!** <:kittycelebrate:835505972952432680>";
                    else:
                        desc += "\n\n<:kittycelebrate:835505972952432680> **Hooray! The " + quantity + "x " + itemName + " are finished!** <:kittycelebrate:835505972952432680>";
                    craftingDone = True;
                    previousBonus = workshopDict.crafted[itemName] if itemName in workshopDict.crafted else 0;
                    workshopDict.crafted.update({itemName:previousBonus+quantity})
                    desc += "\n\n*The " + guildsDict[guildInitials].name + "'s DC cut to crafting " + itemName + "s: `" + workshopDict.crafted[itemName] + "`* <:kittysmug:834292430467104768>"
                elif failures==maxFailures:
                    if quantity == 1:
                        desc += "\n\n<:kittyscream:834292391212482630> **The " + itemName + " is ruined!** <:kittyscream:834292391212482630>"; 
                    else:
                        desc += "\n\n<:kittyscream:834292391212482630> **The " + quantity + "x " + itemName + " are ruined!** <:kittyscream:834292391212482630>";  
                        craftingDone = True;
                
                if craftingDone:
                    workshopDict.update(currentlyCrafting = "")
                else:
                    craftingDict.update(successes=successes, failures=failures, runs=runNumber)
                    workshopDict.update(currentlyCrafting = craftingDict)
                    
                    desc += "\n\n**Next Check: **";
                    if workshopDict.currentlyCrafting.runs%3==0:
                        desc += "__*Dexterity*__"
                    elif workshopDict.currentlyCrafting.runs%3==1:
                        desc += "__*Intelligence*__"
                    else:
                        desc += "__*Wisdom*__"
                
                character().mod_cc("DT", -1)
                desc += "\n\n\n\n**DT Remaining:** "+ cc_str("DT") 
                
guildsJson = dump_json(guildsDict)
desc += "\n\n﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌"
return f""" -title "{title}" -desc "{desc}" -footer "Downtime | GuildWorkshop | RoI" """
</drac2>
!gvar edit {{guildsGvar}} {{guildsJson}}