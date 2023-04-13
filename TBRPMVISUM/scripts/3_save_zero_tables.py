# Save dummy trip tables for unused segments to disk 
# Chetan Joshi, Portland OR 3/22/2022
import os 

SCNAME  = Visum.Net.AttValue("SC_NAME")
BASEDIR = Visum.GetPath(2)
MXNAMES = ['AIRP_0C_OP', 'AIRP_0C_PK', 'COL_0C_OP', 'COL_0C_PK'] 

def save_dummy_trips():
    Visum.Net.Matrices.ItemByKey(5).Init()
    for MX in MXNAMES:
        Visum.Net.Matrices.ItemByKey(5).Save(os.path.join(BASEDIR, "outputs\\{}\\matrix\\{}".format(SCNAME,MX)), 0)

save_dummy_trips()
