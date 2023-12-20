
# Anti Sleep Alarm System

A system for a drowsy drivers. This project includes a Flask Server and an IOT Client.

## Installation

For installation first download this project to the necessary folder location. 

### Server

Open a terminal on the project directory and create a python virtual environment(venv) and run the venv.

```bash
  cd anti-sleeping-system
  py -3 -m venv .venv
  .venv\Scripts\activate
```

If done correctly, a you can see a ` (.venv)  ` at the beggining on your directory. Indicating that you are running the current directory with a virtual environment.

![App Screenshot](https://www.c-sharpcorner.com/article/steps-to-set-up-a-virtual-environment-for-python-development/Images/venv.png)

Now install necessary python Libraries from `requirements.txt`.
```bash
pip install -r requirements.txt
```

You can now run the server by running `app.py`.
```bash
py app.py
```  


### Client 

Start by oppening Arduino IDE. Go to `Tools` then select the `ESP32` Board. And from the list select `AI-Thinker ESP32-CAM`.

![App Screenshot](https://how2electronics.com/wp-content/uploads/2021/06/1x.png)

#### CameraWebServer
Go to the `Files` menu and then select `Examples`. From the examples menu, select the `ESP32` and then `Camera`. Then finally open the `CameraWebServer` Sketch.

![App Screenshot](https://how2electronics.com/wp-content/uploads/2021/06/2x.png)

On the repository you can find a client folder containing `CameraWebServer.ino` and `app_httpd.cpp` files. Copy the contents of this files and paste to change the contents to their example counterparts.


#### SocketIoClient Library
To install SocketIoClient Library. Go to `Sketch` > `Include Library` > `Manage Libraries` then install `SocketIoClient`

Open the **File Explorer** and locate the **SocketIoClient** of Arduino Library by navigating User's `Documents`>`Arduino`>`libraries`>`SocketIoClient`.

In the repository client folder theres a **SocketIoClient** folder with **two(2) files**. Copy files and paste to replace the files in **SocketIoClient Arduino Library**.