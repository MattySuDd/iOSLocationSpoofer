
# iOS Location Spoofer

A python script able to change the location of any iOS device with the version lower than 17.0 with a sleek user interface using pywebview.



Features:
-
- Change location to a specific location
- Select 2 coordinates and simulate a car journey between the 2 using openrouteservice API for routing and average speed.




## Installation

Install requirements using pip or separately

```bash
  pip install -r requirements.txt

  or

  pip install polyline
  pip install python-dotenv
  pip install pywebview
  pip install Requests
```
You will also need an openrouteservice account for the free subscription of the directions API. (You will get enough credits for single use)
Simply sign up, go to your account page and there will be a "Basic Key", remove the .template from the .env file and add the basic key into the API_KEY variable.


Once this is done, just run 

```bash
  python app.py
```

and the application will open

! Make sure to have a device connected when you do either "start location" or "simulate journey" as the script checks if a device is connected before trying to run

## Screenshots

![image](https://github.com/user-attachments/assets/3a44fd69-2f98-423f-a032-86d7c072fbed)
![image](https://github.com/user-attachments/assets/f73feeab-e7f2-4318-9d16-b679b4256f4b)
![image](https://github.com/user-attachments/assets/91bc43c9-c8b1-4a78-ac0f-5cfe06448535)
![image](https://github.com/user-attachments/assets/4e650b56-ea48-41a4-bd4f-2fcb62089dce)
