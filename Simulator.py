from tkinter import *
from time import sleep
import paho.mqtt.client as paho
import random
import time


master = Tk()
master.title('E-Well simulator')


client=paho.Client()
var=client.connect("broker.hivemq.com",1883)
client.loop_start()

WaterLevel=StringVar()
WaterLevel.set(0)
voltage = StringVar()
voltage.set(440)
WaterPressure = StringVar()
WaterPressure.set(0)
WaterFlowRate = StringVar()
WaterFlowRate.set(0)
Current = StringVar()
Current.set(0)
motorState = StringVar()
buttonstate=StringVar()


time1 = ''
motorStatus="0"
clock = Label(master, font=('times',1, 'bold'), bg='green')
clock.pack()
label1=Label(master,text="Water Level")
label1.pack()
w=Scale(master,from_=100,to=0,variable=WaterLevel)
w.pack()
label2=Label(master,text="Voltage")
label2.pack()
s = Spinbox(master, from_=1.0, to=440.0, textvariable=voltage)
s.pack()
label3=Label(master,text="Water Pressure")
label3.pack()
s = Spinbox(master, from_=1.0, to=50.0, textvariable=WaterPressure)
s.pack()
label4=Label(master,text="Water Flow Rate")
label4.pack()
s = Spinbox(master, from_=1.0, to=10.0, textvariable=WaterFlowRate)
s.pack()
label5=Label(master,text="Current")
label5.pack()
s = Spinbox(master, from_=1.0, to=50.0, textvariable=Current)
s.pack()
label7=Label(master,text="Motor Status")
label7.pack()
label6=Label(master,textvariable=motorState)
label6.pack()
def helloCallBack():
    global motorStatus
    if buttonstate.get()=="Stop":
        motorStatus="0"
        buttonstate.set("Start")
    elif buttonstate.get()=="Start":
        motorStatus="1"
        buttonstate.set("Stop")

  
    
        
b=Button(master,textvariable=buttonstate,command = helloCallBack)
b.pack()

def runningStatus(motorStatus):
    if motorStatus=="1":
        motorState.set("Started")
        buttonstate.set("Stop")
    elif motorStatus=="0":
        motorState.set("Stoped")
        buttonstate.set("Start")

def on_message(client, userdata, msg):
    global motorStatus, motorStatus
    motorStatus=msg.payload.decode("utf-8")
    print(motorStatus)
   
    
        
    
    
client.on_message = on_message
client.subscribe("E-well-control", qos=1)



def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    
    motorLoad=((int(voltage.get())*int(Current.get()))*0.75*1.75)/1000
    WaterStatus ="WaterStatus"+","+str(WaterLevel.get())+","+str(WaterPressure.get())+","+str(WaterFlowRate.get())
    MotorStatus = "MotorStatus"+","+motorStatus+","+str(voltage.get())+","+str("{0:0.2}".format(motorLoad,2))+","+str(Current.get())
    CircuitStatus ="CircuitStatus"+","+ str(random.randint(0,1))+","+str(random.randint(0,1))+","+str(random.randint(0,1))
    (rc, mid) = client.publish("E-well",str( "/"+WaterStatus+"/"+MotorStatus+"/"+CircuitStatus), qos=1)
    print("{0:0.2}".format(motorLoad,2))
    print(MotorStatus)
    runningStatus(motorStatus)
    clock.after(2000, tick)
tick()

mainloop() 
