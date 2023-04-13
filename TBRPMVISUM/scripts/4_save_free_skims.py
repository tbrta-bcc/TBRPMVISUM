# Save free skims to disk -> these are then used for all off-peak calculations
# Chetan Joshi, Portland OR 3/22/2022
import os 
# 6	TT0	t0 SOV
# 7	TTC	tCur SOV
# 8	DIS	Trip distance SOV
# 9	TOL	Toll SOV
# 10	TT0	t0 HOV
# 11	TTC	tCur HOV
# 12	DIS	Trip distance HOV
# 13	TOL	Toll HOV
# 61	IMP	Impedance SOV
# 62	IMP	Impedance HOV 
SCNAME  = Visum.Net.AttValue("SC_NAME")
BASEDIR   = Visum.GetPath(2)
SOVMXLIST = [[6, 'TT0'], [7, 'TTC'], [8, 'DIS'], [9, 'TOL'], [61, 'IMP']] 
HOVMXLIST = [[10, 'TT0'], [11, 'TTC'], [12, 'DIS'], [13, 'TOL'], [62, 'IMP']]

for mxno, mxname in SOVMXLIST:
    Visum.Net.Matrices.ItemByKey(mxno).Save(os.path.join(BASEDIR, "outputs\\{}\\skims\\ff_sov.{}".format(SCNAME,mxname)), 0)


for mxno, mxname in HOVMXLIST:
    Visum.Net.Matrices.ItemByKey(mxno).Save(os.path.join(BASEDIR, "outputs\\{}\\skims\\ff_hov.{}".format(SCNAME,mxname)), 0)
