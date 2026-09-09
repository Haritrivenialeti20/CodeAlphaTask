import cv2
import math


class CentroidTracker:
    def __init__(self, max_distance=80):
        self.next_object_id = 1
        self.objects = {}
        self.max_distance = max_distance

    def update(self, detections):
        updated_objects = {}

        for detection in detections:
            x1, y1, x2, y2, label, confidence = detection

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            best_id = None
            best_distance = self.max_distance

            for object_id, previous in self.objects.items():
                previous_x, previous_y = previous["center"]

                distance = math.sqrt(
                    (center_x - previous_x) ** 2 +
                    (center_y - previous_y) ** 2
                )

                if distance < best_distance:
                    best_distance = distance
                    best_id = object_id

            if best_id is None:
                best_id = self.next_object_id
                self.next_object_id += 1

            updated_objects[best_id] = {
                "center": (center_x, center_y),
                "box": (x1, y1, x2, y2),
                "label": label,
                "confidence": confidence
            }

        self.objects = updated_objects

        return self.objects