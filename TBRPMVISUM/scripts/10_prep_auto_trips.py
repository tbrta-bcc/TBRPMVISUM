# prepare trip tables for auto assignment
# Chetan Joshi PTV Portland OR 2/28/2022
import os
import numpy as np
import VisumPy.helpers as h
import VisumPy.matrices as mf
PRIO = 20480
SCNAME  = Visum.Net.AttValue("SC_NAME")
OCCUP = {"SOV_HBW":1.0, "SOV_HBNW":1.0, "SOV_NHB":1.0, "SR2_HBW": 2.0, "SR2_HBNW": 2.0, "SR2_NHB": 2.0, "SR3_HBW": 3.2, "SR3_HBNW": 3.3, "SR3_NHB": 3.4}

def aggregate_auto_trips1(PRD):
    Visum.Log(PRIO, 'PA vehicle trips: {}'.format(PRD))
    nzones= Visum.Net.Zones.Count
    znums = np.array(Visum.Net.Zones.GetMultiAttValues("NO")).astype('int')[:,1]
    purps = ["HBW", "HBNW"]
    autos = ["0C", "1C", "2C"]
    modes = ["SOV", "SR2", "SR3"]
    mx_pool = {"HBW_SOV":np.zeros((nzones, nzones)), "HBW_SR2":np.zeros((nzones, nzones)), "HBW_SR3":np.zeros((nzones, nzones)),
    "HBNW_SOV":np.zeros((nzones, nzones)), "HBNW_SR2":np.zeros((nzones, nzones)),"HBNW_SR3":np.zeros((nzones, nzones)),
    "NHB_SOV":np.zeros((nzones, nzones)), "NHB_SR2":np.zeros((nzones, nzones)), "NHB_SR3":np.zeros((nzones, nzones))}

    mode_map = {"SOV": "SOV", "SR2":"SR2", "SR3":"SR3"}

    for purp in purps:
        for auto in autos:
            for mode in modes:
                mxname = "{}_{}_{}_{}".format(PRD, purp, auto, mode)
                occ = OCCUP["{}_{}".format(mode, purp)]
                pmx = mf.readBIMatrix(os.path.join(Visum.GetPath(2),"outputs\\{}\\matrix\\{}".format(SCNAME,mxname))) / occ 
                mx_pool["{}_{}".format(purp, mode_map[mode])]+=pmx 

    purp = "NHB"
    for mode in modes:
        mxname = "{}_{}_{}".format(PRD, purp, mode)
        occ = OCCUP["{}_{}".format(mode, purp)]
        pmx = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\{}".format(SCNAME,mxname))) / occ 
        mx_pool["{}_{}".format(purp, mode_map[mode])]+=pmx  


    for purp in mx_pool:
        Visum.Log(PRIO, (purp, mx_pool[purp].sum()))
        #mf.writeBIMatrix(nArray, zoneNums, fileName)
        mf.writeBIMatrix(mx_pool[purp], znums, os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_{}_{}".format(SCNAME,PRD, purp)))

def aggregate_auto_trips(PRD):
    Visum.Log(PRIO, 'PA vehicle trips: {}'.format(PRD))
    nzones= Visum.Net.Zones.Count
    znums = np.array(Visum.Net.Zones.GetMultiAttValues("NO")).astype('int')[:,1]
    purps = ["HBW", "HBNW"]
    autos = ["0C", "1C", "2C"]
    modes = ["SOV", "SR2", "SR3"]
    mx_pool = {"HBW_SOV":np.zeros((nzones, nzones)), "HBW_HOV":np.zeros((nzones, nzones)),
    "HBNW_SOV":np.zeros((nzones, nzones)), "HBNW_HOV":np.zeros((nzones, nzones)),
    "NHB_SOV":np.zeros((nzones, nzones)), "NHB_HOV":np.zeros((nzones, nzones))}

    mode_map = {"SOV": "SOV", "SR2":"HOV", "SR3":"HOV"}

    for purp in purps:
        for auto in autos:
            for mode in modes:
                mxname = "{}_{}_{}_{}".format(PRD, purp, auto, mode)
                occ = OCCUP["{}_{}".format(mode, purp)]
                pmx = mf.readBIMatrix(os.path.join(Visum.GetPath(2),"outputs\\{}\\matrix\\{}".format(SCNAME,mxname))) / occ 
                mx_pool["{}_{}".format(purp, mode_map[mode])]+=pmx 

    purp = "NHB"
    for mode in modes:
        mxname = "{}_{}_{}".format(PRD, purp, mode)
        occ = OCCUP["{}_{}".format(mode, purp)]
        pmx = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\{}".format(SCNAME,mxname))) / occ 
        mx_pool["{}_{}".format(purp, mode_map[mode])]+=pmx  


    for purp in mx_pool:
        Visum.Log(PRIO, (purp, mx_pool[purp].sum()))
        #mf.writeBIMatrix(nArray, zoneNums, fileName)
        mf.writeBIMatrix(mx_pool[purp], znums, os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_{}_{}".format(SCNAME,PRD, purp)))



def factor_pk_matrices():
    Visum.Log(PRIO, "start: prepare matrices for peak periods")

    HBW_PA_SOV = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_PK_HBW_SOV").format(SCNAME))
    HBNW_PA_SOV= mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_PK_HBNW_SOV").format(SCNAME))    
    NHB_PA_SOV = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_PK_NHB_SOV").format(SCNAME)) 
    HBW_PA_HOV = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_PK_HBW_HOV").format(SCNAME))
    HBNW_PA_HOV= mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_PK_HBNW_HOV").format(SCNAME))
    NHB_PA_HOV = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_PK_NHB_HOV").format(SCNAME))
    LTRK = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\LTRK_1C_PK").format(SCNAME))
    HTRK = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\HTRK_1C_PK").format(SCNAME))  
    TAXI = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\TAXI_1C_PK").format(SCNAME)) 
    EI   = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\EI_1C_PK".format(SCNAME))) 
    EE_AUTO= h.GetMatrixRaw(Visum, 2)
    EE_MTRK= h.GetMatrixRaw(Visum, 3)
    EE_HTRK= h.GetMatrixRaw(Visum, 4)

    # Create lookup tables PK FAC -> to split PK to AM / PM and directional OD
    PKFACS = dict(Visum.Net.TableDefinitions.ItemByKey("AMPKSF").TableEntries.GetMultipleAttributes(["PURPOSE", "FACTOR"]))  #--> splits for AM/PM | MD/EV
    PAFACS = dict(Visum.Net.TableDefinitions.ItemByKey("PKPAF").TableEntries.GetMultipleAttributes(["PURPOSE", "FACTOR"]))   #--> directional PA factors to get OD
    EEFACS = dict(Visum.Net.TableDefinitions.ItemByKey("EEFAC").TableEntries.GetMultipleAttributes(["PURPOSE", "FACTOR"]))

    # Create matrices for TI --> First calculate AM
    Visum.Log(PRIO, "note: calculate AM trip tables")
    pa_hbw = PAFACS['AMPKPAF-HBW']
    ap_hbw = 1.0 - pa_hbw
    pa_hbnw= PAFACS['AMPKPAF-HBNW']
    ap_hbnw= 1.0 - pa_hbnw 
    SOV_TI = PKFACS['AMPKSF-HBW']*(HBW_PA_SOV*pa_hbw + HBW_PA_SOV.T*ap_hbw) + PKFACS['AMPKSF-HBNW']*(HBNW_PA_SOV*pa_hbnw + HBNW_PA_SOV.T*ap_hbnw) + 0.5*NHB_PA_SOV + EE_AUTO*EEFACS['EE-AMPK'] + TAXI*PKFACS['AMPKSF-TAXI'] + (EI + EI.T) * 0.5 * PKFACS['AMPKSF-EI']
    HOV_TI = PKFACS['AMPKSF-HBW']*(HBW_PA_HOV*pa_hbw + HBW_PA_HOV.T*ap_hbw) + PKFACS['AMPKSF-HBNW']*(HBNW_PA_HOV*pa_hbnw + HBNW_PA_HOV.T*ap_hbnw) + 0.5*NHB_PA_HOV
    TRK_TI = LTRK*PKFACS['AMPKSF-LTRK'] + HTRK*PKFACS['AMPKSF-HTRK'] + (EE_HTRK+EE_MTRK)*EEFACS['EE-AMPK']

    h.SetMatrixRaw(Visum, "SOV_AM_HWY", SOV_TI)
    h.SetMatrixRaw(Visum, "HOV_AM_HWY", HOV_TI)
    h.SetMatrixRaw(Visum, "TRK_AM_HWY", TRK_TI)

    # Create matrices for TI --> Then calculate PM
    Visum.Log(PRIO, "note: calculate PM trip tables")
    pa_hbw = PAFACS['PMPKPAF-HBW']
    ap_hbw = 1.0 - pa_hbw
    pa_hbnw= PAFACS['PMPKPAF-HBNW']
    ap_hbnw= 1.0 - pa_hbnw 
    SOV_TI = (1.0-PKFACS['AMPKSF-HBW'])*(HBW_PA_SOV*pa_hbw + HBW_PA_SOV.T*ap_hbw) + (1.0-PKFACS['AMPKSF-HBNW'])*(HBNW_PA_SOV*pa_hbnw + HBNW_PA_SOV.T*ap_hbnw) + 0.5*NHB_PA_SOV + EE_AUTO*EEFACS['EE-PMPK'] + + TAXI*(1.0-PKFACS['AMPKSF-TAXI']) + (EI + EI.T) * 0.5 * (1.0-PKFACS['AMPKSF-EI'])
    HOV_TI = (1.0-PKFACS['AMPKSF-HBW'])*(HBW_PA_HOV*pa_hbw + HBW_PA_HOV.T*ap_hbw) + (1.0-PKFACS['AMPKSF-HBNW'])*(HBNW_PA_HOV*pa_hbnw + HBNW_PA_HOV.T*ap_hbnw) + 0.5*NHB_PA_HOV
    TRK_TI = LTRK*(1.0-PKFACS['AMPKSF-LTRK']) + HTRK*(1.0-PKFACS['AMPKSF-HTRK']) + (EE_HTRK+EE_MTRK)*EEFACS['EE-PMPK']

    h.SetMatrixRaw(Visum, "SOV_PM_HWY", SOV_TI)
    h.SetMatrixRaw(Visum, "HOV_PM_HWY", HOV_TI)
    h.SetMatrixRaw(Visum, "TRK_PM_HWY", TRK_TI)

    Visum.Log(PRIO, "end: apply directional factors") 


def factor_op_matrices():
    Visum.Log(PRIO, "start: prepare matrices for off-peak periods")

    HBW_PA_SOV = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_OP_HBW_SOV".format(SCNAME)))
    HBNW_PA_SOV= mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_OP_HBNW_SOV".format(SCNAME))) 
    NHB_PA_SOV = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_OP_NHB_SOV".format(SCNAME))) 
    HBW_PA_HOV = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_OP_HBW_HOV".format(SCNAME)))
    HBNW_PA_HOV= mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_OP_HBNW_HOV".format(SCNAME)))
    NHB_PA_HOV = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_OP_NHB_HOV".format(SCNAME)))
    LTRK = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\LTRK_1C_OP".format(SCNAME)))
    HTRK = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\HTRK_1C_OP".format(SCNAME)))  
    TAXI = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\TAXI_1C_OP".format(SCNAME))) 
    EI   = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\EI_1C_OP".format(SCNAME))) 
    EE_AUTO= h.GetMatrixRaw(Visum, 2)
    EE_MTRK= h.GetMatrixRaw(Visum, 3)
    EE_HTRK= h.GetMatrixRaw(Visum, 4)

    # Create lookup tables PK FAC -> to split PK to AM / PM and directional OD
    PKFACS = dict(Visum.Net.TableDefinitions.ItemByKey("MDOPSF").TableEntries.GetMultipleAttributes(["PURPOSE", "FACTOR"]))  #--> splits for AM/PM | MD/EV
    PAFACS = dict(Visum.Net.TableDefinitions.ItemByKey("OPPAF").TableEntries.GetMultipleAttributes(["PURPOSE", "FACTOR"]))   #--> directional PA factors to get OD
    EEFACS = dict(Visum.Net.TableDefinitions.ItemByKey("EEFAC").TableEntries.GetMultipleAttributes(["PURPOSE", "FACTOR"]))

    # Create matrices for TI --> First calculate MD
    Visum.Log(PRIO, "note: calculate MD trip tables")
    pa_hbw = PAFACS['MDOPPAF-HBW']
    ap_hbw = 1.0 - pa_hbw
    pa_hbnw= PAFACS['MDOPPAF-HBNW']
    ap_hbnw= 1.0 - pa_hbnw 
    SOV_TI = PKFACS['MDOPSF-HBW']*(HBW_PA_SOV*pa_hbw + HBW_PA_SOV.T*ap_hbw) + PKFACS['MDOPSF-HBNW']*(HBNW_PA_SOV*pa_hbnw + HBNW_PA_SOV.T*ap_hbnw) + 0.5*NHB_PA_SOV + EE_AUTO*EEFACS['EE-MDOP'] + TAXI*PKFACS['MDOPSF-TAXI'] + (EI + EI.T) * 0.5 * PKFACS['MDOPSF-EI']
    HOV_TI = PKFACS['MDOPSF-HBW']*(HBW_PA_HOV*pa_hbw + HBW_PA_HOV.T*ap_hbw) + PKFACS['MDOPSF-HBNW']*(HBNW_PA_HOV*pa_hbnw + HBNW_PA_HOV.T*ap_hbnw) + 0.5*NHB_PA_HOV
    TRK_TI = LTRK*PKFACS['MDOPSF-LTRK'] + HTRK*PKFACS['MDOPSF-HTRK'] + (EE_HTRK+EE_MTRK)*EEFACS['EE-MDOP']

    h.SetMatrixRaw(Visum, "SOV_MD_HWY", SOV_TI)
    h.SetMatrixRaw(Visum, "HOV_MD_HWY", HOV_TI)
    h.SetMatrixRaw(Visum, "TRK_MD_HWY", TRK_TI)

    # Create matrices for TI --> Then calculate EV
    Visum.Log(PRIO, "note: calculate EV trip tables")
    pa_hbw = PAFACS['EVOPPAF-HBW']
    ap_hbw = 1.0 - pa_hbw
    pa_hbnw= PAFACS['EVOPPAF-HBNW']
    ap_hbnw= 1.0 - pa_hbnw 
    SOV_TI = (1.0-PKFACS['MDOPSF-HBW'])*(HBW_PA_SOV*pa_hbw + HBW_PA_SOV.T*ap_hbw) + (1.0-PKFACS['MDOPSF-HBNW'])*(HBNW_PA_SOV*pa_hbnw + HBNW_PA_SOV.T*ap_hbnw) + 0.5*NHB_PA_SOV + EE_AUTO*EEFACS['EE-EVOP'] + TAXI*(1.0-PKFACS['MDOPSF-TAXI']) + (EI + EI.T) * 0.5 * (1.0-PKFACS['MDOPSF-EI'])
    HOV_TI = (1.0-PKFACS['MDOPSF-HBW'])*(HBW_PA_HOV*pa_hbw + HBW_PA_HOV.T*ap_hbw) + (1.0-PKFACS['MDOPSF-HBNW'])*(HBNW_PA_HOV*pa_hbnw + HBNW_PA_HOV.T*ap_hbnw) + 0.5*NHB_PA_HOV
    TRK_TI = LTRK*(1.0-PKFACS['MDOPSF-LTRK']) + HTRK*(1.0-PKFACS['MDOPSF-HTRK'])  + (EE_HTRK+EE_MTRK)*EEFACS['EE-EVOP']

    h.SetMatrixRaw(Visum, "SOV_EV_HWY", SOV_TI)
    h.SetMatrixRaw(Visum, "HOV_EV_HWY", HOV_TI)
    h.SetMatrixRaw(Visum, "TRK_EV_HWY", TRK_TI)

    Visum.Log(PRIO, "end: apply directional factors") 


if Visum.Net.AttValue("ITER") <=1:
    PRD = "OP"
    aggregate_auto_trips(PRD)
    aggregate_auto_trips1(PRD)
    factor_op_matrices()

PRD = "PK"
aggregate_auto_trips(PRD)
aggregate_auto_trips1(PRD)

factor_pk_matrices()

HBW_PK_SOV = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_PK_HBW_SOV".format(SCNAME)))
HBW_OP_SOV = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_OP_HBW_SOV".format(SCNAME)))
HBNW_PK_SOV = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_PK_HBNW_SOV".format(SCNAME)))
HBNW_OP_SOV = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_OP_HBNW_SOV".format(SCNAME)))
NHB_PK_SOV = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_PK_NHB_SOV".format(SCNAME)))
NHB_OP_SOV = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_OP_NHB_SOV".format(SCNAME)))

HBW_PK_SR2 = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_PK_HBW_SR2".format(SCNAME)))
HBW_OP_SR2 = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_OP_HBW_SR2".format(SCNAME)))
HBNW_PK_SR2 = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_PK_HBNW_SR2".format(SCNAME)))
HBNW_OP_SR2 = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_OP_HBNW_SR2".format(SCNAME)))
NHB_PK_SR2 = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_PK_NHB_SR2".format(SCNAME)))
NHB_OP_SR2 = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_OP_NHB_SR2".format(SCNAME)))

HBW_PK_SR3 = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_PK_HBW_SR3".format(SCNAME)))
HBW_OP_SR3 = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_OP_HBW_SR3".format(SCNAME)))
HBNW_PK_SR3 = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_PK_HBNW_SR3".format(SCNAME)))
HBNW_OP_SR3 = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_OP_HBNW_SR3".format(SCNAME)))
NHB_PK_SR3 = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_PK_NHB_SR3".format(SCNAME)))
NHB_OP_SR3 = mf.readBIMatrix(os.path.join(Visum.GetPath(2), "outputs\\{}\\matrix\\VEH_OP_NHB_SR3".format(SCNAME)))

sov_op=HBW_OP_SOV+HBNW_OP_SOV+NHB_OP_SOV
sr2_op=HBW_OP_SR2+HBNW_OP_SR2+NHB_OP_SR2
sr3_op=HBW_OP_SR3+HBNW_OP_SR3+NHB_OP_SR3

sov_pk=HBW_PK_SOV+HBNW_PK_SOV+NHB_PK_SOV
sr2_pk=HBW_PK_SR2+HBNW_PK_SR2+NHB_PK_SR2
sr3_pk=HBW_PK_SR3+HBNW_PK_SR3+NHB_PK_SR3

h.SetMatrixRaw(Visum, "SOV_OP_VEH", sov_op)
h.SetMatrixRaw(Visum, "SR2_OP_VEH", sr2_op)
h.SetMatrixRaw(Visum, "SR3_OP_VEH", sr3_op)

h.SetMatrixRaw(Visum, "SOV_PK_VEH", sov_pk)
h.SetMatrixRaw(Visum, "SR2_PK_VEH", sr2_pk)
h.SetMatrixRaw(Visum, "SR3_PK_VEH", sr3_pk)
