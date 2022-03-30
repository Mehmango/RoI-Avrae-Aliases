embed
<drac2>
args = &ARGS&
title = name + " tries to join a guild!"
desc = "﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌\n\n"
if len(args)<1:
    desc += "<:kittydotdotdot:770188345187106866> **You have to provide the initials of the guild you're trying to join** <:kittydotdotdot:770188345187106866>\n\nExample: !JoinGuild PM"
else:
    guildInitials = args[0]
    guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
    guildsDict = load_json(get_gvar(guildsGvar))
    if guildInitials == "None":
        title = "**" + name + " leaves their guild...... <:pandacry:841012316509175888>**" if not get("guild") in guildsDict else "**" + name + " leaves the " + guildsDict[get("guild")].name + "....... <:pandacry:841012316509175888>**"
        desc += ":person_walking:﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏:leaves:"
        character().delete_cvar("guild")
    elif guildInitials not in guildsDict:
        desc += "**Invalid Guild Initials Provided! <:kittyscream:834292391212482630>\n\nValid Guild Initials are:** \n\n"
        desc += "".join([guildsDict[key]['name'] + " -> " + "**"+ key + "**\n" for key in guildsDict if key != "Test"])
        desc += "\n<:kittydotdotdot:770188345187106866>"
    elif guildInitials == get("guild"):
        desc += "<:kittydotdotdot:770188345187106866> **"+ name + " is already part of the " + guildsDict[guildInitials].name + "** <:kittydotdotdot:770188345187106866>"
    else:
        character().set_cvar("guild", guildInitials)
        title = name + " joins the " + guildsDict[guildInitials].name + "! <:kittyamazed:770160347881275393>"
        desc += "**:beginner: You can now gain benefits from the guild's modules! :beginner:**"
        # desc += ", as well as contribute towards the guild's success with guild DTs!"
desc += "\n\n﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌"
return f""" -title "{title}" -desc "{desc}" """ 
</drac2>