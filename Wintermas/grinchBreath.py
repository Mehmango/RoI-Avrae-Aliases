embed
<drac2>
args = &ARGS&
if not combat():
    err("Channel not in init")
combatants = [combat().get_combatant(combatant) for combatant in args if combat().get_combatant(combatant) is not None]
title = "The Grinch uses his Icy Breath!"
dc = 15
desc = "**Meta**\n**Damage**: "
damageRoll = vroll("4d8[cold]")
desc += damageRoll.full + "\n**DC**: "+dc+"\n"
conSaves = [combatant.save("con") for combatant in combatants]
strSaves = [combatant.save("str") for combatant in combatants]
[combatants[x].damage(damageRoll.total/2+"[cold]") if conSaves[x].total>=dc else combatants[x].damage(damageRoll.total+"[cold]") for x in range(len(combatants))]
conSuccess = ["Failure!" if conSave.total<dc else "Success!" for conSave in conSaves]
strSuccess = ["Failure!" if strSave.total<dc else "Success!" for strSave in strSaves]
damageStr = ["("+damageRoll.total+") / 2 [cold] = `"+floor(damageRoll.total/2)+"`" if conSave.total>=dc else damageRoll.total+" [cold] = `"+damageRoll.total+"`\n" for conSave in conSaves]
footer = ""
if len(combatants)>0:
    for x in range(len(combatants)):
        desc += "\n\n**"+combatants[x].name + "**\n**CON Save**: " + conSaves[x].full + "; " + conSuccess[x] + "\n**Damage**: " + damageStr[x]
        if conSuccess[x] == "Failure!":
            desc += "**\nSTR Save**: " + strSaves[x].full + "; " + strSuccess[x]
            if strSuccess[x] == "Failure!":
                desc += "\n*" + combatants[x].name + " is knocked prone!*"
                combatants[x].add_effect("Prone", "")
        footer += combatants[x].name+": "+combatants[x].hp_str()+"\n"
desc += "\n\n**Effect**\nThe Grinch exhales ice cold air in a 30-foot cone. Each creature in that area must make a DC 15 Constitution saving throw. On a failed save, the creature takes 21 (4d8) cold damage. On a successful save, the creature takes half as much damage."
return f""" -title "{title}" -desc "{desc}" -footer "{footer}" """
</drac2>