embed
<drac2>
args,n,p=&ARGS&,"\n",proficiencyBonus

desc = ""
guildHasLibrary = False
guildLibraryBonus = proficiencyBonus
B=0
guildInitials = get("guild")
guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
if guildInitials in guildsDict and "library" in guildsDict[guildInitials]:
        guildHasLibrary = True
        B+=guildLibraryBonus
        desc += "\n\n**" + guildsDict[guildInitials]['name'] + " Library Bonus: `+" + guildLibraryBonus + "`** <:kittysmug:834292430467104768>" 

#Skill checks and DCs
C1=vroll("2d20kh1+"+(character().skills.investigation.value+B)) if character().skills.investigation.adv else vroll("1d20+"+(character().skills.investigation.value+B))
C2=vroll("2d20kh1+"+(character().skills.intelligence.value+B)) if character().skills.intelligence.adv else vroll("1d20+"+(character().skills.intelligence.value+B))
C3=vroll("1d20+"+(int(max(get_raw().skills.arcana, get_raw().skills.religion, get_raw().skills.history, get_raw().skills.nature))+B))
DC1, DC2, DC3=roll('1d4+6'), roll('1d4+6'), roll('1d4+6'),

#Checking skills
S=(0 if DC1 > C1.total else 1)+(0 if DC2 > C2.total else 1)+(0 if DC3 > C3.total else 1)
T=(proficiencyBonus*.5) if S==0 else ((proficiencyBonus*3)+roll('6d2')-1)*.5 if S < 3 else (proficiencyBonus*3)+roll('6d2')-1

#Coin pouch
a = load_json(bags)
oldGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
[a[x][1].update({"gp":a[x][1].gp+T}) for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
set_cvar("bags",dump_json(a))
newGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]

#downtime check, End Message, and Results
if get_cc('DT')==0:
    Msg = f' -desc "{name} does not have the required downtime."'
else:
    mod_cc('DT', -1) 
    Msg = f""" -desc 
    "
{desc}

You look for what your told to: (DC {DC3})
**Knowledge:** {C3.full}   

You read what youve found: (DC {DC1})
    **Investigation:** {C1.full}
    
    You try to retain the knowledge: (DC {DC2})
    **Intelligence:** {C2.full}
    
    {"**Success** - You provide a scroll for documentation! <:pandahappy:841009993239101450> " + n + "You gain **" + str(T) + "gp**" if S==3 else "You found some of what was needed." + n + "You gain **" + str(T) + "gp**" if S==2 else "You struggle through the day." + n+ "You gain **" + str(T) + "gp**" if S==1 else "The info you found was useless. <:pandapopcorn:841013412523933776> "}
    {"" if S==0 else n + "**Gold Pieces: **" + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    **DT Remaining:** {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "**<name>** starts work as a Researcher!"
-footer "Downtime | Teaching | RoI"
-thumb <image>
-color <color>