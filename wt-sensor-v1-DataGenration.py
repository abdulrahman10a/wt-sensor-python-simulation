
# In[1]:


import struct
import socket
import time 


# In[32]:



    
## read data from file
ax_file = open(r"data\dataset\train\signals\total_acc_x_train.txt", "r")
ay_file = open(r"data\dataset\train\signals\total_acc_y_train.txt", "r")   
az_file = open(r"data\dataset\train\signals\total_acc_z_train.txt", "r")
gx_file = open(r"data\dataset\train\signals\body_gyro_x_train.txt", "r")
gy_file = open(r"data\dataset\train\signals\body_gyro_y_train.txt", "r")
gz_file = open(r"data\dataset\train\signals\body_gyro_z_train.txt", "r")

## read ax data full file 
ax_lines = ax_file.readlines()
ax_data=[]
for x in range (len(ax_lines)):
    z = ax_lines[x].replace('nan','0').strip().split(',')
    for n in range (810):
        ax_data.append(int(float(z[n])))
    ax_data.append(int(float(z[809]))) # repeat the last value 
ax_file.close()

## read ay data full file 
ay_lines = ay_file.readlines()
ay_data=[]
for x in range (len(ay_lines)):
    z = ay_lines[x].replace('nan','0').strip().split(',')
    for n in range (810):
        ay_data.append(int(float(z[n])))
    ay_data.append(int(float(z[809]))) # repeat the last value 
ay_file.close()

## read az data full file 
az_lines = az_file.readlines()
az_data=[]
for x in range (len(az_lines)):
    z = az_lines[x].replace('nan','0').strip().split(',')
    for n in range (810):
        az_data.append(int(float(z[n])))
    az_data.append(int(float(z[809]))) # repeat the last value 
az_file.close()

## read gx data full file 
gx_lines = gx_file.readlines()
gx_data=[]
for x in range (len(gx_lines)):
    z = gx_lines[x].replace('nan','0').strip().split(',')
    for n in range (810):
        gx_data.append(int(float(z[n])))
    gx_data.append(int(float(z[809]))) # repeat the last value 
gx_file.close()

## read gy data full file 
gy_lines = gy_file.readlines()
gy_data=[]
for x in range (len(gy_lines)):
    z = gy_lines[x].replace('nan','0').strip().split(',')
    for n in range (810):
        gy_data.append(int(float(z[n])))
    gy_data.append(int(float(z[809]))) # repeat the last value 
gy_file.close()

## read gz data full file 
gz_lines = gz_file.readlines()
gz_data=[]
for x in range (len(gz_lines)):
    z = gz_lines[x].replace('nan','0').strip().split(',')
    for n in range (810):
        gz_data.append(int(float(z[n])))
    gz_data.append(int(float(z[809]))) # repeat the last value 
gz_file.close()


# In[61]:


# packet structer (big-endian) first packet

# cut the mac to bytes and sprate them
mac = "ffffffffffaf"
macSplit = []
full_pack = []
n = 0 
for x in range(6):
    tem = int(mac[n:n+2], 16)
    #print (mac[i:i+2])
    macSplit.append (tem)
    n = n + 2
time_unix_int = int(round(time.time()))

#chouse the data line form the data file (frst line is zero)
line = 5
i = 811 * line
for mass in range (7):
    mac = struct.pack('>BBBBBB', macSplit[0],macSplit[1],macSplit[2],macSplit[3],macSplit[4],macSplit[5]) #pack mac 
    pack_number = struct.pack('>B', mass + 1) # pack packet number
    pack_total = struct.pack('>B', 7) # pack the total number of packets
   
    ## gyro data
    ax = b''  
    ay = b'' 
    az = b'' 
    gx = b'' 
    gy = b'' 
    gz = b''
    gyro_data= b''

    # pack the data in the packets 
    for x in range (116):
        if (mass < 1):
            if(x<115):
                ax = struct.pack('>h', ax_data[i])
                ay = struct.pack('>h', ay_data[i])
                az = struct.pack('>h', az_data[i])

                gx = struct.pack('>h', gx_data[i])
                gy = struct.pack('>h', gy_data[i])
                gz = struct.pack('>h', gz_data[i])
                i=i+1
                gyro_data += ax + ay + az + gx + gy + gz
            else:
                temp = struct.pack('>H', 2)
                hum = struct.pack('>H', 2)
                case_temp = struct.pack('>H', 2)
                batray = struct.pack('>H', 2)
                sound = struct.pack('>H', 2)
                time_unix = struct.pack('>I', time_unix_int) ## note which is better B of H
                i=i+1
        else:
            ax = struct.pack('>h', ax_data[i])
            ay = struct.pack('>h', ay_data[i])
            az = struct.pack('>h', az_data[i])

            gx = struct.pack('>h', gx_data[i])
            gy = struct.pack('>h', gy_data[i])
            gz = struct.pack('>h', gz_data[i])
            i=i+1
            gyro_data += ax + ay + az + gx + gy + gz
            
    # construct the full massge   
    if (mass<1):
        full_pack.append( mac + pack_number + pack_total + gyro_data + hum + temp +  case_temp + sound +  batray + time_unix)
    else:
        full_pack.append( mac + pack_number + pack_total + gyro_data )
        
        


#client
import socket

#IPADDR = '10.40.0.19'
IPADDR = '10.40.0.54'
PORTNUM = 2000


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

s.connect((IPADDR, PORTNUM))
print ("connected")

# send the sven packets 
for x in range (7):
    PACKETDATA = full_pack[x]
    s.send(PACKETDATA)
    
s.close()


# In[46]:


len(full_pack[0])





