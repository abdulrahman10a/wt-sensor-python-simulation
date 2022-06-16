

# In[1]:


import struct
import socket


# In[86]:


# server

# to get the IP of the running devise
localIP = "10.40.0.54"
#print (localIP)
localPort = 2000

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

## gyro data
ax = [] 
ay = [] 
az = [] 
gx = [] 
gy = [] 
gz = []
packet_list = []

running = 1 
while running:
    # for receving the packet
    packet = UDPServerSocket.recv(10000)
    
    pack_number = packet[6] # one-byte packet number 
    pack_total =  packet[7] # one-byte packet total number 
    
    packet_list.append(pack_number)
   
    
    if (pack_number == 1): # first pack 1402 bytes 
        
        # get the mac addres and convet it back to string
        mac_bytes = packet[:6]
        mac_int = struct.unpack('>BBBBBB', mac_bytes)
        mac = ""
        for x in range(6):
            tem = hex(mac_int[x])
            mac += tem[2:]
        print ("MAC address >> ", mac)
        
        ## get data for the fist packet
        offcet = 8
        for n in range (115):
            # the gyro. data for the first packet (sined)
            ax.append (struct.unpack('>h',packet[offcet + 0 + 6 * n * 2 : offcet + 0 + 6 * n * 2 + 2 ]))
            ay.append (struct.unpack('>h',packet[offcet + 2 + 6 * n * 2 : offcet + 2 + 6 * n * 2 + 2]))
            az.append (struct.unpack('>h',packet[offcet + 4 + 6 * n * 2 : offcet + 4 + 6 * n * 2 + 2 ]))
            gx.append (struct.unpack('>h',packet[offcet + 6 + 6 * n * 2 : offcet + 6 + 6 * n * 2 + 2]))
            gy.append (struct.unpack('>h',packet[offcet + 8 + 6 * n * 2 : offcet + 8 + 6 * n * 2 + 2]))
            gz.append (struct.unpack('>h',packet[offcet + 10 + 6 * n * 2 : offcet + 10 + 6 * n * 2 + 2 ]))
       
        # fist packet state data (unsined)
        temp = struct.unpack('>H', packet[1388:1390])
        hum = struct.unpack('>H', packet[1390:1392])
        case_temp = struct.unpack('>H', packet[1392:1394])
        batray = struct.unpack('>H', packet[1394:1396])
        sound = struct.unpack('>H', packet[1396:1398])
        time_unix = struct.unpack('>I', packet[1398:1402])      
        
        
    else:
        mac_bytes_check = packet[:6] # mac for the next packets
        if (mac_bytes != mac_bytes_check):# detect packet enjection
            print("packet with defrant MAC")
            UDPServerSocket.close()
            running = 0 
         ## get the date for packet 2-7   
        for n in range (116):
            ax.append (struct.unpack('>h',packet[offcet + 0 + 6 * n * 2 : offcet + 0 + 6 * n * 2 + 2 ]))
            ay.append (struct.unpack('>h',packet[offcet + 2 + 6 * n * 2 : offcet + 2 + 6 * n * 2 + 2]))
            az.append (struct.unpack('>h',packet[offcet + 4 + 6 * n * 2 : offcet + 4 + 6 * n * 2 + 2 ]))
            gx.append (struct.unpack('>h',packet[offcet + 6 + 6 * n * 2 : offcet + 6 + 6 * n * 2 + 2]))
            gy.append (struct.unpack('>h',packet[offcet + 8 + 6 * n * 2 : offcet + 8 + 6 * n * 2 + 2]))
            gz.append (struct.unpack('>h',packet[offcet + 10 + 6 * n * 2 : offcet + 10 + 6 * n * 2 + 2 ]))
        

        
    # got all the packets 
    if (pack_number == 7 ):
        print ("successed")
        
        # remove the tupels    
        ax = [item for t in ax for item in t]
        ay = [item for t in ay for item in t]
        az = [item for t in az for item in t]
        gx = [item for t in gx for item in t]
        gy = [item for t in gy for item in t]
        gz = [item for t in gz for item in t]
        temp = temp[0]
        hum = hum[0]
        case_temp = case_temp[0]
        batray = batray[0]
        sound = sound[0]
        
        time_unix = time_unix[0]
        
        UDPServerSocket.close()
        running = 0
        
print (packet_list)

# show the graphs
'''
import numpy as np
from numpy import *
from matplotlib import pyplot as plt
from scipy.fft import *

N = 810
# sample spacing
T = 1.0 / 810.0

# Number of samplepoints(ax)
x = np.array(ax)
yf = fft(x)
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
fig, axx = plt.subplots()
axx.plot(xf[1:], 2.0/N * np.abs(yf[1:N//2]))
plt.xlabel("ax graph")

# Number of samplepoints(ay)

x = np.array(ay)
yf = fft(x)
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
fig, ayy = plt.subplots()
ayy.plot(xf[1:], 2.0/N * np.abs(yf[1:N//2]))
plt.xlabel ("ay graph")

# Number of samplepoints(az)
x = np.array(az)
yf = fft(x)
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
fig, azz = plt.subplots()
azz.plot(xf[1:], 2.0/N * np.abs(yf[1:N//2]))
plt.xlabel ("az graph")

# Number of samplepoints(gx)
x = np.array(gx)
yf = fft(x)
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
fig, gxx = plt.subplots()
gxx.plot(xf[1:], 2.0/N * np.abs(yf[1:N//2]))
plt.xlabel ("gx graph")

# Number of samplepoints(gy)
x = np.array(gy)
yf = fft(x)
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
fig, gyy = plt.subplots()
gyy.plot(xf[1:], 2.0/N * np.abs(yf[1:N//2]))
plt.xlabel ("gy graph")

# Number of samplepoints(gz)
x = np.array(gz)
yf = fft(x)
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
fig, gzz = plt.subplots()
gzz.plot(xf[1:], 2.0/N * np.abs(yf[1:N//2]))
plt.xlabel ("gz graph")


'''


