# Proyecto-Trenes-INFO-081
## Repositorio del proyecto para programación

Integrantes: Ian Bruning, Daniela Antimilla, Magdalena Delgado, Diego Aguirre.

RESUMEN: En este proyecto incorporaremos un sistema de simulación a traves de una interfaz,
que consistira principalmente en una estación de trenes donde se muestre en pantalla los diferentes
trenes a usar, las rutas para llegar a los diferentes destinos, las estaciones y su número de personas
que suben y bajan en cada estacion, el tiempo estimado para cada viajes, y eventos aleatorios con toma 
de desiciones.

DESCRIPCIÓN DE INDICADORES A UTILIZAR EN INTERFAZ: Los dos indicadores a usar van a ser la capacidad 
del tren(cuantitativo), ya que eso se mostrará en pantalla en números donde se incluira el numero de 
personas que entra y salen del tren para mantener un orden en la capacidad maxima del mismo. El segundo 
indicador a usar sería el mensaje de eventos(cualitativo), porque estos se explicarian en mensajes que 
aparezcan en ventana junto con las desiciones a tomar.

PERSISTENCIA DE DATOS: En lo que respecta a la persistencia de datos, almacenaremos los datos más 
importantes en archivos(.txt), que tendrá información como: la configuración inicial, las estaciones, 
los trenes y las rutas. Este archivo nos permitirá tanto la lectura como la escritura de datos y listas 
simples, facilitando la carga y el guardado de la información del programa.

Para poder correr el programa principal Ventana_principal.py (considerando que ya haya descargado/clonado el repositorio)
necesita abrir un terminal y escribir:
-cd y el nombre de la carpeta en la cual estan los archivos de codigo
Ejemplo: 
cd "Proyecto-Trenes-INFO-081"
en donde puede escribir ls para asegurarse que la se encuentre en la carpeta correcta
-Posteriormente escribe python -m y el archivo que quiera correr eso si el archivo debe contener "if name==__main__"
ya que estos archivos son los que se pueden ejecutar.
Ejemplo:
python -mVentana_principal.py //Para iniciar el programa principal
o
python -mUI.ventanas.py //esta es una ventana secundaria en donde el .UI sirve para localizar la ventana en especifico