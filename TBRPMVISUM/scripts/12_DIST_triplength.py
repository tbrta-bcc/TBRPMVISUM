# script to generate trip generation summary
# Chetan Joshi, Portland OR 3/16/2022
import pandas as pd
import numpy as np
import os 
import glob
PRIO = 20480
scname   = Visum.Net.AttValue("SC_NAME")

#Off-peak 
csv_files_op=glob.glob(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries".format(scname))+"/*1C_OP*.csv")
filename=[os.path.basename(x) for x in csv_files_op]
li_op=[]
for file_op in csv_files_op:
    df_op=pd.read_csv(file_op,error_bad_lines=False)
    df_op=df_op.drop(columns="Total Trips")
    li_op.append(df_op)
optlf_1= pd.concat(li_op, axis=1, ignore_index=False)
optlf=pd.DataFrame(np.vstack([optlf_1.columns,optlf_1]))
optlf.columns=filename
optlf=optlf.rename(columns={"ALL-AIRP_1C_OP-tlf.csv":"AIRP","ALL-COL_1C_OP-tlf.csv":"COL","ALL-EI_1C_OP-tlf.csv":"EI","ALL-HBO_1C_OP-tlf.csv":"HBO","ALL-HBSC_1C_OP-tlf.csv":"HBSC","ALL-HBSH_1C_OP-tlf.csv":"HBSH","ALL-HBSR_1C_OP-tlf.csv":"HBSR","ALL-HBW_1C_OP-tlf.csv":"HBW","ALL-HTRK_1C_OP-tlf.csv":"HTRK","ALL-LTRK_1C_OP-tlf.csv":"LTRK","ALL-NHBO_1C_OP-tlf.csv":"NHBO","ALL-NHBW_1C_OP-tlf.csv":"NHBW","ALL-TAXI_1C_OP-tlf.csv":"TAXI"})
optlf=optlf[["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL"]]

optlf.index=["Total Trips","Intrazonal Trips","Intrazonal Percentage(%)","Average Trip Length (Miles)","Average Trip Length (Minutes)"]
optlf["Total"]=optlf.sum()/2
optlf=optlf.T
optlf=optlf.apply(pd.to_numeric,errors="coerce",axis=1)
optlf["Total Trip Length (Minutes)"]=optlf["Average Trip Length (Minutes)"]*optlf["Total Trips"]
optlf["Total Trip Length (Miles)"]=optlf["Average Trip Length (Miles)"]*optlf["Total Trips"]

op_total=[]

ave_mins_list=list(optlf["Average Trip Length (Minutes)"])

ave_miles_list=list(optlf["Average Trip Length (Miles)"])


total_trips_list=list(optlf["Total Trips"])

total_tlf_mins_list=list(optlf["Total Trip Length (Minutes)"])
total_tlf_miles_list=list(optlf["Total Trip Length (Miles)"])

sum_mins=0
sum_miles=0
total_trips=0
total_tlf_mins=0
total_tlf_miles=0
Visum.Log(PRIO, "length of list:{}{}".format(total_trips_list,len(total_tlf_mins_list)))
optlf=optlf[["Average Trip Length (Minutes)","Average Trip Length (Miles)","Total Trips","Total Trip Length (Minutes)","Total Trip Length (Miles)"]]


for i in range(0,13):
  sum_mins=sum_mins+ave_mins_list[i]*total_trips_list[i]
  sum_miles=sum_miles+ave_miles_list[i]*total_trips_list[i]
  total_trips=total_trips+total_trips_list[i]
  total_tlf_mins=total_tlf_mins+total_tlf_mins_list[i]
  total_tlf_miles=total_tlf_miles+total_tlf_miles_list[i]

ave_mins_overall=sum_mins/total_trips
ave_miles_overall=sum_miles/total_trips
op_total=[ave_mins_overall,ave_miles_overall,total_trips,total_tlf_mins,total_tlf_miles]
Visum.Log(PRIO, "op_total:{}".format(op_total))
optlf=optlf.T
optlf["Overall"]=op_total
optlf=optlf.T

optlf.loc['Person','Total Trips'] = optlf['Total Trips'][0:7].sum() + optlf['Total Trips'][11:13].sum()
optlf.loc['Person','Total Trip Length (Minutes)'] = optlf['Total Trip Length (Minutes)'][0:7].sum() + optlf['Total Trip Length (Minutes)'][11:13].sum()
optlf.loc['Person','Total Trip Length (Miles)'] = optlf['Total Trip Length (Miles)'][0:7].sum() + optlf['Total Trip Length (Miles)'][11:13].sum()
optlf.loc['Person','Average Trip Length (Minutes)'] = optlf.loc['Person','Total Trip Length (Minutes)']/optlf.loc['Person','Total Trips']
optlf.loc['Person','Average Trip Length (Miles)'] = optlf.loc['Person','Total Trip Length (Miles)']/optlf.loc['Person','Total Trips']

optlf.loc['Vehicle','Total Trips'] = optlf['Total Trips'][7:11].sum()
optlf.loc['Vehicle','Total Trip Length (Minutes)'] = optlf['Total Trip Length (Minutes)'][7:11].sum()
optlf.loc['Vehicle','Total Trip Length (Miles)'] = optlf['Total Trip Length (Miles)'][7:11].sum()
optlf.loc['Vehicle','Average Trip Length (Minutes)'] = optlf.loc['Vehicle','Total Trip Length (Minutes)']/optlf.loc['Vehicle','Total Trips']
optlf.loc['Vehicle','Average Trip Length (Miles)'] = optlf.loc['Vehicle','Total Trip Length (Miles)']/optlf.loc['Vehicle','Total Trips']

#change the format
optlf["Average Trip Length (Miles)"]=optlf["Average Trip Length (Miles)"].round(2)
optlf["Average Trip Length (Minutes)"]=optlf["Average Trip Length (Minutes)"].round(2)
optlf["Total Trips"]=optlf["Total Trips"].map("{:,.0f}".format)
optlf["Total Trip Length (Minutes)"]=optlf["Total Trip Length (Minutes)"].map("{:,.0f}".format)
optlf["Total Trip Length (Miles)"]=optlf["Total Trip Length (Miles)"].map("{:,.0f}".format)
optlf=optlf.reindex(["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Overall","Person","Vehicle"])
#convert to html
optlf_html=optlf.to_html()
writer=pd.ExcelWriter(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\Trip Length.xlsx".format(scname)),engine="xlsxwriter")
optlf.to_excel(writer,sheet_name='Off-Peak')
optlf2=optlf["Average Trip Length (Miles)"]
optlf2=pd.DataFrame(optlf2)
optlf2["Average Trip Length (Miles)"]=optlf2["Average Trip Length (Miles)"].astype(str)
optlf_miles=list(optlf2["Average Trip Length (Miles)"])
b="','"
op_miles="["+"'"+b.join(optlf_miles) +"'"+"]"  
optlf2=optlf["Average Trip Length (Minutes)"]
optlf2=pd.DataFrame(optlf2)
optlf2["Average Trip Length (Minutes)"]=optlf2["Average Trip Length (Minutes)"].astype(str)
optlf_mins=list(optlf2["Average Trip Length (Minutes)"])
b="','"
op_mins="["+"'"+b.join(optlf_mins) +"'"+"]"  

#Peak
csv_files_pk=glob.glob(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries".format(scname))+"/*1C_PK*.csv")
filename=[os.path.basename(x) for x in csv_files_pk]
li_pk=[]
for file_pk in csv_files_pk:
    df_pk=pd.read_csv(file_pk,error_bad_lines=False)
    df_pk=df_pk.drop(columns="Total Trips")
    li_pk.append(df_pk)
pktlf_1= pd.concat(li_pk, axis=1, ignore_index=False)
pktlf=pd.DataFrame(np.vstack([pktlf_1.columns,pktlf_1]))
pktlf.columns=filename
pktlf=pktlf.rename(columns={"ALL-AIRP_1C_PK-tlf.csv":"AIRP","ALL-COL_1C_PK-tlf.csv":"COL","ALL-EI_1C_PK-tlf.csv":"EI","ALL-HBO_1C_PK-tlf.csv":"HBO","ALL-HBSC_1C_PK-tlf.csv":"HBSC","ALL-HBSH_1C_PK-tlf.csv":"HBSH","ALL-HBSR_1C_PK-tlf.csv":"HBSR","ALL-HBW_1C_PK-tlf.csv":"HBW","ALL-HTRK_1C_PK-tlf.csv":"HTRK","ALL-LTRK_1C_PK-tlf.csv":"LTRK","ALL-NHBO_1C_PK-tlf.csv":"NHBO","ALL-NHBW_1C_PK-tlf.csv":"NHBW","ALL-TAXI_1C_PK-tlf.csv":"TAXI"})
pktlf=pktlf[["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL"]]

pktlf.index=["Total Trips","Intrazonal Trips","Intrazonal Percentage(%)","Average Trip Length (Miles)","Average Trip Length (Minutes)"]
pktlf["Total"]=pktlf.sum()/2
pktlf=pktlf.T
pktlf=pktlf.apply(pd.to_numeric,errors="coerce",axis=1)
pktlf["Total Trip Length (Minutes)"]=pktlf["Average Trip Length (Minutes)"]*pktlf["Total Trips"]
pktlf["Total Trip Length (Miles)"]=pktlf["Average Trip Length (Miles)"]*pktlf["Total Trips"]

pk_total=[]

ave_mins_list=list(pktlf["Average Trip Length (Minutes)"])
ave_miles_list=list(pktlf["Average Trip Length (Miles)"])
total_trips_list=list(pktlf["Total Trips"])
total_tlf_mins_list=list(pktlf["Total Trip Length (Minutes)"])
total_tlf_miles_list=list(pktlf["Total Trip Length (Miles)"])


sum_mins=0
sum_miles=0
total_trips=0
total_tlf_mins=0
total_tlf_miles=0
pktlf=pktlf[["Average Trip Length (Minutes)","Average Trip Length (Miles)","Total Trips","Total Trip Length (Minutes)","Total Trip Length (Miles)"]]


for i in range(0,13):
  sum_mins=sum_mins+ave_mins_list[i]*total_trips_list[i]
  sum_miles=sum_miles+ave_miles_list[i]*total_trips_list[i]
  total_trips=total_trips+total_trips_list[i]
  total_tlf_mins=total_tlf_mins+total_tlf_mins_list[i]
  total_tlf_miles=total_tlf_miles+total_tlf_miles_list[i]

ave_mins_overall=sum_mins/total_trips
ave_miles_overall=sum_miles/total_trips
pk_total=[ave_mins_overall,ave_miles_overall,total_trips,total_tlf_mins,total_tlf_miles]
pktlf=pktlf.T
pktlf["Overall"]=pk_total
pktlf=pktlf.T

pktlf.loc['Person','Total Trips'] = pktlf['Total Trips'][0:7].sum() + pktlf['Total Trips'][11:13].sum()
pktlf.loc['Person','Total Trip Length (Minutes)'] = pktlf['Total Trip Length (Minutes)'][0:7].sum() + pktlf['Total Trip Length (Minutes)'][11:13].sum()
pktlf.loc['Person','Total Trip Length (Miles)'] = pktlf['Total Trip Length (Miles)'][0:7].sum() + pktlf['Total Trip Length (Miles)'][11:13].sum()
pktlf.loc['Person','Average Trip Length (Minutes)'] = pktlf.loc['Person','Total Trip Length (Minutes)']/pktlf.loc['Person','Total Trips']
pktlf.loc['Person','Average Trip Length (Miles)'] = pktlf.loc['Person','Total Trip Length (Miles)']/pktlf.loc['Person','Total Trips']

pktlf.loc['Vehicle','Total Trips'] = pktlf['Total Trips'][7:11].sum()
pktlf.loc['Vehicle','Total Trip Length (Minutes)'] = pktlf['Total Trip Length (Minutes)'][7:11].sum()
pktlf.loc['Vehicle','Total Trip Length (Miles)'] = pktlf['Total Trip Length (Miles)'][7:11].sum()
pktlf.loc['Vehicle','Average Trip Length (Minutes)'] = pktlf.loc['Vehicle','Total Trip Length (Minutes)']/pktlf.loc['Vehicle','Total Trips']
pktlf.loc['Vehicle','Average Trip Length (Miles)'] = pktlf.loc['Vehicle','Total Trip Length (Miles)']/pktlf.loc['Vehicle','Total Trips']

#change the format
pktlf["Average Trip Length (Miles)"]=pktlf["Average Trip Length (Miles)"].round(2)
pktlf["Average Trip Length (Minutes)"]=pktlf["Average Trip Length (Minutes)"].round(2)
pktlf=pktlf[["Average Trip Length (Minutes)","Average Trip Length (Miles)","Total Trips","Total Trip Length (Minutes)","Total Trip Length (Miles)"]]

pktlf["Total Trips"]=pktlf["Total Trips"].map("{:,.0f}".format)
pktlf["Total Trip Length (Minutes)"]=pktlf["Total Trip Length (Minutes)"].map("{:,.0f}".format)
pktlf["Total Trip Length (Miles)"]=pktlf["Total Trip Length (Miles)"].map("{:,.0f}".format)
pktlf=pktlf.reindex(["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Overall","Person","Vehicle"])

pktlf_html=pktlf.to_html()
pktlf.to_excel(writer,sheet_name='Peak')
writer.close()

pktlf2=pktlf["Average Trip Length (Miles)"]
pktlf2=pd.DataFrame(pktlf2)
pktlf2["Average Trip Length (Miles)"]=pktlf2["Average Trip Length (Miles)"].astype(str)
pktlf_miles=list(pktlf2["Average Trip Length (Miles)"])
b="','"
pk_miles="["+"'"+b.join(pktlf_miles) +"'"+"]" 

pktlf2=pktlf["Average Trip Length (Minutes)"]
pktlf2=pd.DataFrame(pktlf2)
pktlf2["Average Trip Length (Minutes)"]=pktlf2["Average Trip Length (Minutes)"].astype(str)
pktlf_mins=list(pktlf2["Average Trip Length (Minutes)"])
b="','"
pk_mins="["+"'"+b.join(pktlf_mins) +"'"+"]" 

msg1 = "Off-Peak Trip Length"
msg2 = "Peak Trip Length"


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



<!-- Main Style -->
    <link rel="stylesheet" href="css/summary.css"/>


 </head>
    <style>
 
    
    thead {color: black;}
    tbody {color: black;}
    tfoot {color: red;}
    table{width:750px;height:200px;}
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
  width:20%;
     text-align:right;
}
td:nth-child(3) {
  width:20%;
         text-align:right;
}
td:nth-child(4) {
  width:20%;
         text-align:right;
}
td:nth-child(5) {
  width:20%;
         text-align:right;
}
td:nth-child(6) {
  width:20%;
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
            <li><a href="EEOUT.html" class="link-dark d-inline-flex text-decoration-none rounded">Output EE Trips</a></li>
          </ul>
        </div>
      </li>
           <li class="mb-1">
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#generation-collapse" aria-expanded="false">
          Trip Generation
        </button>
        <div class="collapse " id="generation-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
            <li><a href="GEN_Overall.html" class="link-dark d-inline-flex text-decoration-none rounded" >Production & Attraction</a></li>
            <li><a href="GEN_INPUT.html" class="link-dark d-inline-flex text-decoration-none rounded"  >Trip Generation Statistics</a></li>
          </ul>
        </div>
      </li>
      <li class="mb-1">
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#dashboard-collapse" aria-expanded="true">
          Trip Distribution
        </button>
        <div class="collapse show" id="dashboard-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
            <li><a href="Triplength.html" class="link-dark d-inline-flex text-decoration-none rounded" style="background-color:ADCEDE">Trip Length Overall</a></li>
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
            <li><a href="MODE_overall.html" class="link-dark d-inline-flex text-decoration-none rounded" >Mode Choice Overall</a></li>
            <li><a href="MODE_HWY.html" class="link-dark d-inline-flex text-decoration-none rounded" >Highway Trips</a></li>
            <li><a href="MODE_transit.html" class="link-dark d-inline-flex text-decoration-none rounded"">Transit Trips</a></li>
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
      </li>
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
      </li>
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
	<div class="groupbar_tlf" id="barchart_tlf">
        <h4> Average Trip Length (Miles)</h4>
    <canvas id="bar-chart-miles" style="width:100%;max-width:1200px"></canvas>
    </div>
    	<div class="groupbar_tlf1" id="barchart_tlf1">
              <h4> Average Trip Length (Minutes) </h4>

    <canvas id="bar-chart-mins" style="width:100%;max-width:1200px"></canvas>
    </div>
<script>

var xValues = """+str(optlf_miles)+""";
var yValues="""+str(pktlf_miles)+""";

new Chart(document.getElementById("bar-chart-miles"), {
    type: 'bar',
    data: {
      labels: ["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL"],
      datasets: [
        {
          label: "Peak",
          backgroundColor: "#92B6C7",
          data: yValues
        }, {
          label: "Off-Peak",
          backgroundColor: "#F3A27C",
          data: xValues
        }
      ]
    },
    options: {
  
         scales:{
        y:{
        title:{
          display:true,
          text:'Miles'
        }
        }
      },
      
    }
});

</script>

<script>

var xValues1 = """+str(optlf_mins)+""";
var yValues1 ="""+str(pktlf_mins)+""";

new Chart(document.getElementById("bar-chart-mins"), {
    type: 'bar',
    data: {
      labels: ["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL"],
      datasets: [
        {
          label: "Peak",
          backgroundColor: "#92B6C7",
          data: yValues1
        }, {
          label: "Off-Peak",
          backgroundColor: "#F3A27C",
          data: xValues1
        }
      ]
    },
    options: {

      scales:{
        y:{
        title:{
          display:true,
          text:'Minutes'
        }
        }
      },

    
    }
});

</script>

</body>

   <div class="tlf_op" id="tlf_op1">
    <h4 style="padding: 10px 0;color:black">
    """ +msg1 + "</h4>"

table2="""
</div>
   <div class="tlf_pk" id="tlf_pk">
    <h4 style="padding: 10px 0;color:black">
    """ +msg2 + "</h4>"



end_html = """
        </div>
        </body>
        </html>
        """

html = title +optlf_html+table2+pktlf_html+end_html

text_file = open(os.path.join(Visum.GetPath(2), "outputs\\{}\\HTML\\Triplength.html".format(scname)), "w")
text_file.write(html)
text_file.close()


