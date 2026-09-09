import cv2
import torch
from transformers import DetrImageProcessor, DetrForObjectDetection
from tracker import CentroidTracker


MODEL_NAME = "facebook/detr-resnet-50"
INPUT_VIDEO = "input/input.mp4"
OUTPUT_VIDEO = "output/tracked.mp4"


def main():
    print("Loading DETR model...")

    processor = DetrImageProcessor.from_pretrained(MODEL_NAME)
    model = DetrForObjectDetection.from_pretrained(MODEL_NAME)

    tracker = CentroidTracker()

    video = cv2.VideoCapture(INPUT_VIDEO)

    if not video.isOpened():
        print(f"Error: Could not open {INPUT_VIDEO}")
        return

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    output = cv2.VideoWriter(
        OUTPUT_VIDEO,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    frame_number = 0

    while True:
        success, frame = video.read()

        if not success:
            break

        frame_number += 1

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        inputs = processor(images=image, return_tensors="pt")

        with torch.no_grad():
            results = model(**inputs)

        target_sizes = torch.tensor([[height, width]])

        detections = processor.post_process_object_detection(
            results,
            target_sizes=target_sizes,
            threshold=0.7
        )[0]

        objects = []

        for score, label, box in zip(
            detections["scores"],
            detections["labels"],
            detections["boxes"]
        ):
            score = score.item()
            label_id = label.item()

            label_name = model.config.id2label[label_id]

            if label_name != "dog":
                continue

            x1, y1, x2, y2 = map(int, box.tolist())

            objects.append(
                (x1, y1, x2, y2, label_name, score)
            )

        tracked_objects = tracker.update(objects)

        for object_id, data in tracked_objects.items():
            x1, y1, x2, y2 = data["box"]
            label = data["label"]
            confidence = data["confidence"]

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"ID {object_id} | {label} {confidence:.2f}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        output.write(frame)

        if frame_number % 10 == 0:
            print(f"Processed frame {frame_number}")

    video.release()
    output.release()

    print()
    print("Object tracking completed!")
    print(f"Output: {OUTPUT_VIDEO}")


if __name__ == "__main__":
    main()