embed
<drac2>
args,n,p=&ARGS&,"\n",proficiencyBonus

#Skill checks and DCs
C1=vroll("2d20kh1+"+(character().skills.wisdom.value)) if character().skills.wisdom.adv else vroll("1d20+"+(character().skills.wisdom.value))
C2=vroll("2d20kh1+"+(character().skills.religion.value)) if character().skills.religion.adv else vroll("1d20+"+(character().skills.religion.value))
C3=vroll("2d20kh1+"+(character().skills.performance.value)) if character().skills.performance.adv else vroll("1d20+"+(character().skills.performance.value))
DC1, DC2, DC3=roll('1d4+6'), roll('1d4+6'), roll('1d4+6'),

#Checking skills and Money
S=(0 if DC1 > C1.total else 1)+(0 if DC2 > C2.total else 1)+(0 if DC3 > C3.total else 1)
T=ceil(proficiencyBonus*.5) if S==0 else ceil(((proficiencyBonus*3)+roll('6d2')+1)*.25) if S==1 else ceil(((proficiencyBonus*3)+roll('6d2')+1)*.5) if S==2 else ceil((proficiencyBonus*3)+roll('6d2')+1)

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
You remember your faith: (DC {DC2})
**Religion:** {C2.full}   

You impart your wisdom: (DC {DC1})
 **Wisdom:** {C1.full}
    
 You speak it to the crowds!: (DC {DC3})
 **Performance:** {C3.full}
    
    {"**Success** - the followers of faith grow! <:pandahappy:841009993239101450> " + n + "You gain **" + str(T) + "gp**" if S==3 else "Some listened and donated to the temple." + n + "You gain **" + str(T) + "gp**" if S==2 else "Most just pass you by." + n+ "You gain **" + str(T) + "gp**" if S==1 else "You speak to an empty gathering but find **" + str(T) + "gp** under a pew. <:pandapopcorn:841013412523933776> "}
    {"" if S==0 else n + "**Gold Pieces: **" + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    **DT Remaining:** {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "**<name>** starts work as a Preacher!"
-footer "Downtime | Sermon | RoI"
-thumb <image>
-color <color>