embed
<drac2>
args,n=&ARGS&,"\n"

#get cmd
C1=vroll("2d20kh1+"+(character().skills.athletics.value)) if character().skills.athletics.adv else vroll("1d20+"+(character().skills.athletics.value))
C2=vroll("2d20kh1+"+(character().skills.animalHandling.value)) if character().skills.animalHandling.adv else vroll("1d20+"+(character().skills.animalHandling.value))
S1=vroll("2d20kh1+"+(character().saves.get("dex").value)) if character().saves.get("dex").adv else vroll("1d20+"+(character().saves.get("dex").value))
DC1,DC2,DC3=roll('2d4+7'),roll('2d4+7'),roll('2d4+7')
Z=get_cc("Jail") if cc_exists("Jail") else 0

#skill checks
S=0 if DC2 > C2.total else 1
F1=1 if DC1 > C1.total else 0
F2=F1 + (1 if DC3 > S1.total else 0)
total=5 if S==1 else 0
inj=2 if F2==2 else 1

#gold cmd
a=load_json(bags)
oldGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
[a[x][1].update({"gp":a[x][1].gp+total}) for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
set_cvar("bags",dump_json(a))
newGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]

#run cmd
if get_cc('DT')==0:
    Msg = f' -desc "{name} does not have the required downtime."'
else:
    mod_cc('DT', -inj) if get_cc("DT") > inj else mod_cc("Jail", +inj-get_cc("DT")) or set_cc("DT", 0)
    Msg = f""" -desc 
    "
    Climbing the tree (DC {DC1})
    **Athletics:** {C1.full}{n + n + "Landing safely (DC " + str(DC3) + ")" + n + "**Dexterity Save:** " + str(S1.full) if F1==1 else ""}{n + n + "You fall and get injured!" + n + "You now have a **concussion**" + n + "**You Lose 1 DT**" if F2==2 else ""}
    
    Ask the cat to come to you (DC {DC2})
    **Animal Handling:** {C2.full}
    
    {"**Success** - you saved the cat! <:kittywonder:770188525353828353> " + n + "You are rewarded with **5gp**" + n if S==1 else "You **failed** to save the cat!" + n}{n + "**Gold Pieces:** " + str(oldGP) + "gp -> " + str(newGP) + "gp" if S==1 else ""}
    **DT Remaining:** {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "**<name>** attempts to save the cat!"
-footer "Downtime | Cat | RoI"