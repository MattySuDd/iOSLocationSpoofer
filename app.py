import requests
import polyline
import time
import subprocess
import threading
import json
import os
from dotenv import load_dotenv

import webview

stop_sim_boolean = False

# get api key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

class API:
    def checkConnection(self):
        print("Checking connection")
        response = subprocess.run(["powershell", "pymobiledevice3 usbmux list"], capture_output=True, text=True)
        data = json.loads(response.stdout)
        print(data)
        if len(data) == 0:
            print("No device found")
            return False
        else:
            # check if all devices in the array have connectionType = USB
            count = 0
            for device in data:
                print(device)
                print(device["ConnectionType"])
                if device["ConnectionType"] != "USB":
                    print("No device found")
                count += 1
            if count == 0:
                return False
            else:
                return True
        
    def get_speeds(self, start,end):
        if not self.checkConnection():
            return "No device found"
        
        start_location = start
        end_location = end

        if not start_location or not end_location:
            return print("Please provide start and end locations")

        # Switch lat and lon
        start_location = [start_location[1], start_location[0]]
        end_location = [end_location[1], end_location[0]]

        response = requests.post("https://api.openrouteservice.org/v2/directions/driving-car", headers={
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
            "Authorization": API_KEY
        }, json={
            "coordinates": [start_location, end_location],
            "attributes": ["avgspeed"],
            "geometry_simplify": "false"
        })

        if response.status_code != 200:
            return print(f"Error: {response.status_code}")

        print("Route retrieved")
        data = response.json()
        
        # Extract the encoded polyline
        encoded_polyline = data["routes"][0]["geometry"]
        coordinates = polyline.decode(encoded_polyline)  # Decoded list of (lat, lon)

        # List to store speeds with coordinates
        speeds_per_coordinate = []
        
        # Iterate over steps to calculate average speeds
        for segment in data["routes"][0]["segments"]:
            for step in segment["steps"]:
                # Extract the distance and duration for each step
                distance = step["distance"]
                duration = step["duration"]
                print(f"Distance: {distance} m, Duration: {duration} s")
                if duration == 0:
                    continue

                # Calculate the average speed (in km/h)
                avg_speed_kmh = (distance / 1000) / (duration / 3600)
                
                # Now, assign the calculated speed to all coordinates between waypoints
                for i in range(len(step["way_points"]) - 1):
                    start_idx = step["way_points"][i]
                    end_idx = step["way_points"][i + 1]
                    
                    # Get all coordinates between start_idx and end_idx (inclusive)
                    for j in range(start_idx, end_idx + 1):
                        coord = coordinates[j]
                        speeds_per_coordinate.append((coord, avg_speed_kmh))
        
        # Debug: print the calculated speeds for coordinates
        for coord, speed in speeds_per_coordinate:
            print(f"Coordinate: {coord}, Average Speed: {speed} km/h")

        # Start a new thread to simulate the journey
        threading.Thread(target=self.simulateJourney, args=(speeds_per_coordinate,)).start()
        
        return speeds_per_coordinate



    def stop_simulation(self):
        global stop_sim_boolean
        #  destroy thread
        stop_sim_boolean = True
        return "Simulation stopped"


    def simulateJourney(self, speeds_per_coordinate):
        global stop_sim_boolean
        # Use speeds_per_coordinate to simulate movement
        # start timer
        start_time = time.time()
        for coord, speed in speeds_per_coordinate:
            print (f"stop_simulation: {stop_sim_boolean}")
            if stop_sim_boolean:
                stop_sim_boolean = False
                break
            # run this and also check how long it takes to run: subprocess.run(["powershell", f"pymobiledevice3 developer simulate-location set -- {coord[0]} {coord[1]}"])
            start_process_time = time.time()
            subprocess.run(["powershell", f"pymobiledevice3 developer simulate-location set -- {coord[0]} {coord[1]}"])
            end_process_time = time.time()
            print(f"Process took {end_process_time - start_process_time} seconds")
            
            # Wait depending on the speed (simulate movement time)
            print (f"delaying for {1 / (speed / 60)} seconds")
            time.sleep(1 / (speed / 60))  # Speed in km/h, sleep time adjusted
        end_time = time.time()
        print(f"Simulation took {end_time - start_time} seconds")
        
    def set_location(self, coord):
        if not self.checkConnection():
            return "No device found"
        subprocess.run(["powershell", f"pymobiledevice3 developer simulate-location set -- {coord[0]} {coord[1]}"])
        return "Location set"
 

api = API()
webview.create_window("IOS Location Changer", "index.html", width=800, height=600, js_api= api)
webview.start(icon='favicon.ico')
# webview.start(icon='favicon.ico', debug=True) # to enable debug mode