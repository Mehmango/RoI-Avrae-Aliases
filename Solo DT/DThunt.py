embed
<drac2>
args,n,p=&ARGS&,"\n",proficiencyBonus

#get skills and DCs
B=proficiencyBonus
C1=vroll("2d20kh1+"+(character().skills.survival.value)) if character().skills.survival.adv else vroll("1d20+"+(character().skills.survival.value))
C2=vroll("2d20kh1+"+(character().skills.athletics.value)) if character().skills.athletics.adv else vroll("1d20+"+(character().skills.athletics.value))
S1=vroll("2d20kh1+"+(character().saves.get("dex").value)) if character().saves.get("dex").adv else vroll("1d20+"+(character().saves.get("dex").value))
DC1,DC2,DC3=roll('2d4+5'),roll('2d4+5'),roll('2d4+5')
Z=get_cc("Jail") if cc_exists("Jail") else 0

S=2 if C1.total>=DC1 and (C2.total>=DC2 or S1.total>=DC3) else 1 if (C1.total>=DC1 or C2.total>=DC2 or S1.total>=DC3) else 0
T=(B*.5) if S==0 else ((B*3)+roll('11d2'))*.5 if S < 2 else (B*3)+roll('11d2')
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

    Traversing the Environment (DC {DC2})
    **Athletics:** {C2.full}{n+n+"Encountering Difficulties (DC " + str(DC3) + ")" + n + "**Dexterity Save:** " + str(S1.full) if DC2>C2.total else ""}{n + n + "On your travels you get injured and now have a **Concussion** :worried: " + n + "**You Lose 1 DT for Rest**" if (DC2>C2.total and DC3>S1.total) else ""}

    Landing the catch (DC {DC1})
    **Survival:** {C1.full}

    {"Success - You landed the big one :smiley: " + n + "You gain **" + str(T) + "gp.**" if S==2 else "You ran down small game"  + n + "You gain **" + str(T) + "gp.**" if S==1 else "You didn't catch anything, but still made **" + str(T) + "gp** :rolling_eyes: "}
    {"" if S==0 else n + "Gold Pieces: " + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    DT Remaining: {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "<name> starts their work as a Hunter!"
-footer "Downtime | Hunt | RoI"
-thumb <image>
-color <color>