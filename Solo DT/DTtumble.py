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

#get skills and DCs
B+=proficiencyBonus
C1=vroll("2d20kh1+"+(character().skills.performance.value)) if character().skills.performance.adv else vroll("1d20+"+(character().skills.performance.value))
C2=vroll("2d20kh1+"+(character().skills.acrobatics.value)) if character().skills.acrobatics.adv else vroll("1d20+"+(character().skills.acrobatics.value))
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
{desc}

    You draw in a crowd (DC {DC1})
    **Performance:** {C1.full}

    You perform the daring stunt (DC {DC2})
    **Acrobatics:** {C2.full}{n + n + "You try to recover (DC " + str(DC3) + ")" + n + "**Dexterity Save:** " + str(S1.full) if DC2>C2.total else ""}{n + n + "You landed incorrectly and now have a **Twisted Ankle** 😟 " + n + "**You Lose 1 DT for Rest**" if (DC2>C2.total and DC3>S1.total) else ""}

    {"Success - You stun the crowd! 😃 " + n + "You gain **" + str(T) + "gp.**" if S==2 else "Some onlookers are impressed"  + n + "You gain **" + str(T) + "gp.**" if S==1 else "No one found it captivating, but you found **" + str(T) + "gp** 🙄 "}
    {"" if S==0 else n + "Gold Pieces: " + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    DT Remaining: {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "<name> starts their work as a Tumbler!"
-footer "Downtime | Tumble | RoI"
-thumb <image>
-color <color>