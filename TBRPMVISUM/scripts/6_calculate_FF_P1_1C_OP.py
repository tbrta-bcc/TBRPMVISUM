import numpy as np 
import VisumPy.helpers as h
PRIO = 20480

def calculate_FF(dstrat, skmno, ffmxno, fftable, ffcoln):
    Visum.Log(PRIO, "calculate friction factors: {}".format(dstrat))
    # nzones = Visum.Net.Zones.Count
    ff_lookup = np.array(Visum.Net.TableDefinitions.ItemByKey(fftable).TableEntries.GetMultipleAttributes(["MINUTES", ffcoln]))
    SKM = h.GetMatrixRaw(Visum, skmno) #/ 60.0
    FFM = np.interp(SKM, ff_lookup[:,0], ff_lookup[:,1])
    h.SetMatrixRaw(Visum, ffmxno, FFM)
    Visum.Log(PRIO, "done calculating friction factors: {}".format(dstrat))

skmno  =  6
dstrats= {'AIRP': ["FF_ALL", "AIRP", 21], 'COL': ["FF_ALL", "COL", 22], 'HBO': ["FF_ALL", "HBO", 23], 'HBSC': ["FF_ALL", "HBSC", 24], 'HBSH': ["FF_ALL", "HBSH", 25], 
'HBSR': ["FF_ALL", "HBSR", 26], 'HBW': ["FF_ALL", "HBW", 27]}

for dstrat in dstrats:
    fftable, ffcoln, ffmxno =  dstrats[dstrat]
    calculate_FF(dstrat, skmno, ffmxno, fftable, ffcoln)