import numpy as np 
import pandas as pd
import os 
import VisumPy.helpers as h
PRIO = 20480
SCNAME  = Visum.Net.AttValue("SC_NAME")


def load_PA(fnam):
    Visum.Log(PRIO, "Get PANDA_XC from file...")
    PANDA_XC = pd.read_csv(fnam)
    zattrs = PANDA_XC.columns.to_list()
    Visum.Net.Zones.SetMultipleAttributes(zattrs, PANDA_XC.to_numpy())
    Visum.Log(PRIO, "Set PANDA_XC from file.")

fnam = os.path.join(Visum.GetPath(2), "outputs\\{}\\panda\\PANDA_0C_OP.csv".format(SCNAME))
load_PA(fnam)
