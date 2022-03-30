embed
<drac2>
args,n=&ARGS&,"\n"

C1=vroll("2d20kh1+"+(character().skills.perception.value)) if character().skills.perception.adv else vroll("1d20+"+(character().skills.perception.value))
C2=vroll("2d20kh1+"+(character().skills.athletics.value)) if character().skills.athletics.adv else vroll("1d20+"+(character().skills.athletics.value))
C3=vroll("2d20kh1+"+(character().saves.get("cha").value)) if character().saves.get("cha").adv else vroll("1d20+"+(character().saves.get("cha").value))
DC=12

S=(0 if DC > C1.total else 1)+(0 if DC > C2.total else 1)+(0 if DC > C3.total else 1)
R=ceil(proficiencyBonus*.5) if S==0 else ceil(((proficiencyBonus*3)+roll('2d2')+7)*.5) if S < 3 else ceil((proficiencyBonus*3)+roll('2d2')+7)

a = load_json(bags)
oldGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
[a[x][1].update({"gp":a[x][1].gp+R}) for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
set_cvar("bags",dump_json(a))
newGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]

if get_cc('DT')==0:
    Msg = f' -desc "{name} does not have the required downtime."'
else:
    mod_cc('DT', -1) 
    Msg = f""" -desc 
    "
    Keeping a lookout for anyone in trouble (DC {DC})
    **Perception:** {C1.full}
    
    Chasing down runners (DC {DC})
    **Atletics:** {C2.full}
    
    Dissuading criminals and being a presence (DC {DC})
    **Charisma Save:** {C3.full}
    
    {"**Success** - you kept the city safe! <:pandahappy:841009993239101450> " + n + "You gain **" + str(R) + "gp**" if S==3 else "An average day, just getting by." + n + "You gain **" + str(R) + "gp**" if S == 2 or S==1 else "The guard captain is not impressed. <:pandapopcorn:841013412523933776> " + n + "You Gain **" + str(R) + "gp**"}
    
    **Gold Pieces: **{oldGP}gp -> {newGP}gp
    **DT Remaining:** {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "**<name>** starts their patrol as a City Guard!"
-footer "Downtime | Guard | RoI"
-thumb <image>
-color <color>