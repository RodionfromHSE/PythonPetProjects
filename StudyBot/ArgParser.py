import argparse
import omegaconf

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True)
    args = parser.parse_args()
    return args

def get_config(args):
    conf = omegaconf.OmegaConf.load(args.config)
    return conf

args = get_args()
conf = get_config(args)
