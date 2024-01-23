# Brian Lesko 
# This is my second time rendering anything, cool
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

try: 
    p.disconnect()
    p.setPhysicsEngineParameter(enableFileCaching=1)
except:
    pass 

# Start PyBullet in DIRECT mode
p.connect(p.DIRECT)
p.setAdditionalSearchPath(pd.getDataPath())
p.loadURDF('plane.urdf')
table_pos = [0,0,-0.625]
flags = p.URDF_INITIALIZE_SAT_FEATURES
useFixedBase = True
xarm = p.loadURDF("xarm/xarm6_robot.urdf", flags = flags, useFixedBase=useFixedBase)

with st.sidebar:
    st.title("Resolution")
    width = st.slider('width', 128, 1460, 1080)
    height = width
    aspect = 1
    st.title("Camera Viewing Angle")
    x = st.slider('x', -1.0, 2.0, .8)
    y = st.slider('y', -1.0, 2.0, .9)
    z = st.slider('z', -1.0, 2.0, .6)
    fov = st.slider('fov', 1, 179, 60)
    st.write("Clipping planes do not render stuff outside the near-far range")
    near = st.slider('near', 0.0001, 2.0, 0.001)
    far = st.slider('far', 3, 10, 8)

# Camera setup
view_matrix = p.computeViewMatrix(cameraEyePosition=[x, y, z],
                                  cameraTargetPosition=[0, 0, .5],
                                  cameraUpVector=[0, 0, .5])
projection_matrix = p.computeProjectionMatrixFOV(fov, aspect, near, far)

col1, col2, col3 = st.columns([1,6,1])
with col2: image = st.empty()  

targetValue = 0.5
while True: 

    jointIndex = 1
    controlMode = p.POSITION_CONTROL
    targetValue = targetValue + 0.05
    p.setJointMotorControl2(bodyUniqueId=xarm, 
                        jointIndex=jointIndex, 
                        controlMode=controlMode, 
                        targetPosition=targetValue)
    
    p.stepSimulation()

    # Capture image with OpenGL renderer
    images = p.getCameraImage(width, height, view_matrix, projection_matrix, renderer=p.ER_BULLET_HARDWARE_OPENGL)
    rgba_buffer_opengl = np.array(images[2], dtype=np.uint8)
    rgba_opengl = np.reshape(rgba_buffer_opengl, (height, width, 4))

    rgb_opengl = rgba_opengl[:, :, :3]

    with image: st.image(Image.fromarray(rgb_opengl), caption='OpenGL Renderer', use_column_width=True)

# Capture image with Tiny renderer
# images = p.getCameraImage(width, height, view_matrix, projection_matrix, renderer=p.ER_TINY_RENDERER)
# rgba_buffer_tiny = np.array(images[2], dtype=np.uint8)
# rgba_tiny = np.reshape(rgba_buffer_tiny, (height, width, 4))
# rgb_tiny = rgba_tiny[:, :, :3]

# Disconnect PyBullet
p.disconnect()

# Convert to RGB and normalize
rgb_opengl = rgba_opengl[:, :, :3]

# Create two columns
col1, col2, col3 = st.columns([1,5,1])
col2.image(Image.fromarray(rgb_opengl), caption='OpenGL Renderer', use_column_width=True)
#col2.image(Image.fromarray(rgb_tiny), caption='Tiny Renderer', use_column_width=True)