import os
from PIL import Image, ImageDraw, ImageFont
W,H=1024,1024; BG=(247,242,231); INK=(20,20,20); RED=(178,34,34); NAVY=(24,48,84); CREAM=(255,251,240); GREY=(90,90,90); GREEN=(34,120,60); BLUE=(30,90,160); ORANGE=(200,110,20)
def F(sz,b=False,serif=False):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if serif and b else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if b else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try: return ImageFont.truetype(p,sz)
    except Exception: return ImageFont.load_default()
def wrap(d,t,f,w):
    words=t.split(); lines=[]; cur=""
    for wd in words:
        s=(cur+" "+wd).strip()
        if d.textlength(s,font=f)<=w: cur=s
        else:
            if cur: lines.append(cur)
            cur=wd
    if cur: lines.append(cur)
    return lines
def txt(d,x,y,s,f,fill=INK,anchor="la"):
    d.text((x,y),s,font=f,fill=fill,anchor=anchor)
def chip(d,x,y,label,col):
    f=F(7,True); w=d.textlength(label,font=f)+10; d.rounded_rectangle([x,y,x+w,y+13],radius=3,fill=col); d.text((x+5,y+2),label,font=f,fill=(255,255,255)); return w+4
def scene(d,x,y,w,h,kind):
    d.rectangle([x,y,x+w,y+h],fill=(30,50,80) if kind in ("tower","court","drones") else (70,110,140) if kind in ("ship","rocket") else (90,60,40) if kind=="desert" else (40,80,60) if kind=="trophy" else (120,90,60))
    d.ellipse([x+w-28,y+6,x+w-8,y+26],fill=(240,200,90) if kind!="tower" else (220,220,220))
    if h<50:
        d.rectangle([x,y+h-8,x+w,y+h],fill=(40,60,40)); d.rectangle([x+12,y+10,x+44,y+h-8],fill=(240,240,230)); d.rectangle([x+52,y+16,x+84,y+h-8],fill=(200,170,60)); d.polygon([(x+96,y+h-8),(x+112,y+10),(x+128,y+h-8)],fill=(30,30,30)); return
    if kind=="tower":
        d.rectangle([x+18,y+28,x+52,y+h],fill=(60,70,90)); d.rectangle([x+58,y+12,x+92,y+h],fill=(40,50,70)); d.rectangle([x+58,y+12,x+92,y+22],fill=(200,180,60))
        for i in range(5): d.rectangle([x+62,y+28+i*12,x+88,y+34+i*12],fill=(255,220,120))
        d.ellipse([x+100,y+18,x+130,y+48],fill=(255,140,40)); d.ellipse([x+108,y+24,x+124,y+42],fill=(255,200,80)); d.polygon([(x+150,y+30),(x+170,y+38),(x+150,y+46)],fill=(30,30,30)); d.rectangle([x,y+h-14,x+w,y+h],fill=(20,20,20))
    elif kind=="gate":
        d.rectangle([x+10,y+30,x+w-10,y+h],fill=(150,40,40)); d.rectangle([x+w//2-22,y+48,x+w//2+22,y+h],fill=(30,30,30)); d.rectangle([x+14,y+34,x+w-14,y+42],fill=(200,170,60)); d.rectangle([x+30,y+60,x+70,y+78],fill=(240,240,230)); d.text((x+32,y+62),"CCDI",font=F(9,True),fill=(150,40,40))
    elif kind=="court":
        d.rectangle([x+14,y+34,x+w-14,y+h],fill=(200,190,170)); d.polygon([(x+20,y+34),(x+w//2,y+8),(x+w-20,y+34)],fill=(120,30,30)); d.rectangle([x+w//2-4,y+40,x+w//2+4,y+70],fill=(240,240,240)); d.ellipse([x+w//2-18,y+66,x+w//2+18,y+76],fill=(200,170,60))
    elif kind=="drones":
        d.rectangle([x,y+h-16,x+w,y+h],fill=(30,30,30))
        for i,(bx,by) in enumerate([(20,20),(70,14),(120,24)]): d.polygon([(bx,by),(bx+14,by+5),(bx,by+10)],fill=(200,200,200)); d.ellipse([x+bx+4,y+by+2,x+bx+10,y+by+8],fill=(255,80,40))
        d.rectangle([x+140,y+40,x+170,y+h-16],fill=(60,60,60))
    elif kind=="trophy":
        d.ellipse([x+w//2-16,y+14,x+w//2+16,y+46],fill=(230,190,60)); d.rectangle([x+w//2-6,y+44,x+w//2+6,y+62],fill=(200,170,50)); d.rectangle([x+w//2-20,y+62,x+w//2+20,y+70],fill=(180,150,40)); d.rectangle([x+8,y+70,x+40,y+78],fill=(0,120,60)); d.rectangle([x+w-40,y+70,x+w-8,y+78],fill=(200,40,40))
    elif kind=="ship":
        d.rectangle([x,y+h-22,x+w,y+h],fill=(30,90,140)); d.rectangle([x+20,y+52,x+w-20,y+66],fill=(180,60,40)); d.rectangle([x+40,y+38,x+70,y+52],fill=(240,240,240)); d.rectangle([x+80,y+44,x+120,y+52],fill=(240,200,60)); d.polygon([(x+150,y+20),(x+160,y+34),(x+140,y+34)],fill=(255,120,40))
    elif kind=="chart":
        d.rectangle([x,y+h-14,x+w,y+h],fill=(20,20,20)); d.line([(x+10,y+h-24),(x+60,y+44),(x+110,y+50),(x+170,y+14)],fill=(40,180,80),width=4); d.text((x+12,y+10),"50,018",font=F(13,True),fill=(255,255,255))
    elif kind=="data":
        d.rectangle([x+10,y+30,x+40,y+h-10],fill=(40,40,50)); d.rectangle([x+50,y+20,x+80,y+h-10],fill=(60,60,70)); d.ellipse([x+100,y+18,x+150,y+58],fill=(220,40,40)); d.text((x+108,y+30),"CODE",font=F(9,True),fill=(255,255,255))
    elif kind=="heli":
        d.ellipse([x+40,y+34,x+110,y+56],fill=(80,90,80)); d.line([(x+20,y+30),(x+130,y+30)],fill=(40,40,40),width=3); d.rectangle([x+110,y+42,x+140,y+50],fill=(80,90,80)); d.polygon([(x+20,y+56),(x+60,y+h-8),(x+100,y+56)],fill=(60,70,60))
    elif kind=="shop":
        d.rectangle([x+10,y+40,x+w-10,y+h],fill=(200,170,120)); d.rectangle([x+30,y+52,x+w-30,y+64],fill=(40,120,80)); d.text((x+34,y+54),"SUPERMARKET",font=F(8,True),fill=(255,255,255)); d.rectangle([x+40,y+68,x+60,y+88],fill=(30,30,30)); d.rectangle([x+80,y+68,x+100,y+88],fill=(30,30,30))
    elif kind=="desert":
        d.ellipse([x+20,y+16,x+52,y+48],fill=(250,200,90)); d.polygon([(x,y+h),(x+60,y+44),(x+120,y+h)],fill=(180,140,80)); d.polygon([(x+80,y+h),(x+150,y+52),(x+w,y+h)],fill=(160,120,70))
    elif kind=="truck":
        d.rectangle([x+16,y+52,x+90,y+72],fill=(200,80,40)); d.rectangle([x+92,y+58,x+130,y+72],fill=(40,80,140)); d.ellipse([x+30,y+70,x+48,y+84],fill=(20,20,20)); d.ellipse([x+104,y+70,x+122,y+84],fill=(20,20,20))
    elif kind=="rocket":
        d.polygon([(x+w//2,y+10),(x+w//2+12,y+44),(x+w//2-12,y+44)],fill=(240,240,240)); d.ellipse([x+w//2-5,y+22,x+w//2+5,y+32],fill=(60,140,200)); d.polygon([(x+w//2-12,y+44),(x+w//2-22,y+62),(x+w//2-8,y+56)],fill=(220,60,40)); d.polygon([(x+w//2+12,y+44),(x+w//2+22,y+62),(x+w//2+8,y+56)],fill=(220,60,40)); d.ellipse([x+w//2-8,y+62,x+w//2+8,y+78],fill=(255,160,40))
    else:
        d.rectangle([x+14,y+20,x+w-14,y+h-10],fill=(220,220,210)); d.text((x+18,y+30),"NEWS",font=F(12,True),fill=NAVY)
HEROES=[("1 RIYADH","MIDDLE EAST","CONFIRMED",GREEN,"Houthi drone hits Riyadh's tallest tower again, 11 hurt","A Houthi drone struck the PIF tower, Riyadh's tallest, for the second time in a week, injuring 11 people.","Saudi officials","tower"),("2 SHANGHAI","ASIA","OFFICIAL",BLUE,"China probes Shanghai party chief Chen Jining","Chen Jining, 62, the Shanghai party chief, is probed for serious violations, the fourth Politburo member to fall.","CCDI","gate"),("3 NEW YORK","US/TECH","CONFIRMED",GREEN,"Huawei guilty on 10 of 12 counts","A US jury found Huawei guilty on 10 of 12 counts of trade-secret theft and bank fraud, clearing it of racketeering.","US court","court")]
CARDS=[("4 ZAPORIZHZHIA","EUROPE/WAR","REPORTED",GREY,"Russian attacks kill 9 across Ukraine in a day","Russia launched 96 drones at Ukraine and 73 were shot down or jammed, with 9 killed and 81 wounded in a day.","Kyiv officials","drones"),("5 CAS","AFRICA/SPORT","OFFICIAL",BLUE,"CAS hands Senegal back the AFCON title","CAS restored Senegal as African champions after Morocco forfeited 3-0, turning the final into a 1-0 win for Senegal.","CAS","trophy"),("6 HORMUZ","MIDDLE EAST","REPORTED",GREY,"IRGC attacks container ship in Hormuz","An IRGC attack hit a container ship in Hormuz at 18:58 UTC, disabling navigation near Khasab, Oman.","UKMTO","ship"),("7 NEW YORK","WORLD/MARKETS","CONFIRMED",GREEN,"Dow closes above 50,000 for the first time","The Dow closed at 50,018, its first finish above 50,000, while the Nasdaq fell 1.5% and the Taiex hit a record 40,122.","Market close","chart"),("8 REDMOND","WORLD/TECH","REPORTED",GREY,"Microsoft declares 'Code Red' after historic outage","After a 24-hour outage, the worst in Exchange Online history, Microsoft set a one-hour recovery target.","Reuters","data"),("9 ESKISEHIR","EUROPE","REPORTED",GREY,"Turkish military helicopter crash kills 5","A Turkish military AS-532 helicopter crashed at Eskisehir at 19:52 UTC, killing all 5 people on board.","Turkish officials","heli"),("10 CARTAGENA","AMERICAS","REPORTED",GREY,"Supermarket hostages: 25 held in Cartagena","Gunmen held 25 hostages in a Cartagena supermarket, freeing 5 elderly women, as landings were suspended.","Colombian officials","shop"),("11 ADEN","MIDDLE EAST","REPORTED",GREY,"Houthis advance within 60 km of Aden","Houthi forces advanced to within 60 km of Aden, Yemen, at 16:51 UTC.","Wires","desert"),("12 LAHJ","MIDDLE EAST","REPORTED",GREY,"Saudi strikes kill 25, wound 6 in Yemen","Saudi strikes on a bus and truck in Wadi Maabaq, Lahj, killed or left missing 25 people and wounded 6.","Yemeni officials","truck"),("13 JIUQUAN","WORLD/SPACE","OFFICIAL",BLUE,"China names first foreign astronaut for Tiangong","China named the Shenzhou-24 crew with Pakistan's Zeeshan Ali, the first foreign astronaut on Tiangong.","CMSA","rocket")]
ALSO=["14 Ankara: Haftar visits Turkey for the first time.","15 London: UK sanctions Houthis + 4 officials.","16 Villavicencio: Car bomb injures 23.","17 Gaza: Israel kills Hamas internal security chief.","18 Baghdad: Iraq orders federal control of Kurdish oilfields + crossings.","19 Gaza: Meningitis epidemic alert as 272 cases hit in October.","20 DR Congo: Missing Cessna 208, rebels claim shootdown.","21 Hanoi: Hot-pot explosion kills at least 6.","22 Gulf of Finland: Ukraine hits Russian ship Sparta II.","23 Kuala Lumpur: Malaysia to return thousands of migrants to Myanmar.","24 Ulleungdo: S. Korea shelter order as Russian jets enter ADIZ.","25 Dhaka: Hasina plans return 16 Dec.","26 The Hague: 14 nations endorse ICJ Myanmar ruling.","27 Jakarta: Indonesia nominates 2 VP candidates.","28 Beijing: China sentences official Ma to death for spying.","29 Brussels: NATO vows defence against space threat.","30 Mexico City: El Chapo Isidro captured Fri 20 Nov; US drone aided capture.","31 San Salvador: Bukele names 3 Salvadoran soldiers killed in Haiti.","32 Ottawa: Pentagon rebukes Canada as only 41.9% of air fleet ready.","33 Washington: US adds Megaspeed to trade blacklist.","34 Kyiv: Zelensky urges Ukraine/Russia/US/Europe talks soon.","35 Ras Al Khaimah: UAE bus-truck crash kills 13.","36 London: England record 5,258 heat deaths, summer 2026.","37 Kourou: Ariane 6 lofts 36 Amazon satellites.","38 Cikande: Factory-fire toll rises to 26."]
UTC=[("02:15","NATO space defence"),("08:16","Hanoi blast"),("10:42","Saudi strikes Yemen"),("14:27","Riyadh tower hit"),("16:51","Houthis near Aden"),("18:58","Hormuz ship attack"),("20:41","Huawei guilty")]
NUMS=[("11","hurt in Riyadh"),("9","killed in Ukraine"),("50,018","Dow close"),("+8.99%","Taiex record"),("25","killed or missing in Yemen"),("26","Cikande toll")]

CONT=[ [(-168,66),(-165,60),(-155,58),(-145,60),(-135,58),(-128,52),(-124,42),(-120,34),(-114,29),(-108,24),(-102,18),(-95,16),(-88,14),(-83,9),(-79,8),(-82,11),(-86,13),(-90,14),(-91,19),(-96,19),(-97,26),(-93,30),(-88,30),(-83,30),(-80,26),(-79,33),(-75,36),(-74,40),(-70,42),(-67,45),(-60,47),(-55,47),(-59,50),(-64,58),(-68,58),(-75,62),(-82,66),(-90,69),(-100,68),(-115,68),(-130,70),(-145,70),(-158,71),(-166,68)], [(-80,9),(-77,4),(-80,-3),(-81,-6),(-77,-12),(-73,-18),(-70,-23),(-70,-30),(-73,-37),(-74,-44),(-74,-50),(-70,-54),(-66,-55),(-64,-49),(-60,-42),(-55,-35),(-49,-28),(-41,-23),(-39,-16),(-35,-8),(-37,-4),(-42,-2),(-48,0),(-52,4),(-58,6),(-63,10),(-68,11),(-73,12),(-78,10)], [(-9,43),(-9,37),(-5,36),(-1,37),(2,39),(4,42),(8,44),(11,44),(14,42),(18,40),(16,42),(12,45),(7,44),(2,43),(-2,44),(-2,48),(0,49),(3,51),(6,54),(8,57),(10,59),(6,60),(6,58),(11,58),(14,56),(18,56),(21,55),(24,58),(21,61),(18,63),(24,68),(30,70),(31,68),(28,65),(24,62),(20,58),(16,54),(12,54),(9,55)], [(-17,15),(-16,21),(-14,28),(-9,32),(-5,35),(1,36),(10,37),(12,34),(18,32),(25,32),(31,31),(33,28),(36,22),(38,17),(41,13),(48,11),(51,11),(51,7),(47,2),(42,-2),(40,-9),(36,-18),(32,-27),(27,-34),(19,-35),(16,-31),(13,-20),(12,-13),(10,-4),(9,4),(5,6),(-3,5),(-9,5),(-14,8),(-17,12)], [(30,70),(38,68),(45,68),(55,69),(65,69),(75,73),(85,74),(95,76),(105,77),(115,74),(125,72),(135,72),(145,72),(155,70),(162,66),(170,66),(178,65),(172,62),(162,60),(158,53),(150,59),(142,54),(141,46),(138,39),(134,34),(130,33),(127,36),(126,40),(121,38),(120,31),(121,26),(116,23),(110,20),(108,16),(105,10),(102,7),(99,9),(97,15),(93,18),(90,22),(87,21),(83,17),(80,13),(80,8),(76,9),(73,16),(69,21),(64,25),(58,26),(55,27),(52,28),(50,30),(48,30),(43,29),(41,22),(43,15),(45,12),(50,15),(55,17),(58,22),(57,26),(54,26),(51,28),(48,30),(44,30),(40,32),(36,36),(33,39),(30,42),(28,46),(27,52),(28,58)], [(113,-22),(114,-30),(120,-35),(128,-33),(136,-35),(142,-38),(148,-39),(150,-37),(153,-28),(149,-22),(146,-19),(142,-11),(137,-12),(132,-12),(126,-14),(122,-17),(118,-20),(113,-22)] ]
PINS=[(1,46.7,24.7,0,-13),(2,121.5,31.2,0,-13),(3,-74.0,40.7,-17,-12),(4,35.2,47.8,0,-13),(5,-17.4,14.7,-12,10),(6,56.3,26.5,12,-10),(7,-74.0,40.7,17,11),(8,-122.1,47.7,-10,0),(9,30.5,39.8,0,13),(10,-75.5,10.4,-13,9),(11,45.0,12.8,-15,-12),(12,44.9,13.0,15,11),(13,98.5,39.8,0,-13)]
def main():
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im); d.rectangle([0,0,W,10],fill=RED)
    txt(d,16,16,"THE WORLD ON ONE DAY",F(11,True),RED); txt(d,1008,16,"38 STORIES · 6 REGIONS · 13 FIELDS",F(11,True),INK,anchor="ra")
    txt(d,16,34,"Tuesday 24 November 2026",F(34,True,True),INK); txt(d,1008,44,"ONE DAY OF WORLD NEWS, ONE PICTURE",F(10,True),GREY,anchor="ra")
    txt(d,16,76,"Riyadh tower hit again  ·  Shanghai party chief probed  ·  Huawei guilty on 10 of 12 counts",F(12,False,True),RED)
    d.rectangle([16,98,1008,120],fill=NAVY); txt(d,24,104,"Europe 9  ·  Middle East 8  ·  Asia 8  ·  Africa 2  ·  Americas 7  ·  World/Space 4",F(11,True),(255,255,255))
    txt(d,16,126,"THE DAY IN UTC",F(9,True),RED); ux=16
    for t,ev in UTC:
        txt(d,ux,140,t,F(9,True),RED); txt(d,ux+36,141,ev,F(8),INK); ux+=143
    d.line([(16,156),(1008,156)],fill=(180,180,180),width=1); nx=16
    for n,lab in NUMS:
        txt(d,nx,162,n,F(14,True),INK); txt(d,nx,180,lab,F(8),GREY); nx+=166
    hy=190; hw=325; hg=182
    for i,(num,loc,chip_lab,col,head,deck,src,kind) in enumerate(HEROES):
        x=16+i*(hw+8); d.rectangle([x,hy,x+hw,hy+hg],outline=(150,150,150),width=1,fill=CREAM); scene(d,x+1,hy+1,hw-2,78,kind)
        txt(d,x+8,hy+82,num+" "+loc,F(10,True),RED); chip(d,x+8,hy+96,chip_lab,col); yy=hy+112
        for ln in wrap(d,head,F(12,True),hw-16)[:2]: txt(d,x+8,yy,ln,F(12,True),INK); yy+=14
        for ln in wrap(d,deck,F(9),hw-16)[:2]: txt(d,x+8,yy,ln,F(9),INK); yy+=12
        txt(d,x+8,hy+hg-14,"("+src+")",F(8),GREY)
    cy=hy+hg+8; cw=192; ch=122
    for i,(num,loc,chip_lab,col,head,deck,src,kind) in enumerate(CARDS):
        r,c=divmod(i,5); x=16+c*(cw+8); y=cy+r*(ch+8); d.rectangle([x,y,x+cw,y+ch],outline=(150,150,150),width=1,fill=CREAM); scene(d,x+1,y+1,cw-2,32,kind)
        txt(d,x+6,y+38,num+" "+loc,F(7,True),RED); chip(d,x+6,y+50,chip_lab,col); yy=y+66
        for ln in wrap(d,head,F(9,True),cw-12)[:2]: txt(d,x+6,yy,ln,F(9,True),INK); yy+=11
        for ln in wrap(d,deck,F(8),cw-12)[:3]: txt(d,x+6,yy,ln,F(8),INK); yy+=10
    my=cy+2*ch+8; txt(d,16,my,"THE WORLD — 13 STORIES PINNED",F(10,True),RED); txt(d,1008,my,"Pins 1-13 = stories 1-13",F(8),GREY,anchor="ra")
    mx0,my0,mx1,my1=16,my+18,1008,my+164; d.rectangle([mx0,my0,mx1,my1],fill=(215,232,240),outline=(150,150,150))
    def XY(lon,lat): return (mx0+(lon+180)/360*(mx1-mx0), my0+(83-lat)/139*(my1-my0))
    for poly in CONT: d.polygon([XY(lo,la) for lo,la in poly],fill=(198,220,178),outline=(120,140,110))
    d.text((XY(-100,55)[0],XY(-100,55)[1]),"NORTH AMERICA",font=F(7,True),fill=GREY); d.text((XY(-60,-15)[0],XY(-60,-15)[1]),"SOUTH AMERICA",font=F(7,True),fill=GREY); d.text((XY(15,52)[0],XY(15,52)[1]),"EUROPE",font=F(7,True),fill=GREY); d.text((XY(20,5)[0],XY(20,5)[1]),"AFRICA",font=F(7,True),fill=GREY); d.text((XY(95,45)[0],XY(95,45)[1]),"ASIA",font=F(7,True),fill=GREY); d.text((XY(134,-25)[0],XY(134,-25)[1]),"AUSTRALIA",font=F(7,True),fill=GREY)
    for n,lon,lat,dx,dy in PINS:
        px,py=XY(lon,lat); d.ellipse([px-2,py-2,px+2,py+2],fill=INK); qx,qy=px+dx,py+dy; d.line([(px,py),(qx,qy)],fill=RED,width=1); d.ellipse([qx-8,qy-8,qx+8,qy+8],fill=RED,outline=(255,255,255)); d.text((qx,qy),str(n),font=F(8,True),fill=(255,255,255),anchor="mm")
    ay=my1+10; txt(d,16,ay,"ALSO ON TUESDAY 24 NOVEMBER — 25 MORE STORIES",F(10,True),RED); cols=[ALSO[0:9],ALSO[9:18],ALSO[18:25]]; maxyy=ay+18
    for ci,col in enumerate(cols):
        yy=ay+18
        for item in col:
            for ln in wrap(d,item,F(8),318): txt(d,16+ci*331,yy,ln,F(8),INK); yy+=11
        maxyy=max(maxyy,yy)
    dy=maxyy+6; d.rectangle([16,dy,1008,dy+62],fill=(255,235,235),outline=RED,width=1); txt(d,24,dy+5,"DATE CHECK",F(10,True),RED)
    txt(d,24,dy+19,"Every story above happened or was first reported on Tuesday 24 November 2026. Wires read up to 23:00 UTC.",F(8),INK); yy=dy+31
    for ln in wrap(d,"LEFT OUT (not 24 Nov): Hormuz mine claims (23 Nov), Nvidia Huang returns as CEO (23 Nov), EU 22nd sanctions package (23 Nov), COP31 ends with no deal (22 Nov), Merkury corvette sinks (22 Nov), El Chapo Isidro arrested (Fri 20 Nov), Cikande factory fire starts (Sat 21 Nov), Trump hush-money appeal ruling (23 Nov), ATP Finals (22 Nov), F1 Las Vegas GP (Sat 21 Nov).",F(8),960): txt(d,24,yy,ln,F(8),INK); yy+=11
    txt(d,24,yy,"NOT YET: Shenzhou-24 launch (Wed 25 Nov 00:18 UTC), MPR session to pick VP (11 Dec), Huawei sentencing (Sep 2027), Hasina returns to Bangladesh (16 Dec).",F(8),INK)
    fy=dy+68; txt(d,16,fy,"Sources: Reuters · AP · AFP · UKMTO · CCDI · CMSA · CAS · Saudi officials · wires.",F(8),GREY); txt(d,16,fy+11,"CONFIRMED = 2+ outlets · OFFICIAL = on record · REPORTED = one outlet · CLAIM = one side's claim. Scenes are drawn illustrations, not photographs.",F(8),GREY)
    out=os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR","out"),"entry.png"); os.makedirs(os.path.dirname(out) or ".",exist_ok=True); im.save(out,optimize=True)
if __name__=="__main__": main()
