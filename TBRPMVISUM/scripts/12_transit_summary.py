from operator import index
import os
import numpy as np
import pandas as pd
import VisumPy.helpers as h
import VisumPy.matrices as mf
import glob
import matplotlib.pyplot as plt

PRIO = 20480
scname  = Visum.Net.AttValue("SC_NAME")

transit_attr=["Name","TSysCode","CMODE","OPERATOR","PTripsUnlinked_Dseg(TR_OP,AP)","PassMiTrav_DSeg(TR_OP,AP)","PassHourTrav_DSeg(TR_OP,AP)","PTripsUnlinked_Dseg(TR_PK,AP)","PassMiTrav_DSeg(TR_PK,AP)","PassHourTrav_DSeg(TR_PK,AP)"]
summary = pd.DataFrame(data=Visum.Net.Lines.GetMultipleAttributes(transit_attr), columns=transit_attr)
writer=pd.ExcelWriter(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\transit_summary.xlsx".format(scname)),engine="xlsxwriter")
summary.to_excel(writer,sheet_name='summary')

summary_mode=summary.groupby(["CMODE"]).sum().reset_index()
summary_mode["PassHourTrav_DSeg(TR_OP,AP)"]=summary_mode["PassHourTrav_DSeg(TR_OP,AP)"]/3600
summary_mode["PassHourTrav_DSeg(TR_PK,AP)"]=summary_mode["PassHourTrav_DSeg(TR_PK,AP)"]/3600

summary_mode=summary_mode.drop(columns=["OPERATOR"])
summary_operator=summary.groupby(["OPERATOR"]).sum().reset_index()
summary_operator["PassHourTrav_DSeg(TR_OP,AP)"]=summary_operator["PassHourTrav_DSeg(TR_OP,AP)"]/3600
summary_operator["PassHourTrav_DSeg(TR_PK,AP)"]=summary_operator["PassHourTrav_DSeg(TR_PK,AP)"]/3600

summary_operator=summary_operator.drop(columns=["CMODE"])

summary_mode.to_excel(writer,sheet_name="Mode")
summary_operator.to_excel(writer,sheet_name="operator")
writer.close()



#barchart format 
summary_mode2=summary_mode
summary_operator2=summary_operator

summary_mode2=summary_mode2.astype(int)
summary_mode2=summary_mode2.astype(str)
mode=list(summary_mode2["CMODE"])
trips_op=list(summary_mode2["PTripsUnlinked_Dseg(TR_OP,AP)"])
trips_pk=list(summary_mode2["PTripsUnlinked_Dseg(TR_PK,AP)"])
miles_op=list(summary_mode2["PassMiTrav_DSeg(TR_OP,AP)"])
miles_pk=list(summary_mode2["PassMiTrav_DSeg(TR_PK,AP)"])
hr_op=list(summary_mode2["PassHourTrav_DSeg(TR_OP,AP)"])
hr_pk=list(summary_mode2["PassHourTrav_DSeg(TR_PK,AP)"])
b="','"
index_mode="["+"'"+b.join(mode) +"'"+"]"  
trips_op="["+"'"+b.join(trips_op) +"'"+"]"  
trips_pk="["+"'"+b.join(trips_pk) +"'"+"]"  
miles_op="["+"'"+b.join(miles_op) +"'"+"]"  
miles_pk="["+"'"+b.join(miles_pk) +"'"+"]"  
hr_op="["+"'"+b.join(hr_op) +"'"+"]"  
hr_pk="["+"'"+b.join(hr_pk) +"'"+"]"  

summary_operator2=summary_operator2.astype(int)
summary_operator2=summary_operator2.astype(str)
operator=list(summary_operator2["OPERATOR"])
trips_op1=list(summary_operator2["PTripsUnlinked_Dseg(TR_OP,AP)"])
trips_pk1=list(summary_operator2["PTripsUnlinked_Dseg(TR_PK,AP)"])
miles_op1=list(summary_operator2["PassMiTrav_DSeg(TR_OP,AP)"])
miles_pk1=list(summary_operator2["PassMiTrav_DSeg(TR_PK,AP)"])
hr_op1=list(summary_operator2["PassHourTrav_DSeg(TR_OP,AP)"])
hr_pk1=list(summary_operator2["PassHourTrav_DSeg(TR_PK,AP)"])
b="','"
operator="["+"'"+b.join(operator) +"'"+"]"  
trips_op1="["+"'"+b.join(trips_op1) +"'"+"]"  
trips_pk1="["+"'"+b.join(trips_pk1) +"'"+"]"  
miles_op1="["+"'"+b.join(miles_op1) +"'"+"]"  
miles_pk1="["+"'"+b.join(miles_pk1) +"'"+"]"  
hr_op1="["+"'"+b.join(hr_op1) +"'"+"]"  
hr_pk1="["+"'"+b.join(hr_pk1) +"'"+"]"  

#table html 
summary_mode1=summary_mode
summary_operator1=summary_operator
summary_mode1=summary_mode1.rename(columns={"CMODE":"Mode","PTripsUnlinked_Dseg(TR_OP,AP)":"Passenger Trips(OP)","PassMiTrav_DSeg(TR_OP,AP)":"Pass.Mi(OP)","PassHourTrav_DSeg(TR_OP,AP)":"Pass.Hr(OP)","PTripsUnlinked_Dseg(TR_PK,AP)":"Passenger Trips(PK)","PassMiTrav_DSeg(TR_PK,AP)":"Pass.Mi(PK)","PassHourTrav_DSeg(TR_PK,AP)":"Pass.Hr(PK)"})
summary_operator1=summary_operator1.rename(columns={"OPERATOR":"Operator","PTripsUnlinked_Dseg(TR_OP,AP)":"Passenger Trips(OP)","PassMiTrav_DSeg(TR_OP,AP)":"Pass.Mi(OP)","PassHourTrav_DSeg(TR_OP,AP)":"Pass.Hr(OP)","PTripsUnlinked_Dseg(TR_PK,AP)":"Passenger Trips(PK)","PassMiTrav_DSeg(TR_PK,AP)":"Pass.Mi(PK)","PassHourTrav_DSeg(TR_PK,AP)":"Pass.Hr(PK)"})

summary_mode1.loc['All Modes'] = summary_mode1.sum()
summary_operator1.loc['All Operators'] = summary_operator1.sum()

for column in summary_mode1:
  summary_mode1[column] =summary_mode1[column] .map("{:,.0f}".format)

for column in summary_operator1:
  summary_operator1[column] =summary_operator1[column] .map("{:,.0f}".format)

summary_operator1["Description"]=summary_operator1["Operator"]
summary_operator1=summary_operator1.replace({"Description":{"10":"Hillsborough Area Regional Transit (HART)","20":"Pinellas Suncoast Transit Authority (PSTA)","30":"Pasco County Public Transportation (PCPT)","40":"Hernando County TheBUS (TheBUS)","50":"Citrus County Transit (CCT)","60":"Tampa Bay Area Regional Transit Authority (TBARTA)"}})
summary_mode1["Description"]=summary_mode1["Mode"]
summary_mode1=summary_mode1.replace({"Description":{"10":"HART local buses Non-Premium","11":"HART express bus Non-Premium","12":"HART premium bus / in-street BRT Premium","14":"HART streetcar & AGT Non-Premium","15":"HART light rail Premium","17":"HART project circulator Premium","19":"HART project fixed-guideway mode Premium","20":"PSTA local bus Non-Premium","21":"PSTA express bus Non-Premium","22":"PSTA premium bus / in-street BRT Premium","27":"PSTA project circulator Premium","30":"PCPT local bus Non-Premium","31":"PCPT express bus Non-Premium","40":"TheBUS/CCT local bus Non-Premium"}})
summary_operator1=summary_operator1[["Operator","Description","Passenger Trips(PK)","Pass.Mi(PK)","Pass.Hr(PK)","Passenger Trips(OP)","Pass.Mi(OP)","Pass.Hr(OP)"]]
summary_mode1=summary_mode1[["Mode","Description","Passenger Trips(PK)","Pass.Mi(PK)","Pass.Hr(PK)","Passenger Trips(OP)","Pass.Mi(OP)","Pass.Hr(OP)"]]
summary_mode1.loc['All Modes','Mode'] = "All Modes"
summary_mode1.loc['All Modes','Description'] = ""
summary_operator1.loc['All Operators','Operator'] = "All Operators"
summary_operator1.loc['All Operators','Description'] = ""
html_mode=summary_mode1.to_html(index=False)
html_operator=summary_operator1.to_html(index=False)


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
    table{width:600px;height:200px;}
    table, th, td {
      border: 1px solid black;
      text-align: center;
      font-size: 12px;
      height:10px;
      border-collapse: collapse;
    }
td:nth-child(1) {
  width:5%;
}
td:nth-child(2) {
  width:65%;
  text-align: left;
}
td:nth-child(3) {
  width:5%;
   text-align: right;
}
td:nth-child(4) {
  width:5%;
  text-align: right;
}
td:nth-child(5) {
  width:5%;
  text-align: right;
}
td:nth-child(6) {
  width:5%;
  text-align: right;
}
td:nth-child(7) {
  width:5%;
  text-align: right;
}
td:nth-child(8) {
  width:5%;
  text-align: right;
}


tr {
  height: 30px;
  width:100%;
}
    
tr {
  height: 15px;
  width:120%;
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
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#Transit-collapse" aria-expanded="true">
          Transit Assignment
        </button>
        <div class="collapse show" id="Transit-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
            <li><a href="TRANSIT_Overall.html" class="link-dark d-inline-flex text-decoration-none rounded" style="background-color:ADCEDE" >Transit Summary</a></li>
  
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
	  <div class="trips" id="transit_trips">
    <h4 style="padding: 10px 0;color:black"> &nbsp&nbspTransit Summary by Mode </h4>
    <canvas id="trips" style="width:100%;max-width:1200px"></canvas>
    </div>
 	  <div class="miles" id="transit_miles">
    <canvas id="miles" style="width:100%;max-width:1200px"></canvas>
    </div>
	  <div class="hours" id="transit_hours">
    <canvas id="hours" style="width:100%;max-width:1200px"></canvas>
    </div>
    <div class="trips1" id="transit_trips1">
    <h4 style="padding: 10px 0;color:black"> &nbsp&nbspTransit Summary by Operator </h4>
    <canvas id="trips1" style="width:100%;max-width:1200px"></canvas>
    </div>
 	  <div class="miles1" id="transit_miles1">
    <canvas id="miles1" style="width:100%;max-width:1200px"></canvas>
    </div>
	  <div class="hours1" id="transit_hours1">
    <canvas id="hours1" style="width:100%;max-width:1200px"></canvas>
    </div>
<script>
var index_mode="""+str(index_mode)+""";
var xValues = """+str(trips_op)+""";
var yValues="""+str(trips_pk)+""";

new Chart(document.getElementById("trips"), {
    type: 'bar',
    data: {
      labels: index_mode,
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
      plugins:{
      title: {
        display: true,
        text: 'Passenger Trips by Mode'
      }
    }
    }
});

var index_mode="""+str(index_mode)+""";
var xValues = """+str(miles_op)+""";
var yValues="""+str(miles_pk)+""";

new Chart(document.getElementById("miles"), {
    type: 'bar',
    data: {
      labels: index_mode,
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
      plugins:{
      title: {
        display: true,
        text: 'Passenger Miles by Mode'
      }
    }
    }
});


var index_mode="""+str(index_mode)+""";
var xValues = """+str(hr_op)+""";
var yValues="""+str(hr_pk)+""";

new Chart(document.getElementById("hours"), {
    type: 'bar',
    data: {
      labels: index_mode,
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
      plugins:{
      title: {
        display: true,
        text: 'Passenger Hours by Mode'
      }
    }
    }
});

var index_mode="""+str(operator)+""";
var xValues = """+str(trips_op1)+""";
var yValues="""+str(trips_pk1)+""";

new Chart(document.getElementById("trips1"), {
    type: 'bar',
    data: {
      labels: index_mode,
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
      plugins:{
      title: {
        display: true,
        text: 'Passenger Trips by Operator'
      }
    }
    }
});

var index_mode="""+str(operator)+""";
var xValues = """+str(miles_op1)+""";
var yValues="""+str(miles_pk1)+""";

new Chart(document.getElementById("miles1"), {
    type: 'bar',
    data: {
      labels: index_mode,
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
      plugins:{
      title: {
        display: true,
        text: 'Passenger Miles by Operator'
      }
    }
    }
});


var index_mode="""+str(operator)+""";
var xValues = """+str(hr_op1)+""";
var yValues="""+str(hr_pk1)+""";

new Chart(document.getElementById("hours1"), {
    type: 'bar',
    data: {
      labels: index_mode,
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
      plugins:{
      title: {
        display: true,
        text: 'Passenger Hours by Operator'
      }
    }
    }
});
</script>

</body>

   <div class="transit_mode" id="tlf_op1">
    <h4 style="padding: 10px 0;color:black">
    """ +"Transit Summary by Mode" + "</h4>"

table2="""
</div>
   <div class="transit_operator" id="tlf_pk">
    <h4 style="padding: 10px 0;color:black">
    """ +"Transit Summary by Operator"+ "</h4>"



end_html = """
        </div>
        </body>
        </html>
        """
if base==1:
  html = title +diff_45+main_continue+ html_mode+ table2 + html_operator + end_html
else:
  html = title +main_continue+ html_mode+ table2 + html_operator + end_html

text_file = open(os.path.join(Visum.GetPath(2), "outputs\\{}\\HTML\\TRANSIT_Overall.html".format(scname)), "w")
text_file.write(html)
text_file.close()


