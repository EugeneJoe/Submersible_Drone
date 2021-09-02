//RIGHT THRUSTER PINS
int RIGHT_PWM = 11;
int RIGHT_DIR = 13;
//LEFT THRUSTER PINS
int LEFT_PWM = 10;
int LEFT_DIR = 12;
//PITCH THRUSTER PINS
int PITCH_PWM = 9;
int PITCH_DIR = 8;
int PWM = 0;
const byte numChars = 10;
char serIn[numChars];
char tempChars[numChars];
char Direction[numChars] = {0};
boolean newData = false;

void setup() {
  // put your setup code here, to run once:
  pinMode(RIGHT_PWM, OUTPUT);
  pinMode(RIGHT_DIR, OUTPUT);
  pinMode(LEFT_PWM, OUTPUT);
  pinMode(LEFT_DIR, OUTPUT);
  pinMode(PITCH_PWM, OUTPUT);
  pinMode(PITCH_DIR, OUTPUT);
  pinMode(13, OUTPUT);

  Serial.begin(9600);
  Serial.println("Hello Pi,This is Arduino...");
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Hello Pi,This is Arduino UNO...");
  SerialRead();
  if (newData == true){
    strcpy(tempChars, serIn);
    parseData();
    showParsedData();
  }
    if (Direction == 'F'){  //blink LED 5 times if Forward command is received from UNO
      int n = 5;
      for(int i=0;i<n;i++){
        digitalWrite(13,HIGH);
        delay(500);
        digitalWrite(13,LOW);
        delay(500);
        //Serial.println(i+1);
      }
    }
  delay(1000);
}

void SerialRead(){
  static boolean ReadInProgress = false;
  static byte index = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  while (Serial.available() > 0 && newData == false){
    rc = Serial.read();

    if(ReadInProgress == true){
      if(rc != endMarker){
        serIn[index] = rc;
        index++;
        if(index >= numChars){
          index = numChars - 1;
        }
      }
      else{
        serIn[index] = '\0';
        ReadInProgress = false;
        index = 0;
        newData = true;
      }
    }
    else if(rc == startMarker){
      ReadInProgress = true;
    }
  }
}

void parseData(){
  char * strtokIndx;

  strtokIndx = strtok(tempChars,":");
  strcpy(Direction, strtokIndx);

  strtokIndx = strtok(NULL, ":");
  PWM = atoi(strtokIndx);
}

void showParsedData(){
  Serial.print("Message ");
  Serial.println(Direction);
  Serial.println("Integer ");
  Serial.println(PWM);
}
//void Split(){
//  int in = sscanf(serIn, "%c:%d",&Direction,&PWM);
//  Serial.print(Direction + " ");
//  Serial.println(PWM);
////  int len = len(serIn);
////  Direction = serIn[0];
////  PWM = ;
//}

