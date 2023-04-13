# aggregate mode choice results for reporting 
# Chetan Joshi, Portland OR 3/30/2022
import os
import numpy as np
import VisumPy.helpers as h
import VisumPy.matrices as mf
PRIO = 20480
SCNAME  = Visum.Net.AttValue("SC_NAME")
BASEDIR = Visum.GetPath(2)

# 79	SOV_OP
# 80	SR2_OP
# 81	SR3_OP
# 82	TWK_OP
# 83	KNR_OP
# 84	PNR_OP

# 85	SOV_PK
# 86	SR2_PK
# 87	SR3_PK
# 88	TWK_PK
# 89	KNR_PK
# 90	PNR_PK

def aggregate_mode_choice(prd):

    nzns = Visum.Net.Zones.Count
    Purps = ["HBW", "HBNW", "NHB"]
    Modes = ["SOV", "SR2", "SR3", "TWK", "KNR", "PNR"]
    Autos = ["0C", "1C", "2C"]
    modemx = {"SOV":np.zeros((nzns, nzns)), "SR2":np.zeros((nzns, nzns)), "SR3":np.zeros((nzns, nzns)), 
    "TWK":np.zeros((nzns, nzns)), "KNR":np.zeros((nzns, nzns)), "PNR":np.zeros((nzns, nzns))}

    for mode in Modes:
        for purp in Purps:
            if purp == "NHB":
                # OP_NHB_KNR... etc
                mxcode  = "{}_{}_{}".format(prd, purp, mode)
                mx_wrkg = mf.readBIMatrix(os.path.join(BASEDIR, "outputs\\{}\\matrix\\{}".format(SCNAME,mxcode)))
                modemx[mode]+=mx_wrkg
            else:
                # OP_HBW_1C_PNR
                for auto in Autos:
                    mxcode = "{}_{}_{}_{}".format(prd, purp, auto, mode)
                    mx_wrkg = mf.readBIMatrix(os.path.join(BASEDIR, "outputs\\{}\\matrix\\{}".format(SCNAME,mxcode)))
                    modemx[mode]+=mx_wrkg

    h.SetMatrixRaw(Visum, "SOV_{}_PER".format(prd), modemx["SOV"])
    h.SetMatrixRaw(Visum, "SR2_{}_PER".format(prd), modemx["SR2"])
    h.SetMatrixRaw(Visum, "SR3_{}_PER".format(prd), modemx["SR3"])
    h.SetMatrixRaw(Visum, "TWK_{}_PER".format(prd), modemx["TWK"])
    h.SetMatrixRaw(Visum, "KNR_{}_PER".format(prd), modemx["KNR"])
    h.SetMatrixRaw(Visum, "PNR_{}_PER".format(prd), modemx["PNR"])

Visum.Log(PRIO, 'aggregating mode choice matrices: OP')
prd = "OP"
aggregate_mode_choice(prd)

Visum.Log(PRIO, 'aggregating mode choice matrices: PK')
prd = "PK"
aggregate_mode_choice(prd)

Visum.Log(PRIO, 'done aggregating mode choice matrices.')
