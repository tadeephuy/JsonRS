import streamlit as st
import json
from copy import deepcopy
import math
import os

st.set_page_config(layout="wide")

def rotate_point_reverse(point, angle, center):
    x,y = point
    xc,yc = center
    
    x = x - xc
    y = y - yc
    
    x = x*math.cos(-angle) - y*math.sin(-angle)
    y = x*math.sin(-angle) + y*math.cos(-angle)
    
    x = round(x + xc, 0)
    y = round(y + yc, 0)
    return (x,y)

def get_wall_vector(wall_id, data):
        for wall in data['walls']:
            if wall['id'] == wall_id:
                start_point = [p for p in data['points'] if p['id'] == wall['start']][0]
                end_point = [p for p in data['points'] if p['id'] == wall['end']][0]
                return (end_point['x'] - start_point['x'], end_point['y'] - start_point['y'])
        return (0, 0)

def get_length(wall_id, data):
    vector = get_wall_vector(wall_id, data)
    # print(vector)
    return math.sqrt(vector[0]**2 + vector[1]**2)

def process(data, angle=0, center=(0,0)):
    new_data = deepcopy(data)
    # rotate points
    new_points = []
    for p in data['geometry']['points']:
        pr = rotate_point_reverse((p['x'], p['y']), angle=angle, center=center)
        new_points.append({'id': p['id'], 'x': pr[0], 'y': pr[1]})
    new_data['geometry']['points'] = new_points
    
    # add wall length
    geometry = new_data['geometry']

    for item in new_data['geometry']['walls']:
        length = get_length(item['id'], geometry)
        item['length'] = length
        
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
