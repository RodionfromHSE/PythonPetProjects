import argparse
import omegaconf
import os

_CUR_DIR = os.path.dirname(os.path.abspath(__file__))

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default=os.path.join(_CUR_DIR, 'config.yaml'))
    args = parser.parse_args()
    return args

def get_config(args):
    conf = omegaconf.OmegaConf.load(args.config)
    return conf

args = get_args()
conf = get_config(args)
