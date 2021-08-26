# HandTracking

Este proyecto fue desarrollado utilizando la herramienta de [Media Pipe](https://google.github.io/mediapipe/getting_started/python.html)

### Aspectos a tomar en cuenta, los siguientes parametros para configurar el metodo pueden variar segun sea su proposito

> static_image_mode=True

- Puede cambiar a False que esta por defecto, aplica solo para imagenes cuando esta en este estado. Cuando esta en True es recomendado para Stream.

> max_num_hands=2 

- Es la capacidad maxima en la que puede encontrar el numero de manos, es decir 2 0 1

> min_detection_confidence=0.5

- Es el valor maximo de caso de exito en el que puede encontrar el objeto

## Estilos predeterminados

#### Existe una manera de dibujar los puntos detecados de manera ya implementada, tal es el caso de:

> mp_drawing_styles.get_default_hand_landmarks_style()
> mp_drawing_stylesget_default_hand_connections_style()

### Ambos ya implementan lineas de dibujo predefinidas
