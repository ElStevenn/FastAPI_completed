import json

class LargeFloatEncoder(json.JSONEncoder):
    def encode(self, o):
        def hint_tuples(item):
            if isinstance(item, float):
                if abs(item) > 1e10:  # or some other threshold that fits your data
                    return str(item)
            if isinstance(item, list):
                return [hint_tuples(e) for e in item]
            if isinstance(item, dict):
                return {key: hint_tuples(value) for key, value in item.items()}
            return item

        return super().encode(hint_tuples(o))

