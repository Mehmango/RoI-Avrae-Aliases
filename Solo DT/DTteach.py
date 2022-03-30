embed
<drac2>
args,n,p=&ARGS&,"\n",proficiencyBonus

#Skill checks and DCs
C1=vroll("2d20kh1+"+(character().skills.insight.value)) if character().skills.insight.adv else vroll("1d20+"+(character().skills.insight.value))
C2=vroll("2d20kh1+"+(character().skills.wisdom.value)) if character().skills.wisdom.adv else vroll("1d20+"+(character().skills.wisdom.value))
C3=vroll("1d20+"+max(get_raw().skills.arcana, get_raw().skills.religion, get_raw().skills.history, get_raw().skills.nature))
DC1, DC2, DC3=roll('1d4+6'), roll('1d4+6'), roll('1d4+6'),

#Checking skills and Money
S=(0 if DC1 > C1.total else 1)+(0 if DC2 > C2.total else 1)+(0 if DC3 > C3.total else 1)
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
You remember what you learned: (DC {DC3})
**Knowledge:** {C3.full}   

You look into what the student is struggling with: (DC {DC1})
 **Insight:** {C1.full}
    
 You adjust to help them: (DC {DC2})
 **Wisdom:** {C2.full}
    
    {"**Success** - everyone is happy with your service! <:pandahappy:841009993239101450> " + n + "You gain **" + str(T) + "gp**" if S==3 else "Made it through the day." + n + "You gain **" + str(T) + "gp**" if S==2 else "You struggle through the day." + n+ "You gain **" + str(T) + "gp**" if S==1 else "The students are still lost. <:pandapopcorn:841013412523933776> "}
    {"" if S==0 else n + "**Gold Pieces: **" + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    **DT Remaining:** {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "**<name>** starts work as a Teacher!"
-footer "Downtime | Teach | RoI"
-thumb <image>
-color <color>