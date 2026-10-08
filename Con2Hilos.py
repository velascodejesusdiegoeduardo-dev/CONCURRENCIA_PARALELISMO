import cv2
import threading

def convertir_fragmento(video_entrada, inicio, fin, salida):
    cap = cv2.VideoCapture(video_entrada)
    cap.set(cv2.CAP_PROP_POS_FRAMES, inicio)

    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(salida,
                          cv2.VideoWriter_fourcc(*'XVID'),
                          fps, (ancho, alto), isColor=False)

    frame_actual = inicio
    while frame_actual < fin:
        ret, frame = cap.read()
        if not ret:
            break
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out.write(gris)
        frame_actual += 1

    cap.release()
    out.release()

def convertir_video_dos_hilos(video_entrada, video_salida):
    cap = cv2.VideoCapture(video_entrada)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    mitad = total_frames // 2

    hilo1 = threading.Thread(target=convertir_fragmento,
                             args=(video_entrada, 0, mitad, "temp_0.avi"))
    hilo2 = threading.Thread(target=convertir_fragmento,
                             args=(video_entrada, mitad, total_frames, "temp_1.avi"))

    hilo1.start()
    hilo2.start()
    hilo1.join()
    hilo2.join()

    out = cv2.VideoWriter(video_salida,
                          cv2.VideoWriter_fourcc(*'XVID'),
                          fps, (ancho, alto), isColor=False)

    for temp in ["temp_0.avi", "temp_1.avi"]:
        cap_temp = cv2.VideoCapture(temp)
        while True:
            ret, frame = cap_temp.read()
            if not ret:
                break
            out.write(frame)
        cap_temp.release()

    out.release()

# Uso en Pydroid
convertir_video_dos_hilos("video_original.mp4", "video_bn_dos_hilos.avi")