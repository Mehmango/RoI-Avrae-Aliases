embed
<drac2>
h,nd='%1%'.lower()=='help',get_cc('DT')==0
mod_cc('DT', -1) if not (nd or h) else None
args=&ARGS&
desc = ""
guildHasSecretEntrance = False
guildSecretEntranceBonus = 1
escapeBonus=0
guildInitials = get("guild")
guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))
if guildInitials in guildsDict and "secretEntrance" in guildsDict[guildInitials]:
        guildHasSecretEntrance = True
        escapeBonus+=guildSecretEntranceBonus
        desc += "**The " + guildsDict[guildInitials]['name'] + " Secret Entrance Bonus: `" + guildSecretEntranceBonus*33 + "%`** reduced chance of capture <:kittysmug:834292430467104768>"
 

one = get_cc("DT") if cc_exists("DT") else 0
two = get_cc("Jail") if cc_exists("Jail") else 0
per=vroll("2d20kh1+"+(character().skills.perception.value)) if character().skills.perception.adv else vroll("1d20+"+(character().skills.perception.value))
dec=vroll("2d20kh1+"+(character().skills.deception.value)) if character().skills.deception.adv else vroll("1d20+"+(character().skills.deception.value))
sle=vroll("2d20kh1+"+(character().skills.sleightOfHand.value)) if character().skills.sleightOfHand.adv else vroll("1d20+"+(character().skills.sleightOfHand.value))
dc1, dc2, dc3 = roll('2d4+9'), roll('2d4+9'), roll('2d4+9')
S=1 + (0 if dc1 > per.total else 1) + (0 if dc2 > dec.total else 1) + (0 if dc3 > sle.total else 1)

fate=roll('1d3')-escapeBonus
fail=2 if S > fate else 1
jail=roll('2d2') if fail==1 else 0
P=(proficiencyBonus*.5) if fail==1 else ((proficiencyBonus*3)+roll('14d2')+1)*.5 if S < 4 else (proficiencyBonus*3)+roll('14d2')+1

mod_cc("DT",-jail) if one > jail else mod_cc("Jail",+jail-one) or set_cc("DT",0)

a = load_json(bags)
[a[x][1].update({"gp":a[x][1].gp+P}) for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
set_cvar("bags",dump_json(a))

n = "\n"

sMsg=f' -desc "{desc}\n\nYou check to see no one is watching! (DC {dc1})\n**Perception:** {per.full}\n\nYou deceive anyone that gets in your way! (DC {dc2})\n**Deception:** {dec.full}\n\nYou take off with the gold! (DC {dc3})\n**Sleight of Hand:** {sle.full}\n\n{"You **failed** and got caught by the guards! You must now spend **" + str(jail) + "** nights in jail." if fail==1 else "**Success!** You steal the gold!" + n + "You gain **" + str(P) + "gp**"}\n\n**DT Remaining:** "{cc_str("DT")}"\n**Jail Time:** "{cc_str("Jail")}'

ndMsg=f' -desc "{name} does not have the required downtime to perform this work."'

hMsg=f' -desc "**HELP**\n\nPlease check downtime rules to set counters!"'

return hMsg if h else ndMsg if nd else sMsg
</drac2>
-title "**<name>** begins a life of crime!"
-footer "Downtime | Thief | RoI"
-thumb <image>
-color <color>