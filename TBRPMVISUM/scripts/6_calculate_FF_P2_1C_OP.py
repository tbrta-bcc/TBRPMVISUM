import numpy as np 
import VisumPy.helpers as h
PRIO = 20480

def calculate_FF(dstrat, skmno, ffmxno, fftable, ffcoln):
    Visum.Log(PRIO, "calculate friction factors: {}".format(dstrat))
    # nzones = Visum.Net.Zones.Count
    ff_lookup = np.array(Visum.Net.TableDefinitions.ItemByKey(fftable).TableEntries.GetMultipleAttributes(["MINUTES", ffcoln]))
    SKM = h.GetMatrixRaw(Visum, skmno)
    FFM = np.interp(SKM, ff_lookup[:,0], ff_lookup[:,1])
    h.SetMatrixRaw(Visum, ffmxno, FFM)
    Visum.Log(PRIO, "done calculating friction factors: {}".format(dstrat))

skmno  =  6 
dstrats= {'EI': ["FF_ALL", "EI", 21], 'HTRK': ["FF_ALL", "HTK", 22], 'LTRK': ["FF_ALL", "LTK", 23], 'NHBO': ["FF_ALL", "NHBO", 24], 'NHBW': ["FF_ALL", "NHBW", 25], 
'TAXI': ["FF_ALL", "TAXI", 26]}

for dstrat in dstrats:
    fftable, ffcoln, ffmxno =  dstrats[dstrat]
    calculate_FF(dstrat, skmno, ffmxno, fftable, ffcoln)