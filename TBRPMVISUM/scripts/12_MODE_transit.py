import os
import numpy as np
import pandas as pd
import VisumPy.helpers as h
import VisumPy.matrices as mf


PRIO = 20480
scname  = Visum.Net.AttValue("SC_NAME")



twk_op_m = h.GetMatrixRaw(Visum, 82)
KNR_op_m = h.GetMatrixRaw(Visum, 83)
PNR_op_m = h.GetMatrixRaw(Visum, 84)
twk_pk_m = h.GetMatrixRaw(Visum, 88)
KNR_pk_m = h.GetMatrixRaw(Visum, 89)
PNR_pk_m = h.GetMatrixRaw(Visum, 90)
twk_all_m=twk_op_m+twk_pk_m 
KNR_all_m=KNR_op_m+KNR_pk_m 
PNR_all_m=PNR_op_m+PNR_pk_m 


# off Peak
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

KNR_op1=KNR_op_m.sum(axis=1)
KNR_op1_1=sum(KNR_op1[0:1000])
KNR_op1_2=sum(KNR_op1[1000:2000])
KNR_op1_3=sum(KNR_op1[2000:2500])
KNR_op1_4=sum(KNR_op1[2500:2800])
KNR_op1_5=sum(KNR_op1[2800:2950])
KNR_op1_6=sum(KNR_op1[2950:3000])
KNR_op1_7=sum(KNR_op1[3000:3032])
KNR_op1_T=sum(KNR_op1[0:3032])
KNR_op=[KNR_op1_1,KNR_op1_2,KNR_op1_3,KNR_op1_4,KNR_op1_5,KNR_op1_6,KNR_op1_7,KNR_op1_T]
KNR_op=pd.DataFrame(KNR_op)

PNR_op1=PNR_op_m.sum(axis=1)
PNR_op1_1=sum(PNR_op1[0:1000])
PNR_op1_2=sum(PNR_op1[1000:2000])
PNR_op1_3=sum(PNR_op1[2000:2500])
PNR_op1_4=sum(PNR_op1[2500:2800])
PNR_op1_5=sum(PNR_op1[2800:2950])
PNR_op1_6=sum(PNR_op1[2950:3000])
PNR_op1_7=sum(PNR_op1[3000:3032])
PNR_op1_T=sum(PNR_op1[0:3032])
PNR_op=[PNR_op1_1,PNR_op1_2,PNR_op1_3,PNR_op1_4,PNR_op1_5,PNR_op1_6,PNR_op1_7,PNR_op1_T]
PNR_op=pd.DataFrame(PNR_op)

op=pd.concat([twk_op,KNR_op,PNR_op],axis=1)
op.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External","Total"]
op.columns=["Walk","KNR","PNR"]
op[["Walk","KNR","PNR"]]=op[["Walk","KNR","PNR"]].astype(int)
op["Total"]=op["Walk"]+op["KNR"]+op["PNR"]


op2=op[["Walk","KNR","PNR","Total"]]


op2[["Walk","KNR","PNR","Total"]]=op2[["Walk","KNR","PNR","Total"]].astype(str)
op1_walk=list(op2["Walk"])
op1_walk=op1_walk[0:6]
b="','"
x="["+"'"+b.join(op1_walk) +"'"+"]" 
op1_knr=list(op2["KNR"])
op1_knr=op1_knr[0:6]
b="','"
x="["+"'"+b.join(op1_knr) +"'"+"]" 
op1_pnr=list(op2["PNR"])
op1_pnr=op1_pnr[0:6]
b="','"
x="["+"'"+b.join(op1_pnr) +"'"+"]" 


op["Total"]=op["Total"].map("{:,.0f}".format)
op["Walk"]=op["Walk"].map("{:,.0f}".format)
op["KNR"]=op["KNR"].map("{:,.0f}".format)
op["PNR"]=op["PNR"].map("{:,.0f}".format)

op1=op[["Walk","KNR","PNR","Total"]]
hills_op_wtb=op1.loc["Hillsborough"]["Walk"]
hills_op_KNR=op1.loc["Hillsborough"]["KNR"]
hills_op_PNR=op1.loc["Hillsborough"]["PNR"]
pine_op_wtb=op1.loc["Pinellas"]["Walk"]
pine_op_KNR=op1.loc["Pinellas"]["KNR"]
pine_op_PNR=op1.loc["Pinellas"]["PNR"]
pasco_op_wtb=op1.loc["Pasco"]["Walk"]
pasco_op_KNR=op1.loc["Pasco"]["KNR"]
pasco_op_PNR=op1.loc["Pasco"]["PNR"]
hern_op_wtb=op1.loc["Hernando"]["Walk"]
hern_op_KNR=op1.loc["Hernando"]["KNR"]
hern_op_PNR=op1.loc["Hernando"]["PNR"]
cit_op_wtb=op1.loc["Citrus"]["Walk"]
cit_op_KNR=op1.loc["Citrus"]["KNR"]
cit_op_PNR=op1.loc["Citrus"]["PNR"]
op_html=op1.to_html(index=True,bold_rows=True)

 

#peak
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

KNR_pk1=KNR_pk_m.sum(axis=1)
KNR_pk1_1=sum(KNR_pk1[0:1000])
KNR_pk1_2=sum(KNR_pk1[1000:2000])
KNR_pk1_3=sum(KNR_pk1[2000:2500])
KNR_pk1_4=sum(KNR_pk1[2500:2800])
KNR_pk1_5=sum(KNR_pk1[2800:2950])
KNR_pk1_6=sum(KNR_pk1[2950:3000])
KNR_pk1_7=sum(KNR_pk1[3000:3032])
KNR_pk1_T=sum(KNR_pk1[0:3032])
KNR_pk=[KNR_pk1_1,KNR_pk1_2,KNR_pk1_3,KNR_pk1_4,KNR_pk1_5,KNR_pk1_6,KNR_pk1_7,KNR_pk1_T]
KNR_pk=pd.DataFrame(KNR_pk)

PNR_pk1=PNR_pk_m.sum(axis=1)
PNR_pk1_1=sum(PNR_pk1[0:1000])
PNR_pk1_2=sum(PNR_pk1[1000:2000])
PNR_pk1_3=sum(PNR_pk1[2000:2500])
PNR_pk1_4=sum(PNR_pk1[2500:2800])
PNR_pk1_5=sum(PNR_pk1[2800:2950])
PNR_pk1_6=sum(PNR_pk1[2950:3000])
PNR_pk1_7=sum(PNR_pk1[3000:3032])
PNR_pk1_T=sum(PNR_pk1[0:3032])
PNR_pk=[PNR_pk1_1,PNR_pk1_2,PNR_pk1_3,PNR_pk1_4,PNR_pk1_5,PNR_pk1_6,PNR_pk1_7,PNR_pk1_T]
PNR_pk=pd.DataFrame(PNR_pk)

pk=pd.concat([twk_pk,KNR_pk,PNR_pk],axis=1)
pk.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External","Total"]
pk.columns=["Walk","KNR","PNR"]
pk[["Walk","KNR","PNR"]]=pk[["Walk","KNR","PNR"]].astype(int)

pk["Total"]=pk["Walk"]+pk["KNR"]+pk["PNR"]

pk2=pk[["Walk","KNR","PNR","Total"]]

pk2[["Walk","KNR","PNR","Total"]]=pk2[["Walk","KNR","PNR","Total"]].astype(str)
pk1_walk=list(pk2["Walk"])
pk1_walk=pk1_walk[0:6]
b="','"
x="["+"'"+b.join(pk1_walk) +"'"+"]" 
pk1_knr=list(pk2["KNR"])
pk1_knr=pk1_knr[0:6]
b="','"
x="["+"'"+b.join(pk1_knr) +"'"+"]" 
pk1_pnr=list(pk2["PNR"])
pk1_pnr=pk1_pnr[0:6]
b="','"
x="["+"'"+b.join(pk1_pnr) +"'"+"]"  

pk["Total"]=pk["Total"].map("{:,.0f}".format)
pk["Walk"]=pk["Walk"].map("{:,.0f}".format)
pk["KNR"]=pk["KNR"].map("{:,.0f}".format)
pk["PNR"]=pk["PNR"].map("{:,.0f}".format)

pk1=pk[["Walk","KNR","PNR","Total"]]
hills_pk_wtb=pk1.loc["Hillsborough"]["Walk"]
hills_pk_KNR=pk1.loc["Hillsborough"]["KNR"]
hills_pk_PNR=pk1.loc["Hillsborough"]["PNR"]
pine_pk_wtb=pk1.loc["Pinellas"]["Walk"]
pine_pk_KNR=pk1.loc["Pinellas"]["KNR"]
pine_pk_PNR=pk1.loc["Pinellas"]["PNR"]
pasco_pk_wtb=pk1.loc["Pasco"]["Walk"]
pasco_pk_KNR=pk1.loc["Pasco"]["KNR"]
pasco_pk_PNR=pk1.loc["Pasco"]["PNR"]
hern_pk_wtb=pk1.loc["Hernando"]["Walk"]
hern_pk_KNR=pk1.loc["Hernando"]["KNR"]
hern_pk_PNR=pk1.loc["Hernando"]["PNR"]
cit_pk_wtb=pk1.loc["Citrus"]["Walk"]
cit_pk_KNR=pk1.loc["Citrus"]["KNR"]
cit_pk_PNR=pk1.loc["Citrus"]["PNR"]
pk_html=pk1.to_html(index=True,bold_rows=True)

# Daily
twk_all1=twk_all_m.sum(axis=1)
twk_all1_1=sum(twk_all1[0:1000])
twk_all1_2=sum(twk_all1[1000:2000])
twk_all1_3=sum(twk_all1[2000:2500])
twk_all1_4=sum(twk_all1[2500:2800])
twk_all1_5=sum(twk_all1[2800:2950])
twk_all1_6=sum(twk_all1[2950:3000])
twk_all1_7=sum(twk_all1[3000:3032])
twk_all1_T=sum(twk_all1[0:3032])
twk_all=[twk_all1_1,twk_all1_2,twk_all1_3,twk_all1_4,twk_all1_5,twk_all1_6,twk_all1_7,twk_all1_T]
twk_all=pd.DataFrame(twk_all)

KNR_all1=KNR_all_m.sum(axis=1)
KNR_all1_1=sum(KNR_all1[0:1000])
KNR_all1_2=sum(KNR_all1[1000:2000])
KNR_all1_3=sum(KNR_all1[2000:2500])
KNR_all1_4=sum(KNR_all1[2500:2800])
KNR_all1_5=sum(KNR_all1[2800:2950])
KNR_all1_6=sum(KNR_all1[2950:3000])
KNR_all1_7=sum(KNR_all1[3000:3032])
KNR_all1_T=sum(KNR_all1[0:3032])
KNR_all=[KNR_all1_1,KNR_all1_2,KNR_all1_3,KNR_all1_4,KNR_all1_5,KNR_all1_6,KNR_all1_7,KNR_all1_T]
KNR_all=pd.DataFrame(KNR_all)

PNR_all1=PNR_all_m.sum(axis=1)
PNR_all1_1=sum(PNR_all1[0:1000])
PNR_all1_2=sum(PNR_all1[1000:2000])
PNR_all1_3=sum(PNR_all1[2000:2500])
PNR_all1_4=sum(PNR_all1[2500:2800])
PNR_all1_5=sum(PNR_all1[2800:2950])
PNR_all1_6=sum(PNR_all1[2950:3000])
PNR_all1_7=sum(PNR_all1[3000:3032])
PNR_all1_T=sum(PNR_all1[0:3032])
PNR_all=[PNR_all1_1,PNR_all1_2,PNR_all1_3,PNR_all1_4,PNR_all1_5,PNR_all1_6,PNR_all1_7,PNR_all1_T]
PNR_all=pd.DataFrame(PNR_all)

all=pd.concat([twk_all,KNR_all,PNR_all],axis=1)
all.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External","Total"]
all.columns=["Walk","KNR","PNR"]
all[["Walk","KNR","PNR"]]=all[["Walk","KNR","PNR"]].astype(int)
all["Total"]=all["Walk"]+all["KNR"]+all["PNR"]


all2=all[["Walk","KNR","PNR","Total"]]

all2[["Walk","KNR","PNR","Total"]]=all2[["Walk","KNR","PNR","Total"]].astype(str)
all1_walk=list(all2["Walk"])
all1_walk=all1_walk[0:6]
b="','"
x="["+"'"+b.join(all1_walk) +"'"+"]" 
all1_knr=list(all2["KNR"])
all1_knr=all1_knr[0:6]
b="','"
x="["+"'"+b.join(all1_knr) +"'"+"]" 
all1_pnr=list(all2["PNR"])
all1_pnr=all1_pnr[0:6]
b="','"
x="["+"'"+b.join(all1_pnr) +"'"+"]" 

all["Total"]=all["Total"].map("{:,.0f}".format)
all["Walk"]=all["Walk"].map("{:,.0f}".format)
all["KNR"]=all["KNR"].map("{:,.0f}".format)
all["PNR"]=all["PNR"].map("{:,.0f}".format)

all1=all[["Walk","KNR","PNR","Total"]]
hills_all_wtb=all1.loc["Hillsborough"]["Walk"]
hills_all_KNR=all1.loc["Hillsborough"]["KNR"]
hills_all_PNR=all1.loc["Hillsborough"]["PNR"]
pine_all_wtb=all1.loc["Pinellas"]["Walk"]
pine_all_KNR=all1.loc["Pinellas"]["KNR"]
pine_all_PNR=all1.loc["Pinellas"]["PNR"]
pasco_all_wtb=all1.loc["Pasco"]["Walk"]
pasco_all_KNR=all1.loc["Pasco"]["KNR"]
pasco_all_PNR=all1.loc["Pasco"]["PNR"]
hern_all_wtb=all1.loc["Hernando"]["Walk"]
hern_all_KNR=all1.loc["Hernando"]["KNR"]
hern_all_PNR=all1.loc["Hernando"]["PNR"]
cit_all_wtb=all1.loc["Citrus"]["Walk"]
cit_all_KNR=all1.loc["Citrus"]["KNR"]
cit_all_PNR=all1.loc["Citrus"]["PNR"]
all_html=all1.to_html(index=True,bold_rows=True)

hills_op="Walk:"+hills_op_wtb+"<br>KNR:"+hills_op_KNR+"<br>PNR:"+hills_op_PNR
pasco_op="Walk:"+pasco_op_wtb+"<br>KNR:"+pasco_op_KNR+"<br>PNR:"+pasco_op_PNR
pinellas_op="Walk:"+pine_op_wtb+"<br>KNR:"+pine_op_KNR+"<br>PNR:"+pine_op_PNR
hernando_op="Walk:"+hern_op_wtb+"<br>KNR:"+hern_op_KNR+"<br>PNR:"+hern_op_PNR
citrus_op="Walk:"+cit_op_wtb+"<br>KNR:"+cit_op_KNR+"<br>PNR:"+cit_op_PNR

hills_pk="Walk:"+hills_pk_wtb+"<br>KNR:"+hills_pk_KNR+"<br>PNR:"+hills_pk_PNR
pasco_pk="Walk:"+pasco_pk_wtb+"<br>KNR:"+pasco_pk_KNR+"<br>PNR:"+pasco_pk_PNR
pinellas_pk="Walk:"+pine_pk_wtb+"<br>KNR:"+pine_pk_KNR+"<br>PNR:"+pine_pk_PNR
hernando_pk="Walk:"+hern_pk_wtb+"<br>KNR:"+hern_pk_KNR+"<br>PNR:"+hern_pk_PNR
citrus_pk="Walk:"+cit_pk_wtb+"<br>KNR:"+cit_pk_KNR+"<br>PNR:"+cit_pk_PNR

hills_all="Walk:"+hills_all_wtb+"<br>KNR:"+hills_all_KNR+"<br>PNR:"+hills_all_PNR
pasco_all="Walk:"+pasco_all_wtb+"<br>KNR:"+pasco_all_KNR+"<br>PNR:"+pasco_all_PNR
pinellas_all="Walk:"+pine_all_wtb+"<br>KNR:"+pine_all_KNR+"<br>PNR:"+pine_all_PNR
hernando_all="Walk:"+hern_all_wtb+"<br>KNR:"+hern_all_KNR+"<br>PNR:"+hern_all_PNR
citrus_all="Walk:"+cit_all_wtb+"<br>KNR:"+cit_all_KNR+"<br>PNR:"+cit_all_PNR


msg1 = "Off-Peak Transit Person Trips"
msg2="Peak Transit Person Trips"

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
   .my-label{
   background:#F2F2F2;
   width: 120px;
}
    
    thead {color: black;}
    tbody {color: black;}
    tfoot {color: red;}
    table{width:400px;height:500px;}
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

tr {
  height: 20px;
  width:100%;
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
            <li><a href="MODE_overall.html" class="link-dark d-inline-flex text-decoration-none rounded" >Mode Choice Overall</a></li>
            <li><a href="MODE_HWY.html" class="link-dark d-inline-flex text-decoration-none rounded" >Highway Trips</a></li>
            <li><a href="MODE_transit.html" class="link-dark d-inline-flex text-decoration-none rounded" style="background-color:ADCEDE">Transit Trips</a></li>
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
      <button id="pk" type="button" style="width:150px; height:25px; font-size:12px; background-color: #92B6C7;"> Peak </button>
																																							   
      <button id="op" type="button" style="width:150px; height:25px; font-size:12px"> Off-Peak  </button>
        <button id="all" type="button" style="width:150px; height:25px; font-size:12px"> Daily </button>
      </div>

<div class="map_mode" id="map_mode"> </div>



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


	  <div class="MODE_transitop" id="transit_MODE">
    <canvas id="myChart1" style="width:100%;max-width:1200px"></canvas>
    </div>
    	  <div class="MODE_transitpk" id="transit_MODE1">
    <canvas id="myChart2" style="width:100%;max-width:1200px"></canvas>
    </div>
      	  <div class="MODE_transitda" id="transit_MODE1">
    <canvas id="myChart3" style="width:100%;max-width:1200px"></canvas>
    </div>
    
 <div class="notation" id="mode_overall">
    <h6 style="padding: 6px 0;color:black"> *Walk: Walk to Bus  <br>*KNR: Kiss and Ride <br>*PNR: Park and Ride </h6>
    </div>


<script>
var xValues = """+str(op1_walk)+""";
var yValues="""+str(op1_knr)+""";
var zValues="""+str(op1_pnr) +""";

new Chart(document.getElementById("myChart1"), {
    type: 'bar',
    data: {
      labels: ["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External"],
       datasets: [
        {
          label: "Walk",
          backgroundColor: "#6CBE7C",
          data: xValues
        }, {
          label: "KNR",
          backgroundColor: "#D37995",
          data: yValues
        },
        {
          label: "PNR",
          backgroundColor: "#F3A27C",
          data: zValues
        }

      ]
    },
    options: {
       scales: {
          yAxes: [{
            id: 'A',
            type: 'linear',
            position: 'left',
            ticks:{
              max:25000,
            }
          }]
        }, 
      plugins:{
      title: {
        display: true,
        text: 'Off-Peak Transit Trips'
      }
    }
    }
});

var xValues = """+str(pk1_walk)+""";
var yValues="""+str(pk1_knr)+""";
var zValues="""+str(pk1_pnr) +""";

new Chart(document.getElementById("myChart2"), {
    type: 'bar',
    data: {
      labels: ["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External"],
             datasets: [
        {
          label: "Walk",
          backgroundColor: "#6CBE7C",
          data: xValues
        }, {
          label: "KNR",
          backgroundColor: "#D37995",
          data: yValues
        },
        {
          label: "PNR",
          backgroundColor: "#F3A27C",
          data: zValues
        }

      ]
    },
    options: {
      plugins:{
      title: {
        display: true,
        text: 'Peak Transit Person Trips'
      }
    }
    }
});

var xValues="""+str(all1_walk)+""";
var yValues="""+str(all1_knr)+""";
var zValues="""+str(all1_pnr)+""";

new Chart(document.getElementById("myChart3"), {
    type: 'bar',
    data: {
      labels: ["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External"],
              datasets: [
        {
          label: "Walk",
          backgroundColor: "#6CBE7C",
          data: xValues
        }, {
          label: "KNR",
          backgroundColor: "#D37995",
          data: yValues
        },
        {
          label: "PNR",
          backgroundColor: "#F3A27C",
          data: zValues
        }

      ]
    },
    options: {
      plugins:{
      title: {
        display: true,
        text: 'Daily Transit Person Trips'
      }
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

var hills_all= """+"'"+hills_all+"'"+""";
var pasco_all= """+"'"+pasco_all+"'"+""";
var hernando_all= """+"'"+hernando_all+"'"+""";
var pinellas_all= """+"'"+pinellas_all+"'"+""";
var citrus_all= """+"'"+citrus_all+"'"+""";

var map = L.map('map_mode').setView([28.276140, -82.585263], 9);
	
L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/light_all/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
	subdomains: 'abcd',
	maxZoom: 15
    }).addTo(map);
var hillsborough = new L.marker([28.039646, -82.420602], { opacity: 0.01 });
hillsborough.bindLabel("""+"'"+hills_pk+"'"+""", {noHide: true, className: "my-label", offset: [0, 0] });
hillsborough.addTo(map);

var pasco = new L.marker([28.295848, -82.471609], { opacity: 0.01 });
pasco.bindLabel("""+"'"+pasco_pk+"'"+""", {noHide: true, className: "my-label", offset: [0, 0] });
pasco.addTo(map);

var hernando = new L.marker([28.566409, -82.471609], { opacity: 0.01 });
hernando.bindLabel("""+"'"+hernando_pk+"'"+""", {noHide: true, className: "my-label", offset: [0, 0] });
hernando.addTo(map);

var pinellas = new L.marker([27.907086, -82.759073], { opacity: 0.01 });
pinellas.bindLabel("""+"'"+pinellas_pk+"'"+""", {noHide: true, className: "my-label", offset: [0, 0] });
pinellas.addTo(map);

var citrus = new L.marker([28.785449, -82.471609], { opacity: 0.01 });
citrus.bindLabel("""+"'"+citrus_pk+"'"+""", {noHide: true, className: "my-label", offset: [0, 0] });
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
        button_all.style.backgroundColor = "#f0f0f0";
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
        button_all.style.backgroundColor = "#f0f0f0";

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
 

      var button_all = document.getElementById("all");
      button_all.addEventListener("click", function(event){
        button_all.style.backgroundColor = "#92B6C7";
        button_op.style.backgroundColor = "#f0f0f0";
        button_pk.style.backgroundColor = "#f0f0f0";

        var hillsborough = new L.marker([28.039646, -82.420602], { opacity: 0.01 });
        hillsborough.bindLabel(hills_all, {noHide: true, className: "my-label", offset: [0, 0]});
        hillsborough.addTo(map);
        var pasco = new L.marker([28.295848, -82.471609], { opacity: 0.01 });
        pasco.bindLabel(pasco_all, {noHide: true, className: "my-label", offset: [0, 0] });
        pasco.addTo(map);
        var hernando = new L.marker([28.566409, -82.471609], { opacity: 0.01 });
        hernando.bindLabel(hernando_all, {noHide: true, className: "my-label", offset: [0, 0] });
        hernando.addTo(map);
        var pinellas = new L.marker([27.907086, -82.759073], { opacity: 0.01 });
        pinellas.bindLabel(pinellas_all, {noHide: true, className: "my-label", offset: [0, 0] });
        pinellas.addTo(map);
        var citrus = new L.marker([28.785449, -82.471609], { opacity: 0.01 });
        citrus.bindLabel(citrus_all, {noHide: true, className: "my-label", offset: [0, 0] });
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

   <div class="MODEtransit_op" id="op">
    <h4 style="padding: 10px 0;color:black">
    """ +msg1 + "</h4>"

table2="""
</div>
   <div class="MODEtransit_pk" id="pk">
    <h4 style="padding: 10px 0;color:black">
    """ +msg2 + "</h4>"

table3="""
</div>
   <div class="MODEtransit_da" id="pk">
    <h4 style="padding: 10px 0;color:black">
    """ +"Daily Transit Trips"+ "</h4>"

end_html = """
        </div>
        </body>
        </html>
        """
if base==1:
  html = title + diff_45+main_continue+  op_html +table2+pk_html+table3+all_html+ end_html
else:
  html = title +main_continue+  op_html +table2+pk_html+table3+all_html+ end_html

text_file = open(os.path.join(Visum.GetPath(2), "outputs\\{}\\HTML\\MODE_transit.html".format(scname)), "w")
text_file.write(html)
text_file.close()


