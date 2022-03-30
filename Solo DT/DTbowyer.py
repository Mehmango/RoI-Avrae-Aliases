embed
<drac2>
args,n=&ARGS&,"\n"
desc = ""
guildHasWorkshop = False
guildWorkshopBonus = proficiencyBonus
B=0

guildInitials = get("guild")
guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
if guildInitials in guildsDict and "workshop" in guildsDict[guildInitials]:
        guildHasWorkshop = True
        B+=guildWorkshopBonus
        desc += "**The " + guildsDict[guildInitials]['name'] + " Workshop Bonus: `" + guildWorkshopBonus + "`** <:kittysmug:834292430467104768>"
 
B+=proficiencyBonus if "Woodcarver's Tools" in get("pTools","[]") else 0
C1mod = character().skills.sleightOfHand.value+B
C1=vroll("2d20kh1+"+(C1mod)) if character().skills.sleightOfHand.adv else vroll("1d20+"+(C1mod))
if not character().skills.perception.adv and not character().skills.investigation.adv:
    C2mod = max(character().skills.perception.value,character().skills.investigation.value)+B
    C2 = vroll("1d20+"+C2mod)
elif character().skills.perception.adv and not character().skills.investigation.adv:
    C2mod = character().skills.perception.value + B
    C2 = vroll("2d20kh1+"+C2mod)
elif character().skills.investigation.adv and not character().skills.perception.adv:
    C2mod = character().skills.investigationn.value + B
    C2 = vroll("2d20kh1+"+C2mod)
else:
    C2mod = max(character().skills.perception.value,character().skills.investigation.value)+B
    C2 = vroll("2d20kh1+"+C2mod)
C3=vroll("2d20kh1+"+(dexterityMod+B)) if character().skills.dexterity.adv else vroll("1d20+"+(dexterityMod+B))
DC1, DC2, DC3=roll('2d5+6'), roll('2d5+6'), roll('2d5+6')
 
S=(0 if DC1 > C1.total else 1)+(0 if DC2 > C2.total else 1)+(0 if DC3 > C3.total else 1)
R=(proficiencyBonus*.5) if S==0 else ((proficiencyBonus*3)+roll('6d2'))*.5 if S < 3 else (proficiencyBonus*3)+roll('6d2')
 
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
    {desc}

You patiently shape the materials: (DC {DC1})
**Sleight of Hand:** {C1.full}

You check for flaws: (DC {DC2})
**Investigation or Perception:** {C2.full}

You test for trueness: (DC {DC3})
**Dexterity:** {C3.full}
   
    {"**Success** - The bowyer is happy with your work! ⚒️" + n + "You gain **" + str(R) + "gp**" if S>0 else "The project didn't turn out." + n + "You gain only **" + str(R) + "gp.**"}
    \n{"**Gold Pieces: **" + str(oldGP) + "gp -> " + str(newGP) + "gp"}
   **DT Remaining:** {cc_str("DT")}
    "
    """
return Msg
</drac2>
-title "**<name>** starts their job at the bowyery!"
-footer "Downtime | Bowyer | RoI"
-thumb <image>
-color <color>