# script to generate trip generation summary
# Chetan Joshi, Portland OR 3/16/2022
import pandas as pd
import numpy as np
import os 
PRIO = 20480
scname   = Visum.Net.AttValue("SC_NAME")
def report_trip_gen(fnam0, fnam1, groupattr):
    Visum.Log(PRIO, "start: Get PANDA from file...")
    scname   = Visum.Net.AttValue("SC_NAME")
    PANDA_0C = pd.read_csv(fnam0)
    PANDA_1C = pd.read_csv(fnam1)
    PANDA_TT = PANDA_0C + PANDA_1C
    replace_attr = ["Attraction(COL)","Attraction(HBO)","Attraction(HBSC)","Attraction(HBSH)","Attraction(HBSR)","Attraction(HBW)"]        
    for _attr in replace_attr:
        PANDA_TT[_attr] = PANDA_1C[_attr]

    zattrs= PANDA_TT.columns.to_list()
    Visum.Net.Zones.SetMultipleAttributes(zattrs, PANDA_TT.to_numpy())
    Visum.Log(PRIO, "note: Set PANDA from file.")
    zattrs.append(groupattr)
    df = pd.DataFrame(data=Visum.Net.Zones.GetMultipleAttributes(zattrs), columns=zattrs)
    # df.style.format(thousands=",") --> needs jinja2
    
    
    result_county= df.groupby(groupattr).sum()
    result_total = df.sum()
    result_total.pop('COUNTY_NAME')
    result_total = pd.DataFrame(data=[result_total.to_list()], columns=PANDA_TT.columns.to_list(), index=['TOTAL'])
    
    result_county= pd.concat([result_county, result_total], ignore_index=False)
    result_county["Production_order"]=[5,7,4,1,6,3,2,8]
    result_county=result_county.sort_values("Production_order")
    result_county=result_county.drop(["Production_order"],axis=1)
    result_pro=result_county.filter(regex="Production",axis=1)
    result_pro=result_pro[["Production(HBW)","Production(HBSH)","Production(HBSR)","Production(HBSC)","Production(HBO)","Production(NHBW)","Production(NHBO)","Production(LTRK)","Production(HTRK)","Production(TAXI)","Production(EI)","Production(AIRP)","Production(COL)"]]
    result_pro["Total"]=result_pro.sum(axis=1)
    result_atr=result_county.filter(regex="Attraction",axis=1)
    result_atr=result_atr[["Attraction(HBW)","Attraction(HBSH)","Attraction(HBSR)","Attraction(HBSC)","Attraction(HBO)","Attraction(NHBW)","Attraction(NHBO)","Attraction(LTRK)","Attraction(HTRK)","Attraction(TAXI)","Attraction(EI)","Attraction(AIRP)","Attraction(COL)"]]
    result_atr["Total"]=result_atr.sum(axis=1)

    result_pro.to_csv(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\Production_Overall.csv".format(scname)), float_format='%.0f')
    result_atr.to_csv(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\Attraction_Overall.csv".format(scname)), float_format='%.0f')
    
fnam0 = os.path.join(Visum.GetPath(2), "outputs\\{}\\panda\\PANDA_0C.csv".format(scname))
fnam1 = os.path.join(Visum.GetPath(2), "outputs\\{}\\panda\\PANDA_1C.csv".format(scname))

groupattr = "COUNTY_NAME"
report_trip_gen(fnam0, fnam1, groupattr)

result_pro=pd.read_csv(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\Production_Overall.csv".format(scname)))
result_pro.columns=["County","HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Total"]
result_pro1=result_pro
result_pro1["AIRP"]= result_pro1["AIRP"].map("{:,.0f}".format)
result_pro1["COL"]= result_pro1["COL"].map("{:,.0f}".format)
result_pro1["EI"]= result_pro1["EI"].map("{:,.0f}".format)
result_pro1["HBO"]= result_pro1["HBO"].map("{:,.0f}".format)
result_pro1["HBSC"]= result_pro1["HBSC"].map("{:,.0f}".format)
result_pro1["HBSH"]= result_pro1["HBSH"].map("{:,.0f}".format)
result_pro1["HBSR"]= result_pro1["HBSR"].map("{:,.0f}".format)
result_pro1["HBW"]= result_pro1["HBW"].map("{:,.0f}".format)
result_pro1["HTRK"]= result_pro1["HTRK"].map("{:,.0f}".format)
result_pro1["LTRK"]= result_pro1["LTRK"].map("{:,.0f}".format)
result_pro1["NHBO"]= result_pro1["NHBO"].map("{:,.0f}".format)
result_pro1["NHBW"]= result_pro1["NHBW"].map("{:,.0f}".format)
result_pro1["TAXI"]= result_pro1["TAXI"].map("{:,.0f}".format)
result_pro1["Total"]= result_pro1["Total"].map("{:,.0f}".format)

result_pro1["County"]=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External","Total"]
html_pro=result_pro1.to_html(index=False,bold_rows=True)


result_protable=pd.read_csv(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\Production_Overall.csv".format(scname)))
result_protable.columns=["County","HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Total"]



result_atr=pd.read_csv(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\Attraction_Overall.csv".format(scname)))
result_atr.columns=["County","HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Total"]
result_atr1=result_atr
result_atr1["AIRP"]= result_atr1["AIRP"].map("{:,.0f}".format)
result_atr1["COL"]= result_atr1["COL"].map("{:,.0f}".format)
result_atr1["EI"]= result_atr1["EI"].map("{:,.0f}".format)
result_atr1["HBO"]= result_atr1["HBO"].map("{:,.0f}".format)
result_atr1["HBSC"]= result_atr1["HBSC"].map("{:,.0f}".format)
result_atr1["HBSH"]= result_atr1["HBSH"].map("{:,.0f}".format)
result_atr1["HBSR"]= result_atr1["HBSR"].map("{:,.0f}".format)
result_atr1["HBW"]= result_atr1["HBW"].map("{:,.0f}".format)
result_atr1["HTRK"]= result_atr1["HTRK"].map("{:,.0f}".format)
result_atr1["LTRK"]= result_atr1["LTRK"].map("{:,.0f}".format)
result_atr1["NHBO"]= result_atr1["NHBO"].map("{:,.0f}".format)
result_atr1["NHBW"]= result_atr1["NHBW"].map("{:,.0f}".format)
result_atr1["TAXI"]= result_atr1["TAXI"].map("{:,.0f}".format)
result_atr1["Total"]= result_atr1["Total"].map("{:,.0f}".format)
result_atr1["County"]=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External","Total"]
html_atr=result_atr1.to_html(index=False,bold_rows=True)

result_atrtable=pd.read_csv(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\Attraction_Overall.csv".format(scname)))
result_atrtable.columns=["County","HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Total"]

hillspro=str("{:,}".format(result_protable["Total"][0]))
hillsatr=str("{:,}".format(result_atrtable["Total"][0]))
pascopro=str("{:,}".format(result_protable["Total"][2]))
pascoatr=str("{:,}".format(result_atrtable["Total"][2]))
pinepro=str("{:,}".format(result_protable["Total"][1]))
pineatr=str("{:,}".format(result_atrtable["Total"][1]))
herpro=str("{:,}".format(result_protable["Total"][3]))
heratr=str("{:,}".format(result_atrtable["Total"][3]))
citpro=str("{:,}".format(result_protable["Total"][4]))
citatr=str("{:,}".format(result_atrtable["Total"][4]))

hills="Total Production:"+hillspro+"  "+"<br>Total Attraction:"+hillsatr
pasco="Total Production:"+pascopro+"  "+"<br>Total Attraction:"+pascoatr
pinellas="Total Production:"+pinepro+"  "+"<br>Total Attraction:"+pineatr
hernando="Total Production:"+herpro+"  "+"<br>Total Attraction:"+heratr
citrus="Total Production:"+citpro+"  "+"<br>Total Attraction:"+citatr


result_protable[["County","HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Total"]]=result_protable[["County","HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Total"]].astype(str)
pro_str=result_protable.values.tolist()
pro_str=pro_str[7]
pro_str=pro_str[1:14]
b="','"
x="["+"'"+b.join(pro_str ) +"'"+"]"  

result_atrtable[["County","HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Total"]]=result_atrtable[["County","HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Total"]].astype(str)
atr_str=result_atrtable.values.tolist()
atr_str=atr_str[7]
atr_str=atr_str[1:14]
b="','"
y="["+"'"+b.join(atr_str ) +"'"+"]"  



msg1 = "Production by Trip Purpose and by County"
msg2="Attraction by Trip Purpose and by County"

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
   width: 180px;
}
    
   thead {color: black;}
    tbody {color: black;}
    tfoot {color: red;}
    table{width:1000px;height:200px;}
    th, td {
      border: 1px solid black;
      text-align:center;
      font-size: 12px;
      height:10px;
      border-collapse: collapse;
    }
    tr {
  width:140%;
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
         text-align:right;
}
td:nth-child(8) {
         text-align:right;
}
td:nth-child(9) {
         text-align:right;
}
td:nth-child(10) {
         text-align:right;
}
td:nth-child(11) {
         text-align:right;
}
td:nth-child(12) {
         text-align:right;
}
td:nth-child(13) {
         text-align:right;
}
td:nth-child(14) {
         text-align:right;
}
td:nth-child(15) {
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
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#generation-collapse" aria-expanded="true">
          Trip Generation
        </button>
        <div class="collapse show" id="generation-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
            <li><a href="GEN_Overall.html" class="link-dark d-inline-flex text-decoration-none rounded" style="background-color:ADCEDE">Production & Attraction</a></li>
            <li><a href="GEN_INPUT.html" class="link-dark d-inline-flex text-decoration-none rounded"  >Trip Generation Statistics</a></li>
           
          </ul>
        </div>
      </li>
       <li class="mb-1">
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#dashboard-collapse" aria-expanded="false">
          Trip Distribution
        </button>
        <div class="collapse " id="dashboard-collapse">
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


<div class="map_gen" id="map_gen"> </div>



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
	<div class="groupbar" id="barchart_PANDAS">
  <h4> Production and Attraction Overall </h4>
    <canvas id="bar-chart-grouped" style="width:100%;max-width:1200px"></canvas>
    </div>
<script>

var xValues = """+x +""";
var yValues="""+y+""";

new Chart(document.getElementById("bar-chart-grouped"), {
    type: 'bar',
    data: {
      labels: ["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL"],
      datasets: [
        {
          label: "Production",
          backgroundColor: "#92B6C7",
          data: xValues
        }, {
          label: "Attraction",
          backgroundColor: "#F3A27C",
          data: yValues
        }
      ]
    },
    options: {
  
        

    
    }
});

</script>

<script>
    
    var map = L.map('map_gen').setView([28.276140, -82.585263], 9);
	
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






</body>

   <div class="generation1" id="production">
    <h4 style="padding: 5px 0;color:black">
    """ +msg1 + "</h4>"

table2="""
</div>
   <div class="generation2" id="attraction">
    <h4 style="padding: 5px 0;color:black">
    """ +msg2 + "</h4>"

end_html = """
        </div>
        </body>
        </html>
        """
if base==1:
  html = title +diff_45+main_continue+ html_pro +table2+html_atr+ end_html
else:
  html = title +main_continue+ html_pro +table2+html_atr+ end_html

text_file = open(os.path.join(Visum.GetPath(2), "outputs\\{}\\HTML\\GEN_Overall.html".format(scname)), "w")
text_file.write(html)
text_file.close()


