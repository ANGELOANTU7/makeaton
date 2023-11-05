// Define the pins for the 74HC595 shift registers
const int dataPin = 10;    // Connect to SER
const int clockPin = 11;   // Connect to SRCLK
const int latchPin = 12;   // Connect to RCLK
const int numRegisters = 4; // Number of shift registers
const int totalPins = numRegisters * 8; // Total number of output pins
int my=100;

void setup() {
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  Serial.begin(9600);
  Serial.println("Enter LED numbers you want to turn on, separated by commas (e.g., 12,13,4,3):");
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    processLEDs(input);
  }
}

void processLEDs(String input) {
  input.trim();
  input.replace(" ", ""); // Remove spaces
  input.replace("\n", ""); // Remove newline characters
  Serial.println(input);
  // Split the input into an array of LED numbers
    for(int j=0;j<my;j++)
    {
      for(int i=0;i<input.length();i++) {
        Serial.println(input[i]);
        if(input[i]=='1')
        {
          turnOnLED(i);
          delay(5); // Delay to give the app
          turnOffLED(i);
        }

        else
        {
        turnOffLED(i);
        //delay(10);
        }
      }
    }

}
        
  


void turnOnLED(int ledNumber) {
  // Calculate the register index and the bit within the register
  int registerIndex = ledNumber / 8;
  int bitInRegister = ledNumber % 8;

  // The bits you want to send for each register
  byte bitsToSend[numRegisters] = {0};

  // Turn off the output so the pins don't light up while the bits are being shifted in
  digitalWrite(latchPin, LOW);

  // Set the specified bit in the appropriate register
  bitWrite(bitsToSend[numRegisters - 1 - registerIndex], bitInRegister, HIGH);

  // Shift the bits out for each register
  for (int i = numRegisters - 1; i >= 0; i--) {
    shiftOut(dataPin, clockPin, MSBFIRST, bitsToSend[i]);
  }

  // Turn on the output so the LED can light up
  digitalWrite(latchPin, HIGH);
}

void turnOffLED(int ledNumber) {
  // Calculate the register index and the bit within the register
  int registerIndex = ledNumber / 8;
  int bitInRegister = ledNumber % 8;

  // The bits you want to send for each register
  byte bitsToSend[numRegisters] = {0};

  // Turn off the output so the pins don't light up while the bits are being shifted in
  digitalWrite(latchPin, LOW);

  // Set the specified bit in the appropriate register
  bitWrite(bitsToSend[numRegisters - 1 - registerIndex], bitInRegister, LOW);

  // Shift the bits out for each register
  for (int i = numRegisters - 1; i >= 0; i--) {
    shiftOut(dataPin, clockPin, MSBFIRST, bitsToSend[i]);
  }

  // Turn on the output so the LED can turn off
  digitalWrite(latchPin, HIGH);
}
