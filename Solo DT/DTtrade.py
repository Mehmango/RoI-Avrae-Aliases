embed
<drac2>
args,n,p=&ARGS&,"\n",proficiencyBonus
desc = ""
guildHasMarket = False
guildMarketBonus = 0.5
guildInitials = get("guild")
guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
if guildInitials in guildsDict and "market" in guildsDict[guildInitials]:
        guildHasMarket = True
        desc += "**The " + guildsDict[guildInitials]['name'] + " Market Bonus: `" + int(guildMarketBonus*100) + "%`** gold recouped on losses <:kittysmug:834292430467104768>"
 

#Skill checks and DCs
C1=vroll("2d20kh1+"+(character().skills.insight.value)) if character().skills.insight.adv else vroll("1d20+"+(character().skills.insight.value))
C2=vroll("2d20kh1+"+(character().skills.persuasion.value)) if character().skills.persuasion.adv else vroll("1d20+"+(character().skills.persuasion.value))
C3=vroll("2d20kh1+"+(character().skills.wisdom.value)) if character().skills.wisdom.adv else vroll("1d20+"+(character().skills.wisdom.value))
DC1, DC2, DC3=roll('2d4+9'), roll('2d4+9'), roll('2d4+9'),

#Checking skills and Money
S=1+ (0 if DC1 > C1.total else 1)+(0 if DC2 > C2.total else 1)+(0 if DC3 > C3.total else 1)
F=roll('1d3')
Fail=1 if F>=S else 0
R=roll('2d6') if S==2 else roll('3d6') if S==3 else roll('4d6') if S==4 else roll('1d6')
FR=roll('2d6') if S==3 else roll('3d6') if S==2 else roll('4d6') if S==1 else 0
T=R*p if Fail==0 else -FR*p*guildMarketBonus

#Coin pouch
a = load_json(bags)
oldGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
[a[x][1].update({"gp":a[x][1].gp+T}) for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
set_cvar("bags",dump_json(a))
newGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]

#downtime check, End Message, and Results
if get_cc('DT')==0 or oldGP<100:
    Msg = f' -desc "{name} does not have the required downtime or required gold"'
else:
    mod_cc('DT', -1) 
    Msg = f""" -desc 
    "
{desc}

You read in on the investment: (DC {DC1})
**Insight:** {C1.full}   

You try to talk them into a deal: (DC {DC2})
 **Persuasion:** {C2.full}
    
You try to read the market: (DC {DC3})
 **Wisdom:** {C3.full}
    
    {"**Success** - everyone is happy with your service! <:pandahappy:841009993239101450> " + n + "You gain **" + str(T) + "gp**" if Fail==0 else "You investments didn't return!. <:pandacry:841012316509175888>  " + n + "You Lose **" + str(T)+ "gp**"}

    {"" if S==0 else n + "**Gold Pieces: **" + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    **DT Remaining:** {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "**<name>** starts work as a Trader!"
-footer "Downtime | Trade | RoI"
-thumb <image>
-color <color>