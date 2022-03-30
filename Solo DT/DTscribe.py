embed
<drac2>
args,n,p=&ARGS&,"\n",proficiencyBonus
desc = ""
guildHasLibrary = False
guildLibraryBonus = proficiencyBonus
B=0
guildInitials = get("guild")
guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
if guildInitials in guildsDict and "library" in guildsDict[guildInitials]:
        guildHasLibrary = True
        B+=guildLibraryBonus
        desc += "\n\n**" + guildsDict[guildInitials]['name'] + " Library Bonus: `+" + guildLibraryBonus + "`** <:kittysmug:834292430467104768>" 


B+=p if "Calligrapher's Supplies" in get("pTools","[]") else 0
C1=vroll("2d20kh1+"+(character().skills.history.value+B)) if character().skills.history.adv else vroll("1d20+"+(character().skills.history.value+B))
C2=vroll("2d20kh1+"+(character().skills.intelligence.value+B)) if character().skills.intelligence.adv else vroll("1d20+"+(character().skills.intelligence.value+B))
C3=vroll("2d20kh1+"+(character().saves.get("int").value+B)) if character().saves.get("int").adv else vroll("1d20+"+(character().saves.get("int").value+B))
DC1,DC2,DC3=roll('1d4+6'),roll('1d4+6'),roll('1d4+6')

S=(0 if DC1 > C1.total else 1)+(0 if DC2 > C2.total else 1)+(0 if DC3 > C3.total else 1)
T=(proficiencyBonus*.5) if S==0 else ((proficiencyBonus*3)+roll('2d2')+7)*.5 if S < 3 else (proficiencyBonus*3)+roll('2d2')+7

a = load_json(bags)
oldGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
[a[x][1].update({"gp":a[x][1].gp+T}) for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
set_cvar("bags",dump_json(a))
newGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]

if get_cc('DT')==0:
    Msg = f' -desc "{name} does not have the required downtime."'
else:
    mod_cc('DT', -1) 
    Msg = f""" -desc 
    "

    {desc}
    
    Remembering your strokes and styles (DC {DC1})
    **History** {C1.full}
    
    Writing detailed pages and maps (DC {DC2})
    **Intelligence:** {C2.full}
    
    Mental fortitude (DC {DC3})
    **Intelligence Save:** {C3.full}
    
    {"**Success** - everyone is happy with your service! <:pandahappy:841009993239101450> " + n + "You gain **" + str(T) + "gp**" if S==3 else "Made it through the day." + n + "You gain **" + str(T) + "gp**" if S>=1 else "The work was not completed. <:pandapopcorn:841013412523933776> "}
    {"" if S==0 else n + "**Gold Pieces: **" + str(oldGP) + "gp -> " + str(newGP) + "gp"}
    **DT Remaining:** {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "**<name>** starts work as a Scribe!"
-footer "Downtime | Scribe | RoI"
-thumb <image>
-color <color>