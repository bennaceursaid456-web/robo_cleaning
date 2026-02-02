from collections import defaultdict


class StatsManager:
    def __init__(self):
        self.seen_ids = set()
        self.counts = defaultdict(int)
        self.active_categories = set() # Track what is currently in frame

    def set_active(self, categories):
        """Update the set of categories currently visible in the frame."""
        self.active_categories = categories

    def classify(self, label):
        recyclable = ["bottle", "cup", "bowl", "backpack", "handbag", "suitcase"]
        toxic = ["cell phone", "laptop", "keyboard", "mouse"]
        human = ["person", "dog", "cat"]

        if label in recyclable:
            return "recyclable"
        if label in toxic:
            return "toxic"
        if label in human:
            return "human"
        return "other"

    def update(self, detections):
        for d in detections:
            obj_id = d["id"]
            if obj_id in self.seen_ids:
                continue

            self.seen_ids.add(obj_id)
            category = self.classify(d["label"])
            self.counts[category] += 1

    def get_stats(self):
        return {
            "total_objects": sum(self.counts.values()),
            "recyclable": self.counts["recyclable"],
            "toxic": self.counts["toxic"],
            "human": self.counts["human"],
            "active": list(self.active_categories)
        }
