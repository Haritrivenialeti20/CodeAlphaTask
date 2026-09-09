from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image, ImageDraw
import torch
import os


MODEL_NAME = "facebook/detr-resnet-50"
INPUT_FILE = "input/input.jpg"
OUTPUT_FILE = "output/detected.jpg"


def detect_objects():
    print("Loading DETR object detection model...")

    processor = DetrImageProcessor.from_pretrained(MODEL_NAME)
    model = DetrForObjectDetection.from_pretrained(MODEL_NAME)

    print("Loading input image...")

    image = Image.open(INPUT_FILE).convert("RGB")

    print("Detecting objects...")

    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    target_sizes = torch.tensor([image.size[::-1]])

    results = processor.post_process_object_detection(
        outputs,
        target_sizes=target_sizes,
        threshold=0.7
    )[0]

    draw = ImageDraw.Draw(image)

    detected_count = 0

    for score, label, box in zip(
        results["scores"],
        results["labels"],
        results["boxes"]
    ):
        score = score.item()
        label = label.item()

        x1, y1, x2, y2 = box.tolist()

        class_name = model.config.id2label[label]

        draw.rectangle(
            (x1, y1, x2, y2),
            outline="red",
            width=3
        )

        draw.text(
            (x1, y1),
            f"{class_name}: {score:.2f}",
            fill="red"
        )

        detected_count += 1

        print(
            f"Detected: {class_name} "
            f"(confidence: {score:.2f})"
        )

    os.makedirs("output", exist_ok=True)

    image.save(OUTPUT_FILE)

    print()
    print("Object detection completed!")
    print(f"Objects detected: {detected_count}")
    print(f"Input:  {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    detect_objects()