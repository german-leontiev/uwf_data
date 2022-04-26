import shutil
import sys
from pathlib import Path
import random
import sys
import pandas as pd

ROOT = "root_3"

task = sys.argv[1]
cam = sys.argv[2]
split_ration = tuple(float(i) for i in sys.argv[3].split(" "))
output_dir = sys.argv[4]

PARAMS = [task, cam, split_ration, output_dir]



def copy_resourses(id_, task_, split_, labels_index, output_dir):
    src_img = f'{ROOT}/images/{id_}.jpg'

    if task_ == "cls":
        label = "fire" if int(labels_index.iloc[int(id_, 16), 0]) == 1 else "no_fire"
        dst_img = f'{output_dir}/{split_}/images/{label}/{id_}.jpg'
        Path.mkdir(Path(dst_img).parent, parents=True, exist_ok=True)

    if task_ == "loc":
        dst_img = f'{output_dir}/{split_}/images/{id_}.jpg'

        src_bb = f'{ROOT}/bboxes/{id_}.csv'
        dst_bb = f"{output_dir}/{split_}/images/{id_}.txt"
        Path.mkdir(Path(dst_img).parent, parents=True, exist_ok=True)
        shutil.copyfile(src_bb, dst_bb)

    if task_ == "seg":
        dst_img = f'{output_dir}/{split_}/images/{id_}.jpg'

        src_mask = f'{ROOT}/masks/{id_}.jpg'
        dst_mask = f"{output_dir}/{split_}/masks/{id_}.jpg"
        Path.mkdir(Path(dst_mask).parent, parents=True, exist_ok=True)
        shutil.copyfile(src_mask, dst_mask)

    Path.mkdir(Path(dst_img).parent, parents=True, exist_ok=True)
    shutil.copyfile(src_img, dst_img)


def split_data(index_list, split_ration):
    assert 0.99 < sum((0.7, 0.2, 0.1)) < 1.01, (f"Неверные доли разбивки {split_ration}")

    n = len(index_list)
    tr_n = int(split_ration[0] * n)
    te_n = int(split_ration[1] * n)
    va_n = n - te_n - tr_n

    tr_l, te_l, va_l = [], [], []

    for _ in range(tr_n):
        ch_ = random.choice(index_list)
        tr_l.append(ch_)
        index_list.remove(ch_)

    for _ in range(te_n):
        ch_ = random.choice(index_list)
        te_l.append(ch_)
        index_list.remove(ch_)

    va_l = index_list

    return {key: val for key, val in zip(("train", "test", "val"), (tr_l, te_l, va_l))}


# task_filter
def task_filter(task, labels_index):
    assert task in ["cls", "loc", "seg"], (f"Wrong task param \"{task}\" !")
    if task == "cls":
        return True
    if task == "loc":
        return d.bboxes
    return d["mask"]


cam_filter = lambda c_: d.thermal if c_ == "thermal" else ~d.thermal


def gen_dataset(task: str,
                cam: str = "optic",
                split_ration: tuple = (0.8, 0.15, 0.5),
                output_dir: str = "./default/",
                ):
    """
    Generates dataset with suitable parameters

    :param task: "cls" for classification,
                 "loc" for localisation,
                 "seg" for segmentation;
    :param cam:  "therm" for thermal,
                 "optic" for optic cam;
    :param split_ration: tuple of three floats: train_ratio, test_ratio, val_ratio
                         sum(split_ration) must be 1
    :param output_dir:   relative path for dataset creation

    """

    labels_index = pd.read_csv(f"{ROOT}/labels.csv", sep=";", header=None, index_col=0)

    # Labels fix
    t = labels_index.iloc[:, :2]
    t_v = labels_index[1].values
    t_v = [int(i) if len(i) == 1 else int(i[2]) for i in t_v]
    labels_index[1] = t_v

    # Filtering images
    print(task)
    df_filter = task_filter(task, labels_index) & cam_filter(cam)
    index_list = d[df_filter].index

    if len(index_list):
        print(f"Found {len(index_list)} images for current parameters.\nCreating dataset")
    else:
        print("No images found for current parameters")

    # Copying data
    for split, i_val in split_data(list(index_list), split_ration).items():
        for hex_id in i_val:
            copy_resourses(hex_id, task, split, labels_index, output_dir)

    print("Dataset created!")

d = pd.read_csv("index.csv", index_col="hex")

gen_dataset(*PARAMS)