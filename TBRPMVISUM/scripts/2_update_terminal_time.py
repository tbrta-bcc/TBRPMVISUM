# update terminal time based on area types (?)-> what is AT in case of multiple connectors? see TODO[1]
# Chetan Joshi, Portland OR 3/21/2022
import numpy as np 
import VisumPy.helpers as h
PRIO = 20480

# TERMTABLE = "Terminal Time"
TERMTABLE = "TERM"
TOLLTABLE = "TOLLLINK"      #--> suffix removed so it works with table stored in loaded version file!!

def update_terminal_time():
    Visum.Log(PRIO, 'start: update terminal time')

    TERMTIME = dict(Visum.Net.TableDefinitions.ItemByKey(TERMTABLE).TableEntries.GetMultipleAttributes(["AT", "TERMTIME"]))
    zNO = Visum.Net.Zones.Count
    zAT = h.GetMulti(Visum.Net.Zones, "LAST:DESTCONNECTORS\\AREA_TYPE") #----> TODO[1]: Adjusted this based on discussion to take value from last zone connector | change to MIN later
    zTT = np.array(h.GetMulti(Visum.Net.Zones, "TERMTIME"))

    for i in range(zNO):
        if zAT[i] in TERMTIME:
            zTT[i] = TERMTIME[zAT[i]]
        else:
            zTT[i] = 0

    h.SetMulti(Visum.Net.Zones, "TERMTIME", zTT)

    Visum.Log(PRIO, 'end: update terminal time')

# "FROMNODE\\FIRST:CONTAININGTERRITORIES\\COLOR"
#   IF (A = {HINRANGE})
#     LW.CTOLL = {CTOLL1}
#   ELSEIF (A = {PINRANGE})
#     LW.CTOLL = {CTOLL2}
#   ELSEIF (A = {PANRANGE})
#     LW.CTOLL = {CTOLL3}
#   ELSEIF (A = {HENRANGE})
#     LW.CTOLL = {CTOLL4}
#   ELSEIF (A = {CINRANGE})
#     LW.CTOLL = {CTOLL5}
#   ELSEIF (A = {MANRANGE})
#     LW.CTOLL = {CTOLL6}
#   ELSE
#     LW.CTOLL = {CTOLL}
#   ENDIF


def update_link_tolls():
    Visum.Log(PRIO, 'start: update link tolls')
    CTOLL_LKP = {1.0: 0.052, 2.0: 0.062, 3.0: 0.12, 4.0: 0.125, 5.0: 0.152, 6.0: 0.078, '':0.06}
    TOLLLINKS = Visum.Net.TableDefinitions.ItemByKey(TOLLTABLE).TableEntries.GetMultipleAttributes(["FNODE", "TNODE", "CARTOLL", "SVCMINUTES", "SVCSECONDS"])

    for fnode, tnode, cartoll, svcmin, svcsec in TOLLLINKS:
        if Visum.Net.Links.LinkExistsByKey(fnode, tnode):
            iLink = Visum.Net.Links.ItemByKey(fnode, tnode)
            svctime = 60*svcmin + svcsec 
            link_loc = iLink.AttValue("LOCATION")
            if link_loc in CTOLL_LKP:
                ctoll = CTOLL_LKP[link_loc]
            else:
                ctoll = 0.06
            toll_vot= ctoll*cartoll*3600 #toll converted to seconds for assignment

            iLink.SetAttValue("SVCTIME", svctime)
            iLink.SetAttValue("TOLL_PRTSYS(HOV)", cartoll)
            iLink.SetAttValue("TOLL_PRTSYS(SOV)", cartoll)
            iLink.SetAttValue("TOLL_PRTSYS(TRK)", cartoll)
            iLink.SetAttValue("ADDVAL_TSYS(HOV)", toll_vot)
            iLink.SetAttValue("ADDVAL_TSYS(SOV)", toll_vot)
            iLink.SetAttValue("ADDVAL_TSYS(TRK)", toll_vot)
        else:
            Visum.Log(PRIO, "link (fnode, tnode): {} -> {} not found in network!".format(fnode, tnode))
    
    Visum.Log(PRIO, 'end: update link tolls')


def update_ctoll():
    Visum.Log(PRIO, 'start: updating ctoll multipliers by origin zone')
    nzones= Visum.Net.Zones.Count
    znums = np.array(h.GetMulti(Visum.Net.Zones, "NO"))
    _CTOLL= np.ones(nzones)*0.06 #---> default value for ctoll 
    CTOLL_MX = np.zeros((nzones, nzones)) 

    for i in range(nzones):
        if 1 <= znums[i] <= 1000:
            _CTOLL[i] = 0.052
        elif 1001 <= znums[i] <= 2000:
            _CTOLL[i] = 0.062
        elif 2001 <= znums[i] <= 2500:
            _CTOLL[i] = 0.12
        elif 2501 <= znums[i] <= 2800:
            _CTOLL[i] = 0.125
        elif 2801 <= znums[i] <= 2950:
            _CTOLL[i] = 0.152
        elif 2951 <= znums[i] <= 3000:
            _CTOLL[i] = 0.078
        else:
            _CTOLL[i] = 0.06

    CTOLL_MX = _CTOLL[:, np.newaxis] + CTOLL_MX 
    h.SetMatrixRaw(Visum, 75, CTOLL_MX)
    Visum.Log(PRIO, 'end: updated ctoll multipliers by origin zone.')

update_terminal_time()

update_link_tolls()

update_ctoll()