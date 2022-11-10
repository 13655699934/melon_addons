# -*- coding: utf-8 -*-

import os, argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    '--model_dir',
    type=str,
    default=os.path.join(os.path.dirname(__file__), 'fonts')
)
parser.add_argument(
    '--image_file',
    type=str,
    default=''
)
parser.add_argument(
    '--num_top_predictions',
    type=int,
    default=1
)
FLAGS, unparsed = parser.parse_known_args()
