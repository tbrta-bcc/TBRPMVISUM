
import VisumPy.helpers as h
import VisumPy.matrices as mfuncs
import numpy as np
import os
import time 
PRIO = 20480

SCNAME  = Visum.Net.AttValue("SC_NAME")
def skim_parkride(m1, m2, TERMTME, m4, prflag, mx_skims, mx_result):
    Visum.Log(PRIO, 'Start: park and ride skim calculation')
    # start = time.time()
    #Initialization....
    AUWT = 1.75
    TSTERM  = np.array(h.GetMulti(Visum.Net.Zones, TERMTME))
    TSRANGE = np.array(h.GetMulti(Visum.Net.Zones, "TSRANGE"))

    prt_ivt = h.GetMatrixRaw(Visum, m1) #/ 60.0  # divide by 60 to convert IMP in secs to mins 
    put_jrt = h.GetMatrixRaw(Visum, m2) + TSTERM[:, np.newaxis]  # terminal time 

    prt_dis = h.GetMatrixRaw(Visum, mx_skims['dis'])
    prt_ivt[prt_dis>TSRANGE]=999999  # constrain max drive distance to PnR lot
    # prt_ivt[prt_dis > 5] = 999999  #constrain max drive distance to PnR lot
    # prt_ovt = 0.05*prt_tto
    prt_cst = prt_dis*0.125 #convert distance matrix to auto operating cost 12.5 cents/mile

    put_ivt = h.GetMatrixRaw(Visum, mx_skims['ivt']) 
    put_owt = h.GetMatrixRaw(Visum, mx_skims['owt'])
    put_twt = h.GetMatrixRaw(Visum, mx_skims['twt'])
    put_ntr = h.GetMatrixRaw(Visum, mx_skims['ntr'])
    put_far = h.GetMatrixRaw(Visum, mx_skims['far'])
    put_wkt = h.GetMatrixRaw(Visum, mx_skims['wkt']) + h.GetMatrixRaw(Visum, mx_skims['egt'])

    numzones= Visum.Net.Zones.Count
    pnr_time= np.zeros((numzones,numzones)) + np.inf
    optlot  = np.zeros((numzones,numzones)).astype('int')
    pnr_ivt = np.zeros((numzones,numzones)) + 999
    pnr_owt = np.zeros((numzones,numzones)) + 999
    pnr_twt = np.zeros((numzones,numzones)) + 999
    pnr_ntr = np.zeros((numzones,numzones)) + 999
    pnr_tto = np.zeros((numzones,numzones)) + 999 #tto = auto access time 
    pnr_far = np.zeros((numzones,numzones)) + 999
    pnr_wkt = np.zeros((numzones,numzones)) + 999
    
    
    zones = np.array(Visum.Net.Zones.GetMultiAttValues(prflag, False))**(0.85)
    przones = np.extract(zones[:,1] > 0, np.arange(numzones))
    #Skim calculation...
    for k in przones:
        mat = np.add(AUWT*prt_ivt[:, k][:, np.newaxis], put_jrt[k])/zones[k, 1]
        optlot[mat < pnr_time] = k
        pnr_time = np.minimum(mat, pnr_time)

    Visum.Log(PRIO, 'Note: assemble all skim matrices (with index arrays):')
    I = np.arange(numzones)[:, np.newaxis]
    J = np.arange(numzones)[np.newaxis, :]
    pnr_ivt[I,J] = prt_ivt[I, optlot] + put_ivt[optlot, J]
    pnr_wkt[I,J] =                      put_wkt[optlot, J]
    pnr_owt[I,J] =                      put_owt[optlot, J]
    pnr_twt[I,J] =                      put_twt[optlot, J]
    pnr_ntr[I,J] =                      put_ntr[optlot, J]
    pnr_tto[I,J] = prt_ivt[I, optlot]
    pnr_far[I,J] = prt_cst[I, optlot] + put_far[optlot, J]
    # pnr_ovt = pnr_owt + pnr_twt + pnr_tto + pnr_wkt
    # pnr_ovt = pnr_time - pnr_ivt 
    Visum.Log(PRIO, 'Note: writing results to disk...')
    # h.SetMatrixRaw(Visum, m3, pnr_time)
    zoneNums = np.array(h.GetMulti(Visum.Net.Zones, "NO")).astype('int')
    h.SetMatrixRaw(Visum, m4, optlot)
    mfuncs.writeBIMatrix(pnr_wkt, zoneNums, os.path.join(Visum.GetPath(2), mx_result['wkt']))
    mfuncs.writeBIMatrix(pnr_owt, zoneNums, os.path.join(Visum.GetPath(2), mx_result['owt']))
    mfuncs.writeBIMatrix(pnr_twt, zoneNums, os.path.join(Visum.GetPath(2), mx_result['twt']))
    # mfuncs.writeBIMatrix(pnr_ovt, zoneNums, os.path.join(Visum.GetPath(2), mx_result['ovt']))
    mfuncs.writeBIMatrix(pnr_ivt, zoneNums, os.path.join(Visum.GetPath(2), mx_result['ivt']))
    mfuncs.writeBIMatrix(pnr_ntr, zoneNums, os.path.join(Visum.GetPath(2), mx_result['ntr']))
    mfuncs.writeBIMatrix(pnr_far, zoneNums, os.path.join(Visum.GetPath(2), mx_result['far']))
    mfuncs.writeBIMatrix(pnr_tto, zoneNums, os.path.join(Visum.GetPath(2), mx_result['act']))

    Visum.Log(PRIO, 'End: park and ride skim calculation')


#************************************PEAK PERIOD PNR/KNR SKIMS********************************************************#
Visum.Log(PRIO, "start: Peak PNR/KNR Skim Calculation")

#-----PNR------#
prflag  = 'TSPARK'      # user defined zone attribute to identify a P+R zone
TERMTME = 'TSPNRTERM'   # user defined zone attribute for terminal time 
# auto skim matrix number   
mat1 = 6  # 6 -> TT0 SOV including toll cost and terminal time 
# transit skim matrix number
mat2 = 63 #JRT
# skim matrix number to store best lot 
mat4 = 77 #PnR best lot
# matrix number for PnR skim result - not used in D1 model
mat3 = 213 #PnR JRT | NOT USED!!
# dict of skims to compose for mode choice     put_owt = h.GetMatrixRaw(Visum, mx_skims['owt']) , put_twt = h.GetMatrixRaw(Visum, mx_skims['twt']) 
# lb_ivt  = h.GetMatrixRaw(Visum, 36) + h.GetMatrixRaw(Visum, 34)   #CIR + LB
mx_skims = {'dis': 8, 'ivt': 64, 'owt': 65, 'twt': 66, 'ntr': 68, 'far': 69, 'act': 67, 'wkt': 101, 'egt': 102}
mx_result= {'act': "outputs\\{}\\skims\\park_ride_op.ACT".format(SCNAME), 'owt': "outputs\\{}\\skims\\park_ride_op.OWT".format(SCNAME), 'twt': "outputs\\{}\\skims\\park_ride_op.TWT".format(SCNAME), 
'ivt': "outputs\\{}\\skims\\park_ride_op.IVT".format(SCNAME), 'ntr': "outputs\\{}\\skims\\park_ride_op.NTR".format(SCNAME), 'far': "outputs\\{}\\skims\\park_ride_op.FAR".format(SCNAME), 'act': "outputs\\{}\\skims\\park_ride_op.ACT".format(SCNAME), 'wkt': "outputs\\{}\\skims\\park_ride_op.WKT".format(SCNAME)} 
skim_parkride(mat1, mat2, TERMTME, mat4, prflag, mx_skims, mx_result) 

#----KNR--------#
prflag  = 'TSKNRTERM'   # user defined zone attribute to identify a K+R zone
TERMTME = 'TSKNRTERM'   # user defined zone attribute for terminal time 
mat4 = 78 #KnR best lot
# dict of skims to compose for mode choice     put_owt = h.GetMatrixRaw(Visum, mx_skims['owt']) , put_twt = h.GetMatrixRaw(Visum, mx_skims['twt']) 
mx_skims = {'dis': 8, 'ivt': 64, 'owt': 65, 'twt': 66, 'ntr': 68, 'far': 69, 'act': 67, 'wkt': 101, 'egt': 102}
mx_result= {'act': "outputs\\{}\\skims\\kiss_ride_op.ACT".format(SCNAME), 'owt': "outputs\\{}\\skims\\kiss_ride_op.OWT".format(SCNAME), 'twt': "outputs\\{}\\skims\\kiss_ride_op.TWT".format(SCNAME), 
'ivt': "outputs\\{}\\skims\\kiss_ride_op.IVT".format(SCNAME), 'ntr': "outputs\\{}\\skims\\kiss_ride_op.NTR".format(SCNAME), 'far': "outputs\\{}\\skims\\kiss_ride_op.FAR".format(SCNAME), 'act': "outputs\\{}\\skims\\kiss_ride_op.ACT".format(SCNAME), 'wkt': "outputs\\{}\\skims\\kiss_ride_op.WKT".format(SCNAME)} 
skim_parkride(mat1, mat2, TERMTME, mat4, prflag, mx_skims, mx_result) 

Visum.Log(PRIO, "end: Peak PNR/KNR Skim Calculation")