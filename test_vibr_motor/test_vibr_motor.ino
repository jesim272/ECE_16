int vib_mot = 3;

void setup() {
  // initialize the digital pin as an output.
  pinMode(vib_mot, OUTPUT);    
}

void loop() {
  // Short pulses
  digitalWrite(vib_mot, LOW);   // ON
  delay(200);               
  digitalWrite(vib_mot, HIGH);  // OFF
  delay(500);               

}
