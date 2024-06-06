import streamlit as st
import json
from copy import deepcopy
import math
import os

st.set_page_config(layout="wide")

def rotate_point(point, ang_in_radian, origin=(0, 0)):
    """Rotate point around the defined origin"""

    x, y = point
    xo, yo = origin
    
    xc = x - xo
    yc = y - yo
    
    ang_sin = math.sin(ang_in_radian)
    ang_cos = math.cos(ang_in_radian)
    
    xr = xc*ang_cos - yc*ang_sin
    yr = xc*ang_sin + yc*ang_cos
    
    xr =  xr + xo  
    yr =  yr + yo
    
    return (xr, yr)


def process(data, angle=0, center=(0,0)):
    new_data = deepcopy(data)
    # rotate points
    new_points = []
    for p in data['geometry']['points']:
        pr = rotate_point((p['x'], p['y']), -angle, origin=center)
        new_points.append({'id': p['id'], 'x': pr[0], 'y': pr[1]})
    new_data['geometry']['points'] = new_points
    
    # add wall length
    # !TODO
    
    return new_data

def main():
    st.title("Process JSON RoomSketcher")
    col1,col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader("Choose a JSON file", type="json")
    with col2:
        col2_1, col2_2, col2_3 = st.columns(3)
        with col2_1:
            x = st.number_input('x offset:', value=None)
            process_button = st.button('Process')
        with col2_2:
            y = st.number_input('y offset:', value=None)
        with col2_3:
            angle = st.number_input('rotate angle:', value=None)
            
    
    if process_button  and (uploaded_file is not None) :
        # Read the JSON file
        data = json.load(uploaded_file)

        # Process the JSON data
        processed_data = process(data, angle=angle, center=(x,y))

        # Convert processed data back to JSON
        processed_json = json.dumps(processed_data, indent=4)

        with col2:
            with col2_2:
                n,e = os.path.splitext(uploaded_file.name)
                down_name = f'{n}_qa.json'
                # Create a download button
                st.download_button(
                    label=":printer: Download Processed JSON",
                    data=processed_json,
                    file_name=down_name,
                    mime="application/json"
                )
        
        with col1:     
            # st.write("Original JSON:")
            st.json(data, expanded=True)
        with col2:
            st.write("Processed JSON:")
            
            st.json(processed_data, expanded=True)

if __name__ == "__main__":
    main()
