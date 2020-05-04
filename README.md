# Token Bucket Simulator


## Descripción

Pequeño proyecto para la universidad de Granada. Consiste en un simulador del algoritmo "Cubo de testigos" implementado por distintos sistemas para regular la banda ancha disponible en un dispositivo con el fin de moldear el tráfico según las necesidades particulares, muchas veces para cumplir un contrato de QoS con un cliente por parte de un proovedor de servicio.

# Código

En el repositorio se encuentran los módulos token_bucket.py y tbmain.py. El primero contiene la clase TokenBucket, donde están implementados tanto el algoritmo del cubo de testigos, como distintas políticas que puede segir, además del paso de un tiempo ficticeo, distintas variables de configuración como el tamaño del cubo o un sistema para incorporar un envío de tráfico a un supuesto dispositivo que implemente este sistema.

En general, un código que haga uso de esta clase deberá crear un patrón consistente en una lista de túplas. Cada tupla representa un número de paquetes y el tamaño medio de estos. También deberá de cambiar el "mode" de la instancia a 1,2 o 3, dependiendo de la política que se desee representar y deberá ejecutar el método begin() para observar los resultados.

Se incorpora también el módulo tbmain.py como módulo principal de ejemplo que hace uso de la clase TokenBucket y cuenta con su propio interfaz visual para hacer la configuración de la clase tribial al usuario.

## Requisitos

Es necesario tener instalado **matplotlib** de **pyplot** para visualizar los resultados. [enlace](https://matplotlib.org/)

Si se desea hacer uso del "main" proporcionado, también se ha de tener instalado tkinter. En caso contrario, ver [este enlace](https://riptutorial.com/tkinter/example/3206/installation-or-setup)
