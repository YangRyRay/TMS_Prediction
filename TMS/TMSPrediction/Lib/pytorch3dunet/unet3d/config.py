import argparse

import torch
import yaml
import os

from Lib.pytorch3dunet.unet3d import utils

logger = utils.get_logger('ConfigLoader')


def load_config():
    """
    parser = argparse.ArgumentParser(description='UNet3D')
    parser.add_argument('--config', type=str, help='Path to the YAML config file', required=True)
    args = parser.parse_args()
    """

    yamlpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))+"/resources/test_config_regression.yaml"
    config = _load_config_yaml(yamlpath)
    # Get a device to train on
    device_str = config.get('device', None)
    if device_str is not None:
        logger.info(f"Device specified in config: '{device_str}'")
        device_str = 'cpu'
        if device_str.startswith('cuda') and not torch.cuda.is_available():
            logger.warn('CUDA not available, using CPU')
            device_str = 'cpu'
    else:
        device_str = "cuda:0" if torch.cuda.is_available() else 'cpu'
        logger.info(f"Using '{device_str}' device")

    device = device_str #0#torch.cuda.set_device(0)
    config['device'] = device
    return config


def _load_config_yaml(config_file):
    return yaml.safe_load(open(config_file, 'r'))
