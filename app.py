# Brian Lesko 
# This is my first time rendering anything, cool
# 1/22/24
# Robotics Engineer

import streamlit as st
import pybullet as p
import pybullet_data as pd
import numpy as np
from PIL import Image
import customize_gui # streamlit GUI modifications
gui = customize_gui.gui()


def setupgui():
    # Set up the app UI
    gui.clean_format(wide=True)
    gui.about(text = "This code renders a simple cube in the physics engine called pybullet")
    Title, subTitle, Sidebar, image_spot = st.empty(), st.empty(), st.sidebar.empty(), st.columns([1,5,1])[1].empty()
    title = "<span style='font-size:30px;'>Pybullet Rendering and Simulation:</span>"
    with Title: st.markdown(f" {title} &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ", unsafe_allow_html=True)

setupgui() 

# Start PyBullet in DIRECT mode
p.connect(p.DIRECT)
p.setAdditionalSearchPath(pd.getDataPath())
p.loadURDF('plane.urdf')
p.loadURDF('cube_small.urdf', basePosition=[0.0, 0.0, 0.025])

with st.sidebar:
    st.title("Resolution")
    width = st.slider('width', 128, 1460, 512)
    height = width
    aspect = 1
    st.title("Camera Viewing Angle")
    x = st.slider('x', -1.0, 1.0, 0.44)
    y = st.slider('y', -1.0, 1.0, -0.32)
    z = st.slider('z', -1.0, 1.0, 0.33)
    fov = st.slider('fov', 1, 179, 60)
    st.write("Clipping planes do not render stuff outside the near-far range")
    near = st.slider('near', 0.0001, 2.0, 0.001)
    far = st.slider('far', 3, 10, 8)

# Camera setup
view_matrix = p.computeViewMatrix(cameraEyePosition=[x, y, z],
                                  cameraTargetPosition=[0, 0, 0],
                                  cameraUpVector=[0, 0, 1])
projection_matrix = p.computeProjectionMatrixFOV(fov, aspect, near, far)

# Capture image with OpenGL renderer
images = p.getCameraImage(width, height, view_matrix, projection_matrix, renderer=p.ER_BULLET_HARDWARE_OPENGL)
rgba_buffer_opengl = np.array(images[2], dtype=np.uint8)
rgba_opengl = np.reshape(rgba_buffer_opengl, (height, width, 4))

# Capture image with Tiny renderer
images = p.getCameraImage(width, height, view_matrix, projection_matrix, renderer=p.ER_TINY_RENDERER)
rgba_buffer_tiny = np.array(images[2], dtype=np.uint8)
rgba_tiny = np.reshape(rgba_buffer_tiny, (height, width, 4))

# Disconnect PyBullet
p.disconnect()

# Convert to RGB and normalize
rgb_opengl = rgba_opengl[:, :, :3]
rgb_tiny = rgba_tiny[:, :, :3]

# Create two columns
col1, col2 = st.columns(2)

# Convert to PIL images and display using Streamlit
col1.image(Image.fromarray(rgb_opengl), caption='OpenGL Renderer', use_column_width=True)
col2.image(Image.fromarray(rgb_tiny), caption='Tiny Renderer', use_column_width=True)
