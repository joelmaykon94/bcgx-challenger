def l2_distance(a, b):
    """
    Calculates the L2 (Euclidean) distance between two vectors.
    
    Args:
        a (list): First vector.
        b (list): Second vector.
    
    Returns:
        float: The L2 distance between the two vectors.
    """
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5
