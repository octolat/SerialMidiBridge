# SerialMidiBridge
a pc-side driver for arduinos without native usb support to still act as a midi device

reads in serial output from any microcontroller, and translate that to midi messages, using virtual midi ports.

## set up
```
serial_port = None
```
what serial port is your arduino connected to  
- **default**: None  
will scan for the first port with description "USB Serial" (recommended)  
- **alternative**: set to the name of your port  
name must be exact. you can find the name of the port with the helper function described below  

```
serial_baudrate = 1000000
```
baud rate you are using  
you may use any baud rate, just make sure the arduino is using the same baud rate

```
midi_port = "IAC Driver Bus 1" 
```
midi port you are using  
- **default**: "IAC Driver Bus 1" (recommened for macos)  
be sure to bring the device online using the app "audio MIDI setup" [(see guide)](https://support.apple.com/en-sg/guide/audio-midi-setup/ams1013/mac)  
- **alternative**: set to the name of your own virtual port  
if you are using another software that has its own virtual port, you can change it to that. must be exact. you can find the name of the port with the helper function described below  
- **alternative 2**: leave it be  
if you do not want to use a preexisting virtual port, you can leave it be. the software will see that it is unable to find a preexisting port, and open up its own virtual port named "mySerialMidiBridgeVirtualPort" (macos and linux only)
**note:** for windows users, windows does not support native virtual ports. you will need a 3rd party application that is capable of creating one to make one. Then, following the alternative, set the variable to the name of the port you have created.
```
seperator = " "
cmd_keyPress = 1 
cmd_keyRelease = 2
cmd_sustainToggle = 3
```
formatting spesifications for serial
the format is   
**[cmd|seperator|note(if needed)|newline]**.   
cmd, seperator are defined in the functions above.
note follows midi note values conventions. [(as described here)](https://computermusicresource.com/midikeys.html)  
examples:
- "1 48\n" = cmd=1, note=48 -> key C2 is pressed
- "2 48\n" = cmd=2, note=48 -> key C2 is released
- "3" = cmd=3 -> toggle sustain (note the lack of a note argument)
  
make sure your microcontroller follows this convention as well  
you can change the cmd_ variable to any number between 1-9. make sure they do not clash
you can change the seperator to any thing that isnt a number or \n.

```
octave_shift = 0
```
shifts your key up or down
negetive to make it lower, positive to make it higher

##microcontroller side
when you are ready, send a message through serial following the formatting above. Below is a code snippet showing how you can implement it
```
void sendMessage(int command, int note){
  Serial.print(command);
  if (command != cmd_sustainToggle){
    Serial.print(seperator);
    Serial.print(note+OCTAVE_OFFSET); //prints the midi number, plus octave_offest to make the first note c2(depends on ur keyboard, see midi note values)
  }
  Serial.println();
}
```
make sure the baud rate is also the same.  
you can also look at the exemplar .ino file to refer. It hijacks off a broken keyboard and iterates through the multiplexer to find notes with changed states, and sends a message reflecting that.  

## dependicies
depends on the time, rtmidi, serial.tools.list_ports and serial libaries. please make sure to install them.

## common isssues
error resource busy --> close your serial monitor from arudino ide or any other serial moniter you have open  
Cant find port man --> it cant find the serial port  
[Errno 6] Device not configured --> the serial port got unplugged mid way  
key presses are kinda slow to register --> increase your baud rate, and run the python file from terminal. (running from idle console is noticably slower)

## extra: getting my midi output to sound
you can use most DAWs to play your midi output. I have gotten it to work on [waveform free](https://www.tracktion.com/products/waveform-free).  
If you do not care for the other DAW features like editing your midi output, and just want to hear and record audio clips of your sound, i recomend a sfz player like [sforzando](https://www.plogue.com/products/sforzando.html)  
**note:** garageband is terrible with virtual midi ports. it can work, but it is very buggy, and i face issues where the midi output will just stop sounding occasionally, and it will only work if you click away and refocus the track. this seems to be a issue with garageband itself. use other software.  

## todo
- test windows compaitibility
- test the sustain pedal
- support for dynamic velocity
- the other pedals
