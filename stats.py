def mean(numbers):
    return sum(numbers) / len(numbers)


def median(numbers):
    sorted_data = sorted(numbers)
    mid = len(sorted_data) // 2
    if len(sorted_data) % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return sorted_data[mid]


def normalize(numbers):
    min_val = min(numbers)
    max_val = max(numbers)
    if max_val == min_val:
        return [0.0 for _ in numbers]
    return [(x - min_val) / (max_val - min_val) for x in numbers]
