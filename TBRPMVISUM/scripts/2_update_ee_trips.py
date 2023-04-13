#allocate area type to links from nearest zone
import numpy as np 
import VisumPy.helpers as h
PRIO = 20480

def update_externals():
    table_name = "EETRIPS"
    numzones = Visum.Net.Zones.Count
    zone_ix = dict()
    zone_no = Visum.Net.Zones.GetMultiAttValues("NO", False)
    for ix, no in zone_no:
        zone_ix[no] = ix-1
    
    EETRIPS = Visum.Net.TableDefinitions.ItemByKey(table_name).TableEntries.GetMultipleAttributes(["ORZ", "DSZ", "TYPE", "TRIPS"])
    mx_pool = {1:np.zeros((numzones, numzones)), 2:np.zeros((numzones, numzones)), 3:np.zeros((numzones, numzones))}

    for otaz, dtaz, typen, trips in EETRIPS:
        mx_pool[typen][zone_ix[otaz], zone_ix[dtaz]]+=trips

    h.SetMatrixRaw(Visum, 2, mx_pool[1])
    h.SetMatrixRaw(Visum, 3, mx_pool[2])
    h.SetMatrixRaw(Visum, 4, mx_pool[3])

update_externals()



