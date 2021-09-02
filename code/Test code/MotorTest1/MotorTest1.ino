//Enable Driver 2
int ENABLE2 = 8;

//Motor1
int DIR1 = 9;
int PWM1 = 10;

//Motor 2
int DIR2 = 7;
int PWM2 = 6;

void setup() {
  // put your setup code here, to run once:
    pinMode(DIR2, OUTPUT);
  pinMode(PWM2, OUTPUT);
  pinMode(ENABLE2, OUTPUT);
  pinMode(DIR1, OUTPUT);
  pinMode(PWM1, OUTPUT);
  //pinMode(ENABLE1, OUTPUT);  
  digitalWrite(ENABLE2, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  Forward(50);
  delay(1000);

  Stop();
  delay(100);

  Backward(50);
  delay(1000);
  
  Stop();
  delay(100);

  TurnRight(50);
  delay(2000);

  Stop();
  delay(100);

  TurnLeft(50);
  delay(2000);

  Stop();
  delay(100);

  CurveRight(70,50);
  delay(2000);

    Stop();
  delay(100);

  BackRight(70,50);
  delay(1000);

    Stop();
  delay(100);

  CurveLeft(70,50);
  delay(2000);

    Stop();
  delay(100);

  BackLeft(70,50);
  delay(2000);

    Stop();
  delay(100);
}

void Forward(int pwm){
  digitalWrite(DIR1, HIGH);
  analogWrite(PWM1, pwm); 

  digitalWrite(DIR2, HIGH);
  analogWrite(PWM2, pwm);
}

void Backward(int pwm){
  digitalWrite(DIR1, LOW);
  analogWrite(PWM1, pwm);

  digitalWrite(DIR2, LOW);
  analogWrite(PWM2, pwm);
}

void Stop(){
  digitalWrite(DIR1, LOW);
  analogWrite(PWM1, 0);

  digitalWrite(DIR2, LOW);
  analogWrite(PWM2, 0);
}

void TurnLeft(int pwm){
  digitalWrite(DIR1, HIGH);
  analogWrite(PWM1, pwm);

  digitalWrite(DIR2, HIGH);
  analogWrite(PWM2, 0);  
}

void TurnRight(int pwm){
  digitalWrite(DIR1, HIGH);
  analogWrite(PWM1, 0);

  digitalWrite(DIR2, HIGH);
  analogWrite(PWM2, pwm);  
}

void CurveRight(int pwm, int pwm2){
  digitalWrite(DIR1, HIGH);
  analogWrite(PWM1, pwm2);

  digitalWrite(DIR2, HIGH);
  analogWrite(PWM2, pwm);   
}

void CurveLeft(int pwm, int pwm2){
  digitalWrite(DIR1, HIGH);
  analogWrite(PWM1, pwm);

  digitalWrite(DIR2, HIGH);
  analogWrite(PWM2, pwm2);   
}

void BackRight(int pwm, int pwm2){
  digitalWrite(DIR1, LOW);
  analogWrite(PWM1, pwm);

  digitalWrite(DIR2, LOW);
  analogWrite(PWM2, pwm2);  
}

void BackLeft(int pwm, int pwm2){
  digitalWrite(DIR1, LOW);
  analogWrite(PWM1, pwm2);

  digitalWrite(DIR2, LOW);
  analogWrite(PWM2, pwm);  
}
