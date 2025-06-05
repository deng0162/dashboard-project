import streamlit as st
import os
from PIL import Image

# Set the page title
st.title("Interactive Chart Viewer")
st.markdown("Use the dropdowns below to explore charts by region, country, industry, or SDG/BBK topic.")

# Base directory where your image folders are located
base_dir = "/home/acct/schaf/team/yiyid/projects/data_vit/Outfiles"

# Folder options for dropdown
folder_options = {
    "Region": "region_combo_charts",
    "Country": "country_combo_charts",
    "Industry": "industry_combo_charts",
    "SDG/BBK": "sdg_bbk_combo_charts"
}

# First dropdown: chart type
selected_folder_label = st.selectbox("Choose a chart type:", list(folder_options.keys()))
selected_folder = folder_options[selected_folder_label]

# Load image files from the selected folder
image_dir = os.path.join(base_dir, selected_folder)
image_files = sorted([f for f in os.listdir(image_dir) if f.endswith(".png")])

# Second dropdown: specific image
if image_files:
    selected_image = st.selectbox("Choose a chart:", image_files)
    image_path = os.path.join(image_dir, selected_image)
    image = Image.open(image_path)
    st.image(image, caption=selected_image, use_column_width=True)
else:
    st.warning("No images found in the selected folder.")
