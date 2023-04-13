# script to generate trip generation summary
# Chetan Joshi, Portland OR 3/16/2022
import pandas as pd
import numpy as np
import os 
import glob
PRIO = 20480

scname   = Visum.Net.AttValue("SC_NAME")
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
optlf.index=["Total Trips","Intrazonal Trips","Intrazonal Percentage(%)","Average Trip Length (Miles)","Average Trip Length (Minutes)"]
optlf=optlf.head(3)
optlf=optlf.T
optlf=optlf.apply(pd.to_numeric,errors="coerce",axis=1)

Visum.Log(PRIO, "{}".format(optlf))

op_ext=pd.read_csv(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\".format(scname))+"External-HBSC_1C_OP-tlf.csv",error_bad_lines=False)
op_ext=op_ext.drop(columns="Total Trips")

optlf.loc["HBSC"]["Intrazonal Trips"]=optlf.loc["HBSC"]["Intrazonal Trips"]-op_ext.iloc[0,0]

optlf=optlf.reindex(["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL"])
optlf["Intrazonal Percentage(%)"]=optlf["Intrazonal Trips"]/optlf["Total Trips"]*100




op_total=[]
intra_list=list(optlf["Intrazonal Trips"])
total_list=list(optlf["Total Trips"])
sum_intra=0
sum_total=0
for i in intra_list:
  sum_intra=sum_intra+i

for j in total_list:
  sum_total=sum_total+j

overall_percentage=sum_intra/sum_total*100
op_total=[sum_total,sum_intra,overall_percentage]
optlf=optlf.T
optlf["Overall"]=op_total
optlf=optlf.T


optlf2=optlf["Intrazonal Trips"]
optlf2=pd.DataFrame(optlf2)
optlf2["Intrazonal Trips"]=optlf2["Intrazonal Trips"].astype(str)
optlf_intra=list(optlf2["Intrazonal Trips"])
b="','"
op_intra="["+"'"+b.join(optlf_intra) +"'"+"]"  

optlf2=optlf["Total Trips"]
optlf2=pd.DataFrame(optlf2)
optlf2["Total Trips"]=optlf2["Total Trips"].astype(str)
optlf_rest=list(optlf2["Total Trips"])
optlf_rest=optlf_rest[:13]
b="','"
op_rest="["+"'"+b.join(optlf_rest) +"'"+"]"  

optlf["Total Trips"]=optlf["Total Trips"].map("{:,.0f}".format)
optlf["Intrazonal Trips"]=optlf["Intrazonal Trips"].map("{:,.0f}".format)
optlf["Intrazonal Percentage(%)"]=optlf["Intrazonal Percentage(%)"].map("{:,.2f}".format)



optlf1=optlf[["Intrazonal Trips","Total Trips","Intrazonal Percentage(%)"]]
optlf_html=optlf1.to_html()


writer=pd.ExcelWriter(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\Intrazonal.xlsx".format(scname)),engine="xlsxwriter")
optlf1.to_excel(writer,sheet_name='Off-Peak')



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
pktlf.index=["Total Trips","Intrazonal Trips","Intrazonal Percentage(%)","Average Trip Length (Minutes)","Average Trip Length (Miles)"]
pktlf=pktlf.head(3)
pktlf=pktlf.T
pktlf=pktlf.apply(pd.to_numeric,errors="coerce",axis=1)


pk_ext=pd.read_csv(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\".format(scname))+"External-HBSC_1C_PK-tlf.csv",error_bad_lines=False)
pk_ext=pk_ext.drop(columns="Total Trips")
pktlf.loc["HBSC"]["Intrazonal Trips"]=pktlf.loc["HBSC"]["Intrazonal Trips"]-pk_ext.iloc[0,0]

pktlf=pktlf.reindex(["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL"])

op_total=[]
intra_list=list(pktlf["Intrazonal Trips"])
total_list=list(pktlf["Total Trips"])
sum_intra=0
sum_total=0
for i in intra_list:
  sum_intra=sum_intra+i

for j in total_list:
  sum_total=sum_total+j

overall_percentage=sum_intra/sum_total*100

op_total=[sum_total,sum_intra,overall_percentage]

pktlf=pktlf.T
pktlf["Overall"]=op_total
pktlf=pktlf.T

pktlf2=pktlf["Intrazonal Trips"]
pktlf2=pd.DataFrame(pktlf2)
pktlf2["Intrazonal Trips"]=pktlf2["Intrazonal Trips"].astype(str)
pktlf_intra=list(pktlf2["Intrazonal Trips"])
b="','"
pk_intra="["+"'"+b.join(pktlf_intra) +"'"+"]" 
pktlf["Intrazonal Percentage(%)"]=pktlf["Intrazonal Trips"]/pktlf["Total Trips"]*100

pktlf2=pktlf["Total Trips"]
pktlf2=pd.DataFrame(pktlf2)
pktlf2["Total Trips"]=pktlf2["Total Trips"].astype(str)
pktlf_rest=list(pktlf2["Total Trips"])
pktlf_rest=pktlf_rest[:13]
b="','"
pk_rest="["+"'"+b.join(pktlf_rest) +"'"+"]" 

pktlf["Total Trips"]=pktlf["Total Trips"].map("{:,.0f}".format)
pktlf["Intrazonal Trips"]=pktlf["Intrazonal Trips"].map("{:,.0f}".format)
pktlf["Intrazonal Percentage(%)"]=pktlf["Intrazonal Percentage(%)"].map("{:,.2f}".format)


pktlf1=pktlf[["Intrazonal Trips","Total Trips","Intrazonal Percentage(%)"]]
pktlf_html=pktlf1.to_html()

pktlf1.to_excel(writer,sheet_name='Peak')
writer.close()


msg1 = "Off-Peak Intrazonal Trips"
msg2 = "Peak Intrazonal Trips"


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
    table{width:450px;height:200px;}
    th, td {
      border: 1px solid black;
      text-align: center;
      width: 35px;
      font-size: 12px;
      height:10px
      padding:10px;
    }

    
tr {
  height: 25px;
  width:120%;
}

td:nth-child(2) {
         text-align:right;
}

td:nth-child(3) {
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
            <li><a href="Triplength.html" class="link-dark d-inline-flex text-decoration-none rounded" >Trip Length Overall</a></li>
            <li><a href="Triplength_PK_County.html" class="link-dark d-inline-flex text-decoration-none rounded"  >PK Trip Length by County </a></li>
            <li><a href="Triplength_OP_County.html" class="link-dark d-inline-flex text-decoration-none rounded"  >OP Trip Length by County </a></li>
             <li><a href="DIST_Intra.html" class="link-dark d-inline-flex text-decoration-none rounded" style="background-color:ADCEDE">Intrazonal Trips Overall</a></li>
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

	<div class="stack_op" id="stack_op1">
     <h4> Off-Peak Intrazonal Trips </h4>
    <canvas id="stack_op" style="width:100%;max-width:1200px"></canvas>
    </div>
    	<div class="stack_pk" id="stack_pk1">
      <h4> Peak Intrazonal Trips </h4>
    <canvas id="stack_pk" style="width:100%;max-width:1200px"></canvas>
    </div>
<script>

var xValues = """+str(optlf_intra)+""";
var yValues="""+str(optlf_rest)+""";

new Chart(document.getElementById("stack_op"), {
    type: 'bar',
    data: {
      labels: ["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL"],
      datasets: [
        {
          label: "Intrazonal Trips",
          backgroundColor: "#92B6C7",
          data: xValues
        }, 
        {
          label: "Total Trips",
          backgroundColor: "#F3A27C",
          data: yValues
        }
      ]
    },
    options: {
      
         scales:{
          xAxes:[{stacked:true,}],
          yAxes:[{stacked:true,}]
      }
    }
});

</script>

<script>

var xValues1 = """+str(pktlf_intra)+""";
var yValues1 ="""+str(pktlf_rest)+""";


new Chart(document.getElementById("stack_pk"), {
    type: 'bar',
    data: {
      labels: ["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL"],
      datasets: [
        {
          label: "Intrazonal Trips",
          backgroundColor: "#92B6C7",
          data: xValues1
        }, 
        {
          label: "Total Trips",
          backgroundColor: "#F3A27C",
          data: yValues1
        }
      ]
    },
    options: {
        scales:{
          xAxes:[{stacked:true,}],
          yAxes:[{stacked:true,}]
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

text_file = open(os.path.join(Visum.GetPath(2), "outputs\\{}\\HTML\\DIST_intra.html".format(scname)), "w")
text_file.write(html)
text_file.close()


