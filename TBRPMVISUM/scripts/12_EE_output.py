import pandas as pd
import numpy as np
import matplotlib.pyplot 
import os 
import csv 
import json 
import VisumPy.helpers as h
PRIO = 20480

PRIO = 20480
scname  = Visum.Net.AttValue("SC_NAME")

ee_auto = h.GetMatrixRaw(Visum, 2)
ee_htrk = h.GetMatrixRaw(Visum, 3)+h.GetMatrixRaw(Visum, 4)

lst=[]
for i in range (3000,3032):
  lst.append(i)

auto_org=ee_auto[3000:,3000:].sum(axis=1)
htrk_org=ee_htrk[3000:,3000:].sum(axis=1)
auto_des=ee_auto[3000:,3000:].sum(axis=0)
htrk_des=ee_htrk[3000:,3000:].sum(axis=0)

auto=[auto_org,auto_des]
htrk=[htrk_org,htrk_des]

auto=pd.DataFrame(auto,index=["ORIGINS","DESTINATIONS"])
htrk=pd.DataFrame(htrk,index=["ORIGINS","DESTINATIONS"])

writer=pd.ExcelWriter(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\EETrips.xlsx".format(scname)),engine="xlsxwriter")

def summary(ee):
    ee=ee.T
    ee["TOTAL"]=ee["ORIGINS"]+ee["DESTINATIONS"]
    ee.index=ee.index+1
    return ee

auto=summary(auto)
auto.to_excel(writer,sheet_name='auto')

htrk=summary(htrk)
htrk.to_excel(writer,sheet_name='htrk')
writer.close()

def barchart(ee):
    ee_total=ee["TOTAL"].astype(str)
    b="','"
    ee_total="["+"'"+b.join(ee_total) +"'"+"]" 
    return ee_total

bar_auto=barchart(auto) 
bar_htrk=barchart(htrk) 

def html(ee):
    ee["ZONE"]=list(range(3001,3033))
    ee['ZONE']=ee['ZONE'].map("{:.0f}".format)
    ee=ee[["ZONE","ORIGINS","DESTINATIONS","TOTAL"]]
    ee.loc['External Totals','ZONE'] = "External Totals"
    ee.loc['External Totals','ORIGINS'] = ee['ORIGINS'].sum()
    ee["ORIGINS"]=ee["ORIGINS"].map("{:,.0f}".format)
    ee.loc['External Totals','DESTINATIONS'] = ee['DESTINATIONS'].sum()
    ee["DESTINATIONS"]=ee["DESTINATIONS"].map("{:,.0f}".format)
    ee.loc['External Totals','TOTAL'] = ee['TOTAL'].sum()
    ee["TOTAL"]=ee["TOTAL"].map("{:,.0f}".format)
    ee.columns = ['Zone','Origins', 'Destination', 'Total']

    ee_html=ee.to_html(index=False)
   
    return ee_html

html_auto=html(auto) 
html_htrk=html(htrk) 

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
    h2{
font-size:15px

    }
    
    thead {color: black;}
    tbody {color: black;}
    tfoot {color: red;}
    
    table, th, td {
      border: 1px solid black;
      font-size: 14px;
      text-align:center;
      height:10px;
      border-collapse: collapse;
      width: 300px;
    }
td:nth-child(1) {
    text-align:center;
  width:25%;
}
td:nth-child(2) {
     text-align:right;
  width:25%;
}
td:nth-child(3) {
         text-align:right;

  width:25%;
}
td:nth-child(4) {
         text-align:right;

  width:25%;
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


<main class="d-flex flex-nowrap" style="position:relative;">
<div class="flex-shrink-0 p-3" style="width: 230px;background-color:#F2F2F2;">
    <a href="#" class="d-flex align-items-left pb-3 mb-3 link-dark text-decoration-none border-bottom">
      <span class="fs-4 fw-semibold" style="color:#6C8D9C;font-weight:bold">Summary Index</span>
    </a>
    <ul class="list-unstyled ps-0">
      <li><a href="Home.html" class="btn btn-toggle d-inline-flex align-items-center rounded border-0" aria-expanded="false">Home</a></li>
      <li class="mb-1">
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#EE-collapse" aria-expanded="true">
         External
        </button>
        <div class="collapse show" id="EE-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
          <li><a href="EEIN.html" class="link-dark d-inline-flex text-decoration-none rounded" >Input EE Trips</a></li>
            <li><a href="EEOUT.html" class="link-dark d-inline-flex text-decoration-none rounded" style="background-color:ADCEDE">Output EE Trips</a></li>
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
      </li>"""
diff_45="""<li class="mb-1">
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
main_continue="""</ul>
  </div>



    <header class="navbar navbar-expand-md fixed-top navbar-dark bg-dark">
		<nav class="container-xxl flex-wrap flex-md-nowrap" aria-label="Main navigation">
			<a href="https://tdaappsprod.dot.state.fl.us/fto/" target="_blank">
				<img src="images/fdot_logo_white.png" id="fdot_logo" style="height: 48px; float:left"/>
			</a>
		<div class="collapse navbar-collapse" id="bdNavbar">
		<ul class="navbar-nav flex-row flex-wrap bd-navbar-nav pt-2 py-md-0">
			<li class="nav-item col-6 col-md-auto">
			<a class="nav-link p-3 active" style="font-size:20" aria-current="true"><b>"""+scname+" "+""" Tampa Bay Regional Planning Model </b></a>
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

    <div class="eeauto" id="eeauto">
    <canvas id="auto" style="width:100%;max-width:1200px"></canvas>
    </div>

    <div class="eehtrk" id="eehtrk">
    <canvas id="htrk" style="width:100%;max-width:1200px"></canvas>
    </div>

    <script>


var yValues="""+str(bar_auto)+""";

new Chart(document.getElementById("auto"), {
    type: 'bar',
    data: {
      labels: ["3001","3002","3003","3004","3005","3006","3007","3008","3009","3010","3011","3012","3013","3014","3015","3016","3017","3018","3019","3020","3021","3022","3023","3024","3025","3026","3027","3028","3029","3030","3031","3032"],
      datasets: [
        {
          backgroundColor: "#F3A27C",
          data: yValues
        }
      ]
    },
    options: {
     
      plugins:{
           legend: {
         display: false 
      },
      title: {
        display: true,
        text: 'EE Auto Total Trips',
        font:{
            size:14
        }
      }
    }
    }
});





var yValues2="""+str(bar_htrk)+""";
new Chart(document.getElementById("htrk"), {
    type: 'bar',
    data: {
      labels: ["3001","3002","3003","3004","3005","3006","3007","3008","3009","3010","3011","3012","3013","3014","3015","3016","3017","3018","3019","3020","3021","3022","3023","3024","3025","3026","3027","3028","3029","3030","3031","3032"],
      datasets: [
        {
          backgroundColor: "#F3A27C",
          data: yValues2
        }
      ]
    },
    options: {
     
      plugins:{
           legend: {
         display: false 
      },
      title: {
        display: true,
        text: 'EE  Truck Total Trips',
        font:{
            size:14
        }
      }
    }
    }
});


</script>

</body>

   <div class="eetrips_auto" id="auto">
    <h4 style="padding: 10px 0;color:black;font-size:20,width=400px"><span>
    """ +"EE Auto" + "</span></h4>"

table3="""</div><div class="eetrips_htrk" id="htrk">
    <h4 style="padding: 10px 0;color:black;font-size:20,width=400px"><span>
    """ +"EE Truck" + "</span></h4>"


end_html = """
        </div>
        </body>
        </html>
        """
if base==1:
  html = title + diff_45+ main_continue+ html_auto+table3+html_htrk+ end_html
else:
    html = title + main_continue+ html_auto+table3+html_htrk+ end_html


text_file = open(os.path.join(Visum.GetPath(2), "outputs\\{}\\HTML\\EEOUT.html".format(scname)), "w")
text_file.write(html)
text_file.close()








