embed
<drac2>
args,n=&ARGS&,"\n"
desc = ""
guildHasWorkshop = False
guildWorkshopBonus = proficiencyBonus
B=0
guildInitials = get("guild")
guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
if guildInitials in guildsDict and "workshop" in guildsDict[guildInitials]:
        guildHasWorkshop = True
        B+=guildWorkshopBonus
        desc += "**The " + guildsDict[guildInitials]['name'] + " Workshop Bonus: `" + guildWorkshopBonus + "`** <:kittysmug:834292430467104768>"

B+=proficiencyBonus if "Smith's Tools" in get("pTools","[]") else 0 
Q=proficiencyBonus
A=roll('11d2')+1
C1=vroll("2d20kh1+"+(character().skills.investigation.value+character().skills.history.value+B)) if character().skills.investigation.adv or character().skills.history.adv else vroll("1d20+"+(character().skills.investigation.value+character().skills.history.value+B))
C2=vroll("2d20kh1+"+(character().skills.strength.value+B)) if character().skills.strength.adv else vroll("1d20+"+(character().skills.strength.value+B))
C3=vroll("2d20kh1+"+(character().skills.dexterity.value+B)) if character().skills.dexterity.adv else vroll("1d20+"+(character().skills.dexterity.value+B))
S1=vroll("2d20kh1+"+(character().saves.get("con").value+B)) if character().saves.get("con").adv else vroll("1d20+"+(character().saves.get("con").value+B))
DC1=roll('1d10+10')
DC2=roll('1d6+5')
Z=get_cc("Jail") if cc_exists("Jail") else 0

S=(0 if DC1>C1.total else 1) + (0 if DC2>C2.total else 1) + (0 if DC2>C3.total else 1)
F=(1 if S==0 else 0) + (1 if DC2>S1.total else 0)
T=(Q*.5) if S < 1 else ((Q*3)+A)*.5 if S < 3 else (Q*3)+A
inj=2 if F==2 else 1

a = load_json(bags)
oldGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
[a[x][1].update({"gp":a[x][1].gp+T}) for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
set_cvar("bags",dump_json(a))
newGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]

if get_cc('DT')==0:
    Msg = f' -desc "{name} does not have the required downtime."'
else:
    mod_cc('DT', -inj) if get_cc("DT") > inj else mod_cc("Jail", +inj-get_cc("DT")) or set_cc("DT", 0)
    Msg = f""" -desc 
    "
    
    {desc}

    Identifying the materials (DC {DC1})
    **Investigation+History:** {C1.full}

    Maneuvering the items (DC {DC2})
    **Strength:** {C2.full}

    Handling equipment and avoiding the fire (DC {DC2})
    **Dexterity:** {C3.full}

    {"**Success** - The smith is happy with your work! ⚒️" + n + "You gain **" + str(T) + "gp**" if S>0 else "The project didn't turn out."}
    {n + n + "You spilled molten metal (DC " + str(DC2) + ")" + n + "**Constitution Save:** " + str(S1.full) if S==0 else ""}
    {n + n + "You were **burned**, and need a healer. 🔥" + n + "**You Lose 1 DT**" if F==2 else ""}
    {"**Gold Pieces:** " + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    **DT Remaining:** {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "<name> starts their job at the smithy!"
-footer "Downtime | Smith | RoI"
-thumb <image>
-color <color>