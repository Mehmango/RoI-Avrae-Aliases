embed
<drac2>
args,n,p=&ARGS&,"\n",proficiencyBonus

#get skills and DCs
S1=vroll("2d20kh1+"+(character().saves.get("str").value)) if character().saves.get("str").adv else vroll("1d20+"+(character().saves.get("str").value))
C1=vroll("2d20kh1+"+(character().skills.athletics.value)) if character().skills.athletics.adv else vroll("1d20+"+(character().skills.athletics.value))
S2=vroll("2d20kh1+"+(character().saves.get("con").value)) if character().saves.get("con").adv else vroll("1d20+"+(character().saves.get("con").value))
DC1,DC2,DC3=roll('2d4+5'),roll('2d4+5'),roll('2d4+5')
Z=get_cc("Jail") if cc_exists("Jail") else 0

#Checks
S=2 if S1.total>=DC1 and C1.total>=DC2 else 1 if (S1.total>=DC1 or C1.total>=DC2) else 0
T=ceil((proficiencyBonus*.5)) if S==0 else ceil(((proficiencyBonus*3)+roll('11d2')+1)*.5) if S < 2 else ceil((proficiencyBonus*3)+roll('11d2')+1)
inj=2 if DC3>S2.total else 1

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
   You chop at the tree!: (DC {DC1})
    **Strength:** {S1.full}

   You move the lumber!: (DC {DC2})
    **Athletics:** {C1.full}

   You check your form! (DC {DC3})
   **Constitution Save: ** {S2.full}{n+n+ "You didn't stretch first! **Pulled Muscle** 😟 " + n + "**You Lose 1 DT for Rest**" if (DC3>S2.total) else ""}

    {"Success - The trees are chopped! 😃 " + n + "You gain " + str(T) + "gp" if S==2 else "Only some of the work was done"  + n + "You gain " + str(T) + "gp" if S==1 else "It was a hard day today. 🙄 You still gain **" + str(T) + "gp.**"}
    {"" if S==0 else n + "Gold Pieces: " + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    DT Remaining: {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "<name> starts their work as a lumberjack!"
-footer "Downtime | lumberjack | RoI"
-thumb <image>
-color <color>