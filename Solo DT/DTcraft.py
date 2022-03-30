multiline
!embed
<drac2>
args=&ARGS&
title = ":tools: " + name + " crafts an item :tools:"
desc = "﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌\n\n"

guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
workshopDict = {}
workshopJson = None
guildExtraFailures = 0;

guildInitials = get("guild")
hasGuildWorkshop = guildInitials in guildsDict and "workshop" in guildsDict[guildInitials];
if hasGuildWorkshop:
    workshopDict = guildsDict[guildInitials].workshop
    guildExtraFailures = workshopDict.level

currentlyCrafting = get("currentlyCrafting");
magicItemAdept = False;

if get("ArtificerLevel") and int(get("ArtificerLevel")) >= 10:
    magicItemAdept = True
if len(args) > 0 and args[-1] == "MIA":
    magicItemAdept = True;
    args = args[:len(args)-1];

if len(args)<1:
    if not currentlyCrafting:
        desc += "**" + name + " is not currently crafting anything.** \nUse `!DTcraft <item name> <original item cost> [quantity]` to begin crafting an item <:kittydotdotdot:770188345187106866>"
    elif get_cc('DT')==0:
            desc += "**" + name + " does not have the required DT** <:kittydotdotdot:770188345187106866>";
    else:
        craftingDict = load_json(currentlyCrafting);
        itemName = craftingDict.name;
        quantity = int(craftingDict.quantity);
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
        
        if hasGuildWorkshop:
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
            if hasGuildWorkshop:
                previousBonus = workshopDict.crafted[itemName] if itemName in workshopDict.crafted else 0;
                workshopDict.crafted.update({itemName:previousBonus+quantity})
                workshopJson = dump_json(workshopDict);
                desc += "\n\n*The " + guildsDict[guildInitials].name + "'s DC cut to crafting " + itemName + "s: `" + workshopDict.crafted[itemName] + "`* <:kittysmug:834292430467104768>"
        elif failures==maxFailures:
            if quantity == 1:
                desc += "\n\n<:kittyscream:834292391212482630> **The " + itemName + " is ruined!** <:kittyscream:834292391212482630>"; 
            else:
                desc += "\n\n<:kittyscream:834292391212482630> **The " + quantity + "x " + itemName + " are ruined!** <:kittyscream:834292391212482630>"; 
            craftingDone = True;
        
        if craftingDone:
            character().delete_cvar("currentlyCrafting")
        else:
            craftingDict.update(successes=successes, failures=failures, runs=runNumber)
            character().set_cvar("currentlyCrafting", dump_json(craftingDict))
        
        character().mod_cc("DT", -1)
        desc += "\n\n\n\n**DT Remaining:** "+ cc_str("DT")
        
elif currentlyCrafting:
    if load_json(currentlyCrafting).quantity == 1:
        desc += "**" + name + " is currently crafting a(n) " + load_json(currentlyCrafting).name + "**. \nUse `!DTcraft` to continue crafting it. <:kittydotdotdot:770188345187106866>"; 
    else:
        desc += "**" + name + " is currently crafting  " + load_json(currentlyCrafting).quantity + "x " + load_json(currentlyCrafting).name + "**. \nUse `!DTcraft` to continue crafting them. <:kittydotdotdot:770188345187106866>"; 
elif len(args)!=2 and len(args)!=3:
    desc += "**Invalid number of arguments provided.** \nPlease use the format `!DTcraft <item name> <original item cost> [quantity]`. <:kittydotdotdot:770188345187106866>\n*(Eg: `!DTcraft 'Bag of Holding' 4000`)*"
elif not args[1].isnumeric() or args[0].isnumeric() or not (args[2].isnumeric() if len(args)==3 else True):
    desc += "**Invalid argument format.** \nPlease use the format `!DTcraft <item name> <original item cost> [quantity]`. <:kittydotdotdot:770188345187106866>\n*(Eg: `!DTcraft 'Bag of Holding' 4000`)*"
else:
    quantity = 1 if len(args)!=3 else int(args[2]);
    cost = int(args[1])*quantity;
    materialsCost = round(cost/4,2);

    if magicItemAdept:
        materialsCost /= 2;
    
    bags = load_json(bags)
    playerGold=[bags[x][1].get("gp") for x in range(len(bags)) if bags[x][0] == 'Coin Pouch'][0];
    
    if playerGold<materialsCost:
        desc += "**" + name + " does not have the required gold** <:kittydotdotdot:770188345187106866>\n Gold Required: `" + materialsCost + "gp`";
    else:
        itemName = args[0];
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
        character().set_cvar("currentlyCrafting", dump_json(craftingDict))
        
        if quantity == 1:
            desc += ":tools: **" + name + " begins crafting a(n) " + itemName + "!** :tools:"
        else:
            desc += ":tools: **" + name + " begins crafting " + str(quantity) + "x " + itemName + "!** :tools:"
        
        if hasGuildWorkshop:
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
        
desc += "\n\n﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌"

guildsJson = dump_json(guildsDict)

return f""" -title "{title}" -desc "{desc}" -footer "Downtime | DTcraft | RoI" """
</drac2>
!gvar edit {{guildsGvar}} {{guildsJson}}