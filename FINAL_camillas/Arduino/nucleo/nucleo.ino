// Librerias necesarias
#include <DHT.h>

// Asignación de pines
#define DHTPIN1 7       //  Sensor de temperatura asignado al pin 7

int
  act0 = 6,             //  Pin actuador 1 (Emitir calor)
  act1 = 5;             //  Pin actuador 2 (Emitir frio)
  
//  Variables
boolean 
  b_act_status = false;      //  Bandera actuadores
  
String
  //  Variables de control
  str_act_status="",
  str_act_status_ctrl="",
  //  Actuadores
  act_0="",          //  Estado del actuador 0
  act_1="",          //  Estado del actuador 1
  act_0_ctrl="f",     //  Control del estado del actuador 0
  act_1_ctrl="f",     //  Control del estado del actuador 1
  //  Sensores
  t0="";              // Valor de lectura del sensor de temperatura


// Número de sensores
int 
  nSens = 1,        //  Número de sensores incluidos en el módulo
  nAct = 2;         //  Número de actuadores incluidos en el módulo


// Declarar el sensor DHT11
#define DHTTYPE DHT11
DHT dht1(DHTPIN1, DHTTYPE);




/*****************************************************************************************/
//  SETUP
/*****************************************************************************************/
void setup() {
  //  Configurar pines
  pinMode(act0, OUTPUT);
  pinMode(act1, OUTPUT);
  
  // Iniciar serial
  Serial.begin(115200);
  // Iniciar DHT11s
  dht1.begin();
  //  Iniciar estado de los actuadores
  setActuator_Status();
  //  Iniciar actuación
  triggerAct();
}





/*****************************************************************************************/
//  LOOP
/*****************************************************************************************/
void loop() {
 readActuator_Status();
 if(b_act_status) setAct_status();
 triggerAct();
 sendSerial();
 }





/*****************************************************************************************/
//    Funciones para comunicación con interfaz Python
/*****************************************************************************************/
//  Configurar el estado de los actuadores
void setActuator_Status(){
  String ser=Serial.readString();
  if(splitValor(ser,'?',0)=="act_status"){
    str_act_status_ctrl=str_act_status=splitValor(ser,'?',1);
    b_act_status=true;
  }
  else{
    b_act_status=false;
  }
}

//  Leer el estado de los actuadores y cambiar las banderas para ejecuciones
void readActuator_Status(){
  String ser=Serial.readString();
  str_act_status=splitValor(ser,'?',1);
  if(str_act_status!=str_act_status_ctrl){
    b_act_status=true;
    str_act_status_ctrl=str_act_status;
  }
  else 
    b_act_status=false;
}

//  Asignar valores obtenidos desde la interfaz Python a variables del módulo Hardware
void setAct_status(){
  str_act_status.replace(';','|');
  
  for(int i=0;i<nAct+1;i++){
    String params = splitValor(str_act_status,'|',i);
    String v = splitValor(params,':',1);
    if(splitValor(params,':',0)=="a0")
      act_0=v;
    else if(splitValor(params,':',0)=="a1")
      act_1=v;
  }
}


//  Enviar lectura de temperatura a la interfaz de python
void sendSerial(){
  //  Leer humedad del sensor DHT11
  float h0 = dht1.readHumidity();

  //  Leer temperatura en grados centigrados del sensor DHT11
  float t0 = dht1.readTemperature();

  //  Obtener la temperatura
  t0 = dht1.computeHeatIndex(t0, h0, false);

  //  Asignar valor del estado o lectura del sensor
  String s_t0 = (isnan(t0)) ? "error" : String(t0);

  //  Imprimir cadena serial
  Serial.println("arduino?t0:"+s_t0+"@"+"a0:"+act_1_ctrl+"|a1:"+act_1_ctrl);
}

/*****************************************************************************************/
//    FUNCIONES ACTUADORES
/*****************************************************************************************/
//  Disparador de actuadores
void triggerAct(){  
  act0_a();     //  Llamada a la función del actuador 0
  act1_a();     //  Llamada a la función del actuador 0
}

//  Función para interactuar con el actuador 0
void act0_a(){
  if(act_0_ctrl!=act_0){
    act_0_ctrl = act_0; 
  }

  if(act_0_ctrl=="t")
    digitalWrite(act0,HIGH);
  else if(act_0_ctrl=="f")
    digitalWrite(act0,LOW);
  else
    digitalWrite(act0,LOW);
}

//  Función para interactuar con el actuador 1
void act1_a(){
  if(act_1_ctrl!=act_1){
    act_1_ctrl = act_1; 
  }

  if(act_1_ctrl=="t")
    digitalWrite(act1,HIGH);
  else if(act_1_ctrl=="f")
    digitalWrite(act1,LOW);
  else
    digitalWrite(act1,LOW);
}



/*****************************************************************************************/
//    Funciones varias
/*****************************************************************************************/
//  Split a un string
String splitValor(String txt, char separator, int ind){
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = txt.length()-1;
  for(int i=0; i<=maxIndex && found<=ind; i++){
    if(txt.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }
  return found>ind ? txt.substring(strIndex[0], strIndex[1]) : "";
}
