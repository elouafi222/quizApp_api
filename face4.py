from ultralytics import YOLO

model = YOLO("yolov8n.pt")


def main():
    model.train(
        data="C:\\Users\MohammedElouafi\\Desktop\MyWork\\quizApp_api\\quizApp_api\\Dataset\\SplitData\\data.yaml",
        epochs=3,
    )


if __name__ == "__main__":
    main()
