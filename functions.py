def calculate_iou(box1, box2):
    
    # Współrzędne bounding boxa jako (x1, y1, x2, y2)
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    # Obliczenie obszaru przecięcia
    intersection = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
    
    # Obliczenie obszaru sumy
    area_box1 = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    area_box2 = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)
    union = area_box1 + area_box2 - intersection
    
    # Obliczenie IoU
    iou = intersection / union
    
    return iou