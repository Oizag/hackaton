import cv2
import numpy as np
from collections import deque
from keras.models import load_model
from concurrent.futures import ThreadPoolExecutor
import time
import jsonify


def start_analyse(filename):
    # Загрузка модели для обнаружения объектов (например, YOLO)
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

    data_moves = {}
    all_moves = []

    # Загрузка классов для YOLO
    with open("coco.names", "r") as f:
        classes = f.read().strip().split("\n")

    # Загрузка модели для определения действий человека
    LRCN_model = load_model('LRCN_model_Date_Time_2023_11_08_02_11_04_Loss_1_5871212482452393.h5')

    # Откройте видеопоток
    cap = cv2.VideoCapture("videos/video4.mp4")
    # cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    # frame_width = 640
    # frame_height = 360

    # Создайте объект VideoWriter для записи видео
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, fps, (frame_width, frame_height))

    IMAGE_HEIGHT, IMAGE_WIDTH = 64, 64
    SEQUENCE_LENGTH = 20
    frames_queue = deque(maxlen=SEQUENCE_LENGTH)

    lis = ['drink',
        'eat',
        'run',
        'sit',
        'talk',
        'stand',
        'walk']

    CLASSES_LIST = lis
    action_counts = {action: 0 for action in CLASSES_LIST}

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (frame_width, frame_height))

        # Получите высоту и ширину кадра
        height, width = frame.shape[:2]

        # Подготовьте кадр для обнаружения объектов
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (160, 160), (0, 0, 0), True, crop=False)
        net.setInput(blob)

        # Получите идентификаторы классов, оценки уверенности и ограничивающие прямоугольники
        layer_names = net.getUnconnectedOutLayersNames()
        outs = net.forward(layer_names)

        class_ids = []
        confidences = []
        boxes = []

        max_confidence = 0
        person_box = None

        for outf in outs:
            for detection in outf:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and class_id == 0:  # 0 - индекс класса для человека
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

                    if confidence > max_confidence:
                        max_confidence = confidence
                        person_box = (x, y, w, h)

        # Примените подавление немаксимумов для устранения дублирующихся ограничивающих прямоугольников
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.4)

        # Определите действие человека
        if person_box is not None:
            x, y, w, h = person_box

            # Обрежьте и подготовьте кадр для определения действия
            cropped_frame = frame[y:y+h, x:x+w]
            if not cropped_frame.size:
                continue
            resized_frame = cv2.resize(cropped_frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
            normalized_frame = resized_frame / 255.0
            frames_queue.append(normalized_frame)

            if len(frames_queue) == SEQUENCE_LENGTH:
                sequence = np.array(frames_queue)
                predicted_labels_probabilities = LRCN_model.predict(np.expand_dims(sequence, axis=0))[0]
                predicted_label = np.argmax(predicted_labels_probabilities)
                predicted_confidence = predicted_labels_probabilities[predicted_label]
                for idx, class_name in enumerate(CLASSES_LIST):
                    predicted_confidence = predicted_labels_probabilities[idx]
                    if 0 <= predicted_label < len(CLASSES_LIST):
                        predicted_class_name = CLASSES_LIST[predicted_label]
                    else:
                        predicted_class_name = "Unknown"
                action_counts[predicted_class_name] += 1

                # # Рисуем прямоугольник и подписываем действие человека
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # label = f"Action: {predicted_class_name}, Confidence: {predicted_confidence:.2f}"
                # cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                # cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if predicted_class_name not in all_moves:
                    all_moves.append(predicted_class_name)



        # Запишите текущий кадр в файл видео
        out.write(frame)

    # Освободите ресурсы и закройте окно OpenCV
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return {'popular': all_moves}