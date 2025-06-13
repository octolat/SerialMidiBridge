// to make each note not hold even if you hold it down to make it more like a real piano
bool noteTracker[64] = {0};

//depends on your set up 
const int input_pins[8] = {12, 13, A0, A1, A2, A3, A4, A5};
const int output_pins[8] = {4, 5, 6, 7, 8, 9, 10, 11};

void sendMessage(int command, int note);

//--- SETTINGS ---//
const int OCTAVE_OFFSET = (2)*12+24; //put the octave the first C key is in the bracket eg. rn the first c key is c2
const int serial_baudrate = 1000000;

String seperator = " ";
int cmd_keyPress = 1;
int cmd_keyRelease = 2;
int cmd_sustainToggle = 3;
//--- SETTINGS ---//


void setup() {
  // put your setup code here, to run once:
  Serial.begin(1000000);
  pinMode(buzzer, OUTPUT);
  tone(buzzer, 1000, 500);
  for (int i = 0; i < 8; i++) {
    pinMode(output_pins[i], OUTPUT);
    digitalWrite(output_pins[i], LOW);
  }
  for (int i = 0; i < 8; i++) {
    pinMode(input_pins[i], INPUT);
  }
  
}

void loop() {
  // my keyboard uses a multiplexer so im going through each input wire and seeing if any output wire are high
  for (int i = 0; i < 8; i++) {
    digitalWrite(output_pins[i], HIGH);
    for (int j = 0; j < 8; j++) {
      int note = i*8 + j;
      if (digitalRead(input_pins[j]) == 1){
        //make the note not sustain
        if (!noteTracker[note]) {
          sendMessage(cmd_keyPress, note);
          noteTracker[note] = true;
        }
      } else {
        if (noteTracker[note]) {
          sendMessage(cmd_keyRelease, note);
        }
        noteTracker[note] = false;
      }
    }
    digitalWrite(output_pins[i], LOW);
  }

}

void sendMessage(int command, int note){
  Serial.print(command);
  if (command != cmd_sustainToggle){
    Serial.print(seperator);
    Serial.print(note+OCTAVE_OFFSET); //prints the midi number, plus octave_offest to make the first note c2(depends on ur keyboard, see midi note values)
  }
  Serial.println();
  
}