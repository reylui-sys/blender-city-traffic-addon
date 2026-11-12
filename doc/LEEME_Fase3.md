# Fase 3 del Proyecto

## Introducción

Este documento describe el proceso de desarrollo de un script para la orientación a lo largo de una trayectoria. 
Toda esta práctica está realizada en la carpeta "cuaternion_circuito", no confundir con "practica3" que utiliza la ciudad.
Se describe una mini guía de como usar el add-on.

## Estructura del Documento

- [Instrucciones para probar la entrega](#instrucciones-para-probar-la-entrega): Instrucciones para instalar y probar la entrega.
- [Vídeos](#vídeos): Vídeos con los contenidos indicados en la práctica.

## Instrucciones para probar la entrega

1. Abrimos el "ejercicio7.blend" de la práctica 1, donde se encuentra la esfera con los keyframes insertados.

2. Instalamos el add-on, si no lo tenemos ya, en Editar>Preferencias>Add-on. Una vez instalado pasaremos a configurar los parámetros.

3. En este caso ajustaremos el método de interpolación a Catmund-Roll y los siguientes parámetros:

    - La tensión que utilizaremos en cada punto será de 0.45, para que no haya giros muy bruscos, pero aun así se generen esas curvas que buscamos.

    - Seleccionamos la opción de “Controlar Rotación en el eje X” para poder orientar el objeto en la dirección que queramos, en este caso en Y.

    - El alabeo que pondremos será de 0.20 o 0.45 dependiendo de cuanto queramos que el coche se incline. 

4. Por último en el path, seleccionaremos la ubicación donde se encuentre el car.obj para cargar el modelo del coche en el objeto seleccionado, y darle a "Crear trayectoria".

> [!NOTE] El fichero "Videos_Rotaciones_Circuito.blend", en la carpeta "cuaternion_circuito", es el .blend final en el que se puede probar directamente, sin tener que hacer los pasos de cero utilizando el "ejercicio7.blend" de la práctica 1.

> [!NOTE] Si se desea ver el trazo del camino, seleccionar en las propiedades del objeto "Motion Paths" y darle a "Calculate" o "Update path".

## Vídeos 

A continuación se indica el enlace a YouTube de los vídeos con los contenidos indicados en la práctica.

[Captura de video donde se muestra el funcionamiento de la interfaz creada en blender y sus parámetros.] (https://youtu.be/VUtARhZld3E?si=-KtETLX3xTK0MS57)

[Vídeo renderizado del resultado final utilizando el método de interpolación más adecuado y ángulos de alabeo (inclinación) asignados correctamente a las curvas del circuito. También se encuentra en la descripción del primer vídeo.] (https://youtu.be/f3K-VEeumSE?si=tiEEgSH36P4NtA2E)

---