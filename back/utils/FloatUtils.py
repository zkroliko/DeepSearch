FP_TOLERANCE = 1e-05


# This has a floating point comparison
def is_close(first, second):
    return True if abs(first - second) < FP_TOLERANCE else False
