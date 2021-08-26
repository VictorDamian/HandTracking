##############################
##--- VictorDamian
##--- Python 3.7.8 - OpenCV 3.5.3 - Mediapipe - Sys
##--- INFO: https://google.github.io/mediapipe/getting_started/python.html
##############################

import sys
import cv2 as cv
import mediapipe as mp

class HandTracking:
    ### 
    path = "../img/videoEntrada.mp4"
    pathImg="../img/hands.jpg"
    cam = 0

    # Dibuja puntos y conexiones
    points_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    # Redimensiona un video/imagen sin distorcion
    def ResizeVideo(image,window_height):
        aspect_ratio = float(image.shape[1])/float(image.shape[0])
        window_width = window_height/aspect_ratio
        image = cv.resize(image, (int(window_height),int(window_width)))
        return image

    
    # Metodo para configurar parametros
    def ConfigTracking(pathVideo, mode, cHands, prob):    
        # Configuracion
        with HandTracking.mp_hands.Hands(
            # True esta definido para imagenes
            static_image_mode=mode,

            # Num max de manos a tectar
            max_num_hands=cHands,
            
            # Probabilidad de caso exitoso por defecto
            min_detection_confidence=prob
            ) as hands:

            # Gira la img sobres su eje Y para comparar si una mano es izq o der
            pathVideo = cv.flip(pathVideo, 1)
            copyImg = pathVideo.copy()

            # Convierte el video a RGB
            rgb=cv.cvtColor(pathVideo, cv.COLOR_BGR2RGB)

            HandTracking.FindMarks(
                handsDetect=hands,
                videoRGB=rgb, 
                video=copyImg)

    # Metodo para encontrar o acceder a los puntos clave
    def FindMarks(handsDetect,videoRGB, video):

        # muestra: mano, proba, num de manos detectadas 
        results=handsDetect.process(videoRGB)
        print("Results: ", results.multi_handedness)

        # Si existen puntos salta al ciclo para contarlos
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Muestra las coordenas de cara marca
                for mark, coo in enumerate(hand_landmarks.landmark):
                    
                    # Obten el tamaño de video
                    h, w, _ = video.shape

                    # Accede a cada marca individalmente
                    x1, x2 = int(coo.x*w), int(coo.y*h)
                    index = [0,4,8,12,16,20]
                    if mark in index:
                        
                        cv.circle(
                            video, (x1,x2),
                            10,(0,255,0),cv.FILLED)
                        
                        cv.putText(
                            video,
                            str(mark),(x1,x2),
                            cv.FONT_HERSHEY_SIMPLEX,
                            1,(255,255,255),1,
                            cv.LINE_AA)
                            
                        print(
                            f'Mark: 'f'{mark}'f' Coor: ('
                            f'{x1}, '
                            f'{x2})')

                # Dibuja las lineas y puntos clave
                HandTracking.points_drawing.draw_landmarks(
                    video,
                    # Dibuja solo los puntos 
                    hand_landmarks,
                    # Dibuja las conecciones entre los puntos
                    HandTracking.mp_hands.HAND_CONNECTIONS)

            video = cv.flip(video, 1)
            cv.imshow("HandTracking - Mediapipe", video)


    def OpenVideoOrCam(video):
        cap = cv.VideoCapture(video if video else 0)
        if not cap.isOpened():
            print("No se puede abrir la camara")
        while True:
            # captura cada frame
            success, frame = cap.read()
            if not success:
                print("Error frame.")
                break
            # si es correcto aqui ejecuta operaciones

            resizeFrame = HandTracking.ResizeVideo(
                image=frame, 
                window_height=800)
                
            HandTracking.ConfigTracking(
                pathVideo=resizeFrame, mode=True,
                cHands=1, prob=0.5
            )
            
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        # termina la captura
        cap.release()
        cv.destroyAllWindows()

    def OpenImage(image):
        image = cv.imread(cv.samples.findFile(image))
        if image is None:
            sys.exit("No se pudo leer la imagen")
        # Metodos
        resizeFrame = HandTracking.ResizeVideo(
                image=image, 
                window_height=900)

        HandTracking.ConfigTracking(
            pathVideo=resizeFrame, 
            mode=False, cHands=2, 
            prob=0.5
        )

        #cv.imshow("Window", image)
        k = cv.waitKey(0)
        if k==ord('s'):
            cv.imwrite('example.jpg', image)
        cv.destroyAllWindows()

#-- parametro 'cam' para abrir la camara
#HandTracking.OpenVideoOrCam(video=HandTracking.path)
#--
HandTracking.OpenImage(HandTracking.pathImg)