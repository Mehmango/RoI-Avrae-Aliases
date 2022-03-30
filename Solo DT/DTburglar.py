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
 

B=proficiencyBonus if "Thieves' Tools" in get("pTools", "[]") else 0
one = get_cc("DT") if cc_exists("DT") else 0
two = get_cc("Jail") if cc_exists("Jail") else 0
C1=vroll("2d20kh1+"+(character().skills.acrobatics.value+B)) if character().skills.acrobatics.adv else vroll("1d20+"+(character().skills.acrobatics.value+B))
C2=vroll("2d20kh1+"+(character().skills.stealth.value+B)) if character().skills.stealth.adv else vroll("1d20+"+(character().skills.stealth.value+B))
C3=vroll("2d20kh1+"+(character().skills.sleightOfHand.value+B)) if character().skills.sleightOfHand.adv else vroll("1d20+"+(character().skills.sleightOfHand.value+B))
DC1, DC2, DC3=roll('2d4+9'), roll('2d4+9'), roll('2d4+9')

S=1+(0 if DC1 > C1.total else 1)+(0 if DC2 > C2.total else 1)+(0 if DC3 > C3.total else 1)

fate=roll('1d3')-escapeBonus
fail=2 if S > fate else 1
jail=roll('2d2') if fail==1 else 0
P=(proficiencyBonus*.5) if fail==1 else ((proficiencyBonus*3)+roll('14d2')-1)*.5 if S < 4 else (proficiencyBonus*3)+roll('14d2')-1

mod_cc("DT",-jail) if one > jail else mod_cc("Jail",+jail-one) or set_cc("DT",0)

a = load_json(bags)
[a[x][1].update({"gp":a[x][1].gp+P}) for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
set_cvar("bags",dump_json(a))

n = "\n"

sMsg=f' -desc "{desc}\n\nYou leap through the night, rooftop to rooftop for that second-story work!: (DC {DC1})\n**Acrobatics:** {C1.full}\n\nYou avoid detection!: (DC {DC2})\n**Stealth:** {C2.full}\n\nYou liberate the rich of their wealth!: (DC {DC3})\n**Sleight of Hand:** {C3.full}\n\n{"You **failed** and got caught by the guards! You must now spend **" + str(jail) + "** nights in jail." if fail==1 else "**Success!** You make off with the loot!" + n + "You gain **" + str(P) + "gp**"}\n\n**DT Remaining:** "{cc_str("DT")}"\n**Jail Time:** "{cc_str("Jail")}'

ndMsg=f' -desc "{name} does not have the required downtime to perform this work."'

hMsg=f' -desc "**HELP**\n\nPlease check downtime rules to set counters!"'

return hMsg if h else ndMsg if nd else sMsg
</drac2>
-title "**<name>** starts a rooftop caper!"
-footer "Downtime | Burglary | RoI"
-thumb <image>
-color <color>