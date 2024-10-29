int red_light = 4;
int green_light = 5;
int blue_light = 3;
int button = 8;

int order_state = 0;

void setup() {
  pinMode(red_light, OUTPUT);
  pinMode(green_light, OUTPUT);
  pinMode(button, INPUT_PULLUP);

  //serial communication
  Serial.begin(9600);
}

void loop() {
  String cmd;

  if (Serial.available()){
    cmd = Serial.readStringUntil("\n");
    
    if (cmd == "LedOn") {
      digitalWrite(red_light, HIGH);
    } else if (cmd == "LedOff") {
      digitalWrite(red_light, LOW);
    }
  }
}