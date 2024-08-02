#include <MultiStepper.h>
#include <AccelStepper.h> // you need to install library
#include <Arduino.h>

#define ulong unsigned long

#define enable_pin 8

// Define steppers and the pins they will use
AccelStepper translationStepper(AccelStepper::FULL2WIRE, 4, 7);   // Z Fast, bottom left
AccelStepper rotationStepper(AccelStepper::FULL2WIRE, 12, 13); // A Slow, bottom right

int incomingByte = 0; // for incoming serial data

volatile bool data_ready = false;
volatile bool relative = true;
volatile long steps[2]; // Only two motors now
volatile bool set_enable = false;

void setup()
{
  pinMode(enable_pin, OUTPUT);    // sets the digital pin 13 as output?? pin 8
  digitalWrite(enable_pin, HIGH); // Low equals motors enabled; High equals motors disabled

  pinMode(LED_BUILTIN, OUTPUT);

  translationStepper.setMaxSpeed(1000.0);
  translationStepper.setAcceleration(500.0);

  rotationStepper.setMaxSpeed(1000.0);
  rotationStepper.setAcceleration(500.0);

  Serial.begin(115200);          // for serial input
  digitalWrite(enable_pin, LOW); // Low equals motor enabled
}

void loop()
{
  serialEvent();
  if (data_ready) // If you use serial communication
  {
    data_ready = false;
    if (relative)
    {
      translationStepper.move(steps[0]); // linear
      rotationStepper.move(steps[1]); // rotation
    }
    else
    {
      translationStepper.moveTo(steps[0]); // linear
      rotationStepper.moveTo(steps[1]); // rotation
    }
  }

  // This make the motors move and must be call continuously
  bool isRunning = translationStepper.run() || rotationStepper.run();

  if (!isRunning && !data_ready)
  {
    Serial.println("done");
  }
}

// to be used if you want to control the motors from your pc via a serial communication format is one data frame starting with 0x81 0x88 motor1 motor2 motor3  motor4, each motor is signed long on 4 bytes
void serialEvent()
{
  unsigned char data[11];

  if (Serial.available())
  {
    // get the new byte:
    Serial.readBytes(data, 11); // read data from serial
    set_enable = data[0] & 0x01;

    int j = 2;
    for (int i = 0; i < 2; i++) // Loop only for two motors
    {
      steps[i] = ((ulong)(data[j++]) << 24) | ((ulong)(data[j++]) << 16) | ((ulong)(data[j++]) << 8) | data[j++];
    }

    if ((data[0] == 0x81) || (data[0] == 0x80))
      if (data[1] == 0x88)
        data_ready = true;
    if (data[10] == 0x81)
      relative = false;
  }
}
