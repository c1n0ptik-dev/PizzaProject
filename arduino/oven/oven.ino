const int redLedPin = 4;    
const int greenLedPin = 5; 
const long delayTime = 10000; 
const int buzzer = 3;

void setup() {
  Serial.begin(9600);  
  pinMode(redLedPin, OUTPUT);
  pinMode(greenLedPin, OUTPUT);
  pinMode(buzzer, OUTPUT);


  digitalWrite(redLedPin, LOW);
  digitalWrite(greenLedPin, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); 

    if (command == "StartSequence") {
      Serial.println("Sequence started");


      digitalWrite(redLedPin, HIGH);

      delay(delayTime);

      digitalWrite(redLedPin, LOW);
      digitalWrite(greenLedPin, HIGH);

      tone(buzzer, 1000);
      delay(500);
      noTone(buzzer);

      delay(4000);

      digitalWrite(greenLedPin, LOW);
      Serial.println("Sequence finished");
    }
  }
}