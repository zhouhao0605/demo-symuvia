# Demo on SymuVia API 

This demo is an example on how to access the `SymuVia` API from the basics. The structure contains two folders: `darwin`  for MacOS and `windows` for windows platforms. 

## Loading `SymuVia` in Python

In python execute. 

In MacOS

```python
from ctypes import cdll 
simulator = cdll.LoadLibrary('darwin/libSymuVia.dylib')  # load simulator
```

In Windows 

```python
from ctypes import cdll 
simulator = cdll.LoadLibrary('windows\SymuVia.dll')  # load simulator
```


## Running a simulation in a single step 

To launch the simulation, load the XML file into the simulator via `SymLoadNetworkEx`, then play the simulation via `SymRunEx`:

```python
simulator.SymLoadNetworkEx('bottleneck_001.xml'.encode('UTF8')) # load simulation into simulator 
simulator.SymRunEx('bottleneck_001.xml'.encode('UTF8')) # run this file 
```
## Running a simulation step by step 

Please find more details on this within the Jupyter Notebook [Basics_API.ipynb](Basics_API.ipynb)
