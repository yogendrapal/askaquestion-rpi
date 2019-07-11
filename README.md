# askaquestion-rpi
A hardware prototype based on Raspberry Pi to ask a question


## Requirements on RaspberryPi
- FFMPEG
- Python 3.x
- Linux OS
- OpenCV
- dlib
- face_recognition
- shortuuid
- Tkinter
- python-vlc
- requests_toolbelt

For Installation instructions of dlib and face_recognition, refer,
[https://github.com/ageitgey/face_recognition](https://github.com/ageitgey/face_recognition)


## Requirements for Spring-Boot-RestAPI
- Java JDK
- MongoDB


## Usage - Command Line Operation
Use the following command to run in the CLI mode,

```
python3 main_cli.py
```

## Usage - GUI Mode (on raspberry pi)
When running on the raspberry pi, check that in `config.py`,

```python
RPI = True
```

and start the program using,

```
python3 main_rpi.py
```

## Usage - GUI Mode (on a computer with no GPIO)
When you are not on raspberry pi, You need an additional library, `keyboard`

To install, use the following command,

```
pip3 install keyboard
```

then check that in `config.py`,

```python
RPI = False
```

and start the program using,

```
sudo python3 main_rpi.py
```

## To connect to the device via SSH
You need to be on the same local network as the Raspberry Pi device. Then, you can check the IP Address of the device by `Long Pressing the Sync Button` , suppose the IP Address is `192.168.43.149`, then ssh can be done using the following command

```
ssh pi@192.168.43.149
```
When prompted for password, enter `rpi` as the password.

NOTE: Press `CTRL + C` immediately to stop the device from trying to auto-start the gui program in terminal.


## To reset the device
To delete existing database, face encodings and saved question & answers from the device, run
```
python3 reset.py
```
