from GlobalHandler import GlobalHandler
import os
from omegaconf import OmegaConf
import argparse

cur_folder = os.path.dirname(os.path.abspath(__file__))
def read_config(path: str):
    conf = OmegaConf.load(path)
    conf = OmegaConf.create(OmegaConf.to_yaml(conf, resolve=True))
    return conf

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default=os.path.join(cur_folder, "config.yaml"), help="Path to config file")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    config = read_config(args.config)
    handler = GlobalHandler(config)
    handler.extract_and_add()
    if input("Clear? (y/n)") == 'y':
        handler.clear()
