# auto ownership proportions to split 0, 1, 2+ autos for mode choice segmentation
# Chetan Joshi, Portland OR 3/18/2022
import numpy as np

PTYPE = ['DU_RET', 'DU_WNC', 'DU_WHC']
AU    = [0, 1, 2, 3]

def pct_autos(purps, target):
    PRATES = Visum.Net.TableDefinitions.ItemByKey("COEFF_PRATES").TableEntries.GetMultipleAttributes(["DSTRATA", "VARCODE", "COEFF"])
    rate_lkp = {}
    for dstrat, vcode, coeff in PRATES:
        rate_lkp[(dstrat, vcode)] = coeff
    
    nzones = Visum.Net.Zones.Count
    _AUTOS = np.zeros((nzones, 2))

    for purp in purps:

        coeff_map = {}
        for autos in AU:
            for person in PTYPE:
                # print (autos, ':', person+str(autos), purp)
                if autos in coeff_map:
                    beta = rate_lkp[(purp, person+str(autos))]
                    coeff_map[autos]['attrs'].append(person+str(autos))
                    coeff_map[autos]['betas'].append(beta)
                    
                else:
                    beta = rate_lkp[(purp, person+str(autos))]
                    coeff_map[autos]={'attrs':[person+str(autos)], 'betas':[beta]}

        for autos in [1, 2, 3]:
            attrs = coeff_map[autos]['attrs']
            betas = np.array(coeff_map[autos]['betas'])
            DUTABLE = np.array(Visum.Net.Zones.GetMultipleAttributes(attrs))
            AUCLASS = np.dot(DUTABLE, betas)
            #ACCUMULATE 1 and 2/3+ AUTOS
            if autos == 1:
                _AUTOS[:, 0]+= AUCLASS
            else:
                _AUTOS[:, 1]+= AUCLASS
    
    _AUTOS_TOT = np.maximum(0.000001, _AUTOS.sum(1))
    _AUTOS[:, 0] = 100*_AUTOS[:, 0] / _AUTOS_TOT
    _AUTOS[:, 1] = 100*_AUTOS[:, 1] / _AUTOS_TOT

    _AUTOS[:, 0] = np.where(_AUTOS[:, 1]>0, _AUTOS[:, 0], 100)

    Visum.Net.Zones.SetMultipleAttributes(target, _AUTOS)
    

purps = ['HBW']
target= ['PCTHBW1C', 'PCTHBW2C']
pct_autos(purps, target)


purps = ['HBSH', 'HBSR', 'HBSC', 'HBO', 'AIRP', 'COL']
target= ['PCTHBO1C', 'PCTHBO2C']
pct_autos(purps, target)


     