embed
<drac2>
sm=strengthMod
a1,a2,a3=roll("1d20")+sm, roll("1d20")+sm, roll("1d20")+sm
c1,c2,c3=True if a1-sm==20 else False,True if a2-sm==20 else False,True if a3-sm==20 else False
d1,d2,d3=1 if a1>11 else 2, 1 if a2>11 else 2, 1 if a3>11 else 2
fdr1,fdr2,fdr3=roll("1d6"),roll("1d6"),roll("1d6")
sdr1,sdr2,sdr3=roll("1d6"),roll("1d6"),roll("1d6")
tdr1,tdr2,tdr3=roll("1d6"),roll("1d6"),roll("1d6")
fodr1,fodr2,fodr3=roll("1d6"),roll("1d6"),roll("1d6")
h1,h2,h3=int((fdr1+sdr1+(tdr1+fodr1 if c1 else 0)+strengthMod)/d1), int((fdr2+sdr2+(tdr2+fodr2 if c2 else 0)+strengthMod)/d2), int((fdr3+sdr3+(tdr3+fodr3 if c3 else 0)+strengthMod)/d3)
cs,s,f="*The Greathammer smashes the bell into orbit!* <:kittybanhammer:770160552173240351>","*The Greathammer hits hard and true!* <:kittyamazed:770160347881275393>", "*The Greathammer glances off the side of the target!* <:kittydotdotdot:770188345187106866>"
r1,r2,r3=cs if c1 else s if a1>11 else f, cs if c2 else s if a2>11 else f, cs if c3 else s if a3>11 else f
return f""" -title "{name} swings the Greathammer three times! (DC 12)" -desc "**First swing:**  1d20 ({'**20**' if c1 else '**1**' if a1-sm==1 else a1-sm}) {'+' if sm>-1 else '-'} {abs(sm)} = `{a1}`\n{r1}\n**Damage{' (CRIT!)' if c1 else ''}:**  {'4d6' if c1 else '2d6'} ({fdr1}, {sdr1}{', '+tdr1+', '+fodr1 if c1 else ''})  {'+' if sm>-1 else '-'} {abs(sm)} `{'/ 2' if d1>1 else ''}` = `{h1}`\n\n**Second swing:**  1d20 ({'**20**'  if c2 else '**1**' if a2-sm==1 else a2-sm}) {'+' if sm>-1 else '-'} {abs(sm)} = `{a2}`\n{r2}\n**Damage{' (CRIT!)' if c2 else ''}:**  {'4d6' if c2 else '4d6'} ({fdr2}, {sdr2}{', '+tdr2+', '+fodr2 if c2 else ''})  {'+' if sm>-1 else '-'} {abs(sm)} `{'/ 2' if d2>1 else ''}` = `{h2}`\n\n**Third swing:**  1d20 ({'**20**'  if c3 else '**1**' if a3-sm==1 else a3-sm}) {'+' if sm>-1 else '-'} {abs(sm)} = `{a3}`\n{r3}\n**Damage{' (CRIT!)' if c3 else ''}:**  {'4d6' if c3 else '2d6'} ({fdr3}, {sdr3}{', '+tdr3+', '+fodr3 if c3 else ''}) {'+' if sm>-1 else '-'} {abs(sm)} `{'/ 2' if d3>1 else ''}` = `{h3}`\n\n***Total Damage Dealt:    {h1+h2+h3}*** <:kittycelebrate:835505972952432680>" """
</drac2>