import os
import numpy as np
import pandas as pd
import VisumPy.helpers as h
import VisumPy.matrices as mf


PRIO = 20480
scname  = Visum.Net.AttValue("SC_NAME")


sov_op_m = h.GetMatrixRaw(Visum, 79)
hov_op_m = h.GetMatrixRaw(Visum, 80)+h.GetMatrixRaw(Visum, 81)
sov_pk_m = h.GetMatrixRaw(Visum, 85)
hov_pk_m = h.GetMatrixRaw(Visum, 86)+h.GetMatrixRaw(Visum, 87)
sovp_all=sov_op_m +sov_pk_m 
hovp_all=hov_op_m+hov_pk_m

sov_op_m1 = h.GetMatrixRaw(Visum, 105)
hov_op_m1 = h.GetMatrixRaw(Visum, 107)+h.GetMatrixRaw(Visum, 109)
sov_pk_m1= h.GetMatrixRaw(Visum, 106)
hov_pk_m1 = h.GetMatrixRaw(Visum, 108)+h.GetMatrixRaw(Visum, 110)
sovv_all=sov_op_m1 + sov_pk_m1
hovv_all=hov_op_m1 + hov_pk_m1

# off Peak
sov_op1=sov_op_m.sum(axis=1)
sov_op1_1=sum(sov_op1[0:1000])
sov_op1_2=sum(sov_op1[1000:2000])
sov_op1_3=sum(sov_op1[2000:2500])
sov_op1_4=sum(sov_op1[2500:2800])
sov_op1_5=sum(sov_op1[2800:2950])
sov_op1_6=sum(sov_op1[2950:3000])
sov_op1_7=sum(sov_op1[3000:3032])
sov_op1_T=sum(sov_op1[0:3032])
sov_op=[sov_op1_1,sov_op1_2,sov_op1_3,sov_op1_4,sov_op1_5,sov_op1_6,sov_op1_7,sov_op1_T]
sov_op=pd.DataFrame(sov_op)

hov_op1=hov_op_m.sum(axis=1)
hov_op1_1=sum(hov_op1[0:1000])
hov_op1_2=sum(hov_op1[1000:2000])
hov_op1_3=sum(hov_op1[2000:2500])
hov_op1_4=sum(hov_op1[2500:2800])
hov_op1_5=sum(hov_op1[2800:2950])
hov_op1_6=sum(hov_op1[2950:3000])
hov_op1_7=sum(hov_op1[3000:3032])
hov_op1_T=sum(hov_op1[0:3032])
hov_op=[hov_op1_1,hov_op1_2,hov_op1_3,hov_op1_4,hov_op1_5,hov_op1_6,hov_op1_7,hov_op1_T]
hov_op=pd.DataFrame(hov_op)


v_sov_op1=sov_op_m1.sum(axis=1)
v_sov_op1_1=sum(v_sov_op1[0:1000])
v_sov_op1_2=sum(v_sov_op1[1000:2000])
v_sov_op1_3=sum(v_sov_op1[2000:2500])
v_sov_op1_4=sum(v_sov_op1[2500:2800])
v_sov_op1_5=sum(v_sov_op1[2800:2950])
v_sov_op1_6=sum(v_sov_op1[2950:3000])
v_sov_op1_7=sum(v_sov_op1[3000:3032])
v_sov_op1_T=sum(v_sov_op1[0:3032])
v_sov_op=[v_sov_op1_1,v_sov_op1_2,v_sov_op1_3,v_sov_op1_4,v_sov_op1_5,v_sov_op1_6,v_sov_op1_7,v_sov_op1_T]
v_sov_op=pd.DataFrame(v_sov_op)

v_hov_op1=hov_op_m1.sum(axis=1)
v_hov_op1_1=sum(v_hov_op1[0:1000])
v_hov_op1_2=sum(v_hov_op1[1000:2000])
v_hov_op1_3=sum(v_hov_op1[2000:2500])
v_hov_op1_4=sum(v_hov_op1[2500:2800])
v_hov_op1_5=sum(v_hov_op1[2800:2950])
v_hov_op1_6=sum(v_hov_op1[2950:3000])
v_hov_op1_7=sum(v_hov_op1[3000:3032])
v_hov_op1_T=sum(v_hov_op1[0:3032])
v_hov_op=[v_hov_op1_1,v_hov_op1_2,v_hov_op1_3,v_hov_op1_4,v_hov_op1_5,v_hov_op1_6,v_hov_op1_7,v_hov_op1_T]
v_hov_op=pd.DataFrame(v_hov_op)


op=pd.concat([sov_op,hov_op,v_sov_op,v_hov_op],axis=1)
op.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External","Total"]
op.columns=["SOV Person Trips","HOV Person Trips","SOV Vehicle Trips","HOV Vehicle Trips"]
op["Total Person Trips"]=op["SOV Person Trips"]+op["HOV Person Trips"]
op["Total Vehicle Trips"]=op["SOV Vehicle Trips"]+op["HOV Vehicle Trips"]
op["Auto Occupancy"]=op["Total Person Trips"]/op["Total Vehicle Trips"]
op[["SOV Person Trips","HOV Person Trips","SOV Vehicle Trips","HOV Person Trips","Total Person Trips","Total Vehicle Trips"]]=op[["SOV Person Trips","HOV Person Trips","SOV Vehicle Trips","HOV Person Trips","Total Person Trips","Total Vehicle Trips"]].round(decimals = 0)
op[["Auto Occupancy"]]=op[["Auto Occupancy"]].round(decimals = 2)
writer=pd.ExcelWriter(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\MODE_Highway.xlsx".format(scname)),engine="xlsxwriter")
op.to_excel(writer,sheet_name='Off-Peak')

op2=op[["SOV Person Trips","HOV Person Trips"]]
b="','"

op2[["SOV Person Trips","HOV Person Trips"]]=op2[["SOV Person Trips","HOV Person Trips"]].astype(str)
op2_sovp=list(op2["SOV Person Trips"])
op2_sovp=op2_sovp[:7]
op2_sovp="["+"'"+b.join(op2_sovp) +"'"+"]" 
op2_hovp=list(op2["HOV Person Trips"])
op2_hovp=op2_hovp[:7]
op2_hovp="["+"'"+b.join(op2_hovp) +"'"+"]" 

op2=op[["SOV Vehicle Trips","HOV Vehicle Trips"]]
op2[["SOV Vehicle Trips","HOV Vehicle Trips"]]=op2[["SOV Vehicle Trips","HOV Vehicle Trips"]].astype(int)

op2[["SOV Vehicle Trips","HOV Vehicle Trips"]]=op2[["SOV Vehicle Trips","HOV Vehicle Trips"]].astype(str)
op2_sovv=list(op2["SOV Vehicle Trips"])
op2_sovv=op2_sovv[:7]
op2_sovv="["+"'"+b.join(op2_sovv) +"'"+"]" 
op2_hovv=list(op2["HOV Vehicle Trips"])
op2_hovv=op2_hovv[:7]
op2_hovv="["+"'"+b.join(op2_hovv) +"'"+"]" 

op["SOV Person Trips"]=op["SOV Person Trips"].map("{:,.0f}".format)
op["SOV Vehicle Trips"]=op["SOV Vehicle Trips"].map("{:,.0f}".format)
op["HOV Person Trips"]=op["HOV Person Trips"].map("{:,.0f}".format)
op["HOV Vehicle Trips"]=op["HOV Vehicle Trips"].map("{:,.0f}".format)
op["Total Person Trips"]=op["Total Person Trips"].map("{:,.0f}".format)
op["Total Vehicle Trips"]=op["Total Vehicle Trips"].map("{:,.0f}".format)
op_html=op.to_html(index=True,bold_rows=True)



# Peak
sov_pk1=sov_pk_m.sum(axis=1)
sov_pk1_1=sum(sov_pk1[0:1000])
sov_pk1_2=sum(sov_pk1[1000:2000])
sov_pk1_3=sum(sov_pk1[2000:2500])
sov_pk1_4=sum(sov_pk1[2500:2800])
sov_pk1_5=sum(sov_pk1[2800:2950])
sov_pk1_6=sum(sov_pk1[2950:3000])
sov_pk1_7=sum(sov_pk1[3000:3032])
sov_pk1_T=sum(sov_pk1[0:3032])
sov_pk=[sov_pk1_1,sov_pk1_2,sov_pk1_3,sov_pk1_4,sov_pk1_5,sov_pk1_6,sov_pk1_7,sov_pk1_T]
sov_pk=pd.DataFrame(sov_pk)

hov_pk1=hov_pk_m.sum(axis=1)
hov_pk1_1=sum(hov_pk1[0:1000])
hov_pk1_2=sum(hov_pk1[1000:2000])
hov_pk1_3=sum(hov_pk1[2000:2500])
hov_pk1_4=sum(hov_pk1[2500:2800])
hov_pk1_5=sum(hov_pk1[2800:2950])
hov_pk1_6=sum(hov_pk1[2950:3000])
hov_pk1_7=sum(hov_pk1[3000:3032])
hov_pk1_T=sum(hov_pk1[0:3032])
hov_pk=[hov_pk1_1,hov_pk1_2,hov_pk1_3,hov_pk1_4,hov_pk1_5,hov_pk1_6,hov_pk1_7,hov_pk1_T]
hov_pk=pd.DataFrame(hov_pk)


v_sov_pk1=sov_pk_m1.sum(axis=1)
v_sov_pk1_1=sum(v_sov_pk1[0:1000])
v_sov_pk1_2=sum(v_sov_pk1[1000:2000])
v_sov_pk1_3=sum(v_sov_pk1[2000:2500])
v_sov_pk1_4=sum(v_sov_pk1[2500:2800])
v_sov_pk1_5=sum(v_sov_pk1[2800:2950])
v_sov_pk1_6=sum(v_sov_pk1[2950:3000])
v_sov_pk1_7=sum(v_sov_pk1[3000:3032])
v_sov_pk1_T=sum(v_sov_pk1[0:3032])
v_sov_pk=[v_sov_pk1_1,v_sov_pk1_2,v_sov_pk1_3,v_sov_pk1_4,v_sov_pk1_5,v_sov_pk1_6,v_sov_pk1_7,v_sov_pk1_T]
v_sov_pk=pd.DataFrame(v_sov_pk)

v_hov_pk1=hov_pk_m1.sum(axis=1)
v_hov_pk1_1=sum(v_hov_pk1[0:1000])
v_hov_pk1_2=sum(v_hov_pk1[1000:2000])
v_hov_pk1_3=sum(v_hov_pk1[2000:2500])
v_hov_pk1_4=sum(v_hov_pk1[2500:2800])
v_hov_pk1_5=sum(v_hov_pk1[2800:2950])
v_hov_pk1_6=sum(v_hov_pk1[2950:3000])
v_hov_pk1_7=sum(v_hov_pk1[3000:3032])
v_hov_pk1_T=sum(v_hov_pk1[0:3032])
v_hov_pk=[v_hov_pk1_1,v_hov_pk1_2,v_hov_pk1_3,v_hov_pk1_4,v_hov_pk1_5,v_hov_pk1_6,v_hov_pk1_7,v_hov_pk1_T]
v_hov_pk=pd.DataFrame(v_hov_pk)


pk=pd.concat([sov_pk,hov_pk,v_sov_pk,v_hov_pk],axis=1)
pk.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External","Total"]
pk.columns=["SOV Person Trips","HOV Person Trips","SOV Vehicle Trips","HOV Vehicle Trips"]
pk["Total Person Trips"]=pk["SOV Person Trips"]+pk["HOV Person Trips"]
pk["Total Vehicle Trips"]=pk["SOV Vehicle Trips"]+pk["HOV Vehicle Trips"]
pk["Auto Occupancy"]=pk["Total Person Trips"]/pk["Total Vehicle Trips"]
pk[["SOV Person Trips","HOV Person Trips","SOV Vehicle Trips","HOV Person Trips","Total Person Trips","Total Vehicle Trips"]]=pk[["SOV Person Trips","HOV Person Trips","SOV Vehicle Trips","HOV Person Trips","Total Person Trips","Total Vehicle Trips"]].round(decimals = 0)
pk[["Auto Occupancy"]]=pk[["Auto Occupancy"]].round(decimals = 2)
pk_html=pk.to_html(index=True,bold_rows=True)
pk.to_excel(writer,sheet_name='Peak')


pk2=pk[["SOV Person Trips","HOV Person Trips"]]
b="','"
pk2[["SOV Person Trips","HOV Person Trips"]]=pk2[["SOV Person Trips","HOV Person Trips"]].astype(str)
pk2_sovp=list(pk2["SOV Person Trips"])
pk2_sovp=pk2_sovp[:7]
pk2_sovp="["+"'"+b.join(pk2_sovp) +"'"+"]" 
pk2_hovp=list(pk2["HOV Person Trips"])
pk2_hovp=pk2_hovp[:7]
pk2_hovp="["+"'"+b.join(pk2_hovp) +"'"+"]" 
pk2=pk[["SOV Vehicle Trips","HOV Vehicle Trips"]]
b="','"
pk2[["SOV Vehicle Trips","HOV Vehicle Trips"]]=pk2[["SOV Vehicle Trips","HOV Vehicle Trips"]].astype(str)
pk2_sovv=list(pk2["SOV Vehicle Trips"])
pk2_sovv=pk2_sovv[:7]
pk2_sovv="["+"'"+b.join(pk2_sovv) +"'"+"]" 
pk2_hovv=list(pk2["HOV Vehicle Trips"])
pk2_hovv=pk2_hovv[:7]
pk2_hovv="["+"'"+b.join(pk2_hovv) +"'"+"]" 

pk["SOV Person Trips"]=pk["SOV Person Trips"].map("{:,.0f}".format)
pk["SOV Vehicle Trips"]=pk["SOV Vehicle Trips"].map("{:,.0f}".format)
pk["HOV Person Trips"]=pk["HOV Person Trips"].map("{:,.0f}".format)
pk["HOV Vehicle Trips"]=pk["HOV Vehicle Trips"].map("{:,.0f}".format)
pk["Total Person Trips"]=pk["Total Person Trips"].map("{:,.0f}".format)
pk["Total Vehicle Trips"]=pk["Total Vehicle Trips"].map("{:,.0f}".format)
pk_html=pk.to_html(index=True,bold_rows=True)

#DA 
sov_all1=sovp_all.sum(axis=1)
sov_all1_1=sum(sov_all1[0:1000])
sov_all1_2=sum(sov_all1[1000:2000])
sov_all1_3=sum(sov_all1[2000:2500])
sov_all1_4=sum(sov_all1[2500:2800])
sov_all1_5=sum(sov_all1[2800:2950])
sov_all1_6=sum(sov_all1[2950:3000])
sov_all1_7=sum(sov_all1[3000:3032])
sov_all1_T=sum(sov_all1[0:3032])
sov_all=[sov_all1_1,sov_all1_2,sov_all1_3,sov_all1_4,sov_all1_5,sov_all1_6,sov_all1_7,sov_all1_T]
sov_all=pd.DataFrame(sov_all)

hov_all1=hovp_all.sum(axis=1)
hov_all1_1=sum(hov_all1[0:1000])
hov_all1_2=sum(hov_all1[1000:2000])
hov_all1_3=sum(hov_all1[2000:2500])
hov_all1_4=sum(hov_all1[2500:2800])
hov_all1_5=sum(hov_all1[2800:2950])
hov_all1_6=sum(hov_all1[2950:3000])
hov_all1_7=sum(hov_all1[3000:3032])
hov_all1_T=sum(hov_all1[0:3032])
hov_all=[hov_all1_1,hov_all1_2,hov_all1_3,hov_all1_4,hov_all1_5,hov_all1_6,hov_all1_7,hov_all1_T]
hov_all=pd.DataFrame(hov_all)


v_sov_all1=sovv_all.sum(axis=1)
v_sov_all1_1=sum(v_sov_all1[0:1000])
v_sov_all1_2=sum(v_sov_all1[1000:2000])
v_sov_all1_3=sum(v_sov_all1[2000:2500])
v_sov_all1_4=sum(v_sov_all1[2500:2800])
v_sov_all1_5=sum(v_sov_all1[2800:2950])
v_sov_all1_6=sum(v_sov_all1[2950:3000])
v_sov_all1_7=sum(v_sov_all1[3000:3032])
v_sov_all1_T=sum(v_sov_all1[0:3032])
v_sov_all=[v_sov_all1_1,v_sov_all1_2,v_sov_all1_3,v_sov_all1_4,v_sov_all1_5,v_sov_all1_6,v_sov_all1_7,v_sov_all1_T]
v_sov_all=pd.DataFrame(v_sov_all)

v_hov_all1=hovv_all.sum(axis=1)
v_hov_all1_1=sum(v_hov_all1[0:1000])
v_hov_all1_2=sum(v_hov_all1[1000:2000])
v_hov_all1_3=sum(v_hov_all1[2000:2500])
v_hov_all1_4=sum(v_hov_all1[2500:2800])
v_hov_all1_5=sum(v_hov_all1[2800:2950])
v_hov_all1_6=sum(v_hov_all1[2950:3000])
v_hov_all1_7=sum(v_hov_all1[3000:3032])
v_hov_all1_T=sum(v_hov_all1[0:3032])
v_hov_all=[v_hov_all1_1,v_hov_all1_2,v_hov_all1_3,v_hov_all1_4,v_hov_all1_5,v_hov_all1_6,v_hov_all1_7,v_hov_all1_T]
v_hov_all=pd.DataFrame(v_hov_all)


all=pd.concat([sov_all,hov_all,v_sov_all,v_hov_all],axis=1)
all.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External","Total"]
all.columns=["SOV Person Trips","HOV Person Trips","SOV Vehicle Trips","HOV Vehicle Trips"]
all["Total Person Trips"]=all["SOV Person Trips"]+all["HOV Person Trips"]
all["Total Vehicle Trips"]=all["SOV Vehicle Trips"]+all["HOV Vehicle Trips"]
all["Auto Occupancy"]=all["Total Person Trips"]/all["Total Vehicle Trips"]
all[["SOV Person Trips","HOV Person Trips","SOV Vehicle Trips","HOV Person Trips","Total Person Trips","Total Vehicle Trips"]]=all[["SOV Person Trips","HOV Person Trips","SOV Vehicle Trips","HOV Person Trips","Total Person Trips","Total Vehicle Trips"]].round(decimals = 0)
all[["Auto Occupancy"]]=all[["Auto Occupancy"]].round(decimals = 2)
all.to_excel(writer,sheet_name='Daily')
writer.close()

all2=all[["SOV Person Trips","HOV Person Trips"]]
b="','"

all2[["SOV Person Trips","HOV Person Trips"]]=all2[["SOV Person Trips","HOV Person Trips"]].astype(str)
all2_sovp=list(all2["SOV Person Trips"])
all2_sovp=all2_sovp[:7]
all2_sovp="["+"'"+b.join(all2_sovp) +"'"+"]" 
all2_hovp=list(all2["HOV Person Trips"])
all2_hovp=all2_hovp[:7]
all2_hovp="["+"'"+b.join(all2_hovp) +"'"+"]" 

all2=all[["SOV Vehicle Trips","HOV Vehicle Trips"]]
all2[["SOV Vehicle Trips","HOV Vehicle Trips"]]=all2[["SOV Vehicle Trips","HOV Vehicle Trips"]].astype(int)

all2[["SOV Vehicle Trips","HOV Vehicle Trips"]]=all2[["SOV Vehicle Trips","HOV Vehicle Trips"]].astype(str)
all2_sovv=list(all2["SOV Vehicle Trips"])
all2_sovv=all2_sovv[:7]
all2_sovv="["+"'"+b.join(all2_sovv) +"'"+"]" 
all2_hovv=list(all2["HOV Vehicle Trips"])
all2_hovv=all2_hovv[:7]
all2_hovv="["+"'"+b.join(all2_hovv) +"'"+"]" 

all["SOV Person Trips"]=all["SOV Person Trips"].map("{:,.0f}".format)
all["SOV Vehicle Trips"]=all["SOV Vehicle Trips"].map("{:,.0f}".format)
all["HOV Person Trips"]=all["HOV Person Trips"].map("{:,.0f}".format)
all["HOV Vehicle Trips"]=all["HOV Vehicle Trips"].map("{:,.0f}".format)
all["Total Person Trips"]=all["Total Person Trips"].map("{:,.0f}".format)
all["Total Vehicle Trips"]=all["Total Vehicle Trips"].map("{:,.0f}".format)
all_html=all.to_html(index=True,bold_rows=True)

op1=op[["SOV Person Trips","HOV Person Trips","SOV Vehicle Trips","HOV Vehicle Trips","Total Person Trips","Total Vehicle Trips","Auto Occupancy"]]
op1["Auto Occupancy"]=str(op1["Auto Occupancy"])
hills_op_sov=op1.loc["Hillsborough"]["SOV Person Trips"]
hills_op_hov=op1.loc["Hillsborough"]["HOV Person Trips"]
hills_op_tt=op1.loc["Hillsborough"]["Total Person Trips"]
hills_op_auto=op1.loc["Hillsborough"]["Auto Occupancy"]
pine_op_sov=op1.loc["Pinellas"]["SOV Person Trips"]
pine_op_hov=op1.loc["Pinellas"]["HOV Person Trips"]
pine_op_tt=op1.loc["Pinellas"]["Total Person Trips"]
pine_op_auto=op1.loc["Pinellas"]["Auto Occupancy"]
pasco_op_sov=op1.loc["Pasco"]["SOV Person Trips"]
pasco_op_hov=op1.loc["Pasco"]["HOV Person Trips"]
pasco_op_auto=op1.loc["Pasco"]["Auto Occupancy"]
pasco_op_tt=op1.loc["Pasco"]["Total Person Trips"]
hern_op_sov=op1.loc["Hernando"]["SOV Person Trips"]
hern_op_hov=op1.loc["Hernando"]["HOV Person Trips"]
hern_op_tt=op1.loc["Hernando"]["Total Person Trips"]
hern_op_auto=op1.loc["Hernando"]["Auto Occupancy"]
cit_op_sov=op1.loc["Citrus"]["SOV Person Trips"]
cit_op_hov=op1.loc["Citrus"]["HOV Person Trips"]
cit_op_tt=op1.loc["Citrus"]["Total Person Trips"]
cit_op_auto=op1.loc["Citrus"]["Auto Occupancy"]

hills_opp="Hillsborough:"+"<br>SOV:"+hills_op_sov+"<br>HOV:"+hills_op_hov+"<br>Total:"+hills_op_tt
pasco_opp="Pasco:"+"<br>SOV:"+pasco_op_sov+"<br>HOV:"+pasco_op_hov+"<br>Total:"+pasco_op_tt
pinellas_opp="Pinellas:"+"<br>SOV:"+pine_op_sov+"<br>HOV:"+pine_op_hov+"<br>Total:"+pine_op_tt
hernando_opp="Hernando:"+"<br>SOV:"+hern_op_sov+"<br>HOV:"+hern_op_hov+"<br>Total:"+hern_op_tt
citrus_opp="Citrus:"+"<br>SOV:"+cit_op_sov+"<br>HOV:"+cit_op_hov+"<br>Total:"+cit_op_tt

pk1=pk[["SOV Person Trips","HOV Person Trips","SOV Vehicle Trips","HOV Vehicle Trips","Total Person Trips","Total Vehicle Trips","Auto Occupancy"]]
pk1["Auto Occupancy"]=str(pk1["Auto Occupancy"])
hills_pk_sov=pk1.loc["Hillsborough"]["SOV Person Trips"]
hills_pk_hov=pk1.loc["Hillsborough"]["HOV Person Trips"]
hills_pk_tt=pk1.loc["Hillsborough"]["Total Person Trips"]
hills_pk_auto=pk1.loc["Hillsborough"]["Auto Occupancy"]
pine_pk_sov=pk1.loc["Pinellas"]["SOV Person Trips"]
pine_pk_hov=pk1.loc["Pinellas"]["HOV Person Trips"]
pine_pk_tt=pk1.loc["Pinellas"]["Total Person Trips"]
pine_pk_auto=pk1.loc["Pinellas"]["Auto Occupancy"]
pasco_pk_sov=pk1.loc["Pasco"]["SOV Person Trips"]
pasco_pk_hov=pk1.loc["Pasco"]["HOV Person Trips"]
pasco_pk_tt=pk1.loc["Pasco"]["Total Person Trips"]
pasco_pk_auto=pk1.loc["Pasco"]["Auto Occupancy"]
hern_pk_sov=pk1.loc["Hernando"]["SOV Person Trips"]
hern_pk_hov=pk1.loc["Hernando"]["HOV Person Trips"]
hern_pk_tt=pk1.loc["Hernando"]["Total Person Trips"]
hern_pk_auto=pk1.loc["Hernando"]["Auto Occupancy"]
cit_pk_sov=pk1.loc["Citrus"]["SOV Person Trips"]
cit_pk_hov=pk1.loc["Citrus"]["HOV Person Trips"]
cit_pk_tt=pk1.loc["Citrus"]["Total Person Trips"]
cit_pk_auto=pk1.loc["Citrus"]["Auto Occupancy"]
hills_pkp="Hillsborough:"+"<br>SOV:"+hills_pk_sov+"<br>HOV:"+hills_pk_hov+"<br>Total:"+hills_pk_tt
pasco_pkp="Pasco:"+"<br>SOV:"+pasco_pk_sov+"<br>HOV:"+pasco_pk_hov+"<br>Total:"+pasco_pk_tt
pinellas_pkp="Pinellas:"+"<br>SOV:"+pine_pk_sov+"<br>HOV:"+pine_pk_hov+"<br>Total:"+pine_pk_tt
hernando_pkp="Hernando:"+"<br>SOV:"+hern_pk_sov+"<br>HOV:"+hern_pk_hov+"<br>Total:"+hern_pk_tt
citrus_pkp="Citrus:"+"<br>SOV:"+cit_pk_sov+"<br>HOV:"+cit_pk_hov+"<br>Total:"+cit_pk_tt

all1=all[["SOV Person Trips","HOV Person Trips","SOV Vehicle Trips","HOV Vehicle Trips","Total Person Trips","Total Vehicle Trips","Auto Occupancy"]]
all1["Auto Occupancy"]=str(all1["Auto Occupancy"])
hills_all_sov=all1.loc["Hillsborough"]["SOV Person Trips"]
hills_all_hov=all1.loc["Hillsborough"]["HOV Person Trips"]
hills_all_tt=all1.loc["Hillsborough"]["Total Person Trips"]
hills_all_auto=all1.loc["Hillsborough"]["Auto Occupancy"]
pine_all_sov=all1.loc["Pinellas"]["SOV Person Trips"]
pine_all_hov=all1.loc["Pinellas"]["HOV Person Trips"]
pine_all_tt=all1.loc["Pinellas"]["Total Person Trips"]
pine_all_auto=all1.loc["Pinellas"]["Auto Occupancy"]
pasco_all_sov=all1.loc["Pasco"]["SOV Person Trips"]
pasco_all_hov=all1.loc["Pasco"]["HOV Person Trips"]
pasco_all_tt=all1.loc["Pasco"]["Total Person Trips"]
pasco_all_auto=all1.loc["Pasco"]["Auto Occupancy"]
hern_all_sov=all1.loc["Hernando"]["SOV Person Trips"]
hern_all_hov=all1.loc["Hernando"]["HOV Person Trips"]
hern_all_tt=all1.loc["Hernando"]["Total Person Trips"]
hern_all_auto=all1.loc["Hernando"]["Auto Occupancy"]
cit_all_sov=all1.loc["Citrus"]["SOV Person Trips"]
cit_all_hov=all1.loc["Citrus"]["HOV Person Trips"]
cit_all_tt=all1.loc["Citrus"]["Total Person Trips"]
cit_all_auto=all1.loc["Citrus"]["Auto Occupancy"]
hills_allp="Hillsborough:"+"<br>SOV:"+hills_all_sov+"<br>HOV:"+hills_all_hov+"<br>Total:"+hills_all_tt
pasco_allp="Pasco:"+"<br>SOV:"+pasco_all_sov+"<br>HOV:"+pasco_all_hov+"<br>Total:"+pasco_all_tt
pinellas_allp="Pinellas:"+"<br>SOV:"+pine_all_sov+"<br>HOV:"+pine_all_hov+"<br>Total:"+pine_all_tt
hernando_allp="Hernando:"+"<br>SOV:"+hern_all_sov+"<br>HOV:"+hern_all_hov+"<br>Total:"+hern_all_tt
citrus_allp="Citrus:"+"<br>SOV:"+cit_all_sov+"<br>HOV:"+cit_all_hov+"<br>Total:"+cit_all_tt


hills_op_sov=op1.loc["Hillsborough"]["SOV Vehicle Trips"]
hills_op_hov=op1.loc["Hillsborough"]["HOV Vehicle Trips"]
hills_op_tt=op1.loc["Hillsborough"]["Total Vehicle Trips"]
pine_op_sov=op1.loc["Pinellas"]["SOV Vehicle Trips"]
pine_op_hov=op1.loc["Pinellas"]["HOV Vehicle Trips"]
pine_op_tt=op1.loc["Pinellas"]["Total Vehicle Trips"]
pasco_op_sov=op1.loc["Pasco"]["SOV Vehicle Trips"]
pasco_op_hov=op1.loc["Pasco"]["HOV Vehicle Trips"]
pasco_op_tt=op1.loc["Pasco"]["Total Vehicle Trips"]
hern_op_sov=op1.loc["Hernando"]["SOV Vehicle Trips"]
hern_op_hov=op1.loc["Hernando"]["HOV Vehicle Trips"]
hern_op_tt=op1.loc["Hernando"]["Total Vehicle Trips"]
cit_op_sov=op1.loc["Citrus"]["SOV Vehicle Trips"]
cit_op_hov=op1.loc["Citrus"]["HOV Vehicle Trips"]
cit_op_tt=op1.loc["Citrus"]["Total Vehicle Trips"]
hills_opv="Hillsborough:"+"<br>SOV:"+hills_op_sov+"<br>HOV:"+hills_op_hov+"<br>Total:"+hills_op_tt
pasco_opv="Pasco:"+"<br>SOV:"+pasco_op_sov+"<br>HOV:"+pasco_op_hov+"<br>Total:"+pasco_op_tt
pinellas_opv="Pinellas:"+"<br>SOV:"+pine_op_sov+"<br>HOV:"+pine_op_hov+"<br>Total:"+pine_op_tt
hernando_opv="Hernando:"+"<br>SOV:"+hern_op_sov+"<br>HOV:"+hern_op_hov+"<br>Total:"+hern_op_tt
citrus_opv="Citrus:"+"<br>SOV:"+cit_op_sov+"<br>HOV:"+cit_op_hov+"<br>Total:"+cit_op_tt


hills_pk_sov=pk1.loc["Hillsborough"]["SOV Vehicle Trips"]
hills_pk_hov=pk1.loc["Hillsborough"]["HOV Vehicle Trips"]
hills_pk_tt=pk1.loc["Hillsborough"]["Total Vehicle Trips"]
pine_pk_sov=pk1.loc["Pinellas"]["SOV Vehicle Trips"]
pine_pk_hov=pk1.loc["Pinellas"]["HOV Vehicle Trips"]
pine_pk_tt=pk1.loc["Pinellas"]["Total Vehicle Trips"]
pasco_pk_sov=pk1.loc["Pasco"]["SOV Vehicle Trips"]
pasco_pk_hov=pk1.loc["Pasco"]["HOV Vehicle Trips"]
pasco_pk_tt=pk1.loc["Pasco"]["Total Vehicle Trips"]
hern_pk_sov=pk1.loc["Hernando"]["SOV Vehicle Trips"]
hern_pk_hov=pk1.loc["Hernando"]["HOV Vehicle Trips"]
hern_pk_tt=pk1.loc["Hernando"]["Total Vehicle Trips"]
cit_pk_sov=pk1.loc["Citrus"]["SOV Vehicle Trips"]
cit_pk_hov=pk1.loc["Citrus"]["HOV Vehicle Trips"]
cit_pk_tt=pk1.loc["Citrus"]["Total Vehicle Trips"]
hills_pkv="Hillsborough:"+"<br>SOV:"+hills_pk_sov+"<br>HOV:"+hills_pk_hov+"<br>Total:"+hills_pk_tt
pasco_pkv="Pasco:"+"<br>SOV:"+pasco_pk_sov+"<br>HOV:"+pasco_pk_hov+"<br>Total:"+pasco_pk_tt
pinellas_pkv="Pinellas:"+"<br>SOV:"+pine_pk_sov+"<br>HOV:"+pine_pk_hov+"<br>Total:"+pine_pk_tt
hernando_pkv="Hernando:"+"<br>SOV:"+hern_pk_sov+"<br>HOV:"+hern_pk_hov+"<br>Total:"+hern_pk_tt
citrus_pkv="Citrus:"+"<br>SOV:"+cit_pk_sov+"<br>HOV:"+cit_pk_hov+"<br>Total:"+cit_pk_tt

hills_all_sov=all1.loc["Hillsborough"]["SOV Vehicle Trips"]
hills_all_hov=all1.loc["Hillsborough"]["HOV Vehicle Trips"]
hills_all_tt=all1.loc["Hillsborough"]["Total Vehicle Trips"]

pine_all_sov=all1.loc["Pinellas"]["SOV Vehicle Trips"]
pine_all_hov=all1.loc["Pinellas"]["HOV Vehicle Trips"]
pine_all_tt=all1.loc["Pinellas"]["Total Vehicle Trips"]
pasco_all_sov=all1.loc["Pasco"]["SOV Vehicle Trips"]
pasco_all_hov=all1.loc["Pasco"]["HOV Vehicle Trips"]
pasco_all_tt=all1.loc["Pasco"]["Total Vehicle Trips"]
hern_all_sov=all1.loc["Hernando"]["SOV Vehicle Trips"]
hern_all_hov=all1.loc["Hernando"]["HOV Vehicle Trips"]
hern_all_tt=all1.loc["Hernando"]["Total Vehicle Trips"]
cit_all_sov=all1.loc["Citrus"]["SOV Vehicle Trips"]
cit_all_hov=all1.loc["Citrus"]["HOV Vehicle Trips"]
cit_all_tt=all1.loc["Citrus"]["Total Vehicle Trips"]
hills_allv="Hillsborough:"+"<br>SOV:"+hills_all_sov+"<br>HOV:"+hills_all_hov+"<br>Total:"+hills_all_tt
pasco_allv="Pasco:"+"<br>SOV:"+pasco_all_sov+"<br>HOV:"+pasco_all_hov+"<br>Total:"+pasco_all_tt
pinellas_allv="Pinellas:"+"<br>SOV:"+pine_all_sov+"<br>HOV:"+pine_all_hov+"<br>Total:"+pine_all_tt
hernando_allv="Hernando:"+"<br>SOV:"+hern_all_sov+"<br>HOV:"+hern_all_hov+"<br>Total:"+hern_all_tt
citrus_allv="Citrus:"+"<br>SOV:"+cit_all_sov+"<br>HOV:"+cit_all_hov+"<br>Total:"+cit_all_tt


msg1 = "Off-Peak Highway Trips"
msg2="Peak Highway Trips"
msg3="Daily Highway Trips"

base  = Visum.Net.AttValue("Base")
title = """
    <html>
<head>


<title>"""+scname+" "+""" Tampa Bay Regional Planning Model </title>
<meta charset="utf-8" />
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="">
<meta name="author" content="Mark Otto, Jacob Thornton, and Bootstrap contributors">
<meta name="generator" content="Hugo 0.98.0">
<link rel="canonical" href="https://getbootstrap.com/docs/5.2/examples/sidebars/">
<link href="../assets/dist/css/bootstrap.min.css" rel="stylesheet">

<!--Load jQuery-->
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.6.4/js/bootstrap-datepicker.min.js"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.6.4/css/bootstrap-datepicker.min.css" rel="stylesheet"/>


<!-- SEARCH CONTROL -->
	<link rel="stylesheet" href="src/leaflet-search.css"/>

<!-- Chart.js -->	
	<script src="https://cdn.jsdelivr.net/npm/chart.js@3.4.0/dist/chart.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.5.1/chart.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-datalabels/2.0.0/chartjs-plugin-datalabels.min.js"></script>

	<!-- Jquery JS -->
	<script src="http://code.jqiery.com/jquery.js"></script>
	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.0/jquery.min.js"></script>

	<!-- Leaflet JS -->
	<link rel="stylesheet" href="leaflet/leaflet.css">
	<script src="http://cdn.leafletjs.com/leaflet/v0.7.7/leaflet.js"></script>
		  
		   
	
	<link rel="stylesheet" href="leaflet/leaflet.css"/>
	<script src="leaflet/leaflet.js"></script> 
	<script src="js/l.control.geosearch.js"></script>
	<script src="js/l.geosearch.provider.google.js"></script>
    <link rel="stylesheet" href="css/l.geosearch.css"/>
    <script src="src/leaflet.label.js"></script>



<!-- Main Style -->
    <link rel="stylesheet" href="css/summary.css"/>


 </head>
    <style>
 
    
   thead {color: black;}
    tbody {color: black;}
    tfoot {color: red;}
    table{width:550px;height:500px;}
    table, th, td {
      border: 1px solid black;
      text-align:center;
      font-size: 12px;
      height:20px;
      border-collapse: collapse;
    }
td:nth-child(1) {
    text-align:center;
}
td:nth-child(2) {
     text-align:right;
}
td:nth-child(3) {
         text-align:right;
}
td:nth-child(4) {
         text-align:right;
}
td:nth-child(5) {
         text-align:right;
}
td:nth-child(6) {
         text-align:right;
}
td:nth-child(7) {
         text-align:center;
}


.bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }

      .b-example-divider {
        height: 3rem;
        background-color: rgba(0, 0, 0, .1);
        border: solid rgba(0, 0, 0, .15);
        border-width: 1px 0;
        box-shadow: inset 0 .5em 1.5em rgba(0, 0, 0, .1), inset 0 .125em .5em rgba(0, 0, 0, .15);
      }

      .b-example-vr {
        flex-shrink: 0;
        width: 1.5rem;
        height: 100vh;
      }

      .bi {
        vertical-align: -.125em;
        fill: currentColor;
      }

      .nav-scroller {
        position: relative;
        z-index: 2;
        height: 2.75rem;
        overflow-y: hidden;
      }

      .nav-scroller .nav {
        display: flex;
        flex-wrap: nowrap;
        padding-bottom: 1rem;
        margin-top: -1px;
        overflow-x: auto;
        text-align: center;
        white-space: nowrap;
        -webkit-overflow-scrolling: touch;
      }

      * {
  box-sizing: border-box;
}

.box {
  position:absolute;
  top:55px;
  width: 45;
  height:100%;
}
.box_1 {
  position:absolute;
  top:630px;
  left:40px;
  width: 580px;
  height:30;
}

.clearfix::after {
  content: "";
  clear: both;
  display: table;
}

.my-label{
   background:#F2F2F2;
}

    </style>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"></script>
    <body>

<main class="d-flex flex-nowrap" style="position:relative">
<div class="flex-shrink-0 p-3" style="width: 230px;background-color:#F2F2F2">
    <a href="#" class="d-flex align-items-left pb-3 mb-3 link-dark text-decoration-none border-bottom">
      <span class="fs-4 fw-semibold" style="color:#6C8D9C;font-weight:bold">Summary Index</span>
    </a>
    <ul class="list-unstyled ps-0">
      <li><a href="Home.html" class="btn btn-toggle d-inline-flex align-items-center rounded border-0" aria-expanded="false">Home</a></li>
      <li class="mb-1">
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#EE-collapse" aria-expanded="false">
         External
        </button>
        <div class="collapse" id="EE-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
          <li><a href="EEIN.html" class="link-dark d-inline-flex text-decoration-none rounded">Input EE Trips</a></li>
            <li><a href="EEOUT.html" class="link-dark d-inline-flex text-decoration-none rounded" ">Output EE Trips</a></li>
          </ul>
        </div>
      </li>
           <li class="mb-1">
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#generation-collapse" aria-expanded="false">
          Trip Generation
        </button>
        <div class="collapse" id="generation-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
            <li><a href="GEN_Overall.html" class="link-dark d-inline-flex text-decoration-none rounded" >Production & Attraction</a></li>
          <li><a href="GEN_INPUT.html" class="link-dark d-inline-flex text-decoration-none rounded" >Trip Generation Statistics</a></li>
          </ul>
        </div>
      </li>
      <li class="mb-1">
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#dashboard-collapse" aria-expanded="false">
          Trip Distribution
        </button>
        <div class="collapse" id="dashboard-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                     <li><a href="Triplength.html" class="link-dark d-inline-flex text-decoration-none rounded" >Trip Length Overall</a></li>
            <li><a href="Triplength_PK_County.html" class="link-dark d-inline-flex text-decoration-none rounded"  >PK Trip Length by County </a></li>
            <li><a href="Triplength_OP_County.html" class="link-dark d-inline-flex text-decoration-none rounded"  >OP Trip Length by County </a></li>
             <li><a href="DIST_Intra.html" class="link-dark d-inline-flex text-decoration-none rounded" >Intrazonal Trips Overall</a></li>
             <li><a href="DIST_intra_County_PK.html" class="link-dark d-inline-flex text-decoration-none rounded" >PK Intrazonal Trips by County </a></li>
             <li><a href="DIST_intra_County_OP.html" class="link-dark d-inline-flex text-decoration-none rounded" >OP Intrazonal Trips by County </a></li>
          </ul>
        </div>
      </li>
      <li class="mb-1">
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#orders-collapse" aria-expanded="true">
          Mode Choice
        </button>
        <div class="collapse show" id="orders-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
            <li><a href="MODE_overall.html" class="link-dark d-inline-flex text-decoration-none rounded" >Mode Choice Overall</a></li>
            <li><a href="MODE_HWY.html" class="link-dark d-inline-flex text-decoration-none rounded" style="background-color:ADCEDE" >Highway Trips</a></li>
            <li><a href="MODE_transit.html" class="link-dark d-inline-flex text-decoration-none rounded" >Transit Trips</a></li>
          </ul>
        </div>
      </li>
     <li class="mb-1">
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#Transit-collapse" aria-expanded="false">
          Transit Assignment
        </button>
        <div class="collapse" id="Transit-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
            <li><a href="TRANSIT_Overall.html" class="link-dark d-inline-flex text-decoration-none rounded" >Transit Summary</a></li>
  
          </ul>
        </div>
      </li>
            <li class="mb-1">
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#Analysis-collapse" aria-expanded="false">
 Highway Analysis
        </button>
        <div class="collapse" id="Analysis-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
            <li><a href="Analysis_Overall.html" class="link-dark d-inline-flex text-decoration-none rounded" >Volume/Capacity</a></li>
            
          </ul>
        </div>
      </li>"""
diff_45="""
      <li class="mb-1">
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#Highway-collapse" aria-expanded="false">
         Highway Validation
        </button>
        <div class="collapse" id="Highway-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
            <li><a href="Validation_Overall.html" class="link-dark d-inline-flex text-decoration-none rounded">VOL/CNT & RMSE</a></li>
            <li><a href="highway_Corridor.html" class="link-dark d-inline-flex text-decoration-none rounded">VOL/CNT by Corridor</a></li>
            <li><a href="highway_FACL.html" class="link-dark d-inline-flex text-decoration-none rounded">VOL/CNT by FT & AT</a></li>
          </ul>
        </div>
      </li>"""
main_continue="""
    </ul>
  </div>
 <div class="notation" id="mode_overall">
    <h6 style="padding: 6px 0;color:black"> *SOV: Drive Alone  <br>*HOV: Share Ride 2 and 3+ </h6>
    </div>
  <div class="button_op" id="buttons">
      <button id="opPerson" type="button" style="width:222px; height:25px; font-size:12px"> Off-Peak Person Trips </button>
																																							   
      <button id="opVehicle" type="button" style="width:222px; height:25px; font-size:12px"> Off-Peak Vehicle Trips </button>
      </div>
      <div class="map_mode" id="map_mode"> 
      </div>
      
      <div class="button_pk" id="buttons">
																																		 
      <button id="pkPerson" type="button" style="width:222px; height:25px; font-size:12px; background-color: #F3A27C"> Peak Person Trips </button>
      <button id="pkVehicle" type="button" style="width:222px; height:25px; font-size:12px"> Peak Vehicle Trips </button>
      </div>

    <header class="navbar navbar-expand-md fixed-top navbar-dark bg-dark">
		<nav class="container-xxl flex-wrap flex-md-nowrap" aria-label="Main navigation">
			<a href="https://tdaappsprod.dot.state.fl.us/fto/" target="_blank">
				<img src="images/fdot_logo_white.png" id="fdot_logo" style="height: 48px; float:left"/>
			</a>
		<div class="collapse navbar-collapse" id="bdNavbar">
		<ul class="navbar-nav flex-row flex-wrap bd-navbar-nav pt-2 py-md-0">
			<li class="nav-item col-6 col-md-auto">
			<a class="nav-link p-3 active" aria-current="true"><b>"""+scname+" "+""" Tampa Bay Regional Planning Model </b></a>
			</li>
		</ul>
		<ul class="navbar-nav flex-row flex-wrap ms-md-auto">
			<li class="nav-item col-6 col-md-auto">
				<a href="https://bcceng.com/" target="_blank"><img src="images/bcc_logo.png" id="bcc_logo" style="height: 48px;"/></a>
			</li>
		</ul>
		</div>
	</nav>
  <a class="contactlink" id="contactlink" aria-current="true" href="https://bccorlando.wixsite.com/tbrpm" target="_blank" style="color: white;"><b>Feedback</b></a>&nbsp
	</header>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
	<div class="MODE_HWYOP" id="barchart_PANDAS">
    <canvas id="bar-chart" style="width:100%;max-width:1200px"></canvas>
    </div>
 	<div class="MODE_HWYPK" id="barchart_PANDAS1">
    <canvas id="bar-chart1" style="width:100%;max-width:1200px"></canvas>
    </div>   
     	<div class="MODE_HWYDA" id="barchart_PANDAS2">
    <canvas id="bar-chart2" style="width:100%;max-width:1200px"></canvas>
    </div>  
<script>

var op2_sovp = """+str(op2_sovp)+""";
var op2_hovp="""+str(op2_hovp)+""";
var op2_sovv="""+str(op2_sovv)+""";
var op2_hovv="""+str(op2_hovv)+""";

new Chart(document.getElementById("bar-chart"), {
    type: 'bar',
    data: {
      labels: ["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External"],
      datasets: [
        {
          label: "SOV Person Trips",
          backgroundColor: "#C1dfec",
          data: op2_sovp
        }, {
          label: "HOV Person Trips",
          backgroundColor: "#5eadd0",
          data: op2_hovp
        }, {
          label: "SOV Vehicle Trips",
          backgroundColor: "#Eeb092",
          data: op2_sovv
        }, {
          label: "HOV Vehicle Trips",
          backgroundColor: "#Bf6d46",
          data: op2_hovv
        }
      ]
    },
    options: { scales:{
        x: {
            ticks: {
                font: {
                    size: 10,
                }
            }
        },
        y: {
            ticks: {
                font: {
                    size: 10,
                }
            }
        }
      },
      plugins:{
      legend:{
          display:true,
          position:"bottom",
          labels:{
            font:{
              size:10
            }
          }

        },  
      title: {
        display: true,
        text: 'Off-Peak Highway Trips',
        font:{
          size:14
        }
      }
      }
    }
});

var pk2_sovp = """+str(pk2_sovp)+""";
var pk2_hovp="""+str(pk2_hovp)+""";
var pk2_sovv="""+str(pk2_sovv)+""";
var pk2_hovv="""+str(pk2_hovv)+""";

new Chart(document.getElementById("bar-chart1"), {
    type: 'bar',
    data: {
      labels: ["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External"],
      datasets: [
        {
          label: "SOV Person Trips",
          backgroundColor: "#C1dfec",
          data: pk2_sovp
        }, {
          label: "HOV Person Trips",
          backgroundColor: "#5eadd0",
          data: pk2_hovp
        }, {
          label: "SOV Vehicle Trips",
          backgroundColor: "#Eeb092",
          data: pk2_sovv
        }, {
          label: "HOV Vehicle Trips",
          backgroundColor: "#Bf6d46",
          data: pk2_hovv
        }
      ]
    },
    options: {
      scales:{
        x: {
            ticks: {
                font: {
                    size: 10,
                }
            }
        },
        y: {
            ticks: {
                font: {
                    size: 10,
                }
            }
        }
      },
      plugins:{
        legend:{
           position:"bottom",
          display:true,
          labels:{
            font:{
              size:10
            }
          }

        },
      title: {
        display: true,
        text: 'Peak Highway Trips',
        font:{
          size:14
        }
      }
      }
    }
});
var all2_sovp = """+str(all2_sovp)+""";
var all2_hovp="""+str(all2_hovp)+""";
var all2_sovv="""+str(all2_sovv)+""";
var all2_hovv="""+str(all2_hovv)+""";

new Chart(document.getElementById("bar-chart2"), {
    type: 'bar',
    data: {
      labels: ["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External"],
      datasets: [
        {
          label: "SOV Person Trips",
          backgroundColor: "#C1dfec",
          data: all2_sovp
        }, {
          label: "HOV Person Trips",
          backgroundColor: "#5eadd0",
          data: all2_hovp
        }, {
          label: "SOV Vehicle Trips",
          backgroundColor: "#Eeb092",
          data: all2_sovv
        }, {
          label: "HOV Vehicle Trips",
          backgroundColor: "#Bf6d46",
          data: all2_hovv
        }
      ]
    },
    options: {
      scales:{
        x: {
            ticks: {
                font: {
                    size: 10,
                }
            }
        },
        y: {
            ticks: {
                font: {
                    size: 10,
                }
            }
        }
      },
      plugins:{
        legend:{
           position:"bottom",
          display:true,
          labels:{
            font:{
              size:10
            }
          }

        },
      title: {
        display: true,
        text: 'Daily Highway Trips',
        font:{
          size:14
        }
      }
      }
    }
});



</script>	

<script>


var hills_opp= """+"'"+hills_opp+"'"+""";
var pasco_opp= """+"'"+pasco_opp+"'"+""";
var hernando_opp= """+"'"+hernando_opp+"'"+""";
var pinellas_opp= """+"'"+pinellas_opp+"'"+""";
var citrus_opp= """+"'"+citrus_opp+"'"+""";

var hills_pkp= """+"'"+hills_pkp+"'"+""";
var pasco_pkp= """+"'"+pasco_pkp+"'"+""";
var hernando_pkp= """+"'"+hernando_pkp+"'"+""";
var pinellas_pkp= """+"'"+pinellas_pkp+"'"+""";
var citrus_pkp= """+"'"+citrus_pkp+"'"+""";

var hills_allp= """+"'"+hills_allp+"'"+""";
var pasco_allp= """+"'"+pasco_allp+"'"+""";
var hernando_allp= """+"'"+hernando_allp+"'"+""";
var pinellas_allp= """+"'"+pinellas_allp+"'"+""";
var citrus_allp= """+"'"+citrus_allp+"'"+""";

var hills_opv= """+"'"+hills_opv+"'"+""";
var pasco_opv= """+"'"+pasco_opv+"'"+""";
var hernando_opv= """+"'"+hernando_opv+"'"+""";
var pinellas_opv= """+"'"+pinellas_opv+"'"+""";
var citrus_opv= """+"'"+citrus_opv+"'"+""";

var hills_pkv= """+"'"+hills_pkv+"'"+""";
var pasco_pkv= """+"'"+pasco_pkv+"'"+""";
var hernando_pkv= """+"'"+hernando_pkv+"'"+""";
var pinellas_pkv= """+"'"+pinellas_pkv+"'"+""";
var citrus_pkv= """+"'"+citrus_pkv+"'"+""";

var hills_allv= """+"'"+hills_allv+"'"+""";
var pasco_allv= """+"'"+pasco_allv+"'"+""";
var hernando_allv= """+"'"+hernando_allv+"'"+""";
var pinellas_allv= """+"'"+pinellas_allv+"'"+""";
var citrus_allv= """+"'"+citrus_allv+"'"+""";


var map = L.map('map_mode').setView([28.276140, -82.585263], 9);
	
L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/light_all/{z}/{x}/{y}.png', {
attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
subdomains: 'abcd',
maxZoom: 15
  }).addTo(map);

      var hillsborough = new L.marker([28.039646, -82.420602], { opacity: 0.01 });
      hillsborough.bindLabel(hills_pkp, {noHide: true, className: "my-label", offset: [0, 0]});
      hillsborough.addTo(map);

      var pasco = new L.marker([28.295848, -82.471609], { opacity: 0.01 });
      pasco.bindLabel(pasco_pkp, {noHide: true, className: "my-label", offset: [0, 0] });
      pasco.addTo(map);

      var hernando = new L.marker([28.566409, -82.471609], { opacity: 0.01 });
      hernando.bindLabel(hernando_pkp, {noHide: true, className: "my-label", offset: [0, 0] });
      hernando.addTo(map);

      var pinellas = new L.marker([27.907086, -82.759073], { opacity: 0.01 });
      pinellas.bindLabel(pinellas_pkp, {noHide: true, className: "my-label", offset: [0, 0] });
      pinellas.addTo(map);

      var citrus = new L.marker([28.785449, -82.471609], { opacity: 0.01 });
      citrus.bindLabel(citrus_pkp, {noHide: true, className: "my-label", offset: [0, 0] });
      citrus.addTo(map);

	 var hillsborough = L.icon({
        iconUrl: 'images/County/hillsborough.png',
        iconSize: [35,17],
      });
      L.marker([28.039646, -82.420602],{icon: hillsborough}).addTo(map)  
  
      var pinellas = L.icon({
        iconUrl: 'images/County/pinellas.png',
        iconSize: [35,17],

      });
      L.marker([27.907086, -82.759073],{icon: pinellas}).addTo(map)
  
      var pasco = L.icon({
        iconUrl: 'images/County/pasco.png',
        iconSize: [30,30],
      });
      L.marker([28.295848, -82.471609],{icon: pasco}).addTo(map)
      var hernando = L.icon({
        iconUrl: 'images/County/hernando.png',
        iconSize: [30,30],
      });
      L.marker([28.566409, -82.471609],{icon: hernando}).addTo(map)
      var citrus = L.icon({
        iconUrl: 'images/County/citrus.png',
        iconSize: [30,30],
      });
      L.marker([28.785449, -82.471609],{icon: citrus}).addTo(map)

      var button_opp = document.getElementById("opPerson");
      button_opp.addEventListener("click", function(event){
        button_opp.style.backgroundColor = "#92B6C7";
        button_opv.style.backgroundColor = "#f0f0f0";
        button_pkp.style.backgroundColor = "#f0f0f0";
        button_pkv.style.backgroundColor = "#f0f0f0";
        var hillsborough = new L.marker([28.039646, -82.420602], { opacity: 0.01 });
        hillsborough.bindLabel(hills_opp, {noHide: true, className: "my-label", offset: [0, 0]});
        hillsborough.addTo(map);
        var pasco = new L.marker([28.295848, -82.471609], { opacity: 0.01 });
        pasco.bindLabel(pasco_opp, {noHide: true, className: "my-label", offset: [0, 0] });
        pasco.addTo(map);
        var hernando = new L.marker([28.566409, -82.471609], { opacity: 0.01 });
        hernando.bindLabel(hernando_opp, {noHide: true, className: "my-label", offset: [0, 0] });
        hernando.addTo(map);
        var pinellas = new L.marker([27.907086, -82.759073], { opacity: 0.01 });
        pinellas.bindLabel(pinellas_opp, {noHide: true, className: "my-label", offset: [0, 0] });
        pinellas.addTo(map);
        var citrus = new L.marker([28.785449, -82.471609], { opacity: 0.01 });
        citrus.bindLabel(citrus_opp, {noHide: true, className: "my-label", offset: [0, 0] });
        citrus.addTo(map);

        var hillsborough = L.icon({
          iconUrl: 'images/County/hillsborough.png',
          iconSize: [35,17],
        });
        L.marker([28.039646, -82.420602],{icon: hillsborough}).addTo(map)  
        var pinellas = L.icon({
          iconUrl: 'images/County/pinellas.png',
          iconSize: [35,17],
        });
        L.marker([27.907086, -82.759073],{icon: pinellas}).addTo(map)
        var pasco = L.icon({
          iconUrl: 'images/County/pasco.png',
          iconSize: [30,30],
        });
        L.marker([28.295848, -82.471609],{icon: pasco}).addTo(map)
        var hernando = L.icon({
          iconUrl: 'images/County/hernando.png',
          iconSize: [30,30],
        });
        L.marker([28.566409, -82.471609],{icon: hernando}).addTo(map)
        var citrus = L.icon({
          iconUrl: 'images/County/citrus.png',
          iconSize: [30,30],
        });
        L.marker([28.785449, -82.471609],{icon: citrus}).addTo(map)
      });

      var button_opv = document.getElementById("opVehicle");
      button_opv.addEventListener("click", function(event){
        button_opv.style.backgroundColor = "#92B6C7";
        button_opp.style.backgroundColor = "#f0f0f0";
        button_pkp.style.backgroundColor = "#f0f0f0";
        button_pkv.style.backgroundColor = "#f0f0f0";
        var hillsborough = new L.marker([28.039646, -82.420602], { opacity: 0.01 });
        hillsborough.bindLabel(hills_opv, {noHide: true, className: "my-label", offset: [0, 0]});
        hillsborough.addTo(map);
        var pasco = new L.marker([28.295848, -82.471609], { opacity: 0.01 });
        pasco.bindLabel(pasco_opv, {noHide: true, className: "my-label", offset: [0, 0] });
        pasco.addTo(map);
        var hernando = new L.marker([28.566409, -82.471609], { opacity: 0.01 });
        hernando.bindLabel(hernando_opv, {noHide: true, className: "my-label", offset: [0, 0] });
        hernando.addTo(map);
        var pinellas = new L.marker([27.907086, -82.759073], { opacity: 0.01 });
        pinellas.bindLabel(pinellas_opv, {noHide: true, className: "my-label", offset: [0, 0] });
        pinellas.addTo(map);
        var citrus = new L.marker([28.785449, -82.471609], { opacity: 0.01 });
        citrus.bindLabel(citrus_opv, {noHide: true, className: "my-label", offset: [0, 0] });
        citrus.addTo(map);

        var hillsborough = L.icon({
          iconUrl: 'images/County/hillsborough.png',
          iconSize: [35,17],
        });
        L.marker([28.039646, -82.420602],{icon: hillsborough}).addTo(map)  
        var pinellas = L.icon({
          iconUrl: 'images/County/pinellas.png',
          iconSize: [35,17],
        });
        L.marker([27.907086, -82.759073],{icon: pinellas}).addTo(map)
        var pasco = L.icon({
          iconUrl: 'images/County/pasco.png',
          iconSize: [30,30],
        });
        L.marker([28.295848, -82.471609],{icon: pasco}).addTo(map)
        var hernando = L.icon({
          iconUrl: 'images/County/hernando.png',
          iconSize: [30,30],
        });
        L.marker([28.566409, -82.471609],{icon: hernando}).addTo(map)
        var citrus = L.icon({
          iconUrl: 'images/County/citrus.png',
          iconSize: [30,30],
        });
        L.marker([28.785449, -82.471609],{icon: citrus}).addTo(map)
      });

      var button_pkp = document.getElementById("pkPerson");
      button_pkp.addEventListener("click", function(event){
        button_pkp.style.backgroundColor = "#F3A27C";
        button_opv.style.backgroundColor = "#f0f0f0";
        button_opp.style.backgroundColor = "#f0f0f0";
        button_pkv.style.backgroundColor = "#f0f0f0";
        var hillsborough = new L.marker([28.039646, -82.420602], { opacity: 0.01 });
        hillsborough.bindLabel(hills_pkp, {noHide: true, className: "my-label", offset: [0, 0] });
        hillsborough.addTo(map);
        var pasco = new L.marker([28.295848, -82.471609], { opacity: 0.01 });
        pasco.bindLabel(pasco_pkp, {noHide: true, className: "my-label", offset: [0, 0] });
        pasco.addTo(map);
        var hernando = new L.marker([28.566409, -82.471609], { opacity: 0.01 });
        hernando.bindLabel(hernando_pkp, {noHide: true, className: "my-label", offset: [0, 0] });
        hernando.addTo(map);
        var pinellas = new L.marker([27.907086, -82.759073], { opacity: 0.01 });
        pinellas.bindLabel(pinellas_pkp, {noHide: true, className: "my-label", offset: [0, 0] });
        pinellas.addTo(map);
        var citrus = new L.marker([28.785449, -82.471609], { opacity: 0.01 });
        citrus.bindLabel(citrus_pkp, {noHide: true, className: "my-label", offset: [0, 0] });
        citrus.addTo(map);

        var hillsborough = L.icon({
          iconUrl: 'images/County/hillsborough.png',
          iconSize: [35,17],
        });
        L.marker([28.039646, -82.420602],{icon: hillsborough}).addTo(map)  
        var pinellas = L.icon({
          iconUrl: 'images/County/pinellas.png',
          iconSize: [35,17],
        });
        L.marker([27.907086, -82.759073],{icon: pinellas}).addTo(map)
        var pasco = L.icon({
          iconUrl: 'images/County/pasco.png',
          iconSize: [30,30],
        });
        L.marker([28.295848, -82.471609],{icon: pasco}).addTo(map)
        var hernando = L.icon({
          iconUrl: 'images/County/hernando.png',
          iconSize: [30,30],
        });
        L.marker([28.566409, -82.471609],{icon: hernando}).addTo(map)
        var citrus = L.icon({
          iconUrl: 'images/County/citrus.png',
          iconSize: [30,30],
        });
        L.marker([28.785449, -82.471609],{icon: citrus}).addTo(map)
      });

      var button_pkv = document.getElementById("pkVehicle");
      button_pkv.addEventListener("click", function(event){
        button_pkv.style.backgroundColor = "#F3A27C";
        button_opp.style.backgroundColor = "#f0f0f0";
        button_opv.style.backgroundColor = "#f0f0f0";
        button_pkp.style.backgroundColor = "#f0f0f0";
        var hillsborough = new L.marker([28.039646, -82.420602], { opacity: 0.01 });
        hillsborough.bindLabel(hills_pkv, {noHide: true, className: "my-label", offset: [0, 0] });
        hillsborough.addTo(map);
        var pasco = new L.marker([28.295848, -82.471609], { opacity: 0.01 });
        pasco.bindLabel(pasco_pkv, {noHide: true, className: "my-label", offset: [0, 0] });
        pasco.addTo(map);
        var hernando = new L.marker([28.566409, -82.471609], { opacity: 0.01 });
        hernando.bindLabel(hernando_pkv, {noHide: true, className: "my-label", offset: [0, 0] });
        hernando.addTo(map);
        var pinellas = new L.marker([27.907086, -82.759073], { opacity: 0.01 });
        pinellas.bindLabel(pinellas_pkv, {noHide: true, className: "my-label", offset: [0, 0] });
        pinellas.addTo(map);
        var citrus = new L.marker([28.785449, -82.471609], { opacity: 0.01 });
        citrus.bindLabel(citrus_pkv, {noHide: true, className: "my-label", offset: [0, 0] });
        citrus.addTo(map);

        var hillsborough = L.icon({
          iconUrl: 'images/County/hillsborough.png',
          iconSize: [35,17],
        });
        L.marker([28.039646, -82.420602],{icon: hillsborough}).addTo(map)  
        var pinellas = L.icon({
          iconUrl: 'images/County/pinellas.png',
          iconSize: [35,17],
        });
        L.marker([27.907086, -82.759073],{icon: pinellas}).addTo(map)
        var pasco = L.icon({
          iconUrl: 'images/County/pasco.png',
          iconSize: [30,30],
        });
        L.marker([28.295848, -82.471609],{icon: pasco}).addTo(map)
        var hernando = L.icon({
          iconUrl: 'images/County/hernando.png',
          iconSize: [30,30],
        });
        L.marker([28.566409, -82.471609],{icon: hernando}).addTo(map)
        var citrus = L.icon({
          iconUrl: 'images/County/citrus.png',
          iconSize: [30,30],
        });
        L.marker([28.785449, -82.471609],{icon: citrus}).addTo(map)
      });

</script>
</body>

   <div class="MODEhigh_op" id="op">
    <h4 style="padding: 5px 0;color:black">
    """ +msg1 + "</h4>"

table2="""
</div>
   <div class="MODEhigh_pk" id="pk">
    <h4 style="padding: 5px 0;color:black">
    """ +msg2 + "</h4>"
table3="""
</div>
   <div class="MODEhigh_all" id="pk">
    <h4 style="padding: 5px 0;color:black">
    """ +msg3 + "</h4>"

end_html = """
        </div>
        </body>
        </html>
        """


if base==1:
  html = title +diff_45+main_continue+ op_html +table2+pk_html+ table3+all_html+end_html
else:
    html = title +main_continue+ op_html +table2+pk_html+ table3+all_html+end_html

text_file = open(os.path.join(Visum.GetPath(2), "outputs\\{}\\HTML\\MODE_HWY.html".format(scname)), "w")
text_file.write(html)
text_file.close()