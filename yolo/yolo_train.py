from ultralytics import YOLO
import torch


if __name__ == '__main__':
    print('cuda_avail:', torch.cuda.is_available())
    print('cuda_device:', torch.cuda.device_count())

    anapath='E:/Datasets/AmazonAirPrime'

    data = anapath+"/yolo_dataset/custom.yaml"
    # last_weights = "D:/orhan/Belgeler/GitHub/opencv-skills/runs/detect/yolov8x_custom_bs_2/weights/last.pt"

    # Load a model
    model = YOLO("yolo/yolov8x_custom.yaml")  # build a new model from scratch
    # model = YOLO(last_weights)  # load a pretrained model (recommended for training)

    # Train the model

    results = model.train(
    resume=True,
    data=data,
    imgsz=1024,
    epochs=100,
    batch=8,
    name='yolov8x_custom_imgsz_1024',
    device=0
    )

    #model.train(data=data, epochs=2, imgsz=640)