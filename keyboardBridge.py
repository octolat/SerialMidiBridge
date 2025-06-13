#--- SETTINGS ---#
serial_port = None
serial_baudrate = 1000000
 
midi_port = "IAC Driver Bus 1" 

seperator = " "
cmd_keyPress = 1 
cmd_keyRelease = 2
cmd_sustainToggle = 3

octave_shift = 0 #move octave up or down, 0 is default, -1 is one octave down, 1 is one octave up etc
#--- SETTINGS ---#
import time
import rtmidi
import serial.tools.list_ports
import serial

def main():
    #open midi port
    midiout = rtmidi.MidiOut()
    ports = midiout.get_ports()
    for i in range(len(ports)):
        if ports[i] == midi_port:
            midiout.open_port(i)
            break
    if not midiout.is_port_open(): midiout.open_virtual_port("mySerialMidiBridgeVirtualPort")

    #open serial port
    ports = list(serial.tools.list_ports.comports())
    serial_connected = False
    for port, desc, hwid in ports:
        if (serial_port != None and port == serial_port) or (serial_port == None and desc == "USB Serial"):
            ser = serial.Serial(port, serial_baudrate)
            if (ser.is_open): serial_connected = True
            break
    if not serial_connected:
        raise Exception("Cant find port man")
    
    #run the main loop
    sustain = False
    with midiout:
        while True:
            #wait for data
            if ser.in_waiting > 0:
                #process the serial data
                data = ser.readline().decode('utf-8').rstrip().split(seperator)
                command = int(data[0])
                print(command, end='')
                if (command != cmd_sustainToggle):
                    note = int(data[1])
                    print(",", note, end='')
                print()

                #send the midi message
                #key pressed
                if (command == cmd_keyPress): midiout.send_message([0x90, note+octave_shift*12, 127])
                #key released
                elif (command == cmd_keyRelease): midiout.send_message([0x80, note+octave_shift*12, 127])
                #sustain toggle
                elif (command == cmd_sustainToggle): 
                    sustain = not sustain
                    if (sustain): midiout.send_message([0xB0, 64, 127])
                    else: midiout.send_message([0xB0, 64, 0])

                #wait abit to avoid flooding the midi port
                time.sleep(0.001)

    #free resources
    ser.close()
    del midiout

#helper functions to find your ports
def helper_PrintMidiPorts():
    midiout = rtmidi.MidiOut()
    ports = midiout.get_ports()
    print("Available MIDI ports:")
    for i, port in enumerate(ports):
        print(f"{i}: {port}")
    del midiout

def helper_PrintSerialPorts():
    ports = list(serial.tools.list_ports.comports())
    print("Available Serial ports:")
    for i, (port, desc, hwid) in enumerate(ports):
        print(f"{i}: {port} - {desc} ({hwid})")

#run the functions here
main()

