
/* SubD-9(P) pinout:
  * 1 - LOAD
  * 3 - DATA
  * 5 - CLOCK
  * 6 - GND
  * 9 - +5V
*/

/* Arduino pinout
  * LOAD - to digital pin 10 (LOAD pin)
  * SDI - to digital pin 11 (MOSI pin)
  * CLK - to digital pin 13 (SCK pin)
*/

#include <SPI.h>

const int loadPin = 10;
const byte zero_buffer[] = {0x80, 0x00}; //{MSB, LSB, CRC8}

byte serial_buffer[] = {0x80, 0x00, 0x2f}; //{MSB, LSB, CRC8}
byte dac_buffer[] = {0x80, 0x00}; //{MSB, LSB}

void setup() {
  SPI.begin();
  Serial.begin(115200);
  pinMode(loadPin, OUTPUT);
  digitalWrite(loadPin, HIGH);
  digitalWriteDAC16(zero_buffer);
}

void loop() {
  if (Serial.available() >= 3){
    Serial.readBytes(serial_buffer, 3);
    byte crc = CRC8(serial_buffer, 2);
    if(crc == serial_buffer[2]){
      dac_buffer[0] = serial_buffer[0];
      dac_buffer[1] = serial_buffer[1];
    }
  }
  digitalWriteDAC16(dac_buffer);
}

void digitalWriteDAC16(const byte* bytes_buffer){
  unsigned int dac_word = (bytes_buffer[0]<<8) + bytes_buffer[1];
  SPI.beginTransaction(SPISettings(1500000, MSBFIRST, SPI_MODE0));
  SPI.transfer16(dac_word);
  digitalWrite(loadPin, LOW);
  delayMicroseconds(1);
  digitalWrite(loadPin, HIGH);
  SPI.endTransaction();
}

void digitalWriteSerial(const byte* bytes_buffer, int len){
  Serial.write(bytes_buffer, len);
}

byte CRC8(const byte* bytes_buffer, byte len) {
  byte crc=0;
  for (byte i=0; i<len; i++) {
    byte in_byte = bytes_buffer[i];
    for (byte j=0; j<8; j++) {
      byte mix = (crc ^ in_byte) & 0x01;
      crc >>= 1;
      if (mix) crc ^= 0x8C;
      in_byte >>= 1;
    }
  }
  return crc;
}






//unsigned int counter = 0;
//byte buf[] = {0x0,0x0};

//counter = 0;
//  counter++;
//  buf[0]=(counter&0xFF00)>>8;
//  buf[1]=(counter&0x00FF);
//  Serial.write(buf, 2);



// byte spi_buffer[] = {0x80, 0x00}; //{MSB, LSB}
// memcpy(spi_buffer, bytes_buffer, len);
//unsigned int dac_word = ((bytes_buffer[0]<<8)&0xFF00) | (bytes_buffer[1]&0x00FF);
  //unsigned int dac_word = (bytes_buffer[0]<<8) + bytes_buffer[1];
  //SPI.transfer16(dac_word);
  //SPI.transfer(spi_buffer, len);
  //SPI.transfer(bytes_buffer[0]);
  //SPI.transfer(bytes_buffer[1]);
