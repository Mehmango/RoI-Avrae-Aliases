embed
<drac2>
arg = &ARGS&[0] if len(&ARGS&)==1 else None
character().set_cvar_nx("pieLost", "")
character().set_cvar_nx("piesEaten", 0)
character().set_cvar_nx("nextPieDC", 5)
title = "Pie Eating Contest <:kittynom:834292327047888916>"
desc = ""
adv = False
me = combat().me if combat() else None
if me is None:
    return f""" -title "{title}" -desc "\nJoin initiative to start eating pie! <:kittysip:770160303010480199>" -footer "{name}: <{character().hp_str()}>" """

if arg=="reset":
    character().set_cvar("pieLost", "")
    character().set_cvar("piesEaten", 0)
    character().set_cvar("nextPieDC", 5)
    character().set_cvar("lastPieGrease", False)
    character().set_cvar("isGoat", False)
    desc = name + " is ready for another Pie Eating Contest! <:kittycelebrate:835505972952432680>\n\n"
elif arg=="heal":
    character().set_cvar("pieRupture", False)
    desc = name + "'s ruptured stomach is healed! <:kittycelebrate:835505972952432680>\n\n"
elif arg is not None and arg != "adv":
    desc = "Invalid arguments! <:kittythink:834292466571411507>\n\n"
elif get("pieLost")!="":
    desc = get("pieLost")
else:
    if arg=="adv":
        adv = True
    conAdv = character().skills.constitution.adv or get("lastPieGrease")=="True" or adv
    wisAdv = character().skills.wisdom.adv
    if get("pieRupture"):
        damageRoll = me.damage("3d8[necrotic]")
        character().modify_hp(-damageRoll['total'])
        desc += name + " takes " + damageRoll['roll'] + " necrotic damage from a ruptured stomach! <:kittygrimace:834292284006334475>\n\n"
    if me.hp < 1:
        character().set_cvar("pieLost", name + " is unable to continue due to a ruptured stomach! <:kittygrimace:834292284006334475>\n\n")
    else:
        pieRoll = roll("1d100")
        if pieRoll<61:
            conSave = me.save("con", True if conAdv else None) if get("isGoat")!="True" else vroll("2d20kh1+0") if get("lastPieGrease")=="True" else vroll("1d20+0")
            desc += "**CON SAVE (DC "+ int(get("nextPieDC")) + ")**: " + conSave.full + "\n\n"
            if conSave.total<int(get("nextPieDC")):
                character().set_cvar("pieLost", name + " is too stuffed to continue! <:kittyunhappy:770160130301624361>\n\n")
                desc += name + " is unable to finish the pie! <:kittyunhappy:770160130301624361>\n\n"
            else:
                desc += name + " chows down on the pie. It seems like a normal pie. <:kittynom:834292327047888916>\n\n"
                character().set_cvar("lastPieGrease", False)
        elif pieRoll<66:
            desc += "As " + name + " starts to eat the pie, it suddenly doubles in size! (This and all future DCs + 2) <:kittyscream:834292391212482630>\n\n"
            character().set_cvar("nextPieDC", int(get("nextPieDC"))+2)
            conSave = me.save("con", True if conAdv else None) if get("isGoat")!="True" else vroll("2d20kh1+0") if get("lastPieGrease")=="True" else vroll("1d20+0")
            desc += "**CON SAVE (DC "+ int(get("nextPieDC")) + ")**: " + conSave.full + "\n\n"
            if conSave.total<int(get("nextPieDC")):
                character().set_cvar("pieLost", name + " is too stuffed to continue! <:kittyunhappy:770160130301624361>\n\n")
                desc += name + " is unable to eat the enlarged pie! <:kittysweat:770160378201899018>\n\n"
            else:
                desc += name + " still manages to eat the whole pie! <:kittysmug:834292430467104768>\n\n"
                character().set_cvar("lastPieGrease", False)
        elif pieRoll<71:
            desc += "The pie shimmers with an otherwordly energy... and taste. (Disadvantage on this save) :space_invader:\n\n"
            conSave = me.save("con", None if conAdv else False) if get("isGoat")!="True" else vroll("1d20+0") if get("lastPieGrease")=="True" else vroll("2d20kl1+0") #Accounts for Disadvantage
            desc += "**CON SAVE (DC "+ int(get("nextPieDC")) + ")**: " + conSave.full + "\n\n"
            if conSave.total<int(get("nextPieDC")):
                character().set_cvar("pieLost", name + " is too stuffed to continue! <:kittyunhappy:770160130301624361>\n\n")
                desc += name + " is unable to stomach the strange energy, and can't finish the pie! <:kittyunhappy:770160130301624361>\n\n"
            else:
                desc += name + " holds their breath and gobbles up the pie anyway! <:kittysmug:834292430467104768>\n\n"
                character().set_cvar("lastPieGrease", False)
        elif pieRoll<76:
            desc += "The pie bursts into flames as " + name + " tries to eat it! (No Con save needed but take 3d6 fire damage and make a DC 10 Medicine check to cool your mouth and continue) <:kittythisisfine:770160409671499786>\n\n"
            fireDamage = me.damage("3d6[fire]")
            desc += "**Fire Damage**: " + fireDamage['roll'] + " :fire:\n\n"
            medCheck = vroll(me.skills.medicine.d20()) if get("isGoat")!="True" else vroll("1d20+0")
            desc += "**Medicine Check**: " + medCheck.full + " :fire_extinguisher:\n\n"
            if me.hp<1:
                character().set_cvar("pieLost", name + " is burnt out! <:kittythisisfine:770160409671499786>\n\n")
                desc += name + " is burned unconscious by the flaming pie! <:kittyscream:834292391212482630>\n\n"
            elif medCheck.total<10:
                character().set_cvar("pieLost", name + " is burnt out! <:kittythisisfine:770160409671499786>\n\n")
                desc += name + " is unable to extinguish the flames, and has to run to the nearest medical booth! :fire_engine:\n\n"
            else:
                desc += name + " soldiers on with a burnt tongue! <:kittysmug:834292430467104768>\n\n"
                character().set_cvar("lastPieGrease", False)
        elif pieRoll<81:
            desc += "The pie casts Grease as " + name + " swallows it! (Advantage on this and the next Con save) <:kittygrimace:834292284006334475>\n\n"
            character().set_cvar("lastPieGrease", True)
            conSave = me.save("con", True)
            desc += "**CON SAVE (DC "+ int(get("nextPieDC")) + ")**: " + conSave.full + "\n\n"
            if conSave.total<int(get("nextPieDC")):
                character().set_cvar("pieLost", name + " is too stuffed to continue! <:kittyunhappy:770160130301624361>\n\n")
                desc += "Despite the added lubrication, " + name + " is unable to finish the pie! <:kittyunhappy:770160130301624361>\n\n"
            else:
                desc += "The pie slides easily down " + name + "'s throat! <:kittynom:834292327047888916>\n\n"
        elif pieRoll<86:
            desc += name + " turns into a goat! (Stats changed to that of a goat (CON 11). Make sure to run !pie reset to reset your stats!) :goat:\n\n"
            character().set_cvar("isGoat", True)
            conSave = me.save("con", True if conAdv else None) if get("isGoat")!="True" else vroll("2d20kh1+0") if get("lastPieGrease")=="True" else vroll("1d20+0")
            desc += "**CON SAVE (DC "+ int(get("nextPieDC")) + ")**: " + conSave.full + "\n\n"
            if conSave.total<int(get("nextPieDC")):
                character().set_cvar("pieLost", name + " is too stuffed to continue! <:kittyunhappy:770160130301624361>\n\n")
                desc += name + " is unable to finish the pie! <:kittyunhappy:770160130301624361>\n\n"
            else:
                desc += name + " gobbles up the polymorphing pie! <:kittysmug:834292430467104768>\n\n"
                character().set_cvar("lastPieGrease", False)
        elif pieRoll<91:
            desc += "The pie begins yelling painfully personal insults at " + name + ". (Make a DC 10 Wisdom save to continue eating) <:kittycry:770188228107436043>\n\n"
            conSave = me.save("con", True if conAdv else None) if get("isGoat")!="True" else vroll("2d20kh1+0") if get("lastPieGrease")=="True" else vroll("1d20+0")
            wisSave = me.save("wis", wisAdv) if get("isGoat")!="True" else vroll("1d20+0")
            desc += "**WIS SAVE (DC 10)**: " + wisSave.full + "\n\n"
            desc += "**CON SAVE (DC "+ int(get("nextPieDC")) + ")**: " + conSave.full + "\n\n"
            if wisSave.total<10:
                character().set_cvar("pieLost", name + " is too chocked up to continue! <:kittycry:770188228107436043>\n\n")
                desc += "The talking pie's insults hit too close to home, and " + name + " starts crying! <:kittycry:770188228107436043>\n\n"
            elif conSave.total<int(get("nextPieDC")):
                character().set_cvar("pieLost", name + " is too stuffed to continue! <:kittyunhappy:770160130301624361>\n\n")
                desc += name + " is able to weather the insults, but is unable to finish the pie! <:kittyunhappy:770160130301624361>\n\n"
            else:
                desc += name + " ignores the talking pie as it travels down to their stomach, soon to be silenced by their digestive juices. <:kittystab:834295460579115059>\n\n"
                character().set_cvar("lastPieGrease", False)
        elif pieRoll<96:
            desc += "The pie disappears as " + name + " swallows it! (No DC needed and do not add the usual +2 to future DCs) <:kittydotdotdot:770188345187106866>\n\n"
            character().set_cvar("piesEaten", int(get("piesEaten"))-1)
            character().set_cvar("nextPieDC", int(get("nextPieDC"))-2)
        elif pieRoll<99:
            desc += "The pie explodes as it hits your stomach causing a rupture! (Take 3d8 necrotic damage now and at the start of each turn until you are healed) <:kittyscream:834292391212482630>\n\n"
            conSave = me.save("con", True if conAdv else None) if get("isGoat")!="True" else vroll("2d20kh1+0") if get("lastPieGrease")=="True" else vroll("1d20+0")
            desc += "**CON SAVE (DC "+ int(get("nextPieDC")) + ")**: " + conSave.full + "\n\n"
            damageRoll = me.damage("3d8[necrotic]")
            desc += "**Ruptured Stomach Damage**: " + damageRoll['roll'] + " <:kittygrimace:834292284006334475>\n\n"
            if me.hp<1:
                character().set_cvar("pieLost", name + " is unable to continue due to a ruptured stomach! <:kittygrimace:834292284006334475>\n\n")
                desc += name + " kneels over in pain! <:kittydead:834292798429724724>\n\n"
            elif conSave.total<int(get("nextPieDC")):
                character().set_cvar("pieLost", name + " is too stuffed to continue! <:kittyunhappy:770160130301624361>\n\n")
                desc += name + " is tough, but is unfortunately too full to continue! <:kittyunhappy:770160130301624361>\n\n"
            else:
                desc += name + " is able to hold fast, for now... <:kittysweat:770160378201899018>\n\n"
                character().set_cvar("lastPieGrease", False)
        else:
            desc += name + " is teleported to a random location with 5 miles and disqualified from the contest! <:kittybutt:770159487222808596>\n\n"
            character().set_cvar("pieLost", name + " is nowhere to be seen! <:kittydotdotdot:770188345187106866>\n\n")
    if get("pieLost")=="":
        character().set_cvar("piesEaten", int(get("piesEaten"))+1)
        character().set_cvar("nextPieDC", int(get("nextPieDC"))+2)
    else:
        desc += get("pieLost")
desc += "\n" + name + " has eaten a total of `" + get("piesEaten") + "` pies! <:kittyamazed:770160347881275393>"
return f""" -title "{title}" -desc "\n{desc}" -footer "{name}: <{character().hp_str()}>" """
</drac2>








