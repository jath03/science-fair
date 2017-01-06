int sensorPin = A0;
float reading;
void setup() {
  // put your setup code here, to run once:
  pinMode(sensorPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  reading = analogRead(sensorPin) * (5.0 / 1023.0);
  Serial.println(String(reading));
  delay(1000);

}


