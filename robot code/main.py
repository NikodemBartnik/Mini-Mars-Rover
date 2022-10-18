import network, socket, time
from machine import Pin, PWM

SERVO_CALIBRATION_VALUE = 0.60


led = Pin("LED", Pin.OUT)
camera_pin = Pin(3, Pin.OUT)
drv1_in1 = Pin(5, Pin.OUT)
drv1_in2 = Pin(6, Pin.OUT)
drv1_in3 = Pin(7, Pin.OUT)
drv1_in4 = Pin(8, Pin.OUT)
drv2_in1 = Pin(11, Pin.OUT)
drv2_in2 = Pin(12, Pin.OUT)
drv2_in3 = Pin(13, Pin.OUT)
drv2_in4 = Pin(14, Pin.OUT)

camera_pin.value(0)


servo1 = PWM(Pin(21))
servo2 = PWM(Pin(22))
servo3 = PWM(Pin(26))
servo4 = PWM(Pin(27))
drv1_a = PWM(Pin(4))
drv1_b = PWM(Pin(9))
drv2_a = PWM(Pin(10))
drv2_b = PWM(Pin(15))


servo1.freq(50)
servo2.freq(50)
servo3.freq(50)
servo4.freq(50)
drv1_a.freq(50)
drv1_b.freq(50)
drv2_a.freq(50)
drv2_b.freq(50)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('TP-LINK_B71D9D', '87057850')
soc = socket.socket()
# Should be connected and have an IP address
#wlan.status() # 3 == success
#wlan.ifconfig()
time.sleep(5)
    
def servoSet(servo, duty):
    servo.duty_u16(int((1-SERVO_CALIBRATION_VALUE)*3277 + (duty/180) * 3277*(SERVO_CALIBRATION_VALUE+1)))
    
#duty form 0 to 1
#M1 front right, 1 - backwards, 0 - forward
#M2 back right, 1- backwards, 0 - forward
#M3 front left, 1- backwards, 0 - forward
#M4 back left, 1- backwards, 0 - forward
def setMotor(motor, dir, duty):
    if motor is 1:
        drv1_in1.value(dir)
        drv1_in2.value(not dir)
        drv1_a.duty_u16(int(65536 * duty))
    elif motor is 2:
        drv1_in3.value(dir)
        drv1_in4.value(not dir)
        drv1_b.duty_u16(int(65536 * duty))
    elif motor is 3:
        drv2_in1.value(not dir)
        drv2_in2.value(dir)
        drv2_a.duty_u16(int(65536 * duty))
    elif motor is 4:
        drv2_in3.value(not dir)
        drv2_in4.value(dir)
        drv2_b.duty_u16(int(65536 * duty))
    
def drive(value, power):
    print(power)
    if value < 120 and value > 60:
        setMotor(1, 0, power)
        setMotor(2, 0, power)
        setMotor(3, 0, power)
        setMotor(4, 0, power)
    elif value < 210 and value > 150:
        setMotor(1, 0, power)
        setMotor(2, 1, power)
        setMotor(3, 1, power)
        setMotor(4, 0, power)
    elif value > 330 or value < 30:
        setMotor(1, 1, power)
        setMotor(2, 0, power)
        setMotor(3, 0, power)
        setMotor(4, 1, power)
    elif value < 300 and value > 240:
        setMotor(1, 1, power)
        setMotor(2, 1, power)
        setMotor(3, 1, power)
        setMotor(4, 1, power)
        
        
def turn(direction):
    if direction:
        setMotor(1, 0, 0.7)
        setMotor(2, 0, 0.7)
        setMotor(3, 1, 0.7)
        setMotor(4, 1, 0.7)
    else:
        setMotor(1, 1, 0.7)
        setMotor(2, 1, 0.7)
        setMotor(3, 0, 0.7)
        setMotor(4, 0, 0.7)
    
def stop():
    drv1_a.duty_u16(0)
    drv1_b.duty_u16(0)
    drv2_a.duty_u16(0)
    drv2_b.duty_u16(0)
    

soc.connect(("192.168.1.107", 12345))

while True:
    data = soc.readline()
    values = str(data,'utf8').strip().split(',')
    values = [int(x) for x in values]
    print(values, end='\n')
    servoSet(servo1, values[0]/10)
    servoSet(servo2, values[1]/10)
    servoSet(servo3, values[2]/10)
    servoSet(servo4, values[3]/10)
    
    
    if values[4] is -10:
        stop()
    else:
        drive(int(values[4]/10), values[5]/100)
        
    if values[7] is 1:
        turn(1)
    elif values[7] is 2:
        turn(0)
        
    
    if values[6] is 1:
        camera_pin.value(1)
        led.value(1)
    else:
        camera_pin.value(0)
        led.value(0)

    
    #s.send('hello')
