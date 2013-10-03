#include <Servo.h> 
#include <stdio.h>

Servo pan_servo;
Servo tilt_servo;
const int led_pin =  2;      // the number of the LED pin

int direction = 1;
int led_state = LOW;
int position = 0;
long led_interval = 1000;
long previous_led_millis = 0;
long previous_servo_millis = 0;
long sweep_interval = 20;
String incoming_string = "";


void setup() {
  Serial.begin(19200);
  pinMode(led_pin, OUTPUT);      
  pan_servo.attach(9);
  tilt_servo.attach(10);

  digitalWrite(led_pin, LOW);
  Serial.println("Ready Fucker");
}

char command[1024];
char commandBuffer[128];
int commandBufferSize = 0;

void readCommandBuffer(int bytesToRead) {
  int i = 0;
  char c = 0;
  while (i < 128 && (i < bytesToRead || bytesToRead <= 0)) {
    while (!Serial.available())
      ;
    c = Serial.read();
    if (c == '\r' || c == '\n') {
      break;
    }
    commandBuffer[i] = c;
    i++;
  }
  commandBufferSize = i;
}

void readCommand() {
  command[0] = '\0';
  readCommandBuffer(0);
  if (strncmp(commandBuffer, "RCV", 3) == 0) {
    commandBuffer[commandBufferSize] = '\0';
    int expectedSize = atoi(commandBuffer + 4);
    if (expectedSize <= 0 || expectedSize > 1024) {
      return;
    }
    Serial.println("RDY");
    int bytesRead = 0;
    while (bytesRead < expectedSize) {
      readCommandBuffer(expectedSize - bytesRead);
      memcpy(command + bytesRead, commandBuffer, commandBufferSize);
      bytesRead += commandBufferSize;
      Serial.print("ACK ");
      Serial.println(commandBufferSize);
    }
    command[bytesRead] = '\0';
  } else {
    memcpy(command, commandBuffer, commandBufferSize);
    command[commandBufferSize] = '\0';
  }
}

void loop() {
  if (Serial.available()) {
    readCommand();
    // "command" now contains the full command
    Serial.println(command);
  }
}
