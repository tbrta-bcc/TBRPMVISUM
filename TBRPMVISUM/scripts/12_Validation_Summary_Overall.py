import pandas as pd
import numpy as np
import matplotlib.pyplot 
import os 
import csv 
import json 

PRIO = 20480

scname = Visum.Net.AttValue("SC_NAME")
groupattr = "LOCATION"
val=["AL_CNT","VOL_ALL","LOCATION"]
df = pd.DataFrame(data=Visum.Net.Links.GetMultipleAttributes(val), columns=val)

df=df[df["AL_CNT"]>0]

#County
result_validation= pd.DataFrame(df.groupby(groupattr, as_index=False).sum())
result_validation.loc["Overall"]=result_validation.sum()
# overall_count = result_validation['AL_CNT'].sum()
# overall_volume = result_validation['VOL_ALL'].sum()

#result_validation["Number_of Links"]= df.groupby(groupattr).size()
result_validation["Volume/Count"]=result_validation["VOL_ALL"]/result_validation["AL_CNT"]
result_validation["Volume/Count"]=result_validation["Volume/Count"].map("{:,.2f}".format)
result_validation['AL_CNT'] = result_validation['AL_CNT'].map("{:,.0f}".format)
result_validation['VOL_ALL'] = result_validation['VOL_ALL'].map("{:,.0f}".format)
result_validation=result_validation.reset_index(drop=True)
result_validation.rename(columns={"AL_CNT":"Count","VOL_ALL":"Volume","LOCATION":"County"},inplace=True)
result_validation["County"].replace({1.0: "Hillsborough", 2.0: "Pinellas",3.0:"Pasco",4.0:"Hernando",5.0:"Citrus",6.0:"Others",21.0:"Overall"}, inplace=True)
result_validation['Volume/Count'].astype(str)
# result_validation.loc['Overall','County'] = "Overall"
# result_validation.loc['Overall','Count'] = overall_count
# result_validation.loc['Overall','Volume'] = overall_volume
# result_validation.loc['Overall','Volume/Count'] = str(round(overall_volume/overall_count,2))

yValues = result_validation['Volume/Count'].to_list()
b="','"
y="["+"'"+b.join(yValues ) +"'"+"]"  



html_FT=result_validation.to_html(index=False,bold_rows=True)


#RMSE
val_1=["AL_CNT","VOL_ALL","LOCATION"]
df_RMSE= pd.DataFrame(data=Visum.Net.Links.GetMultipleAttributes(val), columns=val)
df_RMSE=df_RMSE[df_RMSE["AL_CNT"]>0]
RMSE_hills=df_RMSE[df_RMSE["LOCATION"]==1]
RMSE_pinellas=df_RMSE[df_RMSE["LOCATION"]==2]
RMSE_pasco=df_RMSE[df_RMSE["LOCATION"]==3]
RMSE_hernando=df_RMSE[df_RMSE["LOCATION"]==4]
RMSE_citrus=df_RMSE[df_RMSE["LOCATION"]==5]
RMSE_others=df_RMSE[df_RMSE["LOCATION"]==6]

#hills
RMSE_hills["V_C"]=(RMSE_hills["VOL_ALL"]-RMSE_hills["AL_CNT"])**2
bins=[0,5000,10000,15000,20000,30000,50000,60000,1000000000]
ind=np.digitize(RMSE_hills["AL_CNT"],bins)
RMSE_hills1=RMSE_hills.groupby(ind).sum()
RMSE_hills1["Number of Links"]=RMSE_hills.groupby(ind).size()
RMSE_hills1["Hillsborough"]=((RMSE_hills1["V_C"]/(RMSE_hills1["Number of Links"]-1))**(1/2))/(RMSE_hills1["AL_CNT"]/RMSE_hills1["Number of Links"])*100
RMSE_hills1["Hillsborough"]=RMSE_hills1["Hillsborough"].map("{:,.2f}".format)
RMSE_hills1=RMSE_hills1["Hillsborough"]

#pasco
RMSE_pasco["V_C"]=(RMSE_pasco["VOL_ALL"]-RMSE_pasco["AL_CNT"])**2
bins=[0,5000,10000,15000,20000,30000,50000,60000,1000000000]
ind=np.digitize(RMSE_pasco["AL_CNT"],bins)
RMSE_pasco1=RMSE_pasco.groupby(ind).sum()
RMSE_pasco1["Number of Links"]=RMSE_pasco.groupby(ind).size()
RMSE_pasco1["Pasco"]=((RMSE_pasco1["V_C"]/(RMSE_pasco1["Number of Links"]-1))**(1/2))/(RMSE_pasco1["AL_CNT"]/RMSE_pasco1["Number of Links"])*100

RMSE_pasco1["Pasco"]=RMSE_pasco1["Pasco"].map("{:,.2f}".format)
RMSE_pasco1.replace("inf","NaN", inplace=True)

RMSE_pasco1=RMSE_pasco1["Pasco"]

#pinellas
RMSE_pinellas["V_C"]=(RMSE_pinellas["VOL_ALL"]-RMSE_pinellas["AL_CNT"])**2
bins=[0,5000,10000,15000,20000,30000,50000,60000,1000000000]
ind=np.digitize(RMSE_pinellas["AL_CNT"],bins)
RMSE_pinellas1=RMSE_pinellas.groupby(ind).sum()
RMSE_pinellas1["Number of Links"]=RMSE_pinellas.groupby(ind).size()
RMSE_pinellas1["Pinellas"]=((RMSE_pinellas1["V_C"]/(RMSE_pinellas1["Number of Links"]-1))**(1/2))/(RMSE_pinellas1["AL_CNT"]/RMSE_pinellas1["Number of Links"])*100
RMSE_pinellas1["Pinellas"]=RMSE_pinellas1["Pinellas"].map("{:,.2f}".format)
RMSE_pinellas1=RMSE_pinellas1["Pinellas"]

#hernando
RMSE_hernando["V_C"]=(RMSE_hernando["VOL_ALL"]-RMSE_hernando["AL_CNT"])**2
bins=[0,5000,10000,15000,20000,30000,50000,60000,1000000000]
ind=np.digitize(RMSE_hernando["AL_CNT"],bins)
RMSE_hernando1=RMSE_hernando.groupby(ind).sum()
RMSE_hernando1["Number of Links"]=RMSE_hernando.groupby(ind).size()
RMSE_hernando1["Hernando"]=((RMSE_hernando1["V_C"]/(RMSE_hernando1["Number of Links"]-1))**(1/2))/(RMSE_hernando1["AL_CNT"]/RMSE_hernando1["Number of Links"])*100
RMSE_hernando1["Hernando"]=RMSE_hernando1["Hernando"].map("{:,.2f}".format)
RMSE_hernando1=RMSE_hernando1["Hernando"]

#citrus
RMSE_citrus["V_C"]=(RMSE_citrus["VOL_ALL"]-RMSE_citrus["AL_CNT"])**2
bins=[0,5000,10000,15000,20000,30000,50000,60000,1000000000]
ind=np.digitize(RMSE_citrus["AL_CNT"],bins)
RMSE_citrus1=RMSE_citrus.groupby(ind).sum()
RMSE_citrus1["Number of Links"]=RMSE_citrus.groupby(ind).size()
RMSE_citrus1["Citrus"]=((RMSE_citrus1["V_C"]/(RMSE_citrus1["Number of Links"]-1))**(1/2))/(RMSE_citrus1["AL_CNT"]/RMSE_citrus1["Number of Links"])*100
RMSE_citrus1["Citrus"]=RMSE_citrus1["Citrus"].map("{:,.2f}".format)
RMSE_citrus1.replace("inf","NaN", inplace=True)

RMSE_citrus1=RMSE_citrus1["Citrus"]

RMSE_others["V_C"]=(RMSE_others["VOL_ALL"]-RMSE_others["AL_CNT"])**2
bins=[0,5000,10000,15000,20000,30000,50000,60000,1000000000]
ind=np.digitize(RMSE_others["AL_CNT"],bins)
RMSE_others1=RMSE_others.groupby(ind).sum()
RMSE_others1["Number of Links"]=RMSE_others.groupby(ind).size()
RMSE_others1["Others"]=((RMSE_others1["V_C"]/(RMSE_others1["Number of Links"]-1))**(1/2))/(RMSE_others1["AL_CNT"]/RMSE_others1["Number of Links"])*100

RMSE_others1["Others"]=RMSE_others1["Others"].map("{:,.2f}".format)
RMSE_others1=RMSE_others1["Others"]

#Overall
df_RMSE["V_C"]=(df_RMSE["VOL_ALL"]-df_RMSE["AL_CNT"])**2
bins=[0,5000,10000,15000,20000,30000,50000,60000,1000000000]
ind=np.digitize(df_RMSE["AL_CNT"],bins)
df_RMSE1=df_RMSE.groupby(ind).sum()
df_RMSE1["Number of Links"]=df_RMSE.groupby(ind).size()
df_RMSE1["Study Area"]=((df_RMSE1["V_C"]/(df_RMSE1["Number of Links"]-1))**(1/2))/(df_RMSE1["AL_CNT"]/df_RMSE1["Number of Links"])*100

RMSE_study=df_RMSE1["Study Area"]

#County_overall
df_RMSE["V_C"]=(df_RMSE["VOL_ALL"]-df_RMSE["AL_CNT"])**2
df_RMSE1=df_RMSE.groupby("LOCATION").sum()
df_RMSE1["Number of Links"]=df_RMSE.groupby("LOCATION").size()
df_RMSE1["Areawide"]=((df_RMSE1["V_C"]/(df_RMSE1["Number of Links"]-1))**(1/2))/(df_RMSE1["AL_CNT"]/df_RMSE1["Number of Links"])*100
df_RMSE1["Areawide"]=df_RMSE1["Areawide"].map("{:,.2f}".format)

RMSE_area=df_RMSE1["Areawide"]

#total
df_RMSE["V_C"]=(df_RMSE["VOL_ALL"]-df_RMSE["AL_CNT"])**2.
total=df_RMSE.count()
RMSE_total=((df_RMSE["V_C"].sum()/(total-1))**(1/2))/(df_RMSE["AL_CNT"].sum()/total)*100
RMSE_area=pd.concat([RMSE_area,RMSE_total],axis=0)
RMSE_area=RMSE_area.iloc[0:7]

#merge
df_merge=pd.concat([RMSE_hills1,RMSE_pinellas1,RMSE_pasco1,RMSE_hernando1,RMSE_citrus1,RMSE_others1,RMSE_study],axis=1)
RMSE_area=pd.DataFrame(RMSE_area)
RMSE_area1=RMSE_area.T
RMSE_area1.columns=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Others","Study Area"]
df_merge1=pd.concat([df_merge,RMSE_area1],axis=0)
df_merge1["Study Area"]=df_merge1["Study Area"].map("{:,.2f}".format)
df_merge1.index=["<5k","5k-10k","10k-15k","15k-20k","20k-30k","30k-50k","50k-60k","60k+","Areawide"]
df_merge1=df_merge1.replace(np.nan,"NA")
df_merge1=df_merge1.replace("NaN","NA")

html_RMSE=df_merge1.to_html(index=True,bold_rows=True)
df_merge1.iloc[8].astype(str)
xValues1=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Others","Study Area"]
yValues1=df_merge1.iloc[8].to_list()
b1="','"
x1="["+"'"+b1.join(xValues1 ) +"'"+"]"  
y1="["+"'"+b1.join(yValues1 ) +"'"+"]" 


hills="V/C:"+result_validation.iloc[0]["Volume/Count"]+"  "+"<br>RMSE:"+df_merge1.iloc[8]["Hillsborough"]
pasco="V/C:"+result_validation.iloc[2]["Volume/Count"]+"  "+"<br>RMSE:"+df_merge1.iloc[8]["Pasco"]
pinellas="V/C:"+result_validation.iloc[1]["Volume/Count"]+"  "+"<br>RMSE:"+df_merge1.iloc[8]["Pinellas"]
hernando="V/C:"+result_validation.iloc[3]["Volume/Count"]+"  "+"<br>RMSE:"+df_merge1.iloc[8]["Hernando"]
citrus="V/C:"+result_validation.iloc[4]["Volume/Count"]+"  "+"<br>RMSE:"+df_merge1.iloc[8]["Citrus"]

Validation_County = "Volume/Count by County"
Validation_RMSE="RMSE by Volume Group"

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
    table {width: 500px}
    th, td {
      border: 1px solid black;
      text-align: center;
      width: 35px;
      font-size: 14px;
      height:10px
      padding:10px;
    }

    
tr {
  height: 25px;
  width:120%;
}

 .my-label{
   background:#F2F2F2;
   width: 100px;
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

    </style>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-annotation/2.0.0/chartjs-plugin-annotation.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-annotation/0.5.7/chartjs-plugin-annotation.js"></script>
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
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#orders-collapse" aria-expanded="false">
          Mode Choice
        </button>
        <div class="collapse" id="orders-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
            <li><a href="MODE_overall.html" class="link-dark d-inline-flex text-decoration-none rounded"   >Mode Choice Overall</a></li>
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
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#Highway-collapse" aria-expanded="true">
         Highway Validation
        </button>
        <div class="collapse show" id="Highway-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
            <li><a href="Validation_Overall.html" class="link-dark d-inline-flex text-decoration-none rounded" style="background-color:ADCEDE">VOL/CNT & RMSE</a></li>
            <li><a href="highway_Corridor.html" class="link-dark d-inline-flex text-decoration-none rounded">VOL/CNT by Corridor</a></li>
            <li><a href="highway_FACL.html" class="link-dark d-inline-flex text-decoration-none rounded">VOL/CNT by FT & AT</a></li>
          </ul>
        </div>
      </li>"""
main_continue="""
    </ul>
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
  
  <div class="map" id="map"> </div>
	<div class="barchart" id="barchart_VC">
  <h4 style="padding: 10px 0;color:black"> Volume/Count by County </h4>
    <canvas id="myChart_1" style="width:100%;max-width:500px"></canvas>
    
    </div>

    	<div class="barchart2" id="barchart_RMSE">
      <h4 style="padding: 10px 0;color:black"> RMSE by County </h4>
    <canvas id="myChart_2" style="width:100%;max-width:500px"></canvas>
    
    </div>

<script>
    
    
    var map = L.map('map').setView([28.276140, -82.585263], 9);
	
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/light_all/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
	subdomains: 'abcd',
	maxZoom: 15
    }).addTo(map);
	
	      var hillsborough = new L.marker([28.039646, -82.420602], { opacity: 0.01 });
      hillsborough.bindLabel("""+"'"+hills+"'"+""", {noHide: true, className: "my-label", offset: [0, 0]});
      hillsborough.addTo(map);

      var pasco = new L.marker([28.295848, -82.471609], { opacity: 0.01 });
      pasco.bindLabel("""+"'"+pasco+"'"+""", {noHide: true, className: "my-label", offset: [0, 0] });
      pasco.addTo(map);

      var hernando = new L.marker([28.566409, -82.471609], { opacity: 0.01 });
      hernando.bindLabel("""+"'"+hernando+"'"+""", {noHide: true, className: "my-label", offset: [0, 0] });
      hernando.addTo(map);

      var pinellas = new L.marker([27.907086, -82.759073], { opacity: 0.01 });
      pinellas.bindLabel("""+"'"+pinellas+"'"+""", {noHide: true, className: "my-label", offset: [0, 0] });
      pinellas.addTo(map);

      var citrus = new L.marker([28.785449, -82.471609], { opacity: 0.01 });
      citrus.bindLabel("""+"'"+citrus+"'"+""", {noHide: true, className: "my-label", offset: [0, 0] });
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
	 
	 
</script>



<script>
var xValues = ['Hillsborough','Pinellas','Pasco','Hernando','Citrus','Others','Overall'];
var yValues="""+y+""";

new Chart("myChart_1", {
  type: "bar",
  data: {
	labels:xValues,
    datasets: [{
      data: yValues,
        backgroundColor:"#F39db8",
    }]

  },
  bar: {
        width: {
            ratio: 0.5 
        }
        
    },
  options: {
    legend: {display: false},
    scales: {
                    xAxes: [{
                            display: true,
                            scaleLabel: {
                                display: false
                            }
                        }],
                    yAxes: [{
                            display: true,
                            ticks: {
                                beginAtZero: true,

                                max: 1.4
                            }
                        }]
                },
  
  },

  plugins: {
      datalabels: {
        color: 'blue',
        anchor: 'end',
        align: 'right',
        labels: {
          title: {
            font: {
              weight: 'bold'
            }
          }
        }
      }
    },
});

var xValues1 = """+x1 +""";
var yValues1="""+y1+""";

new Chart("myChart_2", {
  type: "bar",
  data: {
	labels:xValues1,
    datasets: [{
      data: yValues1,
        backgroundColor:"#F39db8",
    }]
  },
  bar: {
        width: {
            ratio: 0.5 
        }
        
    },
  options: {
    legend: {display: false},
    scales: {
                    xAxes: [{
                            display: true,
                            scaleLabel: {
                                display: false
                            }
                        }],
                    yAxes: [{
                            display: true,
                            ticks: {
                                beginAtZero: true,
                            }
                        }]
                },
  
  }
});


</script>

</body>

   <div class="table1" id="table_VC">
    <h3 style="padding: 10px 0;color:black">
    """ +Validation_County + "</h3>"

RMSE1="""
</div>
   <div class="table2" id="table_RMSE">
    <h3 style="padding: 10px 0;color:black">
    """ +Validation_RMSE + "</h3>"

end_html = """
        </div>
        </body>
        </html>
        """
if base==1:

  html = title +diff_45+main_continue+ html_FT +RMSE1+html_RMSE+ end_html
else:
  html = title +main_continue+ html_FT +RMSE1+html_RMSE+ end_html

text_file = open(os.path.join(Visum.GetPath(2), "outputs\\{}\\HTML\\Validation_Overall.html".format(scname)), "w")
text_file.write(html)
text_file.close()


# PANDA_OVERALL


