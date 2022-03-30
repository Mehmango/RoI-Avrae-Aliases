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
 

#get skills and DCs
C1=vroll("2d20kh1+"+(character().skills.nature.value+B)) if character().skills.nature.adv else vroll("1d20+"+(character().skills.nature.value+B))
C2=vroll("2d20kh1+"+(character().skills.animalHandling.value+B)) if character().skills.animalHandling.adv else vroll("1d20+"+(character().skills.animalHandling.value+B))
C3=vroll("2d20kh1+"+(character().saves.get("con").value+B)) if character().saves.get("con").adv else vroll("1d20+"+(character().saves.get("con").value+B))
DC1,DC2,DC3=roll('2d4+5'),roll('2d4+5'),roll('2d4+5')
Z=get_cc("Jail") if cc_exists("Jail") else 0

#Checks
S=2 if C1.total>=DC1 and C2.total>=DC2 else 1 if (C1.total>=DC1 or C2.total>=DC2) else 0
T=(proficiencyBonus*.5) if S==0 else ((proficiencyBonus*3)+roll('11d2')+1)*.5 if S < 2 else (proficiencyBonus*3)+roll('11d2')+1
inj=2 if DC3>C3.total else 1

#Coin Transfer
a = load_json(bags)
oldGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
[a[x][1].update({"gp":a[x][1].gp+T}) for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
set_cvar("bags",dump_json(a))
newGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]

#results and DT
if get_cc('DT')==0:
    Msg = f' -desc "{name} does not have the required downtime."'
else:
    mod_cc('DT', -inj) if get_cc("DT") > inj else mod_cc("Jail", +inj-get_cc("DT")) or set_cc("DT", 0)
    Msg = f""" -desc 
    "
{desc}

   You remember what crops to grow (DC {DC1})
    **Nature:** {C1.full}

   You lead the plow: (DC {DC2})
    **Animal Handling:** {C2.full}

    You beat the heat!: (DC {DC3})
    **Constitution Save: ** {C3.full}{n+n+"You forgot to drink water **Heat Exhaustion** 😟 " + n + "**You Lose 1 DT for Rest**" if (DC3>C3.total) else ""}

    {"Success - The crops are seeded! 😃 " + n + "You gain **" + str(T) + "gp**" if S==2 else "Some aren't going to make it"  + n + "You gain **" + str(T) + "gp**" if S==1 else "The crops wouldn't take. 🙄 Eek out **" + str(T) + "gp** for your efforts."}
    {"" if S==0 else n + "Gold Pieces: " + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    DT Remaining: {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "<name> starts their work as a Farmer!"
-footer "Downtime | Farming | RoI"
-thumb <image>
-color <color>