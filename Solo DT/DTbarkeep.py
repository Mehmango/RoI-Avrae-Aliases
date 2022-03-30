embed
<drac2>
args,n,p=&ARGS&,"\n",proficiencyBonus
desc = ""
guildHasTavern = False
guildTavernBonus = proficiencyBonus
B=0

guildInitials = get("guild")
guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
if guildInitials in guildsDict and "tavern" in guildsDict[guildInitials]:
    guildHasTavern = True
    B+=guildTavernBonus
    desc += "**The " + guildsDict[guildInitials]['name'] + " Tavern Bonus: `" + guildTavernBonus + "`** <:kittysmug:834292430467104768>"

#Skill checks and DCs
B+=proficiencyBonus if "Brewer's Supplies" in get("pTools", "[]") else 0
C1=vroll("2d20kh1+"+(charismaMod+B)) if character().skills.charisma.adv else vroll("1d20+"+(charismaMod+B))
C2=vroll("2d20kh1+"+(character().skills.sleightOfHand.value+B)) if character().skills.sleightOfHand.adv else vroll("1d20+"+(character().skills.sleightOfHand.value+B))
C3=vroll("2d20kh1+"+(character().skills.insight.value+B)) if character().skills.insight.adv else vroll("1d20+"+(character().skills.insight.value+B))
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
    
You talk up the patrons: (DC {DC1})
**Charisma:** {C1.full}  
 
You get fancy with the mixing: (DC {DC2}) 
**Sleight of Hand:** {C2.full}
 
You help them with their troubles: (DC {DC3})
**Insight:** {C3.full}
   
    {"**Success** - everyone enjoyed the service! <:pandahappy:841009993239101450> " + n + "You gain **" + str(T) + "gp**" if S==3 else "Bar had good company today" + n + "You gain **" + str(T) + "gp**" if S==2 else "Only regulars today." + n + "You gain **" + str(T) + "gp**" if S==1 else "The bar was empty, but you find **" + str(T) + "gp.**"}
    {"" if S==0 else n + "**Gold Pieces: **" + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    **DT Remaining:** {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "**<name>** starts work as a Barkeeper!"
-footer "Downtime | Barkeep | RoI"
-thumb <image>
-color <color>