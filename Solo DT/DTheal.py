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
        guildHasWorkshop = True
        B+=guildHerbBonus
        desc += "\n\n**" + guildsDict[guildInitials]['name'] + " Herb Station Bonus: `+" + guildHerbBonus + "`** <:kittysmug:834292430467104768>" 

B+=proficiencyBonus if "Herbalism Kit" in get("pTools","[]") else 0
Q=(proficiencyBonus*3)+roll('3d2')+16
C1=vroll("2d20kh1+"+(character().skills.medicine.value+B)) if character().skills.medicine.adv else vroll("1d20+"+(character().skills.medicine.value+B))
C2=vroll("2d20kh1+"+(character().skills.insight.value+B)) if character().skills.insight.adv else vroll("1d20+"+(character().skills.insight.value+B))
C3=vroll("2d20kh1+"+(character().saves.get("con").value+B)) if character().saves.get("con").adv else vroll("1d20+"+(character().saves.get("con").value+B))
DC1,DC2,DC3=roll('2d4+7'),roll('2d4+7'),roll('2d4+7')
Z=get_cc("Jail") if cc_exists("Jail") else 0

S=(0 if DC1 > C1.total else 1)+(0 if DC2 > C2.total else 1)
T=(proficiencyBonus*.5) if S==0 else Q*.5 if S < 2 else Q
inj=2 if S==0 and DC3>C3.total else 1

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

    Divining the source of ailments (DC {DC2})
    **Insight:** {C2.full}
    
    Treating wounds, and curing diseases (DC {DC1})
    **Medicine:** {C1.full}{n + n + "Staying healthy (DC " + str(DC3) + ")" + n + "**Constitution Save:** " + str(C3.full) if S<2 else ""}{n + n + "While working you catch the **Common Cold**" + n + "**You Lose 1 DT for Rest**" if inj==2 else ""}
    
    {"**Success** - you make the world a better place! <:pandahappy:841009993239101450> " + n + "You gain **" + str(T) + "gp**" if S>0 else "Not your best day. <:pandapopcorn:841013412523933776> " + n + "You gain **" + str(T) + "gp**"}
    
    {"**Gold Pieces: **" + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    **DT Remaining:** {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "**<name>** starts their work as a Healer!"
-footer "Downtime | Healer | RoI"
-thumb <image>
-color <color>