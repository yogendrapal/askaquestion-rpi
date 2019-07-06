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
