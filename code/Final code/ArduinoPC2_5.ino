

//Enable Driver 2
int ENABLE1 = 8;
int ENABLE3 = 13;

//Motor1
int DIR1 = 9;
int PWM1 = 10;

//Motor 2
int DIR2 = 7;
int PWM2 = 6;

//Motor 3
int DIR3 = 12;
int PWM3 = 11;

//Input Read variables
const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;

char messageFromPC[buffSize] = {0};
char messageFromPC2[buffSize] = {0};
int newFlashInterval = 0;
int PWM_P = 0;
int PWM_S = 0;
int PWM_PP = 0;


unsigned long curMillis;
unsigned long prevReplyToPCmillis = 0;
unsigned long replyToPCinterval = 1000;

//=============

void setup() {
  Serial.begin(9600);
  
  pinMode(DIR2, OUTPUT);
  pinMode(PWM2, OUTPUT);
  pinMode(ENABLE1, OUTPUT);
  pinMode(DIR1, OUTPUT);
  pinMode(PWM1, OUTPUT); 
  digitalWrite(ENABLE1, HIGH);
  pinMode(DIR3, OUTPUT);
  pinMode(PWM3, OUTPUT);
  pinMode(ENABLE3, OUTPUT);
  digitalWrite(ENABLE3, HIGH);
  
    // tell the PC we are ready
  Serial.println("<Arduino is ready>");
}

//=============

void loop() {
  curMillis = millis();
  getDataFromPC(); //Read data from PC
  replyToPC();  //Send back received data to check for data corruption
  updateMotion();
}

//=============

void getDataFromPC() {

    // receive data from PC and save it into inputBuffer
    
  if(Serial.available() > 0) {

    char x = Serial.read();

      // the order of these IF clauses is significant
      
    if (x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}

//=============
 
void parseData() {

    // split the data into its parts
    
  char * strtokIndx; // this is used by strtok() as an index
  
  strtokIndx = strtok(inputBuffer,",");      // get the first part - the string
  strcpy(messageFromPC, strtokIndx); // copy it to messageFromPC; direction - forward or backward
  
  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  PWM_P = atoi(strtokIndx);     // convert this part to an integer

  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  PWM_S = atoi(strtokIndx);     // convert this part to an integer

  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  strcpy(messageFromPC2, strtokIndx);     // convert this part to an integer; direction - up or down

  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  PWM_PP = atoi(strtokIndx);     // convert this part to an integer
}

//=============

void replyToPC() {

  if (newDataFromPC) {
    newDataFromPC = false;
    Serial.print("<Msg ");
    Serial.print(messageFromPC);
    Serial.print(" Primary PWM ");
    Serial.print(PWM_P);
    Serial.print(" Secondary PWM ");
    Serial.print(PWM_S);
    Serial.print(" Msg 2 ");
    Serial.print(messageFromPC2);
    Serial.print(" Pitch PWM ");
    Serial.print(PWM_PP);
    Serial.print(" Time ");
    Serial.print(curMillis >> 9); // divide by 512 is approx = half-seconds
    Serial.println(">");
  }
}

//============

void updateMotion() {
    if (strcmp(messageFromPC, "F") == 0){
      digitalWrite(DIR1, HIGH);
      analogWrite(PWM1, PWM_P);

      digitalWrite(DIR2, HIGH);
      analogWrite(PWM2, PWM_S);   
    }
    else if (strcmp(messageFromPC, "B") == 0){
      digitalWrite(DIR1, LOW);
      analogWrite(PWM1, PWM_P);

      digitalWrite(DIR2, LOW);
      analogWrite(PWM2, PWM_S);   
    }
    else if (strcmp(messageFromPC, "N") == 0){
      Stop();
    }
    if (strcmp(messageFromPC2, "U") == 0){
      digitalWrite(DIR3, HIGH);
      analogWrite(PWM3, PWM_PP);
    }
    else if (strcmp(messageFromPC2, "D") == 0){
      digitalWrite(DIR3, LOW);
      analogWrite(PWM3, PWM_PP);
    }
    else if (strcmp(messageFromPC2, "N") == 0){
      digitalWrite(DIR3, LOW);
      analogWrite(PWM3, 0);
    }
}  

//=============

void Stop(){
  digitalWrite(DIR1, LOW);
  analogWrite(PWM1, 0);

  digitalWrite(DIR2, LOW);
  analogWrite(PWM2, 0);
}


