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

    if (command == "GreenLight") {
      Serial.println("Sequence started");
      tone(buzzer, 1000);
      digitalWrite(greenLedPin, HIGH);
      delay(1000);
      digitalWrite(greenLedPin, LOW);
      noTone(buzzer);
    }
    else if (command == "RedLight") {  
      Serial.println("Sequence started");
      digitalWrite(redLedPin, HIGH);
      delay(1000);
      digitalWrite(redLedPin, LOW); 
    }
  }
}
