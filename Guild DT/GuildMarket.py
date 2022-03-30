multiline
!embed
<drac2>
args=&ARGS&
title = ":convenience_store: " + name + " attempts to help run the guild market :convenience_store: "
desc = "﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌\n\n"

guildsGvar = "142cfbe7-cd55-4814-b037-a1b622c79d6a"
guildsDict = load_json(get_gvar(guildsGvar))

guildInitials = get("guild")
if guildInitials not in guildsDict:
    desc += "**<:kittydotdotdot:770188345187106866> "+name+ " isn't part of a guild** <:kittydotdotdot:770188345187106866>\n\n"
    desc += "Run `!JoinGuild <guild initials>` to join a guild! *(Eg: `!JoinGuild PM`)*"
elif "market" not in guildsDict[guildInitials]:
    desc += "**<:kittydotdotdot:770188345187106866> The " + guildsDict[guildInitials].name + " doesn't have a market! <:kittydotdotdot:770188345187106866>**"
else:
    marketDict = guildsDict[guildInitials].market
    guildsDict.update()
    level = int(marketDict.level)
    maxInvestment = 500*level+200
    invested = float(marketDict.invested)
    sales = int(marketDict.salesCounter)
    supply = int(marketDict.supplyRunsCounter)
    maxSales = 3+level*2
    maxSupply = maxSales
    projectedEarnings = int(marketDict.projectedEarnings)         # Current formula for earnings: Total Invested * ((sales Counter + Supply Runs Counter)*(1 + 0.5*(market level - 1))/(6 + 4*(market level)) + 0.5)
    if len(args)<1:  
        desc += "**__The " + guildsDict[guildInitials].name + "'s Market is Open For Business!__**\n\n\n"
        desc += "║ **Projected Earnings This Week:** `" + projectedEarnings + "gp`"
        desc += ":chart_with_upwards_trend:" if projectedEarnings > invested else ":chart_with_downwards_trend:"
        desc += " ║"

        desc += "\n\n\n💰 **Total Invested:** `" + invested + "` / " + maxInvestment + " gp 💰\n\n"
        investmentPercentage = int(invested/maxInvestment*15)
        investmentLeftover = 15-investmentPercentage
        desc += "".join(["▰" for i in range(0,investmentPercentage)])
        desc += "".join(["▱" for i in range(0,investmentLeftover)])
        desc += "\n\n*(Run `!GuildMarket Invest #` to invest #gp!)*"

        desc += "\n\n:handshake: **Sales Completed** :handshake:\n\n"
        salesLeftover = maxSales - sales
        desc += "".join(["⬤" for i in range(0,sales)])
        desc += "".join(["〇" for i in range(0,salesLeftover)])
        desc += "\n\n*(Run `!GuildMarket Sale` to help complete a sale!)*"

        desc += "\n\n:package: **Supply Runs Completed** :package:\n\n"
        supplyLeftover = maxSupply - supply
        desc += "".join(["⬤" for i in range(0,supply)])
        desc += "".join(["〇" for i in range(0,supplyLeftover)])
        desc += "\n\n*(Run `!GuildMarket Supply` to help complete a supply run!)*"

        desc += "\n\n\nRun `!GuildMarket Help` if you need help"
    elif args[0] in ["Help", "help"]:
        desc += "**Need some help with the shop? <:kittywave:770160454110412800>**\n\n"
        desc += "`!GuildMarket`  ➝  Displays the current status of the guild's market :office_worker:\n\n"
        desc += "`!GuildMarket Help`  ➝  Displays this message <:kittywave:770160454110412800>\n\n"
        desc += "`!GuildMarket Invest #`  ➝  Invests the specified number of gp into the guild market. The more you invest, the bigger the returns! <:kittyrich:834292404629536768>\n\n"
        desc += "`!GuildMarket Sale`  ➝  Spend one DT and roll a persuasion check to see if you can make a sale for the guild! :handshake:\n\n"
        desc += "`!GuildMarket Supply`  ➝  Spend one DT to make a supply run 📦   :person_running:"

    elif args[0] in ["Invest","invest"]:
        if len(args)<2:
            desc += "**Invalid command!** <:kittydotdotdot:770188345187106866>\n\n"
            desc += "Make sure to add the amount to invest in gp after the command. (Eg: `!GuildMarket Invest 100`)"
        elif not args[1].isnumeric():
            desc += "**Invalid command!** <:kittydotdotdot:770188345187106866>\n\n"
            desc += "The gp amount has to be a number! (Eg: `!GuildMarket Invest 100`)"
        else:
            amount = float(args[1])
            a = load_json(bags)
            oldGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
            if oldGP < amount:
                desc += "**" + name + " does not have enough gold to do this** <:kittydotdotdot:770188345187106866>"
            elif invested == maxInvestment:
                desc += "**Oop! The maximum amount of investments have already been made!** <:kittycelebrate:835505972952432680>\n\n"
            else:
                if maxInvestment - invested < amount:
                    amount = maxInvestment - invested
                invested += amount
                marketDict.update({"invested":invested})

                [a[x][1].update({"gp":a[x][1].gp-amount}) for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
                set_cvar("bags",dump_json(a))
                newGP=[a[x][1].get("gp") for x in range(len(a)) if a[x][0] == 'Coin Pouch'][0]
                
                desc += "**" + name + " invested " + amount + "gp into the guild market!** <:kittyrich:834292404629536768>\n\n"
            desc += "\n\n💰 **Total Invested:** `" + invested + "` / " + maxInvestment + " gp 💰\n\n"
            investmentPercentage = int(invested/maxInvestment*15)
            investmentLeftover = 15-investmentPercentage
            desc += "".join(["▰" for i in range(0,investmentPercentage)])
            desc += "".join(["▱" for i in range(0,investmentLeftover)])
            projectedEarnings = int(invested * ((sales + supply) * (1 + 0.5 * (level - 1))/(6 + 4*level) + 0.5))
            marketDict.update({"projectedEarnings":projectedEarnings})
            desc += "\n\n\n**Projected Earnings This Week:** `" + projectedEarnings + "gp`"
            desc += ":chart_with_upwards_trend:" if projectedEarnings > invested else ":chart_with_downwards_trend:"
            desc += "\n\n"

    elif args[0] in ["Sale","sale"]:
        if get_cc('DT')==0:
            desc += "**" + name + " does not have the required DT** <:kittydotdotdot:770188345187106866>"
        else:
            if sales >= maxSales:
                desc += "**Oop! It seems like all the required sales have already been made. Hurray!** <:kittycelebrate:835505972952432680>\n\n"
            else:
                persuasionCheck = vroll("2d20kh1+"+(character().skills.persuasion.value)) if character().skills.persuasion.adv else vroll("1d20+"+(character().skills.persuasion.value))
                dc = vroll("2d4+6").total
                
                desc += "**" + name + " attempts to make a sale: (DC "+dc+")**\n\n"
                desc += "**Persuasion:** "+persuasionCheck.full+"\n\n\n"

                if persuasionCheck.total>=dc:
                    desc += "**Success** - The customer is satisfied and the " + guildsDict[guildInitials].name + " is richer <:kittyrich:834292404629536768>\n\n"
                    sales+=1
                    marketDict.update({"salesCounter": sales})
                else:
                    desc += "**Failure** - The customer walked away <:pandacry:841012316509175888>\n\n"
                
                mod_cc("DT", -1)
            desc += "\n:handshake: **Sales Completed** :handshake:\n\n"
            salesLeftover = maxSales - sales
            desc += "".join(["⬤" for i in range(0,sales)])
            desc += "".join(["〇" for i in range(0,salesLeftover)])
            projectedEarnings = int(invested * ((sales + supply) * (1 + 0.5 * (level - 1))/(6 + 4*level) + 0.5))
            marketDict.update({"projectedEarnings":projectedEarnings})
            desc += "\n\n\n**Projected Earnings This Week:** `" + projectedEarnings + "gp`"
            desc += ":chart_with_upwards_trend:" if projectedEarnings > invested else ":chart_with_downwards_trend:"
            desc += "\n\n\n\n**DT Remaining:** "+ cc_str("DT")
    
    elif args[0] in ["Supply", "supply"]:
        if get_cc('DT')==0:
            desc += name + " does not have the required DT <:kittydotdotdot:770188345187106866>"
        else:
            if supply >= maxSupply:
                desc += "**Oop! It seems like the shelves are fully stocked. Hurray!** <:kittycelebrate:835505972952432680>\n\n"
            else:              
                desc += "**" + name + " makes a run for supplies. The stocks are refreshed! <:pandahappy:841009993239101450>**\n\n"
                supply+=1
                marketDict.update({"supplyRunsCounter": supply})
                mod_cc("DT", -1)

            desc += "\n:package: **Supply Runs Completed** :package:\n\n"
            supplyLeftover = maxSupply - supply
            desc += "".join(["⬤" for i in range(0,supply)])
            desc += "".join(["〇" for i in range(0,supplyLeftover)])
            projectedEarnings = int(invested * ((sales + supply) * (1 + 0.5 * (level - 1))/(6 + 4*level) + 0.5))
            marketDict.update({"projectedEarnings":projectedEarnings})
            desc += "\n\n\n**Projected Earnings This Week:** `" + projectedEarnings + "gp`"
            desc += ":chart_with_upwards_trend:" if projectedEarnings > invested else ":chart_with_downwards_trend:"
            desc += "\n\n\n\n**DT Remaining:** "+ cc_str("DT")
    else:
        desc += "**Invalid option!** <:kittydotdotdot:770188345187106866>\n\n"
        desc += "Run `!GuildMarket Help` to see a list of valid !GuildMarket commands"

guildsJson = dump_json(guildsDict)
desc += "\n\n﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌"
return f""" -title "{title}" -desc "{desc}" -footer "Downtime | GuildMarket | RoI" """
</drac2>
!gvar edit {{guildsGvar}} {{guildsJson}}