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
optlf_hills=optlf.rename(columns={"HIllsborough-AIRP_1C_OP-tlf.csv":"AIRP","HIllsborough-COL_1C_OP-tlf.csv":"COL","HIllsborough-EI_1C_OP-tlf.csv":"EI","HIllsborough-HBO_1C_OP-tlf.csv":"HBO","HIllsborough-HBSC_1C_OP-tlf.csv":"HBSC","HIllsborough-HBSH_1C_OP-tlf.csv":"HBSH","HIllsborough-HBSR_1C_OP-tlf.csv":"HBSR","HIllsborough-HBW_1C_OP-tlf.csv":"HBW","HIllsborough-HTRK_1C_OP-tlf.csv":"HTRK","HIllsborough-LTRK_1C_OP-tlf.csv":"LTRK","HIllsborough-NHBO_1C_OP-tlf.csv":"NHBO","HIllsborough-NHBW_1C_OP-tlf.csv":"NHBW","HIllsborough-TAXI_1C_OP-tlf.csv":"TAXI"})
optlf_hills=optlf_hills[["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL"]]
optlf_hills=optlf_hills.replace(np.nan,0)
optlf_hills=optlf_hills.replace("nan",0)
optlf_hills.index=["Total Trips","Intrazonal Trips","Intrazonal Percentage(%)","Average Trip Length (Miles)","Average Trip Length (Minutes)"]
optlf_hills=optlf_hills.T
optlf_hills=optlf_hills.apply(pd.to_numeric,errors="coerce",axis=1)
optlf_hills["Total Trip Length (Minutes)"]=optlf_hills["Average Trip Length (Minutes)"]*optlf_hills["Total Trips"]
optlf_hills["Total Trip Length (Miles)"]=optlf_hills["Average Trip Length (Miles)"]*optlf_hills["Total Trips"]
optlf_hills=optlf_hills[["Average Trip Length (Minutes)","Average Trip Length (Miles)","Total Trips","Total Trip Length (Minutes)","Total Trip Length (Miles)"]]

pk_total=[]
ave_mins_list=list(optlf_hills["Average Trip Length (Minutes)"])
ave_miles_list=list(optlf_hills["Average Trip Length (Miles)"])
total_trips_list=list(optlf_hills["Total Trips"])
total_tlf_mins_list=list(optlf_hills["Total Trip Length (Minutes)"])
total_tlf_miles_list=list(optlf_hills["Total Trip Length (Miles)"])
sum_mins=0
sum_miles=0
total_trips=0
total_tlf_mins=0
total_tlf_miles=0
optlf_hills=optlf_hills[["Average Trip Length (Minutes)","Average Trip Length (Miles)","Total Trips","Total Trip Length (Minutes)","Total Trip Length (Miles)"]]

for i in range(0,13):
  sum_mins=sum_mins+ave_mins_list[i]*total_trips_list[i]
  sum_miles=sum_miles+ave_miles_list[i]*total_trips_list[i]
  total_trips=total_trips+total_trips_list[i]
  total_tlf_mins=total_tlf_mins+total_tlf_mins_list[i]
  total_tlf_miles=total_tlf_miles+total_tlf_miles_list[i]

ave_mins_overall=sum_mins/total_trips
ave_miles_overall=sum_miles/total_trips
pk_total=[ave_mins_overall,ave_miles_overall,total_trips,total_tlf_mins,total_tlf_miles]
optlf_hills=optlf_hills.T
optlf_hills["Overall"]=pk_total
optlf_hills=optlf_hills.T

#change the format
optlf_hills["Average Trip Length (Miles)"]=optlf_hills["Average Trip Length (Miles)"].round(2)
optlf_hills["Average Trip Length (Minutes)"]=optlf_hills["Average Trip Length (Minutes)"].round(2)
optlf_hills["Total Trips"]=optlf_hills["Total Trips"].map("{:,.0f}".format)
optlf_hills["Total Trip Length (Minutes)"]=optlf_hills["Total Trip Length (Minutes)"].map("{:,.0f}".format)
optlf_hills["Total Trip Length (Miles)"]=optlf_hills["Total Trip Length (Miles)"].map("{:,.0f}".format)
optlf_hills=optlf_hills.reindex(["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Overall"])
optlf_hills_html=optlf_hills.to_html()
writer=pd.ExcelWriter(os.path.join(Visum.GetPath(2), "outputs\\{}\\summaries\\Trip Length by County.xlsx".format(scname)),engine="xlsxwriter")
optlf_hills.to_excel(writer,sheet_name='Hillsborough')
optlf_pasco=optlf.rename(columns={"Pasco-AIRP_1C_OP-tlf.csv":"AIRP","Pasco-COL_1C_OP-tlf.csv":"COL","Pasco-EI_1C_OP-tlf.csv":"EI","Pasco-HBO_1C_OP-tlf.csv":"HBO","Pasco-HBSC_1C_OP-tlf.csv":"HBSC","Pasco-HBSH_1C_OP-tlf.csv":"HBSH","Pasco-HBSR_1C_OP-tlf.csv":"HBSR","Pasco-HBW_1C_OP-tlf.csv":"HBW","Pasco-HTRK_1C_OP-tlf.csv":"HTRK","Pasco-LTRK_1C_OP-tlf.csv":"LTRK","Pasco-NHBO_1C_OP-tlf.csv":"NHBO","Pasco-NHBW_1C_OP-tlf.csv":"NHBW","Pasco-TAXI_1C_OP-tlf.csv":"TAXI"})
optlf_pasco=optlf_pasco[["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL"]]
optlf_pasco.index=["Total Trips","Intrazonal Trips","Intrazonal Percentage(%)","Average Trip Length (Miles)","Average Trip Length (Minutes)"]
optlf_pasco=optlf_pasco.replace(np.nan,0)
optlf_pasco=optlf_pasco.replace("nan",0)
optlf_pasco=optlf_pasco.T
optlf_pasco=optlf_pasco.apply(pd.to_numeric,errors="coerce",axis=1)
optlf_pasco["Total Trip Length (Minutes)"]=optlf_pasco["Average Trip Length (Minutes)"]*optlf_pasco["Total Trips"]
optlf_pasco["Total Trip Length (Miles)"]=optlf_pasco["Average Trip Length (Miles)"]*optlf_pasco["Total Trips"]
optlf_pasco=optlf_pasco[["Average Trip Length (Minutes)","Average Trip Length (Miles)","Total Trips","Total Trip Length (Minutes)","Total Trip Length (Miles)"]]
pk_total=[]
ave_mins_list=list(optlf_pasco["Average Trip Length (Minutes)"])
ave_miles_list=list(optlf_pasco["Average Trip Length (Miles)"])
total_trips_list=list(optlf_pasco["Total Trips"])
total_tlf_mins_list=list(optlf_pasco["Total Trip Length (Minutes)"])
total_tlf_miles_list=list(optlf_pasco["Total Trip Length (Miles)"])


sum_mins=0
sum_miles=0
total_trips=0
total_tlf_mins=0
total_tlf_miles=0
optlf_pasco=optlf_pasco[["Average Trip Length (Minutes)","Average Trip Length (Miles)","Total Trips","Total Trip Length (Minutes)","Total Trip Length (Miles)"]]


for i in range(0,13):
  sum_mins=sum_mins+ave_mins_list[i]*total_trips_list[i]
  sum_miles=sum_miles+ave_miles_list[i]*total_trips_list[i]
  total_trips=total_trips+total_trips_list[i]
  total_tlf_mins=total_tlf_mins+total_tlf_mins_list[i]
  total_tlf_miles=total_tlf_miles+total_tlf_miles_list[i]

ave_mins_overall=sum_mins/total_trips
ave_miles_overall=sum_miles/total_trips
pk_total=[ave_mins_overall,ave_miles_overall,total_trips,total_tlf_mins,total_tlf_miles]
optlf_pasco=optlf_pasco.T
optlf_pasco["Overall"]=pk_total
optlf_pasco=optlf_pasco.T

#change the format
optlf_pasco["Average Trip Length (Miles)"]=optlf_pasco["Average Trip Length (Miles)"].round(2)
optlf_pasco["Average Trip Length (Minutes)"]=optlf_pasco["Average Trip Length (Minutes)"].round(2)



optlf_pasco["Total Trips"]=optlf_pasco["Total Trips"].map("{:,.0f}".format)
optlf_pasco["Total Trip Length (Minutes)"]=optlf_pasco["Total Trip Length (Minutes)"].map("{:,.0f}".format)
optlf_pasco["Total Trip Length (Miles)"]=optlf_pasco["Total Trip Length (Miles)"].map("{:,.0f}".format)
optlf_pasco=optlf_pasco.reindex(["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Overall"])

optlf_pasco_html=optlf_pasco.to_html()


optlf_pasco.to_excel(writer,sheet_name='Pasco')

optlf_pinellas=optlf.rename(columns={"Pinellas-AIRP_1C_OP-tlf.csv":"AIRP","Pinellas-COL_1C_OP-tlf.csv":"COL","Pinellas-EI_1C_OP-tlf.csv":"EI","Pinellas-HBO_1C_OP-tlf.csv":"HBO","Pinellas-HBSC_1C_OP-tlf.csv":"HBSC","Pinellas-HBSH_1C_OP-tlf.csv":"HBSH","Pinellas-HBSR_1C_OP-tlf.csv":"HBSR","Pinellas-HBW_1C_OP-tlf.csv":"HBW","Pinellas-HTRK_1C_OP-tlf.csv":"HTRK","Pinellas-LTRK_1C_OP-tlf.csv":"LTRK","Pinellas-NHBO_1C_OP-tlf.csv":"NHBO","Pinellas-NHBW_1C_OP-tlf.csv":"NHBW","Pinellas-TAXI_1C_OP-tlf.csv":"TAXI"})
optlf_pinellas=optlf_pinellas[["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL"]]

optlf_pinellas.index=["Total Trips","Intrazonal Trips","Intrazonal Percentage(%)","Average Trip Length (Miles)","Average Trip Length (Minutes)"]
optlf_pinellas=optlf_pinellas.T
optlf_pinellas=optlf_pinellas.apply(pd.to_numeric,errors="coerce",axis=1)
optlf_pinellas["Total Trip Length (Minutes)"]=optlf_pinellas["Average Trip Length (Minutes)"]*optlf_pinellas["Total Trips"]
optlf_pinellas["Total Trip Length (Miles)"]=optlf_pinellas["Average Trip Length (Miles)"]*optlf_pinellas["Total Trips"]
optlf_pinellas=optlf_pinellas[["Average Trip Length (Minutes)","Average Trip Length (Miles)","Total Trips","Total Trip Length (Minutes)","Total Trip Length (Miles)"]]
optlf_pinellas=optlf_pinellas.replace(np.nan,0)
optlf_pinellas=optlf_pinellas.replace("nan",0)
pk_total=[]

ave_mins_list=list(optlf_pinellas["Average Trip Length (Minutes)"])
ave_miles_list=list(optlf_pinellas["Average Trip Length (Miles)"])
total_trips_list=list(optlf_pinellas["Total Trips"])
total_tlf_mins_list=list(optlf_pinellas["Total Trip Length (Minutes)"])
total_tlf_miles_list=list(optlf_pinellas["Total Trip Length (Miles)"])


sum_mins=0
sum_miles=0
total_trips=0
total_tlf_mins=0
total_tlf_miles=0
optlf_pinellas=optlf_pinellas[["Average Trip Length (Minutes)","Average Trip Length (Miles)","Total Trips","Total Trip Length (Minutes)","Total Trip Length (Miles)"]]


for i in range(0,13):
  sum_mins=sum_mins+ave_mins_list[i]*total_trips_list[i]
  sum_miles=sum_miles+ave_miles_list[i]*total_trips_list[i]
  total_trips=total_trips+total_trips_list[i]
  total_tlf_mins=total_tlf_mins+total_tlf_mins_list[i]
  total_tlf_miles=total_tlf_miles+total_tlf_miles_list[i]

ave_mins_overall=sum_mins/total_trips
ave_miles_overall=sum_miles/total_trips
pk_total=[ave_mins_overall,ave_miles_overall,total_trips,total_tlf_mins,total_tlf_miles]
optlf_pinellas=optlf_pinellas.T
optlf_pinellas["Overall"]=pk_total
optlf_pinellas=optlf_pinellas.T

#change the format
optlf_pinellas["Average Trip Length (Miles)"]=optlf_pinellas["Average Trip Length (Miles)"].round(2)
optlf_pinellas["Average Trip Length (Minutes)"]=optlf_pinellas["Average Trip Length (Minutes)"].round(2)

optlf_pinellas["Total Trips"]=optlf_pinellas["Total Trips"].map("{:,.0f}".format)
optlf_pinellas["Total Trip Length (Minutes)"]=optlf_pinellas["Total Trip Length (Minutes)"].map("{:,.0f}".format)
optlf_pinellas["Total Trip Length (Miles)"]=optlf_pinellas["Total Trip Length (Miles)"].map("{:,.0f}".format)
optlf_pinellas=optlf_pinellas.reindex(["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Overall"])

optlf_pinellas_html=optlf_pinellas.to_html()


optlf_pinellas.to_excel(writer,sheet_name='Pinellas')


optlf_Hernando=optlf.rename(columns={"Hernando-AIRP_1C_OP-tlf.csv":"AIRP","Hernando-COL_1C_OP-tlf.csv":"COL","Hernando-EI_1C_OP-tlf.csv":"EI","Hernando-HBO_1C_OP-tlf.csv":"HBO","Hernando-HBSC_1C_OP-tlf.csv":"HBSC","Hernando-HBSH_1C_OP-tlf.csv":"HBSH","Hernando-HBSR_1C_OP-tlf.csv":"HBSR","Hernando-HBW_1C_OP-tlf.csv":"HBW","Hernando-HTRK_1C_OP-tlf.csv":"HTRK","Hernando-LTRK_1C_OP-tlf.csv":"LTRK","Hernando-NHBO_1C_OP-tlf.csv":"NHBO","Hernando-NHBW_1C_OP-tlf.csv":"NHBW","Hernando-TAXI_1C_OP-tlf.csv":"TAXI"})
optlf_Hernando=optlf_Hernando[["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL"]]
optlf_Hernando=optlf_Hernando.replace(np.nan,0)
optlf_Hernando=optlf_Hernando.replace("nan",0)
optlf_Hernando.index=["Total Trips","Intrazonal Trips","Intrazonal Percentage(%)","Average Trip Length (Miles)","Average Trip Length (Minutes)"]
optlf_Hernando=optlf_Hernando.T
optlf_Hernando=optlf_Hernando.apply(pd.to_numeric,errors="coerce",axis=1)
optlf_Hernando["Total Trip Length (Minutes)"]=optlf_Hernando["Average Trip Length (Minutes)"]*optlf_Hernando["Total Trips"]
optlf_Hernando["Total Trip Length (Miles)"]=optlf_Hernando["Average Trip Length (Miles)"]*optlf_Hernando["Total Trips"]
optlf_Hernando=optlf_Hernando[["Average Trip Length (Minutes)","Average Trip Length (Miles)","Total Trips","Total Trip Length (Minutes)","Total Trip Length (Miles)"]]

pk_total=[]

ave_mins_list=list(optlf_Hernando["Average Trip Length (Minutes)"])
ave_miles_list=list(optlf_Hernando["Average Trip Length (Miles)"])
total_trips_list=list(optlf_Hernando["Total Trips"])
total_tlf_mins_list=list(optlf_Hernando["Total Trip Length (Minutes)"])
total_tlf_miles_list=list(optlf_Hernando["Total Trip Length (Miles)"])


sum_mins=0
sum_miles=0
total_trips=0
total_tlf_mins=0
total_tlf_miles=0
optlf_Hernando=optlf_Hernando[["Average Trip Length (Minutes)","Average Trip Length (Miles)","Total Trips","Total Trip Length (Minutes)","Total Trip Length (Miles)"]]


for i in range(0,13):
  sum_mins=sum_mins+ave_mins_list[i]*total_trips_list[i]
  sum_miles=sum_miles+ave_miles_list[i]*total_trips_list[i]
  total_trips=total_trips+total_trips_list[i]
  total_tlf_mins=total_tlf_mins+total_tlf_mins_list[i]
  total_tlf_miles=total_tlf_miles+total_tlf_miles_list[i]

ave_mins_overall=sum_mins/total_trips
ave_miles_overall=sum_miles/total_trips
pk_total=[ave_mins_overall,ave_miles_overall,total_trips,total_tlf_mins,total_tlf_miles]
optlf_Hernando=optlf_Hernando.T
optlf_Hernando["Overall"]=pk_total
optlf_Hernando=optlf_Hernando.T

#change the format
optlf_Hernando["Average Trip Length (Miles)"]=optlf_Hernando["Average Trip Length (Miles)"].round(2)
optlf_Hernando["Average Trip Length (Minutes)"]=optlf_Hernando["Average Trip Length (Minutes)"].round(2)
optlf_Hernando["Total Trips"]=optlf_Hernando["Total Trips"].map("{:,.0f}".format)
optlf_Hernando["Total Trip Length (Minutes)"]=optlf_Hernando["Total Trip Length (Minutes)"].map("{:,.0f}".format)
optlf_Hernando["Total Trip Length (Miles)"]=optlf_Hernando["Total Trip Length (Miles)"].map("{:,.0f}".format)
optlf_Hernando=optlf_Hernando.reindex(["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Overall"])

optlf_Hernando_html=optlf_Hernando.to_html()


optlf_Hernando.to_excel(writer,sheet_name='Hernando')



optlf_Citrus=optlf.rename(columns={"Citrus-AIRP_1C_OP-tlf.csv":"AIRP","Citrus-COL_1C_OP-tlf.csv":"COL","Citrus-EI_1C_OP-tlf.csv":"EI","Citrus-HBO_1C_OP-tlf.csv":"HBO","Citrus-HBSC_1C_OP-tlf.csv":"HBSC","Citrus-HBSH_1C_OP-tlf.csv":"HBSH","Citrus-HBSR_1C_OP-tlf.csv":"HBSR","Citrus-HBW_1C_OP-tlf.csv":"HBW","Citrus-HTRK_1C_OP-tlf.csv":"HTRK","Citrus-LTRK_1C_OP-tlf.csv":"LTRK","Citrus-NHBO_1C_OP-tlf.csv":"NHBO","Citrus-NHBW_1C_OP-tlf.csv":"NHBW","Citrus-TAXI_1C_OP-tlf.csv":"TAXI"})
optlf_Citrus=optlf_Citrus[["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL"]]
optlf_Citrus=optlf_Citrus.replace(np.nan,0)
optlf_Citrus=optlf_Citrus.replace("nan",0)
optlf_Citrus.index=["Total Trips","Intrazonal Trips","Intrazonal Percentage(%)","Average Trip Length (Miles)","Average Trip Length (Minutes)"]
optlf_Citrus=optlf_Citrus.T
optlf_Citrus=optlf_Citrus.apply(pd.to_numeric,errors="coerce",axis=1)
optlf_Citrus["Total Trip Length (Minutes)"]=optlf_Citrus["Average Trip Length (Minutes)"]*optlf_Citrus["Total Trips"]
optlf_Citrus["Total Trip Length (Miles)"]=optlf_Citrus["Average Trip Length (Miles)"]*optlf_Citrus["Total Trips"]
optlf_Citrus=optlf_Citrus[["Average Trip Length (Minutes)","Average Trip Length (Miles)","Total Trips","Total Trip Length (Minutes)","Total Trip Length (Miles)"]]
pk_total=[]

ave_mins_list=list(optlf_Citrus["Average Trip Length (Minutes)"])
ave_miles_list=list(optlf_Citrus["Average Trip Length (Miles)"])
total_trips_list=list(optlf_Citrus["Total Trips"])
total_tlf_mins_list=list(optlf_Citrus["Total Trip Length (Minutes)"])
total_tlf_miles_list=list(optlf_Citrus["Total Trip Length (Miles)"])


sum_mins=0
sum_miles=0
total_trips=0
total_tlf_mins=0
total_tlf_miles=0
optlf_Citrus=optlf_Citrus[["Average Trip Length (Minutes)","Average Trip Length (Miles)","Total Trips","Total Trip Length (Minutes)","Total Trip Length (Miles)"]]


for i in range(0,13):
  sum_mins=sum_mins+ave_mins_list[i]*total_trips_list[i]
  sum_miles=sum_miles+ave_miles_list[i]*total_trips_list[i]
  total_trips=total_trips+total_trips_list[i]
  total_tlf_mins=total_tlf_mins+total_tlf_mins_list[i]
  total_tlf_miles=total_tlf_miles+total_tlf_miles_list[i]

ave_mins_overall=sum_mins/total_trips
ave_miles_overall=sum_miles/total_trips
pk_total=[ave_mins_overall,ave_miles_overall,total_trips,total_tlf_mins,total_tlf_miles]
optlf_Citrus=optlf_Citrus.T
optlf_Citrus["Overall"]=pk_total
optlf_Citrus=optlf_Citrus.T

#change the format
optlf_Citrus["Average Trip Length (Miles)"]=optlf_Citrus["Average Trip Length (Miles)"].round(2)
optlf_Citrus["Average Trip Length (Minutes)"]=optlf_Citrus["Average Trip Length (Minutes)"].round(2)
optlf_Citrus["Total Trips"]=optlf_Citrus["Total Trips"].map("{:,.0f}".format)
optlf_Citrus["Total Trip Length (Minutes)"]=optlf_Citrus["Total Trip Length (Minutes)"].map("{:,.0f}".format)
optlf_Citrus["Total Trip Length (Miles)"]=optlf_Citrus["Total Trip Length (Miles)"].map("{:,.0f}".format)
optlf_Citrus=optlf_Citrus.reindex(["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Overall"])

optlf_Citrus_html=optlf_Citrus.to_html()


optlf_Citrus.to_excel(writer,sheet_name='Citrus')

optlf_Manatee=optlf.rename(columns={"Manatee-AIRP_1C_OP-tlf.csv":"AIRP","Manatee-COL_1C_OP-tlf.csv":"COL","Manatee-EI_1C_OP-tlf.csv":"EI","Manatee-HBO_1C_OP-tlf.csv":"HBO","Manatee-HBSC_1C_OP-tlf.csv":"HBSC","Manatee-HBSH_1C_OP-tlf.csv":"HBSH","Manatee-HBSR_1C_OP-tlf.csv":"HBSR","Manatee-HBW_1C_OP-tlf.csv":"HBW","Manatee-HTRK_1C_OP-tlf.csv":"HTRK","Manatee-LTRK_1C_OP-tlf.csv":"LTRK","Manatee-NHBO_1C_OP-tlf.csv":"NHBO","Manatee-NHBW_1C_OP-tlf.csv":"NHBW","Manatee-TAXI_1C_OP-tlf.csv":"TAXI"})
optlf_Manatee=optlf_Manatee[["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL"]]
optlf_Manatee=optlf_Manatee.replace(np.nan,0)
optlf_Manatee=optlf_Manatee.replace("nan",0)
optlf_Manatee.index=["Total Trips","Intrazonal Trips","Intrazonal Percentage(%)","Average Trip Length (Miles)","Average Trip Length (Minutes)"]
optlf_Manatee=optlf_Manatee.T
optlf_Manatee=optlf_Manatee.apply(pd.to_numeric,errors="coerce",axis=1)
optlf_Manatee["Total Trip Length (Minutes)"]=optlf_Manatee["Average Trip Length (Minutes)"]*optlf_Manatee["Total Trips"]
optlf_Manatee["Total Trip Length (Miles)"]=optlf_Manatee["Average Trip Length (Miles)"]*optlf_Manatee["Total Trips"]
optlf_Manatee=optlf_Manatee[["Average Trip Length (Minutes)","Average Trip Length (Miles)","Total Trips","Total Trip Length (Minutes)","Total Trip Length (Miles)"]]
pk_total=[]

ave_mins_list=list(optlf_Manatee["Average Trip Length (Minutes)"])
ave_miles_list=list(optlf_Manatee["Average Trip Length (Miles)"])
total_trips_list=list(optlf_Manatee["Total Trips"])
total_tlf_mins_list=list(optlf_Manatee["Total Trip Length (Minutes)"])
total_tlf_miles_list=list(optlf_Manatee["Total Trip Length (Miles)"])


sum_mins=0
sum_miles=0
total_trips=0
total_tlf_mins=0
total_tlf_miles=0
optlf_Manatee=optlf_Manatee[["Average Trip Length (Minutes)","Average Trip Length (Miles)","Total Trips","Total Trip Length (Minutes)","Total Trip Length (Miles)"]]


for i in range(0,13):
  sum_mins=sum_mins+ave_mins_list[i]*total_trips_list[i]
  sum_miles=sum_miles+ave_miles_list[i]*total_trips_list[i]
  total_trips=total_trips+total_trips_list[i]
  total_tlf_mins=total_tlf_mins+total_tlf_mins_list[i]
  total_tlf_miles=total_tlf_miles+total_tlf_miles_list[i]

ave_mins_overall=sum_mins/total_trips
ave_miles_overall=sum_miles/total_trips
pk_total=[ave_mins_overall,ave_miles_overall,total_trips,total_tlf_mins,total_tlf_miles]
optlf_Manatee=optlf_Manatee.T
optlf_Manatee["Overall"]=pk_total
optlf_Manatee=optlf_Manatee.T

#change the format
optlf_Manatee["Average Trip Length (Miles)"]=optlf_Manatee["Average Trip Length (Miles)"].round(2)
optlf_Manatee["Average Trip Length (Minutes)"]=optlf_Manatee["Average Trip Length (Minutes)"].round(2)
optlf_Manatee["Total Trips"]=optlf_Manatee["Total Trips"].map("{:,.0f}".format)
optlf_Manatee["Total Trip Length (Minutes)"]=optlf_Manatee["Total Trip Length (Minutes)"].map("{:,.0f}".format)
optlf_Manatee["Total Trip Length (Miles)"]=optlf_Manatee["Total Trip Length (Miles)"].map("{:,.0f}".format)
optlf_Manatee=optlf_Manatee.reindex(["HBW","HBSH","HBSR","HBSC","HBO","NHBW","NHBO","LTRK","HTRK","TAXI","EI","AIRP","COL","Overall"])

optlf_Manatee_html=optlf_Manatee.to_html()


optlf_Manatee.to_excel(writer,sheet_name='Manatee')
writer.close()


msg1="Hillsborough Off-Peak Trip Length "
msg2="Pinellas Off-Peak Trip Length  "

msg3="Pasco Off-Peak Trip Length  "

msg4="Hernando Off-Peak Trip Length  "

msg5="Citrus Off-Peak Trip Length  "
msg6="Other Off-Peak Trip Length  "




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
    table{width:500px;height:200px;}
    table, th, td {
      border: 1px solid black;
      text-align:center;
      font-size: 12px;
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
            <li><a href="Triplength_OP_County.html" class="link-dark d-inline-flex text-decoration-none rounded"  style="background-color:ADCEDE">OP Trip Length by County </a></li>
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
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>





   <div class="Hillsborough" id="Hillsborough">
    <h4 style="padding: 10px 0;color:black">
    """ +msg1 + "</h4>"

table2="""
</div>
   <div class="Pinellas" id="Pinellas">
    <h4 style="padding: 10px 0;color:black">
    """ +msg2 + "</h4>"

table3="""
</div>
   <div class="Pasco" id="Pasco">
    <h4 style="padding: 10px 0;color:black">
    """ +msg3 + "</h4>"

table4="""
</div>
   <div class="Hernando" id="Hernando">
    <h4 style="padding: 10px 0;color:black">
    """ +msg4 + "</h4>"

table5="""
</div>
   <div class="Citrus" id="Citrus">
    <h4 style="padding: 10px 0;color:black">
    """ +msg5 + "</h4>"
table6="""
</div>
   <div class="Manatee" id="Manatee">
    <h4 style="padding: 10px 0;color:black">
    """ +msg6 + "</h4>"



end_html = """
        </div>
        </body>
        </html>
        """

html = title+optlf_hills_html +table2+optlf_pinellas_html+table3+optlf_pasco_html+table4+optlf_Hernando_html+table5+optlf_Citrus_html+table6+optlf_Manatee_html+end_html

text_file = open(os.path.join(Visum.GetPath(2), "outputs\\{}\\HTML\\Triplength_OP_County.html".format(scname)), "w")
text_file.write(html)
text_file.close()


