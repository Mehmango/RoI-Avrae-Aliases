embed
<drac2>
args,n,p=&ARGS&,"\n",proficiencyBonus
desc = ""
guildHasHerb = False
guildHerbBonus = proficiencyBonus
B=0
guildInitials = get("guild")
guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
if guildInitials in guildsDict and "herb" in guildsDict[guildInitials]:
        guildHasHerb = True
        B+=guildHerbBonus
        desc += "**The " + guildsDict[guildInitials]['name'] + " Herb Garden Bonus: `" + guildHerbBonus + "`** <:kittysmug:834292430467104768>"
 
#Skill checks and DCs
B+=proficiencyBonus if "Herbalism Kit" in get("pTools", "[]") else 0
C1=vroll("2d20kh1+"+(character().skills.perception.value+B)) if character().skills.perception.adv else vroll("1d20+"+(character().skills.perception.value+B))
C2=vroll("2d20kh1+"+(character().skills.nature.value+B)) if character().skills.nature.adv else vroll("1d20+"+(character().skills.nature.value+B))
C3=vroll("2d20kh1+"+(character().skills.wisdom.value+B)) if character().skills.wisdom.adv else vroll("1d20+"+(character().skills.wisdom.value+B))
DC1, DC2, DC3=roll('1d4+6'), roll('1d4+6'), roll('1d4+6')

#Checking skills and Money
S=(0 if DC1>C1.total else 1)+(0 if DC2>C2.total else 1)+(0 if DC3>C3.total else 1)
T=(proficiencyBonus*.5) if S==0 else ((proficiencyBonus*3)+roll('6d2'))*.5 if S < 3 else (proficiencyBonus*3)+roll('6d2')

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

You observe the garden: (DC {DC1})
**Perception:** {C1.full}   

You remember how to treat the plant: (DC {DC2})
 **Nature:** {C2.full}

You attempt to help it grow: (DC {DC3})
**Wisdom:** {C3.full}
    
    {"**Success** - You keep the garden vibrant! <:pandahappy:841009993239101450> " + n + "You gain **" + str(T) + "gp**" if S==3 else "Some of the plants need work" + n + "You gain **" + str(T) + "gp**" if S==2 else "Everything is sickly." + n + "You gain **" + str(T) + "gp**" if S==1 else "You had to cut out the dead ones. You find **" + str(T) + "gp.** <:pandapopcorn:841013412523933776> "}
    {"" if S==0 else n + "**Gold Pieces: **" + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    **DT Remaining:** {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "**<name>** starts work as a gardener!"
-footer "Downtime | Gardener | RoI"
-thumb <image>
-color <color>