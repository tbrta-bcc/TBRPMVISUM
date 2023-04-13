#trip generation
#Chetan Joshi PTV Portland OR 2/28/2022
import numpy as np 
import pandas as pd
import os 
import VisumPy.helpers as h
PRIO = 20480
SCNAME  = Visum.Net.AttValue("SC_NAME")

def calculate_productions(table_name, table_zdata4, table_zdata5):
    # table_name = "COEFF_PRATES"   
    # table_zdata4 = "ZDATA4"
    # table_zdata5 = "ZDATA5"
    PSCALE = ['HBW', 'HBSH', 'HBSR', 'HBSC', 'HBO', 'NHBW', 'NHBO']
    PURPID = dict(Visum.Net.DemandStrata.GetMultipleAttributes(['CODE', 'PURP']))
    AT_SCALE   = Visum.Net.TableDefinitions.ItemByKey("COEFF_AT_PROD").TableEntries.GetMultipleAttributes(["PURPOSE", "AT", "COEFF"])
    RATES_TABLE= Visum.Net.TableDefinitions.ItemByKey(table_name).TableEntries.GetMultipleAttributes(["DSTRATA", "COEFF", "VARCODE"])
    
    # ZDATA = Visum.Net.Zones.GetMultipleAttributes(prod_attrs)
    rates = {}
    for purp, coeff, varcode in RATES_TABLE:
        if purp in rates:
            rates[purp]['coeffs'].append(coeff)
            rates[purp]['varcodes'].append(varcode)
        else:
            rates[purp]={'coeffs': [coeff], 'varcodes': [varcode]}
    
    area_coeff = {}
    for purpid, areatype, coeff in AT_SCALE:
        area_coeff[(purpid, areatype)] = coeff
    
    Visum.Log(PRIO, "Coeffs for  HBW:")
    for vcode, cf in zip(rates['HBW']['varcodes'], rates['HBW']['coeffs']):
        Visum.Log(PRIO,  "{}, -> {}".format(vcode, cf))

    dstrata = {}
    for purp in rates:
        Visum.Log(PRIO, "processing {}".format(purp))
        rattr = "Production({})".format(purp)
        zattrs = rates[purp]['varcodes']
        coeffs = np.array(rates[purp]['coeffs'])   #make it an array just to make sure.
        zdataX = np.array(Visum.Net.Zones.GetMultipleAttributes(zattrs))
        result = np.dot(zdataX, coeffs)

        ATYPES = h.GetMulti(Visum.Net.Zones, "ATYPES")
        if purp in PSCALE:
            for i in range(len(ATYPES)):
                if (PURPID[purp], ATYPES[i]) in area_coeff:
                   result[i] = area_coeff[(PURPID[purp], ATYPES[i])]*result[i]

        h.SetMulti(Visum.Net.Zones, rattr, result)
        purptrips = np.sum(result)
        dstrata[rattr]= purptrips
        Visum.Log(PRIO, "attributes for purpose: {} |-> {}".format(purp, rates[purp]['varcodes']))
        Visum.Log(PRIO, "coeffs for purpose: {} |-> {}".format(purp, rates[purp]['coeffs']))
        Visum.Log(PRIO, "trips for purpose: {} -> {}".format(purp, purptrips))

    # Now do EI productions using ZDATA4 and ZDATA5 cards
    # EIPROD =  dict(Visum.Net.Zones.GetMultipleAttributes(["NO", "Production(EI)"]))
    ZDATA4 =  Visum.Net.TableDefinitions.ItemByKey(table_zdata4).TableEntries.GetMultipleAttributes(["ZONE", "EEPCT", "TRIPS"])
    ZDATA5 =  Visum.Net.TableDefinitions.ItemByKey(table_zdata5).TableEntries.GetMultipleAttributes(["ZONE", "P_OR_A", "PURP", "AUTO_OCC", "PERCENT"])
    PURPCODE= dict(Visum.Net.DemandStrata.GetMultipleAttributes(["PURP", "CODE"]))
    EIPROD = {}
    for zone, eepct, trips in ZDATA4:
        EIPROD[zone] = trips*(100.0-eepct)/100.0

    for zone, pa, purp, auocc, pct in ZDATA5:
        if pa.strip()=='P':
        # if purp == 11 and pa.strip()=='P':
            if zone in EIPROD:
                EITRIPS = auocc*EIPROD[zone]*pct/100
                Visum.Net.Zones.ItemByKey(zone).SetAttValue("Production({})".format(PURPCODE[purp]), EITRIPS)
                dstrata["Production({})".format(PURPCODE[purp])]+=EITRIPS
            else:
                Visum.Log(PRIO, 'zone: {} not found in ZDATA5!'.format(zone))

        if pa.strip()=='T':
        # if purp == 11 and pa.strip()=='P':
            if zone in EIPROD:
                EITRIPS = auocc*EIPROD[zone]*pct/100
                Visum.Net.Zones.ItemByKey(zone).SetAttValue("Production({})".format(PURPCODE[purp]), 0.5*EITRIPS)
                dstrata["Production({})".format(PURPCODE[purp])]+=(0.5*EITRIPS)
            else:
                Visum.Log(PRIO, 'zone: {} not found in ZDATA5!'.format(zone))

    Visum.Log(PRIO, "raw trip productions: " )
    for purp in dstrata:
        Visum.Log(PRIO, "{} -> {}".format(purp, dstrata[purp]))

def set_0C_attractions(purps):
    nzones = Visum.Net.Zones.Count
    attractions = np.zeros((nzones, len(purps)))
    attributes  = []
    for purp in purps:
        attributes.append("Attraction({})".format(purp))
    Visum.Net.Zones.SetMultipleAttributes(attributes, attractions)

def calculate_attractions(table_name, scale=1, skip_purps=[]):
    # table_name = "COEFF_ARATES"   
    PSCALE = ['HBW', 'HBSH', 'HBSR', 'HBSC', 'HBO', 'NHBW', 'NHBO']
    PURPID = dict(Visum.Net.DemandStrata.GetMultipleAttributes(['CODE', 'PURP']))
    AT_SCALE   = Visum.Net.TableDefinitions.ItemByKey("COEFF_AT_ATTR").TableEntries.GetMultipleAttributes(["PURPOSE", "AT", "COEFF"])
    RATES_TABLE= Visum.Net.TableDefinitions.ItemByKey(table_name).TableEntries.GetMultipleAttributes(["DSTRATA", "COEFF", "VARCODE"])
    # ZDATA = Visum.Net.Zones.GetMultipleAttributes(prod_attrs)
    rates = {}
    for purp, coeff, varcode in RATES_TABLE:
        if purp in rates:
            rates[purp]['coeffs'].append(coeff)
            rates[purp]['varcodes'].append(varcode)
        else:
            rates[purp]={'coeffs': [coeff], 'varcodes': [varcode]}

    area_coeff = {}
    for purp, areatype, coeff in AT_SCALE:
        area_coeff[(purp, areatype)] = coeff

    dstrata = []
    for purp in rates:
        if purp in skip_purps:
            Visum.Log(PRIO, "{} skipped...".format(purp))
        else:
            Visum.Log(PRIO, "processing {}".format(purp))
            rattr  = "Attraction({})".format(purp)
            zattrs = rates[purp]['varcodes']
            coeffs = np.array(rates[purp]['coeffs'])   #make it an array just to make sure.
            zdataX = np.array(Visum.Net.Zones.GetMultipleAttributes(zattrs))
            result = np.dot(zdataX, coeffs)
            ATYPES = h.GetMulti(Visum.Net.Zones, "ATYPES")

            if purp in PSCALE:
                for i in range(len(ATYPES)):
                    if (PURPID[purp], ATYPES[i]) in area_coeff:
                        result[i] = area_coeff[(PURPID[purp], ATYPES[i])]*result[i]

            h.SetMulti(Visum.Net.Zones, rattr, scale*result)    # why do we scale attractions? -> because we do:= PANDA1C - PANDA0C so attractions get normalized back
            purptrips = np.sum(result)
            dstrata.append([rattr, purptrips])
            Visum.Log(PRIO, "attributes for purpose: {} |-> {}".format(purp, rates[purp]['varcodes']))
            Visum.Log(PRIO, "coeffs for purpose: {} |-> {}".format(purp, rates[purp]['coeffs']))
            Visum.Log(PRIO, "trips for purpose: {} -> {}".format(purp, purptrips))


    # Now do EI atractions using ZDATA4 and ZDATA5 cards
    ZDATA4 =  Visum.Net.TableDefinitions.ItemByKey(table_zdata4).TableEntries.GetMultipleAttributes(["ZONE", "EEPCT", "TRIPS"])
    ZDATA5 =  Visum.Net.TableDefinitions.ItemByKey(table_zdata5).TableEntries.GetMultipleAttributes(["ZONE", "P_OR_A", "PURP", "AUTO_OCC", "PERCENT"])
    PURPCODE= dict(Visum.Net.DemandStrata.GetMultipleAttributes(["PURP", "CODE"]))
    EIPROD = {}
    for zone, eepct, trips in ZDATA4:
        EIPROD[zone] = trips*(100.0-eepct)/100.0

    for zone, pa, purp, auocc, pct in ZDATA5:
        if pa.strip()=='A':
            if zone in EIPROD:
                EITRIPS = auocc*EIPROD[zone]*pct/100
                Visum.Net.Zones.ItemByKey(zone).SetAttValue("Attraction({})".format(PURPCODE[purp]), EITRIPS)
                Visum.Net.Zones.ItemByKey(zone).SetAttValue("SPEI_{}".format(int(purp)), EITRIPS)
                # dstrata["Production({})".format(PURPCODE[purp])]+=EITRIPS
            else:
                Visum.Log(PRIO, 'zone: {} not found in ZDATA5!'.format(zone))
            
        if pa.strip()=='T':
            if zone in EIPROD:
                EITRIPS = auocc*EIPROD[zone]*pct/100
                Visum.Net.Zones.ItemByKey(zone).SetAttValue("Attraction({})".format(PURPCODE[purp]), 0.5*EITRIPS)
                # dstrata["Production({})".format(PURPCODE[purp])]+=EITRIPS
                Visum.Net.Zones.ItemByKey(zone).SetAttValue("SPEI_{}".format(int(purp)), 0.5*EITRIPS)
            else:
                Visum.Log(PRIO, 'zone: {} not found in ZDATA5!'.format(zone))
    
    Visum.Log(PRIO, "raw trip attractions: " )
    for purp, trips in dstrata:
        Visum.Log(PRIO, "{} -> {}".format(purp, trips))

def calculate_spgen(table_name):
    Visum.Log(PRIO, 'processing special generators...')
    # table_name = "ZDATA3"
    nzones = Visum.Net.Zones.Count
    purp_lookup = dict(Visum.Net.DemandStrata.GetMultipleAttributes(["PURP", "CODE"]))
    iz = {}
    zones = h.GetMulti(Visum.Net.Zones, "NO")
    for i in range(len(zones)):
        iz[zones[i]]=i

    SPGEN_TABLE= Visum.Net.TableDefinitions.ItemByKey(table_name).TableEntries.GetMultipleAttributes(["PURP", "ZONE", "P_OR_A", "OPERAND", "TRIPS_DIFF"])
    spgen = {}
    for purp, zone, pa, op, trips in SPGEN_TABLE:
        if purp in spgen:
            spgen[purp].append([zone, pa, op, trips])
        else:
            spgen[purp]=[[zone, pa, op, trips]]   

    for purp in spgen:
        purpcode = purp_lookup[purp]
        P = h.GetMulti(Visum.Net.Zones, "Production({})".format(purpcode))
        A = h.GetMulti(Visum.Net.Zones, "Attraction({})".format(purpcode))
        SEI=h.GetMulti(Visum.Net.Zones, "SPEI_{}".format(int(purp)))       
        spgen_purp = spgen[purp]
        for zone, pa, op, trips in spgen_purp:
            SEI[iz[zone]] = 0  #clear out any existing old values to avoid double counting.
            if op == '+':
                if pa == 'P':
                    P[iz[zone]]+=trips
                elif pa == 'A':
                    A[iz[zone]]+=trips
                    SEI[iz[zone]]+=trips
                elif pa == 'T':
                    P[iz[zone]]+=trips*0.5
                    A[iz[zone]]+=trips*0.5
                    SEI[iz[zone]]+=trips*0.5
        
            elif op== '-':
                if pa == 'P':
                    P[iz[zone]]-=trips
                elif pa == 'A':
                    A[iz[zone]]-=trips
                    SEI[iz[zone]]-=trips
                elif pa == 'T':
                    P[iz[zone]]-=trips*0.5
                    A[iz[zone]]-=trips*0.5
                    SEI[iz[zone]]-=trips*0.5

            #this options scales trips by a taking TRIPS input as a percentage -> this input scalar should be entered as: 1 + or - (I or R)/100
            elif op== '*':    
                if pa == 'P':
                    P[iz[zone]]*=trips
                elif pa == 'A':
                    A[iz[zone]]*=trips
                    SEI[iz[zone]]*=trips
                elif pa == 'T':
                    P[iz[zone]]*=trips*0.5
                    A[iz[zone]]*=trips*0.5
                    SEI[iz[zone]]*=trips*0.5

            elif op== 'T':
                if pa == 'P':
                    P[iz[zone]]=trips
                elif pa == 'A':
                    A[iz[zone]]=trips
                    SEI[iz[zone]]=trips
                elif pa == 'T':
                    P[iz[zone]]=trips*0.5
                    A[iz[zone]]=trips*0.5
                    SEI[iz[zone]]=trips*0.5

        h.SetMulti(Visum.Net.Zones, "Production({})".format(purpcode), P)
        h.SetMulti(Visum.Net.Zones, "Attraction({})".format(purpcode), A)
        h.SetMulti(Visum.Net.Zones, "SPEI_{}".format(int(purp)), SEI)
    
    Visum.Log(PRIO, 'done processing special generators.')

def balance_AtoP(DStrat, BALZ):
    # DStrats = h.GetMulti(Visum.Net.DemandStrata, "CODE")
    # BALZ is taken as input attribute as used as balancing group ID -> we just call it DISTRICT here
    Visum.Log(PRIO, 'balance generation: {}'.format(DStrat))
    DSLKP= dict(Visum.Net.DemandStrata.GetMultipleAttributes(["CODE", "PURP"]))
    PATT= "Production({})".format(DStrat)
    AATT= "Attraction({})".format(DStrat)
    CATT= "SPEI_{}".format(int(DSLKP[DStrat]))      #ATTR to hold constant -> SPGEN + EI
    NZONES = Visum.Net.Zones.Count
    P = np.array(Visum.Net.Zones.GetMultiAttValues(PATT))[:,1]
    A = np.array(Visum.Net.Zones.GetMultiAttValues(AATT))[:,1]
    SEI=np.array(Visum.Net.Zones.GetMultiAttValues(CATT))[:,1]
    DISTRICT = np.array(Visum.Net.Zones.GetMultiAttValues(BALZ))[:, 1]
    UNQ_DISTR = list(set(DISTRICT))
    DISTRICT_PT = {}
    DISTRICT_AT = {}
    DISTRICT_SEIT = {}
    for DISTR in UNQ_DISTR:
        DISTRICT_PT[DISTR] = 0
        DISTRICT_AT[DISTR] = 0
        DISTRICT_SEIT[DISTR] = 0

    for zn in range(NZONES):
        DISTRICT_PT[DISTRICT[zn]]+=P[zn]
        DISTRICT_AT[DISTRICT[zn]]+=A[zn]
        DISTRICT_SEIT[DISTRICT[zn]]+=SEI[zn]
    
    Visum.Log(PRIO, "Unbalanced district P/A totals and balancing factors")
    balfac = {}
    for D in UNQ_DISTR:
        balfac[D] = (DISTRICT_PT[D]-DISTRICT_SEIT[D])/max(DISTRICT_AT[D]-DISTRICT_SEIT[D], 0.00001)
        Visum.Log(PRIO, "District: {} | Purpose: {} | Production: {} | Attraction: {} | Balancing factor: {}".format(D, DStrat, DISTRICT_PT[D],  DISTRICT_AT[D], balfac[D]))
            
    for zn in range(NZONES):
        A[zn] = balfac[DISTRICT[zn]]*(A[zn]-SEI[zn]) + SEI[zn]
    
    h.SetMulti(Visum.Net.Zones, AATT, A)
    Visum.Log(PRIO, 'done balancing generation: {}'.format(DStrat))

def balance_PtoA(DStrat, BALZ):
    # DStrats = h.GetMulti(Visum.Net.DemandStrata, "CODE")
    # BALZ is taken as input attribute as used as balancing group ID -> we just call it DISTRICT here
    Visum.Log(PRIO, 'balance generation: {}'.format(DStrat))
    PATT="Production({})".format(DStrat)
    AATT="Attraction({})".format(DStrat)
    NZONES = Visum.Net.Zones.Count
    P = np.array(Visum.Net.Zones.GetMultiAttValues(PATT))[:,1]
    A = np.array(Visum.Net.Zones.GetMultiAttValues(AATT))[:,1]
    DISTRICT = np.array(Visum.Net.Zones.GetMultiAttValues(BALZ))[:, 1]
    UNQ_DISTR = list(set(DISTRICT))
    DISTRICT_PT = {}
    DISTRICT_AT = {}
    for DISTR in UNQ_DISTR:
        DISTRICT_PT[DISTR] = 0
        DISTRICT_AT[DISTR] = 0

    for zn in range(NZONES):
        DISTRICT_PT[DISTRICT[zn]]+=P[zn]
        DISTRICT_AT[DISTRICT[zn]]+=A[zn]
    
    Visum.Log(PRIO, "Unbalanced district P/A totals and balancing factors")
    balfac = {}
    for D in UNQ_DISTR:
        balfac[D] = DISTRICT_AT[D]/max(DISTRICT_PT[D], 0.00001)
        Visum.Log(PRIO, "District: {} | Purpose: {} | Production: {} | Attraction: {} | Balancing factor: {}".format(D, DStrat, DISTRICT_PT[D],  DISTRICT_AT[D], balfac[D]))
            
    for zn in range(NZONES):
        P[zn] = P[zn]*balfac[DISTRICT[zn]]
    
    h.SetMulti(Visum.Net.Zones, PATT, P)
    Visum.Log(PRIO, 'done balancing generation: {}'.format(DStrat))

def simple_AtoP(DStrat):
    Visum.Log(PRIO, 'balance generation As to P - {}'.format(DStrat))
    PATT="Production({})".format(DStrat)
    AATT="Attraction({})".format(DStrat)
    NZONES = Visum.Net.Zones.Count
    P = np.array(Visum.Net.Zones.GetMultiAttValues(PATT))[:,1]
    A = np.array(Visum.Net.Zones.GetMultiAttValues(AATT))[:,1]
    Ptotal = np.sum(P)
    Atotal = np.sum(A)
    balfac = Ptotal / Atotal 
    A = balfac*A 
    h.SetMulti(Visum.Net.Zones, AATT, A)

def set_PtoA(DStrat):
    fac=1.0
    # if DStrat=='TAXI':
    #     fac=0.5
    Visum.Log(PRIO, 'balance (set P to A) generation: {}'.format(DStrat))
    AATTS=np.array(h.GetMulti(Visum.Net.Zones, "Attraction({})".format(DStrat)))
    h.SetMulti(Visum.Net.Zones, "Production({})".format(DStrat), fac*AATTS)
    h.SetMulti(Visum.Net.Zones, "Attraction({})".format(DStrat), fac*AATTS)

def balance_trips_0C():
    # DStratsPara = Visum.Net.DemandStrata.GetMultipleAttributes(["CODE", "BALDIR"])
    DStrats = ['HBW', 'HBSH', 'HBSR', 'HBSC', 'HBO', 'AIRP', 'COL']
    BALZATT = ['BALZ_HBW', 'BALZ_HBSH', 'BALZ_HBSR', 'BALZ_HBSC', 'BALZ_HBO', 'BALZ_AIRPORT', 'BALZ_COLLEGE']
    for dstrat, balz in zip(DStrats, BALZATT):
        balance_AtoP(dstrat, balz)

def balance_trips_1C():
    DStratsPara = Visum.Net.DemandStrata.GetMultipleAttributes(["CODE", "BALDIR", "BALZATTR"])
    for dstrat, baldir, balzatt in DStratsPara:
        if baldir == 1:
            balance_AtoP(dstrat, balzatt)
        elif baldir == 2:
            set_PtoA(dstrat) #, BALZATTR)
        elif baldir == 3:
            balance_PtoA(dstrat, balzatt)
        elif baldir == 4:
            simple_AtoP(dstrat)

def export_gen_result(fname):
    zattrs = [] #["NO"]
    DStratsPara = Visum.Net.DemandStrata.GetMultipleAttributes(["CODE", "BALDIR"])
    for code, baldir in DStratsPara:
        zattrs.append("Production({})".format(code))
        zattrs.append("Attraction({})".format(code))
    
    df = pd.DataFrame(data=Visum.Net.Zones.GetMultipleAttributes(zattrs), columns=zattrs)
    df.to_csv(fname, index=False)

def clear_gen_result():
    zattrs = []
    DStratsPara = Visum.Net.DemandStrata.GetMultipleAttributes(["CODE", "BALDIR"])
    for code, baldir in DStratsPara:
        zattrs.append("Production({})".format(code))
        zattrs.append("Attraction({})".format(code))
    
    PANDA = np.zeros((Visum.Net.Zones.Count, len(zattrs)))
    Visum.Net.Zones.SetMultipleAttributes(zattrs, PANDA)


def update_panda():
    fnam0=os.path.join(Visum.GetPath(2), "outputs\\{}\\panda\\PANDA_0C.csv".format(SCNAME))
    fnam1=os.path.join(Visum.GetPath(2), "outputs\\{}\\panda\\PANDA_1C.csv".format(SCNAME))
    PANDA_0C = pd.read_csv(fnam0)
    PANDA_1C = pd.read_csv(fnam1)
    base, actual = Visum.Net.TableDefinitions.ItemByKey("EMP_ADJ").TableEntries.GetMultipleAttributes(["BASEEMP", "ACTUALEMP"])[0]
    ADJ_FAC = actual / base
    PANDA_1C["Production(HBW)"] = ADJ_FAC*PANDA_1C["Production(HBW)"]
    PANDA_1C["Attraction(HBW)"] = ADJ_FAC*PANDA_1C["Attraction(HBW)"]
    PANDA_0C["Attraction(HBW)"] = PANDA_1C["Attraction(HBW)"]
    ProdXX   = PANDA_0C.columns.to_list()
    for p in ProdXX:
        if p.startswith("Attraction"):
            ProdXX.remove(p)     
            
    for prod_attr in ProdXX:
        PANDA_1C[prod_attr] = np.maximum(0, PANDA_1C[prod_attr]-PANDA_0C[prod_attr])
    # Visum.Log(PRIO, "PANDA_1C -> {}".format(PANDA_1C.head()))
    PANDA_1C.to_csv(fnam1, index=False)  # re-write the file with updated values...
    PANDA_0C.to_csv(fnam0, index=False)


#----1-CAR Generation--------------------------------------------------------#
#1+car demand strata
Visum.Log(PRIO, "start: 1+ car trip generation")
clear_gen_result()
ptable_name = "COEFF_PRATES"   
table_zdata4= "ZDATA4"
table_zdata5= "ZDATA5"
calculate_productions(ptable_name, table_zdata4, table_zdata5)

atable_name = "COEFF_ARATES"
calculate_attractions(atable_name)

stable_name = "ZDATA3"
calculate_spgen(stable_name)

Visum.Log(PRIO, "note: balance 1+ car trip generation")
balance_trips_1C()

Visum.Log(PRIO, "note: export 1+ car trip generation to disk")

fname=os.path.join(Visum.GetPath(2), "outputs\\{}\\panda\\PANDA_1C.csv".format(SCNAME))
export_gen_result(fname)

Visum.Log(PRIO, "end: 1+ car trip generation")

#------------------------0-car demand strata---------------------------------#
Visum.Log(PRIO, "start: 0-car trip generation")
# clear_gen_result()
ptable_name = "COEFF_0CPRATES"   
table_zdata4= "ZDATA4_0C"
table_zdata5= "ZDATA5"
calculate_productions(ptable_name, table_zdata4, table_zdata5)
dstrats = ["AIRP", "COL", "EI", "NHBW", "NHBO", "LTRK", "HTRK", "TAXI"]
set_0C_attractions(dstrats)
# BASED ON DISCUSSION - 0-CAR ATTRACTIONS ARE NOT BALANCED
# atable_name = "COEFF_ARATES"
# calculate_attractions(atable_name, skip_purps=["COL", "NHBW", "NHBO", "LTRK", "HTRK", "TAXI", "EI"])
# stable_name = "ZDATA3_0C"
# calculate_spgen(stable_name)
# balance_trips_0C()
Visum.Log(PRIO, "note: export 0-car trip generation to disk")
fname=os.path.join(Visum.GetPath(2), "outputs\\{}\\panda\\PANDA_0C.csv".format(SCNAME))
export_gen_result(fname)

Visum.Log(PRIO, "end: 0-car trip generation")

##-------update and write back to file---------##
update_panda()

Visum.Log(PRIO, "note: update PANDA for 1C")




