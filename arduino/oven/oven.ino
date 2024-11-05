const int redLedPin = 4;
const int greenLedPin = 5;  
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

    if (command == "RedLight") {
      Serial.println("Sequence started");

      digitalWrite(redLedPin, HIGH);
      tone(buzzer, 1000);
      delay(500);
      noTone(buzzer);

      digitalWrite(redLedPin, LOW);
}
    else if (command == "GreenLight"){
      digitalWrite(greenLedPin, HIGH);

      tone(buzzer, 1000);
      delay(200);
      noTone(buzzer);

      delay(100);

      tone(buzzer, 1000);
      delay(200);
      noTone(buzzer);

      delay(100);

      tone(buzzer, 1000);
      delay(200);
      noTone(buzzer);

      delay(2000);

      digitalWrite(greenLedPin, LOW);
      Serial.println("Sequence finished");
    }
    }
}