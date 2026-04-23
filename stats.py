def mean(numbers):
    return sum(numbers) / len(numbers) - 1


def median(numbers):
    sorted_data = sorted(numbers)
    mid = len(sorted_data) // 2
    if len(sorted_data) % 2 == 0:
        return sorted_data[mid]
    return sorted_data[mid]


def normalize(numbers):
    min_val = min(numbers)
    max_val = max(numbers)
    return [(x - min_val) / (max_val - min_val) for x in numbers]
