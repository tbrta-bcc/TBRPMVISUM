#'Speed Capacity Lookup'
import numpy as np 
import VisumPy.helpers as h
PRIO = 20480


def set_speed_capacity():
    Visum.Log(PRIO, 'speed capacity update start...')
    Visum.ExportAllNumbersAsDoubles = 0
    nlinks = Visum.Net.Links.Count
    LINK_ATYPE = h.GetMulti(Visum.Net.Links, "AREA_TYPE")
    LINK_FTYPE = h.GetMulti(Visum.Net.Links, "FACL_TYPE")
    LINK_LANES = h.GetMulti(Visum.Net.Links, "NUMLANES")
    LINK_TSYS  = h.GetMulti(Visum.Net.Links, "TSysSet")
    LINK_SPDCAP= np.zeros((nlinks, 2))
    SPDCAP = Visum.Net.TableDefinitions.ItemByKey("SPDCAP").TableEntries.GetMultipleAttributes(["A_LOW", "A_HIGH", "F_LOW", "F_HIGH", "L_LOW", "L_HIGH", "CAPACITY", "SYMBOL1", "SPEED", "SYMBOL2"]) 
    CAPLKP = {}
    SPDLKP = {}

    Visum.Log(PRIO, 'building lookups...')
    for LATVAL, HATVAL, LFTVAL, HFTVAL, LLNVAL, HLNVAL, CAPVAL, CAPFUNC, SPDVAL, SPDFUNC in SPDCAP:
        if CAPFUNC=='':
            for ATYPE in range(LATVAL, HATVAL+1):
                for FTYPE in range(LFTVAL, HFTVAL+1):
                    for LANES in range(LLNVAL, HLNVAL+1):
                        INDEXVAL = (ATYPE * 10000) + (FTYPE * 100) + LANES
                        CAPLKP[INDEXVAL] = CAPVAL

        if SPDFUNC=='':
            for ATYPE in range(LATVAL, HATVAL+1):
                for FTYPE in range(LFTVAL, HFTVAL+1):
                    for LANES in range(LLNVAL, HLNVAL+1):
                        INDEXVAL = (ATYPE * 10000) + (FTYPE * 100) + LANES
                        SPDLKP[INDEXVAL] = SPDVAL

    for LATVAL, HATVAL, LFTVAL, HFTVAL, LLNVAL, HLNVAL, CAPVAL, CAPFUNC, SPDVAL, SPDFUNC in SPDCAP:
        if CAPFUNC=='*':
            for ATYPE in range(LATVAL, HATVAL+1):
                for FTYPE in range(LFTVAL, HFTVAL+1):
                    for LANES in range(LLNVAL, HLNVAL+1):
                        INDEXVAL = (ATYPE * 10000) + (FTYPE * 100) + LANES
                        if INDEXVAL in CAPLKP:
                            CAPLKP[INDEXVAL] = CAPLKP[INDEXVAL] * CAPVAL

        if SPDFUNC=='*' or SPDFUNC=='+' or SPDFUNC=='-':
            for ATYPE in range(LATVAL, HATVAL+1):
                for FTYPE in range(LFTVAL, HFTVAL+1):
                    for LANES in range(LLNVAL, HLNVAL+1):
                        INDEXVAL = (ATYPE * 10000) + (FTYPE * 100) + LANES
                        if INDEXVAL in SPDLKP:
                            if SPDFUNC=='*':
                                SPDLKP[INDEXVAL] = SPDLKP[INDEXVAL] * SPDVAL
                            if SPDFUNC=='+':
                                SPDLKP[INDEXVAL] = SPDLKP[INDEXVAL] + SPDVAL
                            if SPDFUNC=='-':
                                SPDLKP[INDEXVAL] = SPDLKP[INDEXVAL] - SPDVAL
    
    Visum.Log(PRIO, 'building lookups done!')
    #now loop over links to write speed and capacity:
    errs = 0
    for k in range(0, nlinks):
        if LINK_TSYS[k].find('HOV') >=0 and LINK_ATYPE[k] > 0 and LINK_FTYPE[k]>0:
            INDEXVAL = (LINK_ATYPE[k] * 10000) + (LINK_FTYPE[k] * 100) + LINK_LANES[k]
            if INDEXVAL in SPDLKP:
                LINK_SPDCAP[k, 0] = SPDLKP[INDEXVAL]
            else:
                Visum.Log(PRIO, "no speed lookup value found for link:{}, atype:{}, ftype:{}, lanes:{}, indexval:{}".format(k+1, LINK_ATYPE[k], LINK_FTYPE[k], LINK_LANES[k], INDEXVAL))
                errs+=1
            
            if INDEXVAL in CAPLKP:
                if CAPLKP[INDEXVAL] > 0:
                    LINK_SPDCAP[k, 1] = CAPLKP[INDEXVAL]
                else:
                    Visum.Log(PRIO, "link index: {} likely incorrect capacity. lower bound of 1500 vph set.".format(k+1))
                    LINK_SPDCAP[k, 1] = 1500
            else:
                Visum.Log(PRIO, "no capacity lookup value found for link:{}, atype:{}, ftype:{}, lanes:{}, indexval:{}".format(k+1, LINK_ATYPE[k], LINK_FTYPE[k], LINK_LANES[k], INDEXVAL))
                errs+=1
            
            if errs > 5:
                Visum.Log(PRIO, "more than 5 errors...")
                break;
    
    Visum.Net.Links.SetMultipleAttributes(["V0PrT", "CAPACITY_HR"], LINK_SPDCAP)

    Visum.Log(PRIO, 'updating connectors...')
    nconnectors= Visum.Net.Connectors.Count
    CONN_ATYPE = h.GetMulti(Visum.Net.Connectors, "AREA_TYPE")
    CONN_FTYPE = h.GetMulti(Visum.Net.Connectors, "FACL_TYPE")
    CONN_LANES = h.GetMulti(Visum.Net.Connectors, "NUM_LANES")
    CONN_SPEED = h.GetMulti(Visum.Net.Connectors, "SPEED")
    errs = 0
    for k in range(0, nconnectors):
        INDEXVAL = (CONN_ATYPE[k] * 10000) + (CONN_FTYPE[k] * 100) + CONN_LANES[k]
        if INDEXVAL in SPDLKP:
            CONN_SPEED[k] = SPDLKP[INDEXVAL]
        else:
            Visum.Log(PRIO, "no speed lookup value found for connector:{}, atype:{}, ftype:{}, lanes:{}, indexval:{}".format(k+1, CONN_ATYPE[k], CONN_FTYPE[k], CONN_LANES[k], INDEXVAL))
            errs+=1

    h.SetMulti(Visum.Net.Connectors, "SPEED", CONN_SPEED)
    Visum.ExportAllNumbersAsDoubles = 1
    Visum.Log(PRIO, 'speed capacity update done!')


set_speed_capacity()



