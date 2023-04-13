#update area type for zones and links
import numpy as np
import VisumPy.helpers as h
PRIO = 20480

def update_taz_areatype():
    #get zdata
    #loop over each taz
    izones = 3000
    DIDMX  = 1
    nzones = Visum.Net.Zones.Count
    _TAZAREA = np.array(h.GetMulti(Visum.Net.Zones, "TAZ_AREA"))
    _TOTPOP  = np.array(h.GetMulti(Visum.Net.Zones, "POP")) + np.array(h.GetMulti(Visum.Net.Zones, "GQPOP"))
    _TOTEMP  = np.array(h.GetMulti(Visum.Net.Zones, "TOT_EMP"))
    _CBDZONE = np.array(h.GetMulti(Visum.Net.Zones, "CBD_ZONES"))
    _RATIO = np.sum(_TOTPOP) / np.sum(_TOTEMP)
    Visum.Log(PRIO, "regional density: {}".format(_RATIO))
    POPDEN = np.zeros(nzones)
    EMPDEN = np.zeros(nzones)
    ADEN   = np.zeros(nzones)
    AT     = np.zeros(nzones)

    POPDEN_1M = np.zeros(nzones)
    EMPDEN_1M = np.zeros(nzones)
    ADEN_1M   = np.zeros(nzones)
    AT_1M     = np.zeros(nzones)
    
    TOTPOP_1M= np.zeros(nzones)
    TOTEMP_1M= np.zeros(nzones)
    ACRES_1M = np.zeros(nzones)
    _SelDist= np.zeros(nzones)
    _DISTANCE=h.GetMatrixRaw(Visum, DIDMX) #Get DID matrix here
    _countTAZ = np.zeros(nzones)

    NEWHU = np.array(Visum.Net.Zones.GetMultipleAttributes(["BHU", "EHU", "RHU"])).sum(1)
    CBDHU = np.zeros(nzones) #; Business, Economy, and Resort Designations
    MEDHU = np.zeros(nzones)
    LOWHU = np.zeros(nzones)

    for iz in range(izones):
        if _TAZAREA[iz] == 0 and (_TOTPOP[iz] + _TOTEMP[iz] > 0):
            Visum.Log(PRIO, ['ERROR IN TAZ ', iz, ' POPULATION IS ', _TOTPOP[iz], ' AND EMPLOYMENT IS ', _TOTEMP[iz], ' FOR A TAZ WITH 0.0 AREA.'])
            POPDEN[iz] = 0
            EMPDEN[iz] = 0
            ADEN[iz] = 0
        
        elif _TAZAREA[iz] == 0:
            POPDEN[iz] = 0
            EMPDEN[iz] = 0
            ADEN[iz]   = 0

        else:
            POPDEN[iz] = _TOTPOP[iz] / _TAZAREA[iz]
            EMPDEN[iz] = _TOTEMP[iz] / _TAZAREA[iz]
            ADEN[iz] =   POPDEN[iz] + (_RATIO * EMPDEN[iz])

        # ACRES  = _TAZAREA
        # TOTPOP = _TOTPOP
        # TOTEMP = _TOTEMP

        if _CBDZONE[iz] > 0:
            AT[iz] = 1
        elif ADEN[iz] > 40.0:  #; (ADEN > 49.6) SERPM EFFECTIVE RATES APPLYING (NET AREA / GROSS AREA) RATIO
            AT[iz] = 2
        elif ADEN[iz] >= 18.5: #  ; (ADEN >= 23.0)
            AT[iz] = 3
        elif ADEN[iz] >= 2.5: #   ; (ADEN >= 3.2)
            AT[iz] = 4
        elif ADEN[iz] > 0 or _TAZAREA[iz] > 0:
            AT[iz] = 5
        else:
            AT[iz] = 0

        if _TAZAREA[iz] <= 100:
            _SelDist[iz] = 1/4
        elif _TAZAREA[iz] <= 300:
            _SelDist[iz] = 1/2
        elif _TAZAREA[iz] > 300:
            _SelDist[iz] = 1

        if _TAZAREA[iz] > 0:
            TOTPOP_1M[iz] = np.sum(_TOTPOP[_DISTANCE[iz, :] <= _SelDist[iz]])
            TOTEMP_1M[iz] = np.sum(_TOTEMP[_DISTANCE[iz, :] <= _SelDist[iz]])
            TMP_AREA = _TAZAREA[_DISTANCE[iz, :]<= _SelDist[iz]]
            ACRES_1M[iz]  = np.sum(TMP_AREA)
            _countTAZ[iz] = len(TMP_AREA)
            # JLOOP
            #     _DISTANCE = SQRT((ZI.3.X[I] - ZI.3.X[J])^2 + (ZI.3.Y[I] - ZI.3.Y[J])^2) / 5280
            #     MW[1][J]  = _DISTANCE
            #     _TAZAREAJ = TAZ_AREA(3,J)

            #     IF ((_DISTANCE <= _SelDist) && ((_TAZAREAJ > 0) || (ZI.1.POP[J] > 0) || (ZI.1.GQPOP[J] > 0) || (ZI.2.TOT_EMP[J] > 0)))
            #         _countTAZ = _countTAZ + 1
            #         _AREA = _AREA + _TAZAREAJ

            #         IF ((_TAZAREAJ = 0) && ((ZI.1.POP[J] > 0) || (ZI.1.GQPOP[J] > 0) || (ZI.2.TOT_EMP[J] > 0)))
            #             PRINT LIST='ERROR IN TAZ ', J(5), ' POPULATION IS ', ZI.1.POP[J](10.0), ' AND EMPLOYMENT IS ', ZI.2.TOT_EMP[J](10.0), ' FOR A TAZ WITH 0.0 AREA.' PRINTO=1
            #         ELSE
            #             _TOTPOP = _TOTPOP + (ZI.1.POP[J] + ZI.1.GQPOP[J])
            #             _TOTEMP = _TOTEMP + ZI.2.TOT_EMP[J]
            #         ENDIF
            #     ENDIF
            # ENDJLOOP

        # TOTPOP_1M = _TOTPOP
        # TOTEMP_1M = _TOTEMP
        POPDEN_1M[iz] = TOTPOP_1M[iz] / max(1, ACRES_1M[iz])
        EMPDEN_1M[iz] = TOTEMP_1M[iz] / max(1, ACRES_1M[iz])
        ADEN_1M[iz]   = POPDEN_1M[iz] + (_RATIO * EMPDEN_1M[iz])
        # TAZ_Cnt = _countTAZ
        # BuffDist = _SelDist

        if _CBDZONE[iz] > 0:
            AT_1M[iz] = 1
        elif ADEN_1M[iz] > 40.0:   
            #; (ADEN > 49.6) SERPM EFFECTIVE RATES APPLYING (NET AREA / GROSS AREA) RATIO
            AT_1M[iz] = 2
        elif ADEN_1M[iz] >= 18.5:  
            #; (ADEN >= 23.0)
            AT_1M[iz] = 3
        elif ADEN_1M[iz] >= 2.5:   
            #; (ADEN >= 3.2)
            AT_1M[iz] = 4
        elif ADEN_1M[iz] > 0 or _TAZAREA[iz] > 0:
            AT_1M[iz] = 5
        else:
            AT_1M[iz] = 0

        if AT_1M[iz] < 3:
            CBDHU[iz] = NEWHU[iz]  #; Business, Economy, and Resort Designations
            MEDHU[iz] = 0
            LOWHU[iz] = 0
        elif AT_1M[iz] < 5:
            CBDHU[iz] = 0
            MEDHU[iz] = NEWHU[iz]
            LOWHU[iz] = 0
        else:
            CBDHU[iz] = 0
            MEDHU[iz] = 0
            LOWHU[iz] = NEWHU[iz]
    
    h.SetMulti(Visum.Net.Zones, "AT", AT)
    h.SetMulti(Visum.Net.Zones, "AT_1M", AT_1M)
    h.SetMulti(Visum.Net.Zones, "ADDVAL1", _countTAZ)

    h.SetMulti(Visum.Net.Zones, "CBDHU", CBDHU)
    h.SetMulti(Visum.Net.Zones, "MEDHU", MEDHU)
    h.SetMulti(Visum.Net.Zones, "LOWHU", LOWHU)


update_taz_areatype()