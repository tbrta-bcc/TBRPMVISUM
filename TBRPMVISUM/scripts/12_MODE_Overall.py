import os
import numpy as np
import pandas as pd
import VisumPy.helpers as h
import VisumPy.matrices as mf


PRIO = 20480
scname  = Visum.Net.AttValue("SC_NAME")


sov_op_m = h.GetMatrixRaw(Visum, 79)
sr2_op_m = h.GetMatrixRaw(Visum, 80)
sr3_op_m = h.GetMatrixRaw(Visum, 81)
twk_op_m = h.GetMatrixRaw(Visum, 82)
knr_op_m = h.GetMatrixRaw(Visum, 83)
pnr_op_m = h.GetMatrixRaw(Visum, 84)
sov_pk_m = h.GetMatrixRaw(Visum, 85)
sr2_pk_m = h.GetMatrixRaw(Visum, 86)
sr3_pk_m = h.GetMatrixRaw(Visum, 87)
twk_pk_m = h.GetMatrixRaw(Visum, 88)
knr_pk_m = h.GetMatrixRaw(Visum, 89)
pnr_pk_m = h.GetMatrixRaw(Visum, 90)

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

sr2_op1=sr2_op_m.sum(axis=1)
sr2_op1_1=sum(sr2_op1[0:1000])
sr2_op1_2=sum(sr2_op1[1000:2000])
sr2_op1_3=sum(sr2_op1[2000:2500])
sr2_op1_4=sum(sr2_op1[2500:2800])
sr2_op1_5=sum(sr2_op1[2800:2950])
sr2_op1_6=sum(sr2_op1[2950:3000])
sr2_op1_7=sum(sr2_op1[3000:3032])
sr2_op1_T=sum(sr2_op1[0:3032])
sr2_op=[sr2_op1_1,sr2_op1_2,sr2_op1_3,sr2_op1_4,sr2_op1_5,sr2_op1_6,sr2_op1_7,sr2_op1_T]
sr2_op=pd.DataFrame(sr2_op)

sr3_op1=sr3_op_m.sum(axis=1)
sr3_op1_1=sum(sr3_op1[0:1000])
sr3_op1_2=sum(sr3_op1[1000:2000])
sr3_op1_3=sum(sr3_op1[2000:2500])
sr3_op1_4=sum(sr3_op1[2500:2800])
sr3_op1_5=sum(sr3_op1[2800:2950])
sr3_op1_6=sum(sr3_op1[2950:3000])
sr3_op1_7=sum(sr3_op1[3000:3032])
sr3_op1_T=sum(sr3_op1[0:3032])
sr3_op=[sr3_op1_1,sr3_op1_2,sr3_op1_3,sr3_op1_4,sr3_op1_5,sr3_op1_6,sr3_op1_7,sr3_op1_T]
sr3_op=pd.DataFrame(sr3_op)

twk_op1=twk_op_m.sum(axis=1)
twk_op1_1=sum(twk_op1[0:1000])
twk_op1_2=sum(twk_op1[1000:2000])
twk_op1_3=sum(twk_op1[2000:2500])
twk_op1_4=sum(twk_op1[2500:2800])
twk_op1_5=sum(twk_op1[2800:2950])
twk_op1_6=sum(twk_op1[2950:3000])
twk_op1_7=sum(twk_op1[3000:3032])
twk_op1_T=sum(twk_op1[0:3032])
twk_op=[twk_op1_1,twk_op1_2,twk_op1_3,twk_op1_4,twk_op1_5,twk_op1_6,twk_op1_7,twk_op1_T]
twk_op=pd.DataFrame(twk_op)

knr_op1=knr_op_m.sum(axis=1)
knr_op1_1=sum(knr_op1[0:1000])
knr_op1_2=sum(knr_op1[1000:2000])
knr_op1_3=sum(knr_op1[2000:2500])
knr_op1_4=sum(knr_op1[2500:2800])
knr_op1_5=sum(knr_op1[2800:2950])
knr_op1_6=sum(knr_op1[2950:3000])
knr_op1_7=sum(knr_op1[3000:3032])
knr_op1_T=sum(knr_op1[0:3032])
knr_op=[knr_op1_1,knr_op1_2,knr_op1_3,knr_op1_4,knr_op1_5,knr_op1_6,knr_op1_7,knr_op1_T]
knr_op=pd.DataFrame(knr_op)

pnr_op1=pnr_op_m.sum(axis=1)
pnr_op1_1=sum(pnr_op1[0:1000])
pnr_op1_2=sum(pnr_op1[1000:2000])
pnr_op1_3=sum(pnr_op1[2000:2500])
pnr_op1_4=sum(pnr_op1[2500:2800])
pnr_op1_5=sum(pnr_op1[2800:2950])
pnr_op1_6=sum(pnr_op1[2950:3000])
pnr_op1_7=sum(pnr_op1[3000:3032])
pnr_op1_T=sum(pnr_op1[0:3032])
pnr_op=[pnr_op1_1,pnr_op1_2,pnr_op1_3,pnr_op1_4,pnr_op1_5,pnr_op1_6,pnr_op1_7,pnr_op1_T]
pnr_op=pd.DataFrame(pnr_op)

op=pd.concat([sov_op,sr2_op,sr3_op,twk_op,knr_op,pnr_op],axis=1)
op.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External","Total"]
op.columns=["sov","sr2","sr3","walk to bus","kiss&ride","park&ride"]
op["transit"]=op["walk to bus"]+op["kiss&ride"]+op["park&ride"]
op["total"]=op["sov"]+op["sr2"]+op["sr3"]+op["transit"]
op["hov"]=op["sr2"]+op["sr3"]
op["sov_per"]=op["sov"]/op["total"]*100
op["sr2_per"]=op["sr2"]/op["total"]*100
op["sr3_per"]=op["sr3"]/op["total"]*100
op["transit_per"]=op["transit"]/op["total"]*100
op["hov_per"]=op["hov"]/op["total"]*100

op_bar=op[["sov_per","sr2_per","sr3_per","transit_per"]]

for columns in op_bar:
  op_bar[columns]=op_bar[columns].round(2)

op_bar["sov_per"]=op_bar["sov_per"].astype(str)
op_bar["sr2_per"]=op_bar["sr2_per"].astype(str)
op_bar["sr3_per"]=op_bar["sr3_per"].astype(str)
op_bar["transit_per"]=op_bar["transit_per"].astype(str)

op_barsov=list(op_bar["sov_per"])
op_barsr2=list(op_bar["sr2_per"])
op_barsr3=list(op_bar["sr3_per"])
op_bartransit=list(op_bar["transit_per"])
b="','"
op_barsov="["+"'"+b.join(op_barsov) +"'"+"]"
op_barsr2="["+"'"+b.join(op_barsr2) +"'"+"]"
op_barsr3="["+"'"+b.join(op_barsr3) +"'"+"]"
op_bartransit="["+"'"+b.join(op_bartransit) +"'"+"]"



op2=op[["sov","hov","transit","total"]]
op2[["sov","hov","transit","total"]]=op2[["sov","hov","transit","total"]].astype(str)


op1_str=op2.values.tolist()
op1_str=op1_str[7]

x="["+"'"+b.join(op1_str) +"'"+"]" 
op3=op[["sov_per","hov_per","transit_per"]]
op3=op3.round(2)
op3[["sov_per","hov_per","transit_per"]]=op3[["sov_per","hov_per","transit_per"]].astype(str)
op3_str=op3.values.tolist()
op3_str=op3_str[7]
x1="["+"'"+b.join(op3_str) +"'"+"]" 

op["sov"]=op["sov"].map("{:,.0f}".format)
op["sr2"]=op["sr2"].map("{:,.0f}".format)
op["sr3"]=op["sr3"].map("{:,.0f}".format)
op["hov"]=op["hov"].map("{:,.0f}".format)
op["total"]=op["total"].map("{:,.0f}".format)
op["transit"]=op["transit"].map("{:,.0f}".format)
op["walk to bus"]=op["walk to bus"].map("{:,.0f}".format)
op["kiss&ride"]=op["kiss&ride"].map("{:,.0f}".format)
op["park&ride"]=op["park&ride"].map("{:,.0f}".format)

writer=pd.ExcelWriter(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\PersonTrips.xlsx".format(scname)),engine="xlsxwriter")
op.to_excel(writer,sheet_name='Off-Peak')






op1=op[["sov","hov","transit","total"]]
op2=op[["sov","sr2","sr3","transit","total"]]
op2.columns=["Drive Alone","Share Ride 2","Share Ride 3+","Transit Trips","Total"]
hills_op_sov=op1.loc["Hillsborough"]["sov"]
hills_op_hov=op1.loc["Hillsborough"]["hov"]
hills_op_transit=op1.loc["Hillsborough"]["transit"]
pine_op_sov=op1.loc["Pinellas"]["sov"]
pine_op_hov=op1.loc["Pinellas"]["hov"]
pine_op_transit=op1.loc["Pinellas"]["transit"]
pasco_op_sov=op1.loc["Pasco"]["sov"]
pasco_op_hov=op1.loc["Pasco"]["hov"]
pasco_op_transit=op1.loc["Pasco"]["transit"]
hern_op_sov=op1.loc["Hernando"]["sov"]
hern_op_hov=op1.loc["Hernando"]["hov"]
hern_op_transit=op1.loc["Hernando"]["transit"]
cit_op_sov=op1.loc["Citrus"]["sov"]
cit_op_hov=op1.loc["Citrus"]["hov"]
cit_op_transit=op1.loc["Citrus"]["transit"]
op_html=op2.to_html(index=True,bold_rows=True)



#peak
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

sr2_pk1=sr2_pk_m.sum(axis=1)
sr2_pk1_1=sum(sr2_pk1[0:1000])
sr2_pk1_2=sum(sr2_pk1[1000:2000])
sr2_pk1_3=sum(sr2_pk1[2000:2500])
sr2_pk1_4=sum(sr2_pk1[2500:2800])
sr2_pk1_5=sum(sr2_pk1[2800:2950])
sr2_pk1_6=sum(sr2_pk1[2950:3000])
sr2_pk1_7=sum(sr2_pk1[3000:3032])
sr2_pk1_T=sum(sr2_pk1[0:3032])
sr2_pk=[sr2_pk1_1,sr2_pk1_2,sr2_pk1_3,sr2_pk1_4,sr2_pk1_5,sr2_pk1_6,sr2_pk1_7,sr2_pk1_T]
sr2_pk=pd.DataFrame(sr2_pk)

sr3_pk1=sr3_pk_m.sum(axis=1)
sr3_pk1_1=sum(sr3_pk1[0:1000])
sr3_pk1_2=sum(sr3_pk1[1000:2000])
sr3_pk1_3=sum(sr3_pk1[2000:2500])
sr3_pk1_4=sum(sr3_pk1[2500:2800])
sr3_pk1_5=sum(sr3_pk1[2800:2950])
sr3_pk1_6=sum(sr3_pk1[2950:3000])
sr3_pk1_7=sum(sr3_pk1[3000:3032])
sr3_pk1_T=sum(sr3_pk1[0:3032])
sr3_pk=[sr3_pk1_1,sr3_pk1_2,sr3_pk1_3,sr3_pk1_4,sr3_pk1_5,sr3_pk1_6,sr3_pk1_7,sr3_pk1_T]
sr3_pk=pd.DataFrame(sr3_pk)

twk_pk1=twk_pk_m.sum(axis=1)
twk_pk1_1=sum(twk_pk1[0:1000])
twk_pk1_2=sum(twk_pk1[1000:2000])
twk_pk1_3=sum(twk_pk1[2000:2500])
twk_pk1_4=sum(twk_pk1[2500:2800])
twk_pk1_5=sum(twk_pk1[2800:2950])
twk_pk1_6=sum(twk_pk1[2950:3000])
twk_pk1_7=sum(twk_pk1[3000:3032])
twk_pk1_T=sum(twk_pk1[0:3032])
twk_pk=[twk_pk1_1,twk_pk1_2,twk_pk1_3,twk_pk1_4,twk_pk1_5,twk_pk1_6,twk_pk1_7,twk_pk1_T]
twk_pk=pd.DataFrame(twk_pk)

knr_pk1=knr_pk_m.sum(axis=1)
knr_pk1_1=sum(knr_pk1[0:1000])
knr_pk1_2=sum(knr_pk1[1000:2000])
knr_pk1_3=sum(knr_pk1[2000:2500])
knr_pk1_4=sum(knr_pk1[2500:2800])
knr_pk1_5=sum(knr_pk1[2800:2950])
knr_pk1_6=sum(knr_pk1[2950:3000])
knr_pk1_7=sum(knr_pk1[3000:3032])
knr_pk1_T=sum(knr_pk1[0:3032])
knr_pk=[knr_pk1_1,knr_pk1_2,knr_pk1_3,knr_pk1_4,knr_pk1_5,knr_pk1_6,knr_pk1_7,knr_pk1_T]
knr_pk=pd.DataFrame(knr_pk)

pnr_pk1=pnr_pk_m.sum(axis=1)
pnr_pk1_1=sum(pnr_pk1[0:1000])
pnr_pk1_2=sum(pnr_pk1[1000:2000])
pnr_pk1_3=sum(pnr_pk1[2000:2500])
pnr_pk1_4=sum(pnr_pk1[2500:2800])
pnr_pk1_5=sum(pnr_pk1[2800:2950])
pnr_pk1_6=sum(pnr_pk1[2950:3000])
pnr_pk1_7=sum(pnr_pk1[3000:3032])
pnr_pk1_T=sum(pnr_pk1[0:3032])
pnr_pk=[pnr_pk1_1,pnr_pk1_2,pnr_pk1_3,pnr_pk1_4,pnr_pk1_5,pnr_pk1_6,pnr_pk1_7,pnr_pk1_T]
pnr_pk=pd.DataFrame(pnr_pk)

pk=pd.concat([sov_pk,sr2_pk,sr3_pk,twk_pk,knr_pk,pnr_pk],axis=1)
pk.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External","Total"]
pk.columns=["sov","sr2","sr3","walk to bus","kiss&ride","park&ride"]
pk["transit"]=pk["walk to bus"]+pk["kiss&ride"]+pk["park&ride"]
pk["total"]=pk["sov"]+pk["sr2"]+pk["sr3"]+pk["transit"]
pk["hov"]=pk["sr2"]+pk["sr3"]
pk["sov_per"]=pk["sov"]/pk["total"]*100
pk["hov_per"]=pk["hov"]/pk["total"]*100
pk["sr2_per"]=pk["sr2"]/pk["total"]*100
pk["sr3_per"]=pk["sr3"]/pk["total"]*100
pk["transit_per"]=pk["transit"]/pk["total"]*100

pk_bar=pk[["sov_per","sr2_per","sr3_per","transit_per"]]

for columns in pk_bar:
  pk_bar[columns]=pk_bar[columns].round(2)


pk_bar["sov_per"]=pk_bar["sov_per"].astype(str)
pk_bar["sr2_per"]=pk_bar["sr2_per"].astype(str)
pk_bar["sr3_per"]=pk_bar["sr3_per"].astype(str)
pk_bar["transit_per"]=pk_bar["transit_per"].astype(str)

pk_barsov=list(pk_bar["sov_per"])
pk_barsr2=list(pk_bar["sr2_per"])
pk_barsr3=list(pk_bar["sr3_per"])
pk_bartransit=list(pk_bar["transit_per"])
b="','"
pk_barsov="["+"'"+b.join(pk_barsov) +"'"+"]"
pk_barsr2="["+"'"+b.join(pk_barsr2) +"'"+"]"
pk_barsr3="["+"'"+b.join(pk_barsr3) +"'"+"]"
pk_bartransit="["+"'"+b.join(pk_bartransit) +"'"+"]"





pk2=pk[["sov","hov","transit","total"]]
pk2[["sov","hov","transit","total"]]=pk2[["sov","hov","transit","total"]].astype(str)

pk1_str=pk2.values.tolist()
pk1_str=pk1_str[7]
b="','"
y="["+"'"+b.join(pk1_str) +"'"+"]"  
pk3=pk[["sov_per","hov_per","transit_per"]]
pk3=pk3.round(2)
pk3[["sov_per","hov_per","transit_per"]]=pk3[["sov_per","hov_per","transit_per"]].astype(str)
pk3_str=pk3.values.tolist()
pk3_str=pk3_str[7]
y1="["+"'"+b.join(pk3_str) +"'"+"]" 
pk["sov"]=pk["sov"].map("{:,.0f}".format)
pk["sr2"]=pk["sr2"].map("{:,.0f}".format)
pk["sr3"]=pk["sr3"].map("{:,.0f}".format)
pk["hov"]=pk["hov"].map("{:,.0f}".format)
pk["total"]=pk["total"].map("{:,.0f}".format)
pk["transit"]=pk["transit"].map("{:,.0f}".format)
pk["walk to bus"]=pk["walk to bus"].map("{:,.0f}".format)
pk["kiss&ride"]=pk["kiss&ride"].map("{:,.0f}".format)
pk["park&ride"]=pk["park&ride"].map("{:,.0f}".format)

pk.to_excel(writer,sheet_name='Peak')
writer.close()

pk1=pk[["sov","hov","transit","total"]]
pk2=pk[["sov","sr2","sr3","transit","total"]]
pk2.columns=["Drive Alone","Share Ride 2","Share Ride 3+","Transit Trips","Total"]
hills_pk_sov=pk1.loc["Hillsborough"]["sov"]
hills_pk_hov=pk1.loc["Hillsborough"]["hov"]
hills_pk_transit=pk1.loc["Hillsborough"]["transit"]
pine_pk_sov=pk1.loc["Pinellas"]["sov"]
pine_pk_hov=pk1.loc["Pinellas"]["hov"]
pine_pk_transit=pk1.loc["Pinellas"]["transit"]
pasco_pk_sov=pk1.loc["Pasco"]["sov"]
pasco_pk_hov=pk1.loc["Pasco"]["hov"]
pasco_pk_transit=pk1.loc["Pasco"]["transit"]
hern_pk_sov=pk1.loc["Hernando"]["sov"]
hern_pk_hov=pk1.loc["Hernando"]["hov"]
hern_pk_transit=pk1.loc["Hernando"]["transit"]
cit_pk_sov=pk1.loc["Citrus"]["sov"]
cit_pk_hov=pk1.loc["Citrus"]["hov"]
cit_pk_transit=pk1.loc["Citrus"]["transit"]
pk_html=pk2.to_html(index=True,bold_rows=True)

hills_op="OP-SOV:"+hills_op_sov+"<br>OP-HOV:"+hills_op_hov+"<br>OP-Transit:"+hills_op_transit
hills_pk="PK-SOV:"+hills_pk_sov+"<br>PK-HOV:"+hills_pk_hov+"<br>PK-Transit:"+hills_pk_transit
pasco_op="OP-SOV:"+pasco_op_sov+"<br>OP-HOV:"+pasco_op_hov+"<br>OP-Transit:"+pasco_op_transit
pasco_pk="PK-SOV:"+pasco_pk_sov+"<br>PK-HOV:"+pasco_pk_hov+"<br>PK-Transit:"+pasco_pk_transit
pinellas_op="OP-SOV:"+pine_op_sov+"<br>OP-HOV:"+pine_op_hov+"<br>OP-Transit:"+pine_op_transit
pinellas_pk="PK-SOV:"+pine_pk_sov+"<br>PK-HOV:"+pine_pk_hov+"<br>PK-Transit:"+pine_pk_transit
hernando_op="OP-SOV:"+hern_op_sov+"<br>OP-HOV:"+hern_op_hov+"<br>OP-Transit:"+hern_op_transit
hernando_pk="PK-SOV:"+hern_pk_sov+"<br>PK-HOV:"+hern_pk_hov+"<br>PK-Transit:"+hern_pk_transit
citrus_op="OP-SOV:"+cit_op_sov+"<br>OP-HOV:"+cit_op_hov+"<br>OP-Transit:"+cit_op_transit
citrus_pk="PK-SOV:"+cit_pk_sov+"<br>PK-HOV:"+cit_pk_hov+"<br>PK-Transit:"+cit_pk_transit


msg1 = "Off-Peak Person Trips"
msg2="Peak Person Trips"

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
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js"></script>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"></script>


	<!-- Jquery JS -->
	<script src="http://code.jqiery.com/jquery.js"></script>
	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.0/jquery.min.js"></script>

	<!-- Leaflet JS -->
	<link rel="stylesheet" href="leaflet/leaflet.css">
	<script src="http://cdn.leafletjs.com/leaflet/v0.7.7/leaflet.js"></script>
      <script src="src/leaflet.label.js"></script>

		  
		   
	
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
  .my-label{
   background:#F2F2F2;
   width: 120px;
}

    
    thead {color: black;}
    tbody {color: black;}
    tfoot {color: red;}
    table{width:550px;height:200px;}
    table, th, td {
      border: 1px solid black;
      text-align:center;
      font-size: 14px;
      height:10px;
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
            <li><a href="MODE_overall.html" class="link-dark d-inline-flex text-decoration-none rounded" style="background-color:ADCEDE">Mode Choice Overall</a></li>
            <li><a href="MODE_HWY.html" class="link-dark d-inline-flex text-decoration-none rounded" >Highway Trips</a></li>
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

  
<div class="button_MODE_transit" id="buttons">
      <button id="pk" type="button" style="width:150px; height:25px; font-size:12px; background-color: #92B6C7;"> Peak Person Trips </button>
																																							   
      <button id="op" type="button" style="width:150px; height:25px; font-size:12px"> Off-Peak Person Trips </button>
      </div>

<div class="map_mode1" id="map_mode"> </div>



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

     <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"></script>

    	<script src="[https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.3.0/Chart.min.js](https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.3.0/Chart.min.js)"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-datalabels/2.1.0/chartjs-plugin-datalabels.min.js"></script>
	  
    
    <div class="groupbar_mode" id="barchart_PANDAS">
   <h4 style="padding: 10px 0;color:black"> Off-Peak Mode Share </h4>

    <canvas id="myChart4" tyle="width:100%;max-width:1200px"></canvas>
    </div> 
    
    <div class="groupbar_mode2" id="barchart_PANDAS">
    <h4 style="padding: 10px 0;color:black"> Peak Mode Share </h4>
     <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0-rc"></script>
    <canvas id="myChart5" tyle="width:100%;max-width:1200px"></canvas>
    </div>


    <div class="notation" id="mode_overall">
    <h6 style="padding: 6px 0;color:black"> *SOV: Drive Alone  <br>*HOV: Share Ride 2 and 3+ </h6>
    </div>

    
    <script>

var xValues ="""+str(op_barsov)+""";
var yValues="""+str(op_barsr2)+""";
var zValues="""+str(op_barsr3)+""";
var mValues="""+str(op_bartransit)+""";

new Chart(document.getElementById("myChart4"), {
    type: 'bar',
    plugins: [ChartDataLabels],
    data: {
      labels: ["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External","Total"],
      datasets: [
        {
          label: "Drive Alone",
          backgroundColor: "#92B6C7",
          data: xValues
        }, 
        {
          label: "Shared Ride 2",
          backgroundColor: "#F3A27C",
          data: yValues
        }, 
        {
          label: "Share Ride 3+",
          backgroundColor: "#D37995",
          data: zValues
        }, 
        {
          label: "Transit",
          backgroundColor: "#6CBE7C",
          data: mValues
        }
      ]
    },
    options: {
      responsive: true,      
      scales: {
      x: {
	
								  
        stacked: true,
				   
					  
				   
      },
      y: {
            stacked: true,
            min: 0,
            max: 100,
        }
    },
      plugins: {
        legend:{
          display:true,
          position:"bottom",
          labels:{
            font:{
              size:10
            }
          }

        },  
        datalabels: {
          formatter: function(value) {
            if(value >= 0){
            return value + '%';}else{
              value = "";
              return value;
            }
          },
          anchor: 'center',
          align: 'center',
          labels: {
            value: {
              color: 'dark gray',
              font:{size:9}
            }
          }
        }
      }
    }
});

var xValues ="""+str(pk_barsov)+""";
var yValues="""+str(pk_barsr2)+""";
var zValues="""+str(pk_barsr3)+""";
var mValues="""+str(pk_bartransit)+""";

new Chart(document.getElementById("myChart5"), {
    type: 'bar',
    plugins: [ChartDataLabels],
    data: {
      labels: ["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External","Total"],
      datasets: [
        {
          label: "Drive Alone",
          backgroundColor: "#92B6C7",
          data: xValues
        }, 
        {
          label: "Shared Ride 2",
          backgroundColor: "#F3A27C",
          data: yValues
        }, 
        {
          label: "Share Ride 3+",
          backgroundColor: "#D37995",
          data: zValues
        }, 
        {
          label: "Transit",
          backgroundColor: "#6CBE7C",
          data: mValues
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
      x: {
        stacked: true,
      },
      y: {
            stacked: true,
            min: 0,
            max: 100,
				   
				
        }
    },
      plugins: {
        legend:{
          display:true,
          position:"bottom",
          labels:{
            font:{
              size:10
            }
          }

        },  
  
        datalabels: {
          formatter: function(value) {
            if(value >= 0){
            return value + '%';}else{
              value = "";
              return value;
            }
          },
          anchor: 'center',
          align: 'center',
          labels: {
            value: {
              color: 'dark gray',
              font:{size:9}
            }
          }
        }
      }
    }
});
</script>
    




    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/emn178/chartjs-plugin-labels/src/chartjs-plugin-labels.js"></script>

    <div class="pie" id="pie">
    <canvas id="myChart_op" style="width:100%;max-width:600px"></canvas>
    </div>
        <div class="pie1" id="pie">
    <canvas id="myChart_pk" style="width:100%;max-width:600px"></canvas>
    </div>
<script>
var xValues = ["Drive Alone", "High Occupancy Vehicle", "Transit"];
var yValues = """+x1+""";
var yValues1 = """+y1+""";
var barColors = [
  "#92B6C7",
  "#F3A27C",
  "#6CBE7C",
];

new Chart("myChart_op", {
  type: "doughnut",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {
       legend:{
          position: 'right',
          labels:{
            fontColor: "gray"
          }
        },
    title: {
      display: true,
      text: "Person Trips Mode Share - Off-Peak",
      font:{
        size:20
      }
    },
    datalabels:{
    formatter:(value)=>{
    return value*100 + "%";
    },
    color:"#fff",
    }
  }
});

new Chart("myChart_pk", {
  type: "doughnut",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues1
    }]
  },
  options: {
       legend:{
          position: 'right',
          labels:{
            fontColor: "gray"
          }
        },
    title: {
      display: true,
      text: "Person Trips Mode Share - Peak"
    },
    datalabels:{
    formatter:(value)=>{
    return value*100 + "%";
    },
    color:"#fff",
    }
  }
});
</script>

<script>
var hills_op= """+"'"+hills_op+"'"+""";
var pasco_op= """+"'"+pasco_op+"'"+""";
var hernando_op= """+"'"+hernando_op+"'"+""";
var pinellas_op= """+"'"+pinellas_op+"'"+""";
var citrus_op= """+"'"+citrus_op+"'"+""";

var hills_pk= """+"'"+hills_pk+"'"+""";
var pasco_pk= """+"'"+pasco_pk+"'"+""";
var hernando_pk= """+"'"+hernando_pk+"'"+""";
var pinellas_pk= """+"'"+pinellas_pk+"'"+""";
var citrus_pk= """+"'"+citrus_pk+"'"+""";


var map = L.map('map_mode').setView([28.276140, -82.585263], 9);
	
L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/light_all/{z}/{x}/{y}.png', {
attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
subdomains: 'abcd',
maxZoom: 15
  }).addTo(map);

      var hillsborough = new L.marker([28.039646, -82.420602], { opacity: 0.01 });
      hillsborough.bindLabel(hills_pk, {noHide: true, className: "my-label", offset: [0, 0]});
      hillsborough.addTo(map);

      var pasco = new L.marker([28.295848, -82.471609], { opacity: 0.01 });
      pasco.bindLabel(pasco_pk, {noHide: true, className: "my-label", offset: [0, 0] });
      pasco.addTo(map);

      var hernando = new L.marker([28.566409, -82.471609], { opacity: 0.01 });
      hernando.bindLabel(hernando_pk, {noHide: true, className: "my-label", offset: [0, 0] });
      hernando.addTo(map);

      var pinellas = new L.marker([27.907086, -82.759073], { opacity: 0.01 });
      pinellas.bindLabel(pinellas_pk, {noHide: true, className: "my-label", offset: [0, 0] });
      pinellas.addTo(map);

      var citrus = new L.marker([28.785449, -82.471609], { opacity: 0.01 });
      citrus.bindLabel(citrus_pk, {noHide: true, className: "my-label", offset: [0, 0] });
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

 var button_op = document.getElementById("op");
      button_op.addEventListener("click", function(event){
        button_op.style.backgroundColor = "#92B6C7";
        button_pk.style.backgroundColor = "#f0f0f0";
        var hillsborough = new L.marker([28.039646, -82.420602], { opacity: 0.01 });
        hillsborough.bindLabel(hills_op, {noHide: true, className: "my-label", offset: [0, 0]});
        hillsborough.addTo(map);
        var pasco = new L.marker([28.295848, -82.471609], { opacity: 0.01 });
        pasco.bindLabel(pasco_op, {noHide: true, className: "my-label", offset: [0, 0] });
        pasco.addTo(map);
        var hernando = new L.marker([28.566409, -82.471609], { opacity: 0.01 });
        hernando.bindLabel(hernando_op, {noHide: true, className: "my-label", offset: [0, 0] });
        hernando.addTo(map);
        var pinellas = new L.marker([27.907086, -82.759073], { opacity: 0.01 });
        pinellas.bindLabel(pinellas_op, {noHide: true, className: "my-label", offset: [0, 0] });
        pinellas.addTo(map);
        var citrus = new L.marker([28.785449, -82.471609], { opacity: 0.01 });
        citrus.bindLabel(citrus_op, {noHide: true, className: "my-label", offset: [0, 0] });
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

      var button_pk = document.getElementById("pk");
      button_pk.addEventListener("click", function(event){
        button_pk.style.backgroundColor = "#92B6C7";
        button_op.style.backgroundColor = "#f0f0f0";
        var hillsborough = new L.marker([28.039646, -82.420602], { opacity: 0.01 });
        hillsborough.bindLabel(hills_pk, {noHide: true, className: "my-label", offset: [0, 0]});
        hillsborough.addTo(map);
        var pasco = new L.marker([28.295848, -82.471609], { opacity: 0.01 });
        pasco.bindLabel(pasco_pk, {noHide: true, className: "my-label", offset: [0, 0] });
        pasco.addTo(map);
        var hernando = new L.marker([28.566409, -82.471609], { opacity: 0.01 });
        hernando.bindLabel(hernando_pk, {noHide: true, className: "my-label", offset: [0, 0] });
        hernando.addTo(map);
        var pinellas = new L.marker([27.907086, -82.759073], { opacity: 0.01 });
        pinellas.bindLabel(pinellas_pk, {noHide: true, className: "my-label", offset: [0, 0] });
        pinellas.addTo(map);
        var citrus = new L.marker([28.785449, -82.471609], { opacity: 0.01 });
        citrus.bindLabel(citrus_pk, {noHide: true, className: "my-label", offset: [0, 0] });
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

   <div class="MODE_op" id="op">
    <h4 style="padding: 10px 0;color:black">
    """ +msg1 + "</h4>"

table2="""
</div>
   <div class="MODE_pk" id="pk">
    <h4 style="padding: 10px 0;color:black">
    """ +msg2 + "</h4>"

end_html = """
        </div>
        </body>
        </html>
        """
if base==1:
  html = title +diff_45+main_continue+ op_html +table2+pk_html+ end_html
else:
  html = title +main_continue+ op_html +table2+pk_html+ end_html

text_file = open(os.path.join(Visum.GetPath(2), "outputs\\{}\\HTML\\MODE_overall.html".format(scname)), "w")
text_file.write(html)
text_file.close()


