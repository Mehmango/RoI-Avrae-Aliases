embed
<drac2>
h,nd='%1%'.lower()=='help',get_cc('DT')==0
mod_cc('DT', -1) if not (nd or h) else None
args=&ARGS&

one = get_cc("DT") if cc_exists("DT") else 0
two = get_cc("Jail") if cc_exists("Jail") else 0
C1=vroll("2d20kh1+"+charismaMod) if character().skills.charisma.adv else vroll("1d20+"+charismaMod)
C2=vroll('2d20kh1+'+get_raw().skills.deception) if character().skills.deception.adv else vroll('1d20+'+get_raw().skills.deception)
C3=vroll('2d20kh1+'+get_raw().skills.persuasion) if character().skills.persuasion.adv else vroll('1d20+'+get_raw().skills.persuasion)
DC1, DC2, DC3=roll('2d4+9'), roll('2d4+9'), roll('2d4+9')

S=1+(0 if DC1 > C1.total else 1)+(0 if DC2 > C2.total else 1)+(0 if DC3 > C3.total else 1)

fate=roll('1d3')
fail=2 if S > fate else 1
jail=roll('2d2') if fail==1 else 0
P=ceil((proficiencyBonus*.5))if fail==1 else ceil(((proficiencyBonus*3)+roll('14d2')-1)*.5) if S < 4 else ceil((proficiencyBonus*3)+roll('14d2')-1)

mod_cc("DT",-jail) if one > jail else mod_cc("Jail",+jail-one) or set_cc("DT",0)

a = load_json(bags)
[a[x][1].update({"gp":a[x][1].gp+P}) for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
set_cvar("bags",dump_json(a))

n = "\n"

sMsg=f' -desc "You find some juicy dirt!: (DC {DC1})\n**Charisma:** {C1.full}\n\nYou imply you know how to leverage dirt!: (DC {DC2})\n**Deception:** {C2.full}\n\nYou convince them to exchange coin for silence!: (DC {DC3})\n**Persuasion:** {C3.full}\n\n{"You **failed** and got caught by the guards! You must now spend **" + str(jail) + "** nights in jail." if fail==1 else "**Success!** Your bluff was not called!" + n + "You gain **" + str(P) + "gp**"}\n\n**DT Remaining:** "{cc_str("DT")}"\n**Jail Time:** "{cc_str("Jail")}'

ndMsg=f' -desc "{name} does not have the required downtime to perform this work."'

hMsg=f' -desc "**HELP**\n\nPlease check downtime rules to set counters!"'

return hMsg if h else ndMsg if nd else sMsg
</drac2>
-title "**<name>** threatens to reveal secret dirt, unless!"
-footer "Downtime | Blackmail | RoI"
-thumb <image>
-color <color>