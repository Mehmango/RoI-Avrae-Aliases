embed
<drac2>
args,n=&ARGS&,"\n"

p=proficiencyBonus
Lveh=p if "Land Vehicles" in get("pTools","[]") else p if "Cartographer's Tools" in get("pTools","[]") else 0
Wveh=p if "Navigator's Tools" in get("pTools","[]") else p if "Water Vehicles" in get("pTools","[]") else 0

C1=max(Lveh,Wveh)+roll('1d20')
C2=max(get_raw().skills.persuasion,get_raw().skills.deception)+roll('1d20')
S1=get('strengthSave')+roll('1d20')
DC1,DC2,DC3=roll('2d4+7'),roll('2d4+7'),roll('2d4+7')

S=0 if DC2 > C2 else 1
F1=1 if DC1 > C1 else 0
F2=(1 if F1==1 else 0) + (1 if DC3 > S1 else 0)

R=(S+1)*(4+p)
T=R

a = load_json(bags)
oldGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
[a[x][1].update({"gp":a[x][1].gp+T}) for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
set_cvar("bags",dump_json(a))
newGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]

if get_cc('DT') < 4:
    Msg = f' -desc "{name} does not have the required downtime.\n\nFor this activity you must have 4 DT to plan for unexpected delays."'
else:
    mod_cc('DT', -4) if F2 ==2 else mod_cc('DT', -3)
    Msg = f""" -desc 
    "
    Traversing the environment (DC {DC1})
    Vehicle check: {C1}{n + n + "Encountering difficulties (DC " + str(DC3) + ")" + n + "Strength Save: " + str(S1) if F1==1 else ""}{n + n + "On your travels you encounter a delay! <:kittysweat:770160378201899018>" if F2==2 else ""}

    Trading goods (DC {DC2})
    Charisma check: {C2}

    {"Success - you make a profit! <:pandahappy:841009993239101450>" + n + "You gain " + str(T) + "gp" if S==1 else "A decent trade. <:pandapopcorn:841013412523933776>" + n + "You gain " + str(T) + "gp"}

    {"Gold Pieces: " + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    DT Remaining: {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "<name> starts their work as a Merchant!"
-footer "Downtime | Merchant | Impiltur"
-thumb <image>
-color <color>