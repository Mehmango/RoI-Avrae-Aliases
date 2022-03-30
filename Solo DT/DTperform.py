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

C1=vroll("2d20kh1+"+(character().skills.insight.value+B)) if character().skills.insight.adv else vroll("1d20+"+(character().skills.insight.value+B))
C2=vroll("2d20kh1+"+(character().skills.performance.value+B)) if character().skills.performance.adv else vroll("1d20+"+(character().skills.performance.value+B))
C3=vroll("2d20kh1+"+(character().skills.persuasion.value+B)) if character().skills.persuasion.adv else vroll("1d20+"+(character().skills.persuasion.value+B))
DC1,DC2,DC3=roll('2d4+7'),roll('2d4+7'),roll('2d4+7')

S=1 + (0 if DC1 > C1.total else 1) + (0 if DC2 > C2.total else 1) + (0 if DC3 > C3.total else 1)
R=roll('6d2') + 3*p
T=R if S==4 else ceil(R*.75) if S==3 else ceil(R*0.5) if S==2 else ceil(p*0.5)


a = load_json(bags)
oldGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
[a[x][1].update({"gp":a[x][1].gp+T}) for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
set_cvar("bags",dump_json(a))
newGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]

if get_cc('DT')==0:
    Msg = f' -desc "{name} does not have the required downtime."'
else:
    mod_cc('DT', -1) 
    Msg = f""" -desc 
    "
{desc}

    Reading the audience (DC {DC1})
    **Insight:** {C1.full}
    
    Putting on a performance (DC {DC2})
    **Performance:** {C2.full}

    Asking For You Fair Share (DC {DC3})
    **Persuasion:** {C3.full}
    
    {"**Success** - the crowd loves your performance! <:pandahappy:841009993239101450>" + n + "You gain **" + str(T) + "gp**" if S==4 else "Made it through the day." + n + "You gain **" + str(T) + "gp**" if (S==3 or S==2) else "Nobody was impressed. <:pandapopcorn:841013412523933776>"}
    {"" if S==1 else n + "**Gold Pieces: **" + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    **DT Remaining:** {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "**<name>** attempts to put on a show!"
-footer "Downtime | Perform | RoI"
-thumb <image>
-color <color>