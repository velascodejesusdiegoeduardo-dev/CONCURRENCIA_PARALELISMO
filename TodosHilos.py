import cv2
import multiprocessing

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

def convertir_video_todos_hilos(video_entrada, video_salida):
    cap = cv2.VideoCapture(video_entrada)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    num_hilos = multiprocessing.cpu_count()
    fragmento = total_frames // num_hilos

    procesos = []
    for i in range(num_hilos):
        inicio = i * fragmento
        fin = (i + 1) * fragmento if i < num_hilos - 1 else total_frames
        salida = f"temp_{i}.avi"
        p = multiprocessing.Process(target=convertir_fragmento,
                                    args=(video_entrada, inicio, fin, salida))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()

    out = cv2.VideoWriter(video_salida,
                          cv2.VideoWriter_fourcc(*'XVID'),
                          fps, (ancho, alto), isColor=False)

    for i in range(num_hilos):
        cap_temp = cv2.VideoCapture(f"temp_{i}.avi")
        while True:
            ret, frame = cap_temp.read()
            if not ret:
                break
            out.write(frame)
        cap_temp.release()

    out.release()

# Uso en Pydroid
convertir_video_todos_hilos("video_original.mp4", "video_bn_final.avi")