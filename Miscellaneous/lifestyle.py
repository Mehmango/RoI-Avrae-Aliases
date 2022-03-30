embed
<drac2>
args,n = &ARGS&,"\n"
desc = ""
guildHasTavern = False
guildTavernBonus = 2
B=0
guildInitials = get("guild")
guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
if guildInitials in guildsDict and "tavern" in guildsDict[guildInitials]:
        guildHasTavern = True
        B+=guildTavernBonus
        desc += "**The " + guildsDict[guildInitials]['name'] + " Tavern Bonus: `" + guildTavernBonus + "`** <:kittysmug:834292430467104768>"
 
if cc_exists("Experience"):
    None
else:
    Msg = f""" -desc 
    "
    Experience counter not setup.\nPlease type `!xp`
    "
    """
    return Msg
    
if exists("bags"):
    None
else:
    Msg = f""" -desc 
    "
    Coins not setup.\nPlease type `!coins`
    "
    """
    return Msg

one = get_cc("RPXP") if cc_exists("RPXP") else 0
two = get_cc("Jail") if cc_exists("Jail") else 0
three = get_cc("Staff") if cc_exists("Staff") else 0

create_cc("DT",0,7+B,"none","bubble")
create_cc("Jail",0,5,"none","bubble")
create_cc("Staff",0,50,"none")
create_cc("RPXP",0,proficiencyBonus*280,"none") 

set_cc("DT",7-two+B)
set_cc("Jail",0)
set_cc("Staff",0)
set_cc("RPXP",0)

staffe = three * 15 * proficiencyBonus

mod_cc("Experience",one+staffe)
days = get_cc("DT")

a = load_json(bags)
[a[x][1].update({"gp":a[x][1].gp-7}) for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
set_cvar("bags",dump_json(a))
money = [a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]

Msg=f""" -desc 
"
{desc}

**Experience**
{"Staff Rewards: **" + str(staffe) + "xp**" + n if staffe > 0 else ""}{"RPXP: **" + str(one) + "xp**" + n if one > 0 else ""} Total: **{cc_str("Experience")}xp**

**Gold**
Modest lifestyle: **-7gp**
Total: **{money}gp**

**Counters**
{"Jail/Injury: **-" + str(two) + " DT**" + n if two > 0 else ""} Downtime: **{days} DT** 
"
"""

return Msg
</drac2>
-title "**<name>'s summary for the week!**"
-footer "Lifestyle | Summary | RoI"
-thumb <image>
-color <color>