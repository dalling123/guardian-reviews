import requests
from datetime import datetime
import pandas as pd
import streamlit as st

# API CALL TO GUARIDAN / SAVE RESPONSE AS PYTHON DICT
my_key = st.secrets["guardian_api"]
url = f"https://content.guardianapis.com/search?&api-key={my_key}&section=film|tv-and-radio&star-rating=5&page=1&page-size=7&show-fields=headline,trailText,starRating,thumbnail"
response = requests.get(url)
resp = response.json()

# grab first 7 films/series 
items = resp['response']['results'][:8]

# helper methods
def extract_title(text):
    return text.split('review')[0].strip()

def extract_date(date_str):
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return dt.strftime("%d %b").lstrip("0")

def image_prep(image_url):
    str = f'<img src={image_url}>'
    return str

# create a new dict to hold data for table and populate it in for loop
top_7 = {}
count = 1

for x in items:

    top_7[count] = {
        "title" : extract_title(x['webTitle']),
        "thumbnail" : x["fields"]["thumbnail"],
        "link" : x["webUrl"],
        "trailText" : x["fields"]["trailText"],
        "date" : extract_date(x['webPublicationDate']),
        "type" : "film" if x["sectionId"] == 'film' else 'series',
        "star" : "⭐⭐⭐⭐⭐"
    }
    count += 1

# FIRST STREAMLIT CALL OF SCRIPT. ALLOWS FULL BROWSER WIDTH 
st.set_page_config(layout="wide")

# UI
st.header("Guardian 5-Star Reviews - Film & TV")
st.header("")

for x in top_7:
    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns(spec=[2,1.5,2.5,0.75,0.75,1], vertical_alignment='center')
        with col1:
            st.subheader(top_7[x]['title'])
        with col2:
            st.image(top_7[x]['thumbnail'], link=top_7[x]['link'])
        with col3:
            st.markdown(top_7[x]['trailText'])
        with col4:
            st.markdown(top_7[x]['date'])
        with col5:
            st.markdown(top_7[x]['type'])
        with col6:
            st.markdown(top_7[x]['star'])
    st.divider()

st.markdown("Find above the 7x most recent 5-star rated titles from the Guardian. Click image to navigate to article.")