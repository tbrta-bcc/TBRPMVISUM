import os
import numpy as np
import pandas as pd
import VisumPy.helpers as h
import VisumPy.matrices as mf


PRIO = 20480
scname  = Visum.Net.AttValue("SC_NAME")
groupattr="COUNTY"
population=["COUNTY","POP","GQPOP"]
df_pop = pd.DataFrame(data=Visum.Net.Zones.GetMultipleAttributes(population), columns=population)
df_pop= df_pop.groupby(groupattr).sum()
df_pop["Total Population"]=df_pop["POP"]+df_pop["GQPOP"]
df_pop=df_pop.rename(columns={"POP": "Permanent", "GQPOP": "Group Quarters"})
df_pop.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External"]
df_pop=df_pop.drop(index="External")
df_pop.loc["Total"]=df_pop.sum()
df_pop=df_pop.T
perm_pop=df_pop.loc["Permanent"].reset_index(drop=True).squeeze()
tot_pop=df_pop.loc["Total Population"].reset_index(drop=True).squeeze()
df_pop=df_pop.T
df_pop["Group Quarters"]=df_pop["Group Quarters"].map("{:,.0f}".format)
df_pop["Total Population"]=df_pop["Total Population"].map("{:,.0f}".format)
df_pop["Permanent"]=df_pop["Permanent"].map("{:,.0f}".format)
df_pop=df_pop.T

writer=pd.ExcelWriter(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\Generation_Input.xlsx".format(scname)),engine="xlsxwriter")
df_pop.to_excel(writer,sheet_name='population')
df_pop_html=df_pop.to_html(index=True,bold_rows=True)

DU=["COUNTY","DU","PCTVNP","PCTVAC"]
df_du = pd.DataFrame(data=Visum.Net.Zones.GetMultipleAttributes(DU), columns=DU)

df_du["Seasonally Occupied"]=df_du["DU"]*(df_du["PCTVNP"]-df_du["PCTVAC"])/100
df_du["Vacant Dwelling Units"]=df_du["DU"]*(df_du["PCTVAC"])/100
df_du["Permanently Occupied"]=df_du["DU"]-df_du["Seasonally Occupied"]-df_du["Vacant Dwelling Units"]
df_du["Total Dwelling Units"]=df_du["DU"]
df_du= df_du.groupby(groupattr).sum()
df_du.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External"]
df_du=df_du.drop(index="External")
df_du.loc["Total"]=df_du.sum()

df_du=df_du[["Permanently Occupied","Seasonally Occupied","Vacant Dwelling Units","Total Dwelling Units"]].astype(int)
df_du=df_du.T
perm_occu=df_du.loc["Permanently Occupied"].reset_index(drop=True).squeeze()

tot_occu=(df_du.loc["Permanently Occupied"]+df_du.loc["Seasonally Occupied"]).reset_index(drop=True).squeeze()
df_du.to_excel(writer,sheet_name='DU')
df_du=df_du.T

for column in df_du:
  df_du[column]=df_du[column].map("{:,.0f}".format)

df_du=df_du.T

df_du_html=df_du.to_html(index=True,bold_rows=True)

PDU=["COUNTY","DU","PCTVNP","RET0" ,"RET1","RET2","RET3"]
df_pdu = pd.DataFrame(data=Visum.Net.Zones.GetMultipleAttributes(PDU), columns=PDU)
df_pdu["DU1"]=df_pdu["DU"]*(100-df_pdu["PCTVNP"])/100
df_pdu["Retired 0 Auto"] = df_pdu["DU1"]*df_pdu["RET0"]/100
df_pdu["Retired 1 Auto"] = df_pdu["DU1"]*df_pdu["RET1"]/100
df_pdu["Retired 2 Auto"] = df_pdu["DU1"]*df_pdu["RET2"]/100
df_pdu["Retired 3+ Auto"] = df_pdu["DU1"]*df_pdu["RET3"]/100
df_pdu["Total Retired"]=df_pdu["Retired 0 Auto"]+df_pdu["Retired 1 Auto"]+df_pdu["Retired 2 Auto"]+df_pdu["Retired 3+ Auto"]
df_pdu= df_pdu.groupby(groupattr).sum()
df_pdu.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External"]
df_pdu=df_pdu.drop(index="External")
df_pdu.loc["Total"]=df_pdu.sum()

df_pdu=df_pdu[["Retired 0 Auto","Retired 1 Auto","Retired 2 Auto","Retired 3+ Auto","Total Retired"]].astype(int)
df_pdu=df_pdu.T

df_pdu.to_excel(writer,sheet_name='Permanently Occupied DU')
df_pdu=df_pdu.T

for column in df_pdu:
  df_pdu[column]=df_pdu[column].map("{:,.0f}".format)
df_pdu=df_pdu.T
df_pdu_html=df_pdu.to_html(index=True,bold_rows=True)

DU_WOC=["COUNTY","DU","PCTVNP","WNC0" ,"WNC1","WNC2","WNC3"]

df_wocdu = pd.DataFrame(data=Visum.Net.Zones.GetMultipleAttributes(DU_WOC), columns=DU_WOC)
df_wocdu["DU1"]=df_wocdu["DU"]*(100-df_wocdu["PCTVNP"])/100
df_wocdu["Working w/o Children 0 Auto"] = df_wocdu["DU1"]*df_wocdu["WNC0"]/100
df_wocdu["Working w/o Children 1 Auto"] = df_wocdu["DU1"]*df_wocdu["WNC1"]/100
df_wocdu["Working w/o Children 2 Auto"] = df_wocdu["DU1"]*df_wocdu["WNC2"]/100
df_wocdu["Working w/o Children 3+ Auto"] = df_wocdu["DU1"]*df_wocdu["WNC3"]/100
df_wocdu["Total Working w/o Children"]=df_wocdu["Working w/o Children 0 Auto"]+df_wocdu["Working w/o Children 1 Auto"]+df_wocdu["Working w/o Children 2 Auto"]+df_wocdu["Working w/o Children 3+ Auto"]
df_wocdu= df_wocdu.groupby(groupattr).sum()
df_wocdu.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External"]
df_wocdu=df_wocdu.drop(index="External")
df_wocdu.loc["Total"]=df_wocdu.sum()

df_wocdu=df_wocdu[["Working w/o Children 0 Auto","Working w/o Children 1 Auto","Working w/o Children 2 Auto","Working w/o Children 3+ Auto","Total Working w/o Children"]].astype(int)
df_wocdu=df_wocdu.T
work_hhs1=df_wocdu.loc["Total Working w/o Children"].reset_index(drop=True).squeeze()
df_wocdu=df_wocdu.T

df_wocdu.to_excel(writer,sheet_name="Working wo Children")
for column in df_wocdu:
  df_wocdu[column]=df_wocdu[column].map("{:,.0f}".format)
df_wocdu=df_wocdu.T

df_wocdu_html=df_wocdu.to_html(index=True,bold_rows=True)


DU_WC=["COUNTY","DU","PCTVNP","WHC0" ,"WHC1","WHC2","WHC3"]

df_wcdu = pd.DataFrame(data=Visum.Net.Zones.GetMultipleAttributes(DU_WC), columns=DU_WC)
df_wcdu["DU1"]=df_wcdu["DU"]*(100-df_wcdu["PCTVNP"])/100
df_wcdu["Working w/ Children 0 Auto"] = df_wcdu["DU1"]*df_wcdu["WHC0"]/100
df_wcdu["Working w/ Children 1 Auto"] = df_wcdu["DU1"]*df_wcdu["WHC1"]/100
df_wcdu["Working w/ Children 2 Auto"] = df_wcdu["DU1"]*df_wcdu["WHC2"]/100
df_wcdu["Working w/ Children 3+ Auto"] = df_wcdu["DU1"]*df_wcdu["WHC3"]/100
df_wcdu["Total Working w/ Children"]=df_wcdu["Working w/ Children 0 Auto"]+df_wcdu["Working w/ Children 1 Auto"]+df_wcdu["Working w/ Children 2 Auto"]+df_wcdu["Working w/ Children 3+ Auto"]
df_wcdu= df_wcdu.groupby(groupattr).sum()
df_wcdu.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External"]
df_wcdu=df_wcdu.drop(index="External")
df_wcdu.loc["Total"]=df_wcdu.sum()

df_wcdu=df_wcdu[["Working w/ Children 0 Auto","Working w/ Children 1 Auto","Working w/ Children 2 Auto","Working w/ Children 3+ Auto","Total Working w/ Children"]].astype(int)
df_wcdu=df_wcdu.T
df_wcdu.to_excel(writer,sheet_name="Working w Children")
work_hhs2=df_wcdu.loc["Total Working w/ Children"].reset_index(drop=True).squeeze()
df_wcdu=df_wcdu.T
for column in df_wcdu:
  df_wcdu[column]=df_wcdu[column].map("{:,.0f}".format)
df_wcdu=df_wcdu.T
df_wcdu_html=df_wcdu.to_html(index=True,bold_rows=True)

# re-write the ZDATA1 database file, classifying the updated Hotel / Motel units into one of three types: CBD
# (High Density), Medium Density, and Low Density. The Dynamic Area Types 1 and 2 are combined for the CBD (High
# Density) group, Types 3 and 4 are combined for the Medium Density group, and Type 5 is used for the Low Density group.
DU_BHU=["COUNTY","AT","BHU"]

df_dubhu = pd.DataFrame(data=Visum.Net.Zones.GetMultipleAttributes(DU_BHU), columns=DU_BHU)
df_dubhu[['AT']] = df_dubhu[['AT']].replace([1, 2, 3,4,5], ["High","High","Med","Med","Low"])

groupattr1=df_dubhu["AT"]
df_dubhu1= df_dubhu.groupby(["COUNTY","AT"]).sum().unstack().reset_index().fillna(0)
df_dubhu1=pd.DataFrame(df_dubhu1)
df_dubhu1=df_dubhu1.iloc[0:6,2:]
df_dubhu1.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other"]
hillsborough = df_dubhu1.iloc[0].reset_index(drop=True).squeeze()
pinellas=df_dubhu1.iloc[1].reset_index(drop=True).squeeze()
pasco=df_dubhu1.iloc[2].reset_index(drop=True).squeeze()
hernando=df_dubhu1.iloc[3].reset_index(drop=True).squeeze()
citrus=df_dubhu1.iloc[4].reset_index(drop=True).squeeze()
other=df_dubhu1.iloc[5].reset_index(drop=True).squeeze()

df_dubhu2=pd.concat([hillsborough,pinellas,pasco,hernando,citrus,other],axis=1)
df_dubhu2.index=["Number of CBD / High Density","Number of Very Low Density","Number of Med / Low Density"]
df_dubhu2.loc["Total Hotel / Motel Units"]=df_dubhu2.sum()
df_dubhu2["Total"]=df_dubhu2.sum(axis=1)
df_dubhu2=df_dubhu2.reindex(["Number of CBD / High Density","Number of Med / Low Density","Number of Very Low Density"])

df_dubhu2.to_excel(writer,sheet_name="Hotel Motel")
df_dubhu2=df_dubhu2.T

for column in df_dubhu2:
  df_dubhu2[column]=df_dubhu2[column].map("{:,.0f}".format)

df_dubhu2=df_dubhu2.T

df_dubhu2_html=df_dubhu2.to_html(index=True,bold_rows=True)


ED=["COUNTY","K12ENR","HIEDUC"]
df_ed = pd.DataFrame(data=Visum.Net.Zones.GetMultipleAttributes(ED), columns=ED)
df_ed= df_ed.groupby(["COUNTY"]).sum().fillna(0)
df_ed["Total School Enrollment"]=df_ed["K12ENR"]+df_ed["HIEDUC"]
df_ed.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","EXternal"]
df_ed=df_ed.drop(index="EXternal")
df_ed.loc["Total"]=df_ed.sum()
df_ed=df_ed.rename(columns={"K12ENR": "K-12", "HIEDUC": "College/University"})
df_ed=df_ed.T
tot_sch=df_ed.loc["Total School Enrollment"].reset_index(drop=True).squeeze()
df_ed.to_excel(writer,sheet_name="Educational Enrolment")
df_ed=df_ed.T

for column in df_ed:
  df_ed[column]=df_ed[column].map("{:,.0f}".format)
df_ed=df_ed.T

df_ed_html=df_ed.to_html(index=True,bold_rows=True)

EMP=["COUNTY","IND_EMP","COMM_REMP","COMM_LEMP","SERV_REMP","SERV_LEMP","TOT_EMP"]
df_emp = pd.DataFrame(data=Visum.Net.Zones.GetMultipleAttributes(EMP), columns=EMP)
df_emp["Commercial Total"]=df_emp["COMM_REMP"]+df_emp["COMM_LEMP"]
df_emp["Service Total"]=df_emp["SERV_REMP"]+df_emp["SERV_LEMP"]
df_emp= df_emp.groupby(groupattr).sum()
df_emp=df_emp.rename(columns={"IND_EMP":"Industrial","COMM_REMP":"Commercial Regional","COMM_LEMP":"Commercial Local","SERV_REMP":"Service Regional","SERV_LEMP":"Service Local","TOT_EMP":"Total Employment"})
df_emp=df_emp[["Industrial","Commercial Regional","Commercial Local","Service Regional","Service Local","Commercial Total","Service Total","Total Employment"]]
df_emp.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","External"]
df_emp=df_emp.drop(index="External")
df_emp.loc["Total"]=df_emp.sum()

df_emp=df_emp.T
ser_emp=df_emp.loc["Service Total"].reset_index(drop=True).squeeze()
tot_emp=df_emp.loc["Total Employment"].reset_index(drop=True).squeeze()
df_emp.to_excel(writer,sheet_name="Employment")
df_emp=df_emp.T

for column in df_emp:
  df_emp[column]=df_emp[column].map("{:,.0f}".format)
df_emp=df_emp.T

df_emp_html=df_emp.to_html(index=True,bold_rows=True)

ratio=pd.concat([perm_pop,perm_occu,tot_pop,tot_occu,ser_emp,tot_emp,work_hhs1,work_hhs2,tot_sch],axis=1)
ratio.index=["Hillsborough","Pinellas","Pasco","Hernando","Citrus","Other","EXternal"]
ratio=ratio.drop(index="EXternal")
ratio.loc["Total"]=ratio.sum()
ratio.columns=["perm_pop","perm_occu","tot_pop","tot_occu","ser_emp","tot_emp","work_hhs1","work_hhs2","tot_sch"]
ratio["PERM POP/PERM OCCDU"]=round(ratio["perm_pop"]/ratio["perm_occu"],2)
ratio["TOT POP/TOT OCCDU"]=round(ratio["tot_pop"]/ratio["tot_occu"],2)
ratio["SERVICE EMP/TOT EMP"]=round(ratio["ser_emp"]/ratio["tot_emp"],2)
ratio["TOT EMP/PERM POP"]=round(ratio["tot_emp"]/ratio["perm_pop"],2)
ratio["workingshhs"]=round(ratio["work_hhs1"]+ratio["work_hhs2"],2)
ratio["TOT EMP/WORKING HHS"]=round(ratio["tot_emp"]/ratio["workingshhs"],2)
ratio["TOT SCH/TOT WWC HHS"]=round(ratio["tot_sch"]/ratio["work_hhs2"],2)
ratio["TOT SCH/TOT OCCDU"]=round(ratio["tot_sch"]/ratio["tot_occu"],2)
ratio=ratio[["PERM POP/PERM OCCDU","TOT POP/TOT OCCDU","SERVICE EMP/TOT EMP","TOT EMP/PERM POP","TOT EMP/WORKING HHS","TOT SCH/TOT WWC HHS","TOT SCH/TOT OCCDU"]]
ratio=ratio.T
ratio.to_excel(writer,sheet_name="Ratio")
ratio_html=ratio.to_html(index=True,bold_rows=True)


writer.close()
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
    table{width:750px}
    table, th, td {
      border: 1px solid black;
      text-align:center;
      font-size: 12px;
      height:10px;
      border-collapse: collapse;
    }
td:nth-child(1) {
  width:20%;
    text-align:center;
}
td:nth-child(2) {
    width:10%;

     text-align:right;
}
td:nth-child(3) {
      width:10%;

         text-align:right;
}
td:nth-child(4) {
      width:10%;

         text-align:right;
}
td:nth-child(5) {
      width:10%;

         text-align:right;
}
td:nth-child(6) {
      width:10%;

         text-align:right;
}
td:nth-child(7) {
      width:10%;

         text-align:right;
}
td:nth-child(8) {
      width:10%;

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
            <li><a href="GEN_Overall.html" class="link-dark d-inline-flex text-decoration-none rounded" >Production & Attraction</a></li>
            <li><a href="GEN_INPUT.html" class="link-dark d-inline-flex text-decoration-none rounded" style="background-color:ADCEDE" >Trip Generation Statistics</a></li>
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
	<div class="groupbar" id="barchart_PANDAS">
    <canvas id="bar-chart-grouped" style="width:100%;max-width:1200px"></canvas>
    </div>


</body>

   <div class="pop" id="pop">
 <h4 style="padding: 10px 0;color:black;background-color:#F39db8">
     """ +"Population" + "</h4>"

table2="""
</div>
   <div class="dwell" id="oc_ta1">
 <h4 style="padding: 10px 0;color:black;background-color:#4b7185">
     """ +"Total Dwelling Units" + "</h4>"

table3="""
</div>
   <div class="pemocc" id="pemocc">
    <h4 style="padding: 10px 0;color:black;background-color:#4b7185">
    """ +"Permanently Occupied Dwelling Units: Retirement" + "</h4>"
table4="""
</div>
   <div class="woc" id="woc">
    <h4 style="padding: 10px 0;color:black;background-color:#4b7185">
    """ +"Permanently Occupied Dwelling Units: Working without Children" + "</h4>"
  
table5="""
</div>
   <div class="wc" id="wc">
    <h4 style="padding: 10px 0;color:black;background-color:#4b7185">
    """ +"Permanently Occupied Dwelling Units: Working with Children" + "</h4>"

table6="""
</div>
   <div class="bhu" id="bhu">
    <h4 style="padding: 10px 0;color:black;background-color:#4b8582">
    """ +"Hotel/Motel Units" + "</h4>"
table7="""
</div>
   <div class="ed" id="ed">
    <h4 style="padding: 10px 0;color:black;background-color:#75d6a9">
    """ +"Educational Enrollment" + "</h4>"
table8="""
</div>
   <div class="emp" id="emp">
    <h4 style="padding: 10px 0;color:black;background-color:#d69875">
    """ +"Employment" + "</h4>"
  
table9="""
</div>
   <div class="ratio1" id="ratio1">
    <h4 style="padding: 10px 0;color:black;background-color:#4b8552">
    """ +"Ratio Statistics" + "</h4>"


end_html = """
        </div>
        </body>
        </html>
        """

if base==1:

  html = title +diff_45+main_continue+  df_pop_html+table2+df_du_html +table3+ df_pdu_html+table4+ df_wocdu_html+table5+df_wcdu_html+table6+ df_dubhu2_html+table7+df_ed_html+table8+df_emp_html+table9+ratio_html+end_html
else:
  html = title +main_continue+df_pop_html +table2+df_du_html+table3+ df_pdu_html+table4+ df_wocdu_html+table5+df_wcdu_html +table6+ df_dubhu2_html+table7+df_ed_html+table8+df_emp_html+table9+ratio_html+end_html


text_file = open(os.path.join(Visum.GetPath(2), "outputs\\{}\\HTML\\GEN_INPUT.html".format(scname)), "w")
text_file.write(html)
text_file.close()


