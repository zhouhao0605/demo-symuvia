from ctypes import cdll
import os

simulator_location = ("darwin", "libSymuVia.dylib")
simulator_path = os.path.join(os.getcwd(), *simulator_location)
print(f"Simulation location: {simulator_path}")


xml_location = "botleneck_001.xml"
xml_path = os.path.join(os.getcwd(), xml_location)
print(f"XML location: {xml_path}")

simulator = cdll.LoadLibrary(simulator_path)
simulator.SymLoadNetworkEx(xml_path.encode("UTF8"))
simulator.SymRunEx(xml_path.encode("UTF8"))
