# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy


# First some MPG Data Exploration
@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

#df_raw=load_data(path=r".\data\raw\renewable_power_plants_CH.csv")
df_raw=load_data(path=r"./data/raw/renewable_power_plants_CH.csv")
df=deepcopy(df_raw)

# Add title and header
st.title("Clean Energy Sources in Switzerland")
st.header("Analysis of Renewable Energy")

# st.table(data=mpg_df)
left_column, middle_column, right_column = st.columns([1, 1, 1])

#add sidebar

if st.sidebar.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=df)


#cleaning dataframe
cantons_dict = {'TG':'Thurgau', 'GR':'Graubünden', 'LU':'Luzern', 'BE':'Bern', 'VS':'Valais',
                'BL':'Basel-Landschaft', 'SO':'Solothurn', 'VD':'Vaud', 'SH':'Schaffhausen', 'ZH':'Zürich',
                'AG':'Aargau', 'UR':'Uri', 'NE':'Neuchâtel', 'TI':'Ticino', 'SG':'St. Gallen', 'GE':'Genève',
                'GL':'Glarus', 'JU':'Jura', 'ZG':'Zug', 'OW':'Obwalden', 'FR':'Fribourg', 'SZ':'Schwyz',
                'AR':'Appenzell Ausserrhoden', 'AI':'Appenzell Innerrhoden', 'NW':'Nidwalden', 'BS':'Basel-Stadt'}

df['canton']= df['canton'].map(cantons_dict)


#inserting the 3 radio buttons

show_map = left_column.radio(
    label='Show major renewable energy sources by Canton', options=['No', 'Yes'])


show_whole_swiss= middle_column.radio(label='Show location of renewal energy plants', options=['No', 'Yes'])


show_analysis=right_column.radio(label='Show number of plant and plant capacity analysis by Energy Type',
                            options=['No', 'Yes'])


#importing geojson
#with open(r".\data\raw\georef-switzerland-kanton.geojson") as response:
#    swiss_cantons = json.load(response)
with open("./data/raw/georef-switzerland-kanton.geojson") as response:
    swiss_cantons = json.load(response)



#plotting first map
fig = px.choropleth_mapbox(df,
                           geojson=swiss_cantons,
                           locations='canton',
                           featureidkey="properties.kan_name",
                           color="energy_source_level_2",
                           
                           labels={'energy_source_level_2': "Renewal Energy Source"},
                           title='Major Renewal Energy Source by Canton',
                           center={'lat':47.3769, 'lon':8.5417},
                           mapbox_style="carto-positron",
                           zoom=6)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


if show_map == "Yes":
    st.plotly_chart(fig)
else:
    ""

#plot second map in middle column

fig_scattermap = px.scatter_mapbox(df,
                       color="energy_source_level_2", title="Location of energy source",
                       lat = 'lat',
                       lon= 'lon',
                       labels={'energy_source_level_2':'Renewal Energy Source'},
                       zoom=7,
                       height=1000)

fig_scattermap.update_layout(mapbox_style="open-street-map")

if show_whole_swiss == "Yes":
    st.plotly_chart(fig_scattermap)
else:
    ""

#show analysis in right column
capacity = df.groupby('energy_source_level_2').electrical_capacity.sum().reset_index()
fig3 = px.bar(capacity, x='energy_source_level_2', y='electrical_capacity', title="Electrical capacity by energy source",
             labels={'energy_source_level_2':'Renewable Energy Source',
                    'electrical_capacity': "Capacity of Source"})

number_plants = df['energy_source_level_2'].value_counts().reset_index()
fig4 = px.bar(number_plants, x='index', y='energy_source_level_2', title="Number of plants by energy source",
             labels={'energy_source_level_2':'Renewable Energy Source',
                    'index': "Number of plants"})
if show_analysis == "Yes":
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)

else:
    ""
