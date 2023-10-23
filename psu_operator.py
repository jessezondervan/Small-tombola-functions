#time to neaten up this package

#importing required python libraries
import pyvisa
import time
import types

#opening the resource manager within PyVisa
rm = pyvisa.ResourceManager()
print(rm.list_resources())
#from this list of resources, we can locate our desired device
#the string naming our device may vary

#this function connects to our given device
def open_supply():
    global power_supply
    power_supply = rm.open_resource('ASRL3::INSTR')


#this line can be used to query the serial number of the device, so we can check
#if we have chosen the correct one

#print(power_supply.query('*IDN?'))




#function to start the supply (and tombola)
def start_tombola():
    #engage over-current protection
    power_supply.write('OCP:ON')
    #recall function 'M2'
    power_supply.write('RCL:2')
    #set starting voltage to 4 V (minimum to spin the tombola)
    power_supply.write('VSET:4')
    #activate the output
    power_supply.write('OUT:1')

#function to 'warm up' the tombola, by running at 12V for user specified time, which will then also slow itself down

def warm_up():
    #set our voltage step for a smooth acceleration
    power_supply.write('VSTEP:0.1')
    #increase voltage to 12V 
    for i in range(80):
        time.sleep(0.2)
        power_supply.write('VUP')
    #allow a userinput
    user_error2 = True
    while user_error2 == True:
        time1 = input("How many minutes to run?")
        try:
            time_delay = float(time1) * 60
            user_error2 = False
        except ValueError:
            pass
            
    time.sleep(time_delay)
    slow_tombola()

    



 


#future version of this will include parameters to put in first

#function to produce cataracting for a 300g load of 8mm beads (approx. 85 RPM)
#assuming startup() has been run, starting at 4V
def cataract():

    # show options for cataracting
    # input
    # if function
    user_error = True
    while user_error == True:
        
        user_option = input(""" Enter a number to select one of the programs
1. 8 mm beads, going from 4 - 20 V, pause at 12V and slow to 12V
2. 4.7 mm beads, going from 4 - 20 V, pause at 12 V and slow to 11V
3. 6 mm beads, going from 4 - 20 V, pause at 12V and slow to 14 V
""")
        #option 1 = 8 mm beads
        if user_option == '1':
            volt_decrease = 8 * 10
            volt_cap = 8 * 10
            user_error = False
        #option 2 = 4.7 mm beads
        elif user_option == '2':
            volt_decrease = 9 * 10
            volt_cap = 8 * 10 
            user_error = False

        #option 3  = 6 mm metal beads
        elif user_option == '3':
            volt_decrease = 8 * 10
            volt_cap = 10 * 10
            user_error = False
        #any other input, leading to a repeat of the question
        else:
            user_error = True
            
    #sets the in-built power supply step to 0.1 V
    power_supply.write('VSTEP:0.1')

    #loop to increase the voltage by 8 V
    for i in range(80):
        time.sleep(0.2)
        power_supply.write('VUP')
    
    #now at 12 V
    #accelerate to 20V, more slowly
    for i in range(volt_cap):
        time.sleep(0.5)
        power_supply.write('VUP')
    
    #slow back down to chosen voltage to induce cataracting
    time.sleep(6)
    for i in range(volt_decrease):
        time.sleep(0.2)
        power_supply.write('VDOWN')




#this function reduces our voltage to 4V, from any voltage
def slow_tombola():
    #find the current voltage
    current_voltage = power_supply.query('VOUT?')
    power_supply.write('VSTEP:0.1')
    #turn the output string into a number
    current_voltage = float(current_voltage[:6])
    #round it to the nearest integer (whole number for the loop)
    current_voltage = int(round(current_voltage,0))
    #set the power supply to that nearest integer
    #combine voltage + VSET to create a SCPI command
    voltage_set = 'VSET:' + str(current_voltage)
    power_supply.write(voltage_set)
    #subtract 4 so we stop at 4V 
    current_voltage = current_voltage - 4
    #multiply by 10 as we are moving in steps of 0.1 V 
    voltage_steps = current_voltage * 10
    for i in range(int(voltage_steps)):
        time.sleep(0.2)
        power_supply.write('VDOWN')

#this function closes the connection to the device
def stop_supply():
    power_supply.write('OUT:0')
    power_supply.close()

#this function lists the other functions (ease of use)
def help_list():
    print("Here is a list of all available functions \nremember to use () at the end")
    user_functions = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType)]
    for function_name in user_functions:
        print(function_name)


#the main body of the code
#this line prompts the user to use the functions
print("Use help_list() to see what functions are available")
