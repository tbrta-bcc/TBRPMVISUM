import VisumPy.helpers as h
import numpy as np
# import time 
PRIO = 20480


def demand_parkride(mx_pnr, mx_lot, mx_prt, mx_put, isadditive=0):
    Visum.Log(PRIO, 'Start: park and ride demand calculation')
    # start = time.time()
    #Initialization....
    numzones = Visum.Net.Zones.Count
    pnr_dmd = h.GetMatrixRaw(Visum, mx_pnr)
    if pnr_dmd.sum() > 0:
        pnr_lot = h.GetMatrixRaw(Visum, mx_lot).astype('int')
        prt_leg = np.zeros(pnr_dmd.shape)
        put_leg = np.zeros(pnr_dmd.shape)
        
        Visum.Log(PRIO, 'Note: split pnr demand matrix to prt and put legs')
        for i in range(numzones):
            for j in range(numzones):
                prt_leg[i,pnr_lot[i,j]]+= pnr_dmd[i,j]
                put_leg[pnr_lot[i,j],j]+= pnr_dmd[i,j]
        
        if isadditive==0:
            h.SetMatrixRaw(Visum, mx_put, put_leg)
        else:
            put_leg+=h.GetMatrixRaw(Visum, mx_put)
            h.SetMatrixRaw(Visum, mx_put, put_leg)
        
        # h.SetMatrixRaw(Visum, mx_put, put_leg)
        h.SetMatrixRaw(Visum, mx_prt, prt_leg)
    else:
        Visum.Log(PRIO, 'Note: pnr/knr demand is 0')

    Visum.Log(PRIO, 'End: park and ride demand calculation')


Visum.Log(PRIO, 'peak auto access transit')
Visum.Log(PRIO, 'PnR')
mx_pnr = 90   # 90	PNR_PK	PNR_PK
mx_lot = 40   # 40	OPTLOT_PNR_PK
mx_prt = 14   # 14	DMC1	PrT-Leg PnR PK
mx_put = 56   # 56	TRA_PK	PEAK Transit Auto
demand_parkride(mx_pnr, mx_lot, mx_prt, mx_put)

Visum.Log(PRIO, 'KnR')
mx_pnr = 89   # 89	KNR_PK
mx_lot = 41   # 41	OPTLOT_KNR_PK
mx_prt = 15   # 15	DMC2	PrT-Leg KnR PK
mx_put = 56   # 56	TRA_PK	PEAK Transit Auto
demand_parkride(mx_pnr, mx_lot, mx_prt, mx_put,  isadditive=1)

Visum.Log(PRIO, 'off-peak auto access transit')
Visum.Log(PRIO, 'PnR')
mx_pnr = 84   # 84	PNR_OP	PNR_OP
mx_lot = 77   # 77	OPTLOT_PNR_OP	OPTLOT_PNR_OP
mx_prt = 16   # 16	DMC3	PrT-Leg PnR OP
mx_put = 57   # 57	TRA_OP	OFF-PEAK Transit Auto
demand_parkride(mx_pnr, mx_lot, mx_prt, mx_put)

Visum.Log(PRIO, 'KnR')
mx_pnr = 83   # 83	KNR_OP	KNR_OP
mx_lot = 78   # 78	OPTLOT_KNR_OP	OPTLOT_KNR_OP
mx_prt = 17   # 17	DMC4	PrT-Leg KnR OP
mx_put = 57   # 57	TRA_OP	OFF-PEAK Transit Auto
demand_parkride(mx_pnr, mx_lot, mx_prt, mx_put,  isadditive=1)




