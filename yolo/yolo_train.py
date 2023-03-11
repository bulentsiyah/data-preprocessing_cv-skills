from ultralytics import YOLO
import torch

if __name__ == '__main__':
    print('cuda_avail:', torch.cuda.is_available())
    print('cuda_device:', torch.cuda.device_count())

    data = 'E:/Datasets/Mantis-Shrimp-Eye-s-Collision-Avoidance'+"/yolo_dataset/custom.yaml"
    last_weights = "E:/Codes/data-preprocessing_cv-skills/runs/detect/yolov8x_custom_imgsz_10242/weights/last.pt"

    # Load a model
    model = YOLO(last_weights)  # load a pretrained model (recommended for training)

    # Train the model
    results = model.train(
    data=data,
    imgsz=1024,
    epochs=50,
    batch=8,
    name='yolov8x_custom_imgsz_1024',
    device=0
    )
