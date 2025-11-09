# Proyecto-Trenes-INFO-081
## Repositorio del proyecto para programación

### Integrantes: Ian Bruning, Daniela Antimilla, Magdalena Delgado, Diego Aguirre.

En este proyecto desarrollaremos un sistema de simulación a traves de una interfaz grafico,
que consistira principalmente en representar una estación de trenes. El sistema nos permitira 
visualizar en pantalla los diferentes trenes disponibles, las rutas para llegar a los diferentes 
destinos, las estaciones del recorrido y su número de pasajeros que suben y bajan en cada estacion. 
Ademas el tiempo estimado para cada viaje y la incorporacion de eventos aleatorios los cuales 
requeriran una toma de decisiones por parte del usuario, haciendo que la simulacion sea mas dinamica.

### DESCRIPCIÓN DE INDICADORES A UTILIZAR EN INTERFAZ:
* Se utilizaran 2 tipos de indicadores principales:

    * Capacidad del tren (cuantitativo):
    Este indicador mostrará en pantalla el numero de pasajeros que suben y bajan en cada estacion, 
    manteniendo actualizado el conteo de capacidad, controlando que supere la capacidad maxima del tren.

    * Mensajes de eventos (cualitativo):
    Representara las situaciones o imprevistos que ocurran durante la simulacion (por ejemplo: retrasos 
    o fallas). Esto se mostraran mediante mensajes emergentes en la interfaz, acompañado de decisiones en
    la cual el usuario tendra que tomar una decision para resolver cada evento.

### PERSISTENCIA DE DATOS:
* Para garantizar la persistencia de la informacion, el sistema almacenara los datos mas relevantes en 
archivos de texto (.txt). Estos tendran informacion como:

    * La configuracion inicial del sistema.
    * Las estaciones registradas.
    * Los trenes disponibles.
    * Las rutas definidas.

Este metodo nos permitira realizar operaciones de lectura y escritura, facilitando tanto la carga
como el guardado de informacion en listas simples, asegurando que los datos puedan ser reutilizados
o actualizados sin perder el progreso de simulacion.

### Ejemplo de cómo correr archivos principales:

Para poder correr el programa principal Ventana_principal.py (considerando que ya haya descargado/clonado el repositorio)
necesita abrir un terminal y escribir:
-cd y el nombre de la carpeta en la cual estan los archivos de codigo
Ejemplo: 
cd "Proyecto-Trenes-INFO-081"
en donde puede escribir ls para asegurarse que la se encuentre en la carpeta correcta
-Posteriormente escribe python -m y el archivo que quiera correr eso si el archivo debe contener "if name==__main__"
ya que estos archivos son los que se pueden ejecutar.
Ejemplo:
python -mVentana_principal //Para iniciar el programa principal
o
python -mUI.ventanas //esta es una ventana secundaria en donde el .UI sirve para localizar la ventana en especifico