# Demo on SymuVia API 

This demo is an example on how to access the `SymuVia` API from the basics. The structure contains two folders: `darwin`  for MacOS and `windows` for windows platforms.

The demo file [simulation_test.py](simulation_test.py) is a file containing necessary instructions to launch the script in a MacOS platform. In order to modify to windows just 
change the value `darwin` by `windows` and the value `libSymuVia.dylib` by `SymuVia.dll`

**Note**: Use absolute paths when importing the shared library.

## Loading `SymuVia` in Python

In python execute. 

In MacOS

```python
from ctypes import cdll 
simulator = cdll.LoadLibrary('your_mac_dir/demo-symuvia/darwin/libSymuVia.dylib')  # load simulator
```

Replace `your_mac_dir` for the absolute path to the directory where `demo-symuvia` is placed 

In Windows 

```python
from ctypes import cdll 
simulator = cdll.LoadLibrary('your_windows_dir\windows\SymuVia.dll')  # load simulator
```
Replace `your_windows_dir` for the absolute path to the directory where `demo-symuvia` is placed  

## Running a simulation in a single step 

To launch the simulation, load the XML file into the simulator via `SymLoadNetworkEx`, then play the simulation via `SymRunEx`:

```python
import os 
xml_file = os.path.join(os.getcwd(),'bottleneck_001.xml') # Absolute path of xml file 
print(xml_file)
simulator.SymLoadNetworkEx(xml_file.encode('UTF8')) # load simulation into simulator 
simulator.SymRunEx(xml_file.encode('UTF8')) # run this file 
```
## Running a simulation step by step 

Please find more details on this within the Jupyter Notebook [Basics_API.ipynb](Basics_API.ipynb)

## Note about `launcher.py` and `spydsla.py`

These files are dedicated to reconfigure the dependencies for shared libraries inside `darwin`. They are useful to import the library within python in MacOS, not in windows. 

Only in MacOSX 

If you get an error when doing `cdll.LoadLibrary('darwin/libSymuVia.dylib')`, try: 

1. Create a folder called `log` 
2. Install developer tools as `xcode-select --install`
3. In a terminal launch `python3 launcher.py`.
4. Start a python console and restart the procedure. 
