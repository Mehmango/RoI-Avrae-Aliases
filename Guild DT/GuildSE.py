multiline
!embed
<drac2>
args=&ARGS&
title = ":spy: " + name + " dabbles in a little crime :spy:"
desc = "﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌\n\n"

guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
seDict = None
seJson = None

guildInitials = get("guild")
if guildInitials not in guildsDict:
    desc += "**<:kittydotdotdot:770188345187106866> "+name+ " isn't part of a guild** <:kittydotdotdot:770188345187106866>"
elif "secretEntrance" not in guildsDict[guildInitials]:
    desc += "**<:kittydotdotdot:770188345187106866> The " + guildsDict[guildInitials].name + " doesn't have a secret entrance! <:kittydotdotdot:770188345187106866>**"
else:
    seDict = guildsDict[guildInitials].secretEntrance
    level = int(seDict.level)
    loot = int(seDict.loot);
    crime = seDict.crime;
    dc = int(seDict.dc);
    crew = seDict.crew;
    rolls = seDict.rolls;

    if crime == "failure":
        desc += "**The crime was botched** <:kittydead:834292798429724724>\n"
        desc += "Try again next week!"
        
    elif crime == "success":
        desc += "**The plan was a success! Claim your loot at the end of your week!** <:kittyrich:834292404629536768>"

    elif len(args)<1 and crime == "":
        desc += "**__The " + guildsDict[guildInitials].name + " plans a crime!__**\n\n\n"
        desc += "**__Crimes Available:__**\n\n\n";
        desc += "🏃 **Robbery** 🏪\n\n";
        desc += "__Difficulty__: Easy\n"
        desc += "__Crew Needed__: 3\n"
        desc += "__Payout__: Low (200+50d5)\n";
        
        desc += "\n\n*(Run `!GuildSE Plan <crime name>` to start planning a crime`)*";
        
        desc += "\n\n\nRun `!GuildSE Help` if you need help"
    elif len(args)<1 and crime != "":
        desc += "**__The " + guildsDict[guildInitials].name + " plans a " + crime + "!__**\n\n\n"
        desc += "**Current DC: " + dc +"**\n";
        desc += "*(Run `!GuildSE Scout` to help reduce the DC!)*\n\n\n"
        desc += "🕴️ **Crew:** 🕴️\n\n";
        if crime == "robbery":
            desc += "🧠 __Position 1: Leader__ (Wisdom check): ";
            desc += "**Empty**" if crew[0] == "" else "**"+crew[0]+"**";
            desc += "\n\n";
            desc += "💪 __Position 2: Muscle__ (Attack roll): ";
            desc += "**Empty**" if crew[1] == "" else "**"+crew[1]+"**";
            desc += "\n\n";
            desc += "👀 __Position 3: Lookout__ (Perception check): ";
            desc += "**Empty**" if crew[2] == "" else "**"+crew[2]+"**";
            desc += "\n\n*(Run `!GuildSE Crew #` to take up a position!)*"
        
        else:
            desc += "**Whoops! Something's wrong. Please contact a Dragonspeaker! <:kittyscream:834292391212482630>**"
            
        desc += "\n\n\n*Run `!GuildSE Execute` to execute the plan! (Make sure everyone's ready first!)*"
        desc += "\n\n\nRun `!GuildSE Help` if you need help"
    elif args[0].lower() == "help":
        desc += "**Need some help with the garden? <:kittywave:770160454110412800>**\n\n"
        desc += "`!GuildSE`  ➝  Displays the current status of the guild's crime planning :spy:\n\n"
        desc += "`!GuildSE Help`  ➝  Displays this message <:kittywave:770160454110412800>\n\n"
        desc += "`!GuildSE Plan <crime name>`  ➝  Starts planning for a crime! 🗓️\n*(Eg: `!GuildSE Plan robbery`)*\n\n"
        desc += "`!GuildSE Scout`  ➝  Spend one DT and roll an investigation check to scout the area and reduce the DC of the crime! :mag:\n\n"
        desc += "`!GuildSE Crew #`  ➝  Take up a position for the upcoming crime! :chess_pawn:\n*(Eg: `!GuildSE Crew 2`)*\n\n"
        desc += "`!GuildSE Execute`  ➝  Execute the crime :smiling_imp:"

    elif args[0].lower() == "scout":
        if get_cc('DT')==0:
            desc += "**" + name + " does not have the required DT** <:kittydotdotdot:770188345187106866>"
        else:
            if crime == "":
                desc += "**No crime is being planned yet! Select a crime to start planning first.** <:kittydotdotdot:770188345187106866>"
            elif dc <= 0:
                desc += "**You already know everything there is to know. This literally could not be any easier.** <:kittydotdotdot:770188345187106866>"
            else:
                investigationCheck = vroll("2d20kh1+"+(character().skills.investigation.value)) if character().skills.investigation.adv else vroll("1d20+"+(character().skills.investigation.value))
                scoutDC = vroll("2d4+9").total

                desc += "**" + name + " scouts out the scene: (DC "+scoutDC+")**\n\n"
                desc += "**Idnvestigation:** "+investigationCheck.full+"\n\n\n"
                
                if investigationCheck.total>=scoutDC:
                    desc += "**Success** - " + name + " gains valuable information! <:kittywonder:770188525353828353>\n\n\n"
                    dc -= 2 if dc > 0 else 0;
                    seDict.update({"dc": dc})
                else:
                    desc += "**Failure** - " + name + " finds nothing useful <:kittyunhappy:770160130301624361>\n\n\n"
                mod_cc("DT", -1)

                desc += "**Current DC: " + dc + "**";
            desc += "\n\n\n\n**DT Remaining:** "+ cc_str("DT")
            
    elif args[0].lower() == "plan":
        if crime != "":
            desc += "**A crime is already being planned this week!** <:kittydotdotdot:770188345187106866>"
        elif len(args)<2:
            desc += "**Pick a crime to start planning!** *(Eg: `!GuildSE Plan Robbery`)* <:kittydotdotdot:770188345187106866>"
        elif args[1].lower() == "robbery":
            if level<1:
                desc += "**That crime isn't available!** <:kittydotdotdot:770188345187106866>"
            else:
                dc = 18;
                crime = "robbery";
                crew = ["","",""];
                rolls = ["","",""];
                seDict.update(dc=dc, crime=crime, crew=crew, rolls=rolls);
                desc += "**The " + guildsDict[guildInitials].name + " starts planning a robbery!** :spy:\n"
                desc += "*(Run `!GuildSE Scout` to help scout out the target, `!GuildSE Crew #` to join the crew, and `!GuildSE Execute` to execute the plan)*"
    
    elif args[0].lower() == "crew":
        if get_cc('DT')==0:
            desc += "**" + name + " does not have the required DT** <:kittydotdotdot:770188345187106866>"
        elif crime == "":
            desc += "**No crime is being planned yet! Select a crime to start planning first.** <:kittydotdotdot:770188345187106866>"
        elif len(args)<2 or not args[1].isnumeric():
            desc += "**Pick a position to join!** *(Eg: `!GuildSE Crew 2`)* <:kittydotdotdot:770188345187106866>"
        else:
            index = int(args[1]);
            if index<1 or index>len(crew):
                desc += "**That's not a valid position!** <:kittydotdotdot:770188345187106866>"
            elif name in crew:
                desc += "**" + name + " is already part of this week's crew!** <:kittydotdotdot:770188345187106866>"
            elif crew[index-1] != "":
                desc += "**That position is already taken!** <:kittydotdotdot:770188345187106866>";
            else:
                crew[index-1] = name;
                tempRoll = "";
                if crime == "robbery":
                    if index == 1:
                        tempRoll = "2d20kh1+"+(character().skills.wisdom.value) if character().skills.wisdom.adv else "1d20+"+(character().skills.wisdom.value);
                        desc += "**" + name + " takes the roll of the leader!** <:kittysmug:834292430467104768>"
                    elif index == 2:
                        tempRoll = "1d20+"+(int(max(dexterityMod,strengthMod,wisdomMod,charismaMod,intelligenceMod)));
                        desc += "**" + name + " takes the roll of the muscle!** <:kittycool:770160684448088094>"
                    elif index == 3:
                        tempRoll = "2d20kh1+"+(character().skills.perception.value) if character().skills.perception.adv else "1d20+"+(character().skills.perception.value);
                        desc += "**" + name + " takes the roll of the lookout!** <:kittyposh:834292368785014804>"
                
                desc += "\n\n\n"
                desc += "🧠 __Position 1: Leader__ (Wisdom check): ";
                desc += "**Empty**" if crew[0] == "" else "**"+crew[0]+"**";
                desc += "\n\n";
                desc += "💪 __Position 2: Muscle__ (Attack roll): ";
                desc += "**Empty**" if crew[1] == "" else "**"+crew[1]+"**";
                desc += "\n\n";
                desc += "👀 __Position 3: Lookout__ (Perception check): ";
                desc += "**Empty**" if crew[2] == "" else "**"+crew[2]+"**";
                desc += "\n\n*(Run `!GuildSE Crew #` to take up a position!)*"
                
                rolls[index-1] = tempRoll;
                seDict.update(rolls=rolls);
                
                mod_cc("DT", -1)
                desc += "\n\n\n\n**DT Remaining:** "+ cc_str("DT")
    
    elif args[0].lower() == "execute":
        if crime == "":
            desc += "**No crime is being planned yet!** <:kittydotdotdot:770188345187106866>\n";
            desc += "*(Run `!GuildSE Plan <crime name>` to start planning a crime)*"
        else:
            if "" in crew:
                desc += "**Your crew isn't ready yet! <:kittydotdotdot:770188345187106866>**\n"
                desc += "*(Run `!GuildSE Crew #` to take up a position in the crew)*"
            else:
                if crime=="robbery":
                    wisdomCheck = vroll(rolls[0]);
                    attackRoll = vroll(rolls[1]);
                    perceptionCheck = vroll(rolls[2]);
                    wisdomPass = wisdomCheck.total>=dc;
                    attackPass = attackRoll.total>=dc;
                    perceptionPass = perceptionCheck.total>=dc;                    

                    desc += "**The " + guildsDict[guildInitials].name + " conducts a robbery!** :spy:\n\n\n"
                    desc += "***The plan in place, the crew step up to the store and bust open the door!***\n"
                    desc += "***But even with the most intricate plan, things are always bound to go wrong. When it does, it's up to " + crew[0] + " to steer the crew out of trouble! :brain:***\n\n"
                    desc += "**Wisdom: (DC "+dc+")**: " + wisdomCheck.full + "\n";
                    desc += ("*" + crew[0] + " leads the crew with cunning!* <:kittycool:770160684448088094>") if wisdomPass else ("*" + crew[0] + " falters under the pressure!* <:kittyscream:834292391212482630>")
                    desc += "\n\n\n"
                    
                    desc += "***The store is guarded, but " + crew[1] + " steps up to the task! :muscle:***\n\n";
                    desc += "**Attack: (AC "+dc+")**: " + attackRoll.full + "\n";
                    desc += ("*" + crew[1] + " delivers a knockout hit!* <:kittycool:770160684448088094>") if attackPass else ("*" + crew[1] + " misses their mark!* <:kittyscream:834292391212482630>")
                    desc += "\n\n\n"
                    
                    desc += "***Admist all the chaos, " + crew[2] + " needs to keep a lookout for authorities! :eyes:***\n\n";
                    desc += "**Perception: (DC "+dc+")**: " + perceptionCheck.full + "\n";
                    desc += ("*" + crew[2] + " spots the approaching guards and signals the crew to slip away!* <:kittycool:770160684448088094>") if perceptionPass else ("*" + crew[2] + " doesn't spot the guards until it's too late!* <:kittyscream:834292391212482630>")
                    desc += "\n\n\n"
                    
                    if wisdomPass and attackPass and perceptionPass:
                        loot = 200 + int(roll('50d5'));
                        crime = "success";
                        desc += "*Everyone carries their weight, and the crew escapes successfully with bags full of loot!* <:kittyamazed:770160347881275393>\n\n"
                        desc += "**Loot Gained: " + loot + "gp!** 💰\n";
                        desc += "*(Collect your loot at the end of the week by running `!GuildPayout SE`)*";
                    else:
                        crime = "failure";
                        desc += "*The plan goes awry and the robbery fails. You're still able to escape safely, but without any spoils this time.* <:kittyunhappy:770160130301624361>";
                    
                    seDict.update(loot=loot, crime=crime);
                    
    else:
        desc += "**Invalid option!** <:kittydotdotdot:770188345187106866>\n\n"
        desc += "Run `!GuildSE Help` to see a list of valid !GuildSE commands"

guildsJson = dump_json(guildsDict)
desc += "\n\n﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌"
return f""" -title "{title}" -desc "{desc}" -footer "Downtime | GuildSE | RoI" """
</drac2>
!gvar edit {{guildsGvar}} {{guildsJson}}