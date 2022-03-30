embed
<drac2>
args = &ARGS&
if not combat():
    err("Channel not in init")
combatants = [combat().get_combatant(combatant) for combatant in args if combat().get_combatant(combatant) is not None]
title = "Bad elfs fall from the sky!"
dc = 15
desc = "**Meta**\n**Damage**: "
damageRoll = vroll("4d8[bludgeoning]")
desc += damageRoll.full + "\n**DC**: "+dc+"\n"
dexSaves = [combatant.save("dex") for combatant in combatants]
[combatants[x].damage(damageRoll.total/2+"[bludgeoning]") if dexSaves[x].total>=dc else combatants[x].damage(damageRoll.total+"[bludgeoning]") for x in range(len(combatants))]
success = ["Failure!" if dexSave.total<dc else "Success!" for dexSave in dexSaves]
damageStr = ["("+damageRoll.total+") / 2 [bludgeoning] = `"+floor(damageRoll.total/2)+"`" if dexSave.total>=dc else damageRoll.total+" [bludgeoning] = `"+damageRoll.total+"`\n" for dexSave in dexSaves]
footer = ""
if len(combatants)>0:
    desc += "".join(["\n\n**"+combatants[x].name + "**\n**DEX Save**: " + dexSaves[x].full + "; " + success[x] + "\n**Damage**: " + damageStr[x] for x in range(len(combatants))])
    footer += "".join([combatant.name+": "+combatant.hp_str()+"\n" for combatant in combatants])
desc += "\n\n**Effect**\nBad elfs drop from the Grinch's sled in a 20ft diameter circle. Each creature in the circle must succeed on a DC15 Dexterity saving throw, taking 18 (4d8) bludgeoning damage on a failed save, or half as much damage on a successful one."
return f""" -title "{title}" -desc "{desc}" -footer "{footer}" """
</drac2>