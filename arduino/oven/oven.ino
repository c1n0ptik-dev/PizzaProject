const int redLedPin = 4;    
const int greenLedPin = 5; 
const long delayTime = 10000; 

void setup() {
  Serial.begin(9600);  
  pinMode(redLedPin, OUTPUT);
  pinMode(greenLedPin, OUTPUT);


  digitalWrite(redLedPin, LOW);
  digitalWrite(greenLedPin, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); 

    if (command == "StartSequence") {
      Serial.println("Sequence started");

      // Turn on the red LED
      digitalWrite(redLedPin, HIGH);

      // Wait for 10 seconds
      delay(delayTime);

      // Turn off the red LED and turn on the green LED
      digitalWrite(redLedPin, LOW);
      digitalWrite(greenLedPin, HIGH);

      delay(5000);

      digitalWrite(greenLedPin, LOW);
      Serial.println("Sequence finished");
    }
  }
}
