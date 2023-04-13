import pandas as pd
import numpy as np
import matplotlib.pyplot 
import os 
import csv 
import json 

PRIO = 20480


scname = Visum.Net.AttValue("SC_NAME")
groupattr = "LOCATION"
val=["AL_Capacity","VOL_ALL","LOCATION",]
df = pd.DataFrame(data=Visum.Net.Links.GetMultipleAttributes(val), columns=val)

df=df[df["VOL_ALL"]>0]

#County
result_validation= pd.DataFrame(df.groupby(groupattr, as_index=False).sum())
#result_validation["Number_of Links"]= df.groupby(groupattr).size()
result_validation["Volume/Capacity"]=result_validation["VOL_ALL"]/result_validation["AL_Capacity"]
result_validation["Volume/Capacity"]=result_validation["Volume/Capacity"].map("{:,.2f}".format)
result_validation['AL_Capacity'] = result_validation['AL_Capacity'].map("{:,.0f}".format)
result_validation['VOL_ALL'] = result_validation['VOL_ALL'].map("{:,.0f}".format)
result_validation=result_validation.reset_index(drop=True)
result_validation.rename(columns={"AL_Capacity":"Capacity","VOL_ALL":"Volume","LOCATION":"County"},inplace=True)
result_validation=result_validation[result_validation["County"]>0]
result_validation["County"].replace({1.0: "Hillsborough", 2.0: "Pinellas",3.0:"Pasco",4.0:"Hernando",5.0:"Citrus",6.0:"Others"}, inplace=True)


result_validation['Volume/Capacity'].astype(str)
xValues = result_validation['County'].to_list()
yValues = result_validation['Volume/Capacity'].to_list()
b="','"
x_County="["+"'"+b.join(xValues ) +"'"+"]"  
y_County="["+"'"+b.join(yValues ) +"'"+"]"  
html_county=result_validation.to_html(index=False,bold_rows=True)

val1=["FromNodeNo","ToNodeNo","FACL_TYPE","AL_Capacity","VOL_ALL","AREA_TYPE"]
df_ORG=pd.DataFrame(data=Visum.Net.Links.GetMultipleAttributes(val1), columns=val1)
df2=df_ORG[df_ORG["VOL_ALL"]>0]
df2["Facility Type"]=df2["FACL_TYPE"]//10*10
df2=df2.groupby(["Facility Type"]).sum().reset_index()
df2["Volume/Capacity"]=df2["VOL_ALL"]/df2["AL_Capacity"]
df2["Volume/Capacity"]=df2["Volume/Capacity"].round(2)
df2["Facility Type"]=df2["Facility Type"].map("{:,.0f}".format)
df2=df2.replace ({"Facility Type":{"10":"Freeway","20":"Divided Arterial","30":"Undivided Arterial","40":"Collector","60":"One Way Facility","70":"Ramps","90":"Toll Facilities"}})

df2["AL_Capacity"]=df2["AL_Capacity"].map("{:,.0f}".format)
df2["VOL_ALL"]=df2["VOL_ALL"].map("{:,.0f}".format)
df2=df2[["Facility Type","AL_Capacity","VOL_ALL","Volume/Capacity"]]
df2.columns=["Facility Type","Capacity","Volume","Volume/Capacity"]
df2.to_csv(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\HWYASSIN_FACLTYPE.csv".format(scname)))

FACL_html1=df2.to_html(index=False)
df2["Facility Type"]=df2["Facility Type"].astype(str)
FACL=list(df2["Facility Type"])
b="','"
x_FT="["+"'"+b.join(FACL) +"'"+"]"  

df2["Volume/Capacity"]=df2["Volume/Capacity"].astype(str)
vc=list(df2["Volume/Capacity"])
b="','"
y_FT="["+"'"+b.join(vc) +"'"+"]"  

df_AT=df_ORG.groupby(["AREA_TYPE"]).sum().reset_index()

df_AT["Volume/Capacity"]=df_AT["VOL_ALL"]/df_AT["AL_Capacity"]
df_AT=df_AT[["AREA_TYPE","AL_Capacity","VOL_ALL","Volume/Capacity"]]
df_AT.columns=["Area Type","Capacity","Volume","Volume/Capacity"]

df_AT.to_csv(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\HWYASSIN_AREATYPE.csv".format(scname)))

df_AT["Volume/Capacity"]=df_AT["Volume/Capacity"].round(2)
df_AT["Area Type"]=df_AT["Area Type"].map("{:,.0f}".format)
df_AT["Area Type"]=df_AT["Area Type"].astype(str)
df_AT=df_AT[1:]

AREA=list(df_AT["Area Type"])
b="','"
x_at="["+"'"+b.join(AREA) +"'"+"]"  
df_AT=df_AT.replace ({"Area Type":{"11":"11: Urbanized Area (over 500,000) Primary City CBD","12":"12: Urbanized Area (under 500,000) CBD","13":"13: Other Urbanized Area CBD and Small City Dowtown","14":"14: Non-Urbanized Area Small City Downtown","21":"21: All CBD Fringe Areas","31":"31: Developed Portions of Urbanized Areas","32":"32: Undeveloped Portions of Urbanized Areas","33":"33: Transitioning Areas/Urban Areas over 5,000 Population","34":"34: Residential Beach Area","41":"41: Major Outlying Business Districts","42":"42: Other Outlying Business Districts","43":"43: Beach OBD","51":"51: Developed Rural Areas/Small Cities under 5,000 Population","52":"52: Undeveloped Rural Areas"}})

df_AT["Capacity"]=df_AT["Capacity"].map("{:,.0f}".format)
df_AT["Volume"]=df_AT["Volume"].map("{:,.0f}".format)

AREA_html=df_AT.to_html(index=False)


df_AT["Volume/Capacity"]=df_AT["Volume/Capacity"].astype(str)
vc=list(df_AT["Volume/Capacity"])
b="','"
y_at="["+"'"+b.join(vc) +"'"+"]"  






mg1 = "Volume/Capacity by County"
mg2 = "Volume/Capacity by Facility Type"
mg3 = "Volume/Capacity by Area Type"



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
    table{width:700px;}
    th,td{
      border: 1px solid black;
      text-align: center;
      width: 35px;
      font-size: 12px;
    }

td:nth-child(1) {
  width:50%;
}
td:nth-child(2) {
  width:20%;
  text-align:right
}
td:nth-child(3) {
  width:20%;
  text-align:right
}
td:nth-child(4) {
  width:20%;

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
        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#Highway-collapse" aria-expanded="true">
         Highway Analysis
        </button>
        <div class="collapse show" id="Highway-collapse">
          <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
            <li><a href="Analysis_Overall.html" class="link-dark d-inline-flex text-decoration-none rounded" style="background-color:ADCEDE">Volume/Capacity</a></li>
            
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
            <li><a href="Validation_Overall.html" class="link-dark d-inline-flex text-decoration-none rounded" >VOL/CNT & RMSE</a></li>
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
<div class="barchart_County" id="barchart_VC">
  <h4 style="padding: 10px 0;color:black"> Volume/Capacity by County </h4>
    <canvas id="myChart_1" style="position: relative; height:18vh; width:35vw"></canvas>
    
    </div>

    <div class="barchart_AT" id="barchart_AT">
  <h4 style="padding: 10px 0;color:black"> Volume/Capacity by Area Type </h4>
    <canvas id="myChart_2" style="position: relative; height:30vh; width:35vw"></canvas>
    
    </div>

<div class="barchart_FT" id="barchart_FT">
  <h4 style="padding: 10px 0;color:black"> Volume/Capacity by Facility Type </h4>
    <canvas id="myChart_3" style="position: relative; height:20vh; width:35vw"></canvas>
    
    </div>



<script>
var xValues = """+x_County +""";
var yValues="""+y_County+""";

var xValues1 = """+x_at +""";
var yValues1 ="""+y_at+""";

var xValues2 = """+x_FT +""";
var yValues2 ="""+y_FT+""";

new Chart("myChart_1", {
  type: "bar",
  data: {
	labels:xValues,
    datasets: [{
      data: yValues,
        backgroundColor:"#92B6C7",
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

                                max: 1
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

new Chart("myChart_2", {
  type: "bar",
  data: {
	labels:xValues1,
    datasets: [{
      data: yValues1,
        backgroundColor:"#D37995",
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

                                max: 1
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

new Chart("myChart_3", {
  type: "bar",
  data: {
	labels:xValues2,
    datasets: [{
      data: yValues2,
        backgroundColor:"#6CBE7C",
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

                                max: 1
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




</script>

</body>

   <div class="table_county" id="County">
    <h3 style="padding: 10px 0;color:black">
    """ +mg1 + "</h3>"

table2="""
</div>
   <div class="table_FT" id="FT">
    <h4 style="padding: 5px 0;color:black">
    """ +mg2 + "</h4>"

table3="""
</div>
   <div class="table_AT" id="AT">
    <h4 style="padding: 5px 0;color:black">
    """ +mg3 + "</h4>"

end_html = """
        </div>
        </body>
        </html>
        """
if base==1:

  html = title +diff_45+main_continue+ html_county+table2 +FACL_html1 +table3+AREA_html+ end_html
else:
    html = title +main_continue+ html_county+table2 +FACL_html1 +table3+AREA_html+ end_html

text_file = open(os.path.join(Visum.GetPath(2), "outputs\\{}\\HTML\\Analysis_Overall.html".format(scname)), "w")
text_file.write(html)
text_file.close()


# PANDA_OVERALL


