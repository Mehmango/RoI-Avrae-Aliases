embed
<drac2>
args,n,p,eM = &ARGS&,"\n","Progress",f' -desc "Command not entered correctly.\nPlease type `!DTlearn List` for help.\n\n(If you are already learning a skill, just use `!DTLearn`, the alias will remember the skill you are learning!)"'

skillsDict=load_json(get_gvar("db791f09-cf9d-48ae-a5be-5ecb17fd1142"))

M1=f""" -desc 
    " 
    {get_gvar("0d54f63e-98eb-45c0-9373-b418911ee1d3")}
    "
    """

desc = ""
c = ""
if get_cc('DT')==0:
    Msg = f' -desc "{name} does not have the required downtime."'
else:
    guildModules ={
        "Herb Garden": {
            "key" : "herb",
            "exists" : False,
            "bonus" : 1,
            "learns" : ["Alchemist's Supplies", "Poisoner's Kit", "Herbalism Kit"]
        },
        "Library": {
            "key" : "library",
            "exists" : False,
            "bonus" : 1,
            "learns" : ["Calligrapher's Supplies", "Cartographer's Tools"]+skillsDict['LSL']+skillsDict['LEL']+skillsDict['LI']
        },
        "Workshop": {
            "key" : "workshop",
            "exists" : False,
            "bonus" : 1,
            "learns" : ["Carpenter's Tools", "Cobbler's Tools", "Glassblower's Tools", "Jeweler's Tools", "Leatherworker's Tools", "Mason's Tools", "Tinker's Tools", "Weaver's Tools", 
    "Woodcarver's Tools", "Painter's Supplies"]
        },
        "Tavern": {
            "key" : "tavern",
            "exists" : False,
            "bonus" : 1,
            "learns" : ["Dice Set", "Playing Card Set", "Brewer's Supplies", "Cook's Utensils"]
        },
    }

    S=0
    guildTotalBonus = 0
    guildInitials = get("guild")
    skill = get("currentlyLearning")
    if len(args)>0:
        if args[0] in skillsDict.LO:
            return M1
        elif not get("currentlyLearning"):
            skill = "&1&"
        else:
            return eM

    guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
    guildsDict = load_json(get_gvar(guildsGvar))
    if guildInitials in guildsDict:
        [guildModules[module].update({"exists": True}) for module in guildModules if guildModules[module]['key'] in guildsDict[guildInitials]]
        guildTotalBonus += sum([int(guildModules[module]['bonus']) for module in guildModules if guildModules[module]['exists'] and skill in guildModules[module]['learns']])
        if guildTotalBonus != 0:
            desc += "".join(["\n\n**" + guildsDict[guildInitials]['name'] + " " + module + " Bonus: `+" + guildModules[module]['bonus'] + "` Progress Point(s)** <:kittysmug:834292430467104768>" for module in guildModules if guildModules[module]['exists'] and skill in guildModules[module]['learns']])

    S += guildTotalBonus
    C1=vroll("1d20+"+max(intelligenceMod, charismaMod))
    S1=vroll("2d20kh1+"+(character().saves.get("int").value)) if character().saves.get("int").adv else vroll("1d20+"+(character().saves.get("int").value))
    DC1,DC2=roll('2d4+3'),roll('2d4+3')
    S+=(0 if DC1 > C1.total else 1)+(0 if DC2 > S1.total else 1)

    if skill in skillsDict.LI:
        LP=30
    elif skill in skillsDict.LT:
        LP=40 
    elif skill in skillsDict.LSL:
        LP=36
    elif skill in skillsDict.LEL:
        LP=50
    elif not get("currentlyLearning"):
        return eM
        
    if cc_exists(p):
        LP=get_cc_max(p)
    else:
        create_cc_nx(p,0,LP,"none")
        set_cc(p,0)
        character().set_cvar("currentlyLearning", skill)

    if LP==30:
        c="an Instrument"
    elif LP==40:
        c="a Tool"
    elif LP==36:
        c="a Language"
    elif LP==50:
        c="an Exotic Language"
    else:
        c=""

    mod_cc('DT', -1) 
    mod_cc(p, +S)
    C=1 if get_cc(p)==LP else 2    
    Msg = f""" -desc 
    "
    {desc}

    You study and practice hard! (DC {DC1})
    Check: {C1.full}

    You remember what you have learned! (DC {DC2})
    Save: {S1.full}
    
    {"**Overwhelming Success!** - You absorbed knowledge like a sponge and gain " + str(S) + " progress points. <:kittywonder:770188525353828353>" if S==3 else "**Success!** - You studied hard and gain " + str(S) + " progress points." if S==2 else "You found it hard to study, and only gain " + str(S) + " progress point." if S==1 else "You found it too hard this time, but dont give up!"}
    
    DT Remaining: {cc_str("DT")}
    {p}: {cc_str(p)}{n + n + "Congratulations you have learned " + str(c) + "! <:kittywonder:770188525353828353>" if C==1 else ""}
    "
    """
    if C==1:
        delete_cc(p)
        character().delete_cvar("currentlyLearning")
    else:
        mod_cc(p, +0)
return Msg
</drac2>
-title "<name> begins learning {{c}}!"
-footer "Downtime | Learn | RoI"
-thumb <image>
-color <color>