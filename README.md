# uwf_data

Please, download [archive]() and extract it to project folder.

Использование (запускать из папки проекта):

`python create_dataset.py "task" "cam" "split_ration" "output_dir"`

* task: "cls" for classification,
                 "loc" for localisation,
                 "seg" for segmentation;
* cam: "therm" for thermal,
                 "optic" for optic cam;
* split_ration: three floats, separated with whitespace: train_ratio, test_ratio, val_ratio. *sum(split_ration) must be 1*
`"0.75 0.1 0.05"`
* output_dir - relative path to target folder, where you need to create dataset

Example:

`python create_dataset.py "loc" "optic" "0.7 0.2 0.1" "final_test"`
