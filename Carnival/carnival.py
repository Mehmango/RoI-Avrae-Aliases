embed
<drac2>
args,result = &ARGS&, "\n"
character().set_cvar_nx("carnivalTickets", 0)
if len(args)==1 and args[0].isnumeric:
    set_cvar("carnivalTickets", int(get("carnivalTickets", 0)) + int(args[0]))
    result += "*Added `" + abs(int(args[0])) + "` to " if int(args[0])>-1 else "*Subtracted `" + abs(int(args[0])) + "` from "
    result += name + "'s total carnival tickets!*"
elif len(args)>0:
    result += "Invalid arguments provided!"
return f""" -title "Carnival Tickets :tickets::tickets::tickets:" -desc "{result}\n\n**{name} now has `{get("carnivalTickets", 0)}` carnival tickets! <:kittywonder:770188525353828353>**" """
</drac2>