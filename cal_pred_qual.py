import argparse
from pathlib import Path
import os
from functions import calculate_iou

class num_cars:
    def __init__(self, filename, quan_test, quan_det, diff, iou, testbox, detectbox, mean_iou):
        self.name = filename
        self.quan_test = quan_test
        self.quan_det = quan_det
        self.diff = diff
        self.iou = iou
        self.testbox = testbox
        self.detectbox = detectbox
        self.mean_iou = mean_iou

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]

parser = argparse.ArgumentParser()
parser.add_argument('--tlds', type = str, default = ROOT / "datasets/car_dataset/test/labels", help='Path to test label data set')
parser.add_argument('--dlds', type = str, default = ROOT / "runs/detect/yolov5s_b32_e10_car_det", help='Path to detect label data set')
args = parser.parse_args()

ncpf = []
directory_test = ROOT / args.tlds
os.chdir(directory_test)
contents = os.listdir(directory_test)
for item in contents: # Iteracja po współrzędnych bounding-boxów w zbiorze testowym
    box = []
    f = open(item)
    det_cars = 0
    for line in f:
        det_cars += 1
        columns = line.split(' ')
        box.append((float(columns[1]), float(columns[2]), float(columns[3]), float(columns[4])))
    f.close()
    ncpf.append(num_cars(filename = item, quan_test = det_cars, quan_det = 0, diff = 0, iou = 0, testbox=box, detectbox=0, mean_iou=0))

directory_detect = ROOT / args.dlds
os.chdir(directory_detect)
contents = os.listdir(directory_detect)
for item in contents: # Iteracja po współrzędnych bounding-boxów otrzymanych w wyniku detekcji
    box = []
    f = open(item)
    det_cars = 0
    for line in f:
        det_cars += 1
        columns = line.split(' ')
        box.append((float(columns[1]), float(columns[2]), float(columns[3]), float(columns[4])))
    f.close()
    for obj in ncpf:
        if obj.name == item:
            obj.quan_det = det_cars
            obj.detectbox = box
            obj.diff = abs(obj.quan_test - obj.quan_det)
            iou = []
            if len(obj.detectbox) != 0 and len(obj.testbox) != 0:
                if len(obj.detectbox) >= len(obj.testbox): # Są brane pod uwagę tylko bounding-boxy niezerowe
                    for x in range(0, len(obj.testbox)):
                        iou.append(calculate_iou(obj.testbox[x], obj.detectbox[x]))
                else:
                    for x in range(0, len(obj.detectbox)):
                        iou.append(calculate_iou(obj.testbox[x], obj.detectbox[x]))
            obj.iou = iou 
            obj.mean_iou = sum(obj.iou)/len(obj.iou)  

bct = 0
bco = 0
bo = 0
sum_ovr_iou = 0
for obj in ncpf:
    sum_ovr_iou += obj.mean_iou 
    bct += obj.quan_test
    bco += obj.quan_det
    bo += obj.diff

mean_ovr_iou = sum_ovr_iou / len(ncpf)
print(f"Liczba boundingbox w zbiorze testowym: {bct}")
print(f"Liczba boundingbox wykryta przez algorytm po detekcji: {bco}")
print(f"Liczba błędnie rozpoznanych bounding-boxów: {bo}")
print(f"Liczba błędów rozpoznanmych bounding-boxów (%): {bo/bct * 100}%")
print(f"Średnia wartość iou na cały zbiór: {mean_ovr_iou}")
