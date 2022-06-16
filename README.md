# wt-sensor-v1 python simulation  
 this python code simulate the data exchange between the sensor (client) and the server. for that we have to make a python code that simulate that connection.
 
------------

## Client :
first the client read the gyroscope data from the file and save it on it receptive variables. After that it will protocol brake the UDP protocol construct the packet using 7 packet:

###### first packet : size 1402 bytes
* 0-5	mac
* 6  	packet number 8-bit int
* 7	    total number of packets 8-bit int 
* 8-1388    gyroscope data as (ax,ay,az,gx,gy,gz)
* 1388-1389     humidity  16-bit int
* 1390-1391     temperate   16-bit int
* 1392-1393     case temperate  16-bit int
* 1394-1395     battery  16-bit int
* 1396-1397     sound   16-bit int
* 1398 -1402    Time Unix   32-bit int

###### second to seventh packets: size 1400 bytes
* 0-5	mac
* 6  	packet number 8-bit int
* 7	    total number of packets 8-bit int 
* 8-1400    gyroscope data as (ax,ay,az,gx,gy,gz)

after constructing the packets it sends it to the server using UDP protocol and python socket

###### libraries used for client:
    
    import struct
    import socket
    import time
    
###### saving the data to the variables:
        
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
###### construct the massage:
this massage have have the seven packets organized as shown before the date use is the fist line in data files (if you want to change it change the variable [line] in the code to the line you want)

Note : in the futter it will otumaticly send all the lines in diffrant massages now it is only one massage with the first line

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
    line = 0
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
            
            


###### send massage (7 packets):
this code only send one massage that was constructed on the code before it only the first line of data at the moment

the IPADDR is the IP for the server and the port must be the same in the server and client

    #client
  
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

------------

## Server :

the server job is to receive the data form the client and deconstruct the packets. After that it graph the FFT for the gyro values 

###### libraries used for server:
        
        import struct
        import socket
        import numpy as np
        from numpy import *
        from matplotlib import pyplot as plt
        from scipy.fft import *
        
###### get the packet and deconstruct
    
Note : this code deconstruct one packet at a time and close the connection after that

the localIP is the IP for host device
    
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
        #print (packet[1389])
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
    
   ###### graph the data using FFT:
   
   on this code we use  Nyquist-theorem to show the data in frequency domain and form that data i can visually see the vibration on motor 
   
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
    

###### server output for (ax,ay,az,gx,gy,gz) :

![](ax.png)
![](ay.png) 
![](az.png)

![](gx.png)
![](gz.png)
![](gy.png)



