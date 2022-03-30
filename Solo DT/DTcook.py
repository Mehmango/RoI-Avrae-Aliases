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
 

#get skills and DCs
B+=proficiencyBonus if "Cook's Utensils" in get("pTools","[]") else 0
C1=vroll("2d20kh1+"+(character().saves.get("wis").value+B)) if character().saves.get("wis").adv else vroll("1d20+"+(character().saves.get("wis").value+B))
C2=vroll("2d20kh1+"+(character().skills.insight.value+B)) if character().skills.insight.adv else vroll("1d20+"+(character().skills.insight.value+B))
S1=vroll("2d20kh1+"+(character().saves.get("con").value+B)) if character().saves.get("con").adv else vroll("1d20+"+(character().saves.get("con").value+B))
DC1,DC2,DC3=roll('2d4+5'),roll('2d4+5'),roll('2d4+5')
Z=get_cc("Jail") if cc_exists("Jail") else 0

S=2 if C1.total>=DC1 and (C2.total>=DC2 or S1.total>=DC3) else 1 if (C1.total>=DC1 or C2.total>=DC2 or S1.total>=DC3) else 0
T=ceil(p*.5) if S==0 else ceil(((p*3)+roll('11d2'))*.5) if S < 2 else ceil((p*3)+roll('11d2'))
inj=2 if DC2>C2.total and DC3>S1.total else 1

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

    You prepare a meal (DC {DC1})
    **Wisdom:** {C1.full}

    You adjust with taste (DC {DC2})
    **Insight:** {C2.full}{n+n+"Is it made properly? (DC " + str(DC3) + ")" + n + "**Constitution Save:** " + str(S1.full) if DC2>C2.total else ""}{n + n + "It wasn't proper **Food Poisoned** 😟 " + n + "**You Lose 1 DT for Rest**" if (DC2>C2.total and DC3>S1.total) else ""}

    {"Success - It tastes wonderful! 😃 " + n + "You gain **" + str(T) + "gp.**" if S==2 else "The food was ok."  + n + "You gain **" + str(T) + "gp.**" if S==1 else "It was not enjoyable.**" + str(T) + "gp** 🙄 "}
    {"" if S==0 else n + "Gold Pieces: " + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    DT Remaining: {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "<name> starts their work as a Chef!"
-footer "Downtime | Chef | RoI"
-thumb <image>
-color <color>