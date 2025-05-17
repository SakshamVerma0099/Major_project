import airsim
import math
import numpy as np
import cv2
import os
import time
import base64
from PIL import Image, ImageTk
import openai
import os
import cv2
import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
# runner.py
import subprocess



client = airsim.MultirotorClient()
version = client.getServerVersion()
print("AirSim version:", version)
objects_dict = {
    "chair one": "Chair",
    "chair two": "Chair_15",
    "statue": "statue",
    "Table": "Table",
}

class AirSimWrapper:
    
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)

    def takeoff(self):
        self.client.takeoffAsync().join()

    def land(self):
        self.client.landAsync().join()

    def get_drone_position(self):
        
        pose = self.client.simGetVehiclePose()
       
        return [pose.position.x_val, pose.position.y_val, pose.position.z_val]

    def fly_to(self, point):
        
           if point[2] > 0:
            self.client.moveToPositionAsync(point[0], point[1], -point[2], 5).join()
            print("point[2] > 0")
           else:
            self.client.moveToPositionAsync(point[0], point[1], point[2], 5).join()
            print("else")

    def fly_path(self, points):
        airsim_points = []
        for point in points:
            if point[2] > 0:
                airsim_points.append(airsim.Vector3r(point[0], point[1], -point[2]))
            else:
                airsim_points.append(airsim.Vector3r(point[0], point[1], point[2]))
        self.client.moveOnPathAsync(airsim_points, 5, 120, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False, 0), 20, 1).join()

    def set_yaw(self, yaw):
        self.client.rotateToYawAsync(yaw, 5).join()

    def get_yaw(self):
        orientation_quat = self.client.simGetVehiclePose().orientation
        yaw = airsim.to_eularian_angles(orientation_quat)[2]
        return yaw

    def get_position(self, object_name):
        query_string = objects_dict[object_name] + ".*"
        object_names_ue = []
        while len(object_names_ue) == 0:
            object_names_ue = self.client.simListSceneObjects(query_string)
        pose = self.client.simGetObjectPose(object_names_ue[0])
        return [pose.position.x_val, pose.position.y_val, pose.position.z_val] 

    def take_picture(self, image_filename="picture.png"):
        # Capture a single picture
        responses = self.client.simGetImages([airsim.ImageRequest(0, airsim.ImageType.Scene, False, False)])
        image = np.frombuffer(responses[0].image_data_uint8, dtype=np.uint8)
        image = image.reshape(responses[0].height, responses[0].width, 3)
        

        # Save the image
        image_path = os.path.join("C:\\class work\\NLP\\codes\\pictures\\", image_filename)
        cv2.imwrite(image_path, image)
        print(f"Image saved at {image_path}")  
        os.system("start python test_picture_detail.py")

    def move_forward(self, distance):
        """Move the drone forward."""
        velocity=1
        duration=distance/velocity
        self.client.moveByVelocityAsync(velocity, 0, 0, duration).join()
        self.client.hoverAsync().join()
        time.sleep(2)
        

    def move_backward(self,distance):
        """Move the drone backward."""
        velocity=1
        duration=distance/velocity
        self.client.moveByVelocityAsync(-velocity, 0, 0, duration).join()
        self.client.hoverAsync().join()
        time.sleep(2)
   

    def move_right(self, distance):
        """Move the drone to the right."""
        velocity=1
        duration=distance/velocity
        self.client.moveByVelocityAsync(0, velocity, 0, duration).join()
        self.client.hoverAsync().join()
        time.sleep(2)


    def move_left(self, distance):
        """Move the drone to the left."""
        velocity=1
        duration=distance/velocity
        self.client.moveByVelocityAsync(0, -velocity, 0, duration).join()
        self.client.hoverAsync().join()
        time.sleep(2)
  

    def move_up(self,distance):
        """Move the drone upwards."""
        velocity=1
        duration=distance/velocity
        self.client.moveByVelocityAsync(0, 0, velocity, duration).join()
        self.client.hoverAsync().join()
        time.sleep(2)
      

    def move_down(self, distance):
        """Move the drone downwards."""
        velocity=1
        duration=distance/velocity
        self.client.moveByVelocityAsync(0, 0, -velocity, duration).join()
        self.client.hoverAsync().join()
        time.sleep(2)
           