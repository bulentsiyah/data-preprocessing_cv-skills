import cv2

from algorithms.dense_optical_flow import dense_optical_flow
from algorithms.lucas_kanade import lucas_kanade_method


def main():

    choices=["farneback", "lucaskanade", "lucaskanade_dense", "rlof"]
    args_algorithm = choices[0]
    video_path = "_videos/s1000_otonom_test_1_nisan_2022.mp4"
    if args_algorithm == "lucaskanade":
        lucas_kanade_method(video_path)
    elif args_algorithm == "lucaskanade_dense":
        method = cv2.optflow.calcOpticalFlowSparseToDense
        dense_optical_flow(method, video_path, to_gray=True)
    elif args_algorithm == "farneback":
        method = cv2.calcOpticalFlowFarneback
        params = [0.5, 3, 15, 3, 5, 1.2, 0]  # Farneback's algorithm parameters
        dense_optical_flow(method, video_path, params, to_gray=True)
    elif args_algorithm == "rlof":
        method = cv2.optflow.calcOpticalFlowDenseRLOF
        dense_optical_flow(method, video_path)


if __name__ == "__main__":
    main()
