#allocate area type to links from nearest zone
import numpy as np 
import pandas as pd
import os 
import VisumPy.helpers as h
PRIO = 20480
SCNAME  = Visum.Net.AttValue("SC_NAME")

def update_panda():
    fnam0=os.path.join(Visum.GetPath(2), "outputs\\{}\\panda\\PANDA_0C.csv".format(SCNAME))
    fnam1=os.path.join(Visum.GetPath(2), "outputs\\{}\\panda\\PANDA_1C.csv".format(SCNAME))
    PANDA_0C = pd.read_csv(fnam0)
    PANDA_1C = pd.read_csv(fnam1)
    ProdXX   = PANDA_0C.columns.to_list()
    for p in ProdXX:
        if p.startswith("Attraction"):
            ProdXX.remove(p)
            
    PANDA_1C = np.maximum(0, PANDA_1C.subtract(PANDA_0C, axis=ProdXX))
    # Visum.Log(PRIO, "PANDA_1C -> {}".format(PANDA_1C.head()))
    PANDA_1C.to_csv(fnam1)  # re-write the file with updated values...

def split_panda(fnam0, fnam0cpk, fnam0cop):
    # fnam0=r"C:\Projects\florida_D7\model\outputs\\panda\\{}\PANDA_0C.csv"
    # fnam0cpk=r"C:\Projects\florida_D7\model\outputs\\panda\\{}\PANDA_0C_PK.csv"
    # fnam0cop=r"C:\Projects\florida_D7\model\outputs\\panda\\{}\PANDA_0C_OP.csv"

    table_name = 'TODFACTORS'
    cnty = {1:'HI', 2:'PI', 3:'OT'}
    #split panda into PK and OP
    nzones = Visum.Net.Zones.Count
    todfactors = dict(Visum.Net.TableDefinitions.ItemByKey(table_name).TableEntries.GetMultipleAttributes(["SEGMENT", "FACTOR"]))
    zncnty= h.GetMulti(Visum.Net.Zones, "COUNTY") 
    #split 0-car hh 
    Visum.Log(PRIO, "Get PANDA_XC from file...")
    PANDA_0C = pd.read_csv(fnam0)
    zattrs = PANDA_0C.columns.to_list()
    Visum.Net.Zones.SetMultipleAttributes(zattrs, PANDA_0C.to_numpy())
    Visum.Log(PRIO, "Set PANDA_XC from file.")
    DStratNoCounty = ['LTRK', 'HTRK', 'TAXI', 'EI', 'AIRP', 'COL']
    DStratsPara = Visum.Net.DemandStrata.GetMultipleAttributes(["CODE", "BALDIR"])
    for dstrat, bdir in DStratsPara:
        if dstrat in DStratNoCounty:
            pkfac = todfactors[dstrat+"-PK"]
            P = np.array(h.GetMulti(Visum.Net.Zones, "Production({})".format(dstrat)))
            A = np.array(h.GetMulti(Visum.Net.Zones, "Attraction({})".format(dstrat)))
            h.SetMulti(Visum.Net.Zones, "Production({})".format(dstrat), pkfac*P)
            h.SetMulti(Visum.Net.Zones, "Attraction({})".format(dstrat), pkfac*A)
        else:
            P = np.array(h.GetMulti(Visum.Net.Zones, "Production({})".format(dstrat)))
            A = np.array(h.GetMulti(Visum.Net.Zones, "Attraction({})".format(dstrat)))
            # pkfacs = np.zeros(nzones)
            for i in range(nzones):
                if zncnty[i]==1:
                    P[i] = P[i]*todfactors[dstrat+"-PK-HI"]
                    A[i] = A[i]*todfactors[dstrat+"-PK-HI"]
                elif zncnty[i]==2:
                    P[i] = P[i]*todfactors[dstrat+"-PK-PI"]
                    A[i] = A[i]*todfactors[dstrat+"-PK-PI"]
                else:
                    P[i] = P[i]*todfactors[dstrat+"-PK-OT"]
                    A[i] = A[i]*todfactors[dstrat+"-PK-OT"]
            h.SetMulti(Visum.Net.Zones, "Production({})".format(dstrat), P)
            h.SetMulti(Visum.Net.Zones, "Attraction({})".format(dstrat), A)
    
    PANDA_0C_PK = pd.DataFrame(data=Visum.Net.Zones.GetMultipleAttributes(zattrs), columns=zattrs)
    PANDA_0C_OP = PANDA_0C - PANDA_0C_PK
    PANDA_0C_PK.to_csv(fnam0cpk, index=False)
    PANDA_0C_OP.to_csv(fnam0cop, index=False)
         

fnam0   =os.path.join(Visum.GetPath(2), "outputs\\{}\\panda\\PANDA_0C.csv".format(SCNAME))
fnam0cpk=os.path.join(Visum.GetPath(2), "outputs\\{}\\panda\\PANDA_0C_PK.csv".format(SCNAME))
fnam0cop=os.path.join(Visum.GetPath(2), "outputs\\{}\\panda\\PANDA_0C_OP.csv".format(SCNAME))
split_panda(fnam0, fnam0cpk, fnam0cop)

fnam0   =os.path.join(Visum.GetPath(2), "outputs\\{}\\panda\\PANDA_1C.csv".format(SCNAME))
fnam0cpk=os.path.join(Visum.GetPath(2), "outputs\\{}\\panda\\PANDA_1C_PK.csv".format(SCNAME))
fnam0cop=os.path.join(Visum.GetPath(2), "outputs\\{}\\panda\\PANDA_1C_OP.csv".format(SCNAME))
split_panda(fnam0, fnam0cpk, fnam0cop)



