embed
<drac2>
args,n,p,e=&ARGS&,"\n",proficiencyBonus,"Experience"
desc = ""
guildHasTrainingYard = False
guildTrainingYardRollBonus = proficiencyBonus
guildTrainingYardXpBonus = level
XpB = 0
B=0
guildInitials = get("guild")
guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
if guildInitials in guildsDict and "trainingYard" in guildsDict[guildInitials]:
        guildHasTrainingYard = True
        B+=guildTrainingYardRollBonus
        XpB+=guildTrainingYardXpBonus
        desc += "**The " + guildsDict[guildInitials]['name'] + " Training Yard Bonus: `" + guildTrainingYardRollBonus + "`** <:kittysmug:834292430467104768>"


#get cmd
C1=vroll("1d20+"+(int(max(dexterityMod,strengthMod,wisdomMod,charismaMod,intelligenceMod))+proficiencyBonus+B))
C2=vroll("2d20kh1+"+(character().skills.acrobatics.value+B)) if character().skills.acrobatics.adv else vroll("1d20+"+(character().skills.acrobatics.value+B))
S1=vroll("2d20kh1+"+(character().saves.get("dex").value+B)) if character().saves.get("dex").adv else vroll("1d20+"+(character().saves.get("dex").value+B))
DC=12
Z=get_cc("Jail") if cc_exists("Jail") else 0

#checks
S=0 if DC > C1.total else 1
F1=1 if DC > C2.total else 0
F2=(1 if F1==1 else 0) + (1 if DC > S1.total else 0)
T=roll('5d10+'+XpB) * level if S==1 else 0
inj=2 if F2==2 else 1

#xp cmd
oldXP=get_cc(e)
mod_cc(e,T)
newXP=get_cc(e)

#run cmd
if get_cc('DT')==0:
    Msg = f' -desc "{name} does not have the required downtime."'
else:
    mod_cc('DT', -inj) if get_cc("DT") > inj else mod_cc("Jail", +inj-get_cc("DT")) or set_cc("DT", 0)
    Msg = f""" -desc 
    "

{desc}

    Dodging the obstacles (DC {DC})
    **Acrobatics:** {C2.full}{n + n + "Encountering difficulties (DC " + str(DC) + ")" + n + "**Dexterity Save:** " + str(S1.full) if F1==1 else ""}{n + n + "While training you get injured!" + n +"You now have a **Twisted Ankle** <:kittynotlike:770189258366910475> " + n + "**You Lose 1 DT**" if F2==2 else ""}
    
    Attacking the targets (DC {DC})
    **Attack:** {C1.full}
    
    {"**Success** - you completed the training! <:kittywonder:770188525353828353> " + n + "You gain **" + str(T) + "xp**" if S==1 else "Further training is needed. <:kittydotdotdot:770188345187106866> "}
    {n + "**Experience: **" + n + str(oldXP) + "xp -> " + str(newXP) + "xp" if S==1 else ""}
    **DT Remaining:** {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "**<name>** begins combat training!"
-footer "Downtime | Combat Training | RoI"
-thumb <image>
-color <color>