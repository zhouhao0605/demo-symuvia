# from ctypes import cdll
# import os

# simulator_location = ("darwin", "libSymuVia.dylib")
# simulator_path = os.path.join(os.getcwd(), *simulator_location)
# print(f"Simulation location: {simulator_path}")


# xml_location = "botleneck_001.xml"
# xml_path = os.path.join(os.getcwd(), xml_location)
# print(f"XML location: {xml_path}")

# simulator = cdll.LoadLibrary(simulator_path)
# simulator.SymLoadNetworkEx(xml_path.encode("UTF8"))
# simulator.SymRunEx(xml_path.encode("UTF8"))

'''
For windows, I managed to implement the following test. 
'''
from ctypes import cdll
import os


os.chdir(r"D:\Projects\demo_symuvia\windows") #66, for windows, we need to change the working directory to this path

cwd = os.getcwd()
print('directory changed, and current directory is ', cwd)

print('load symuvia simulator')
simulator = cdll.LoadLibrary(r"D:\Projects\demo_symuvia\windows\SymuVia.dll")  # load simulator

print('load input network')
xml_file = os.path.join(r"D:\Projects\demo_symuvia\bottleneck_001.xml") # Absolute path of xml file # 66, a test xml input file
#66, for windows, it's better to use r"..." to give the raw string

print('the input xml file is', xml_file)
simulator.SymLoadNetworkEx(xml_file.encode('UTF8')) # load simulation into simulator
simulator.SymRunEx(xml_file.encode('UTF8')) #66 run this file

#66, looks like simulator is a loaded Symuvia object, we can call the functions in Symuvia like its attributes
simulator.SymLoadNetworkEx(xml_file.encode('UTF8')) # load simulation into simulator # 66, load the input xml file

print('run the experiment given the input file')
simulator.SymRunEx(xml_file.encode('UTF8')) # run this file
