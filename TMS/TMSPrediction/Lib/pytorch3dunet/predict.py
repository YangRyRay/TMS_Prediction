import importlib
import os
import sys
# sys.path.append("/home/jq748/TMS/pytorch-3dunet-master-test/")
import torch
import torch.nn as nn

import time

from Lib.pytorch3dunet.datasets.utils import get_test_loaders
from Lib.pytorch3dunet.unet3d import utils
from Lib.pytorch3dunet.unet3d.config import load_config
from Lib.pytorch3dunet.unet3d.model import get_model

logger = utils.get_logger('UNet3DPredict')


def _get_predictor(model, output_dir, config):
    predictor_config = config.get('predictor', {})
    class_name = predictor_config.get('name')

    m = importlib.import_module('Lib.pytorch3dunet.unet3d.predictor')
    predictor_class = getattr(m, class_name)

    return predictor_class(model, output_dir, config, **predictor_config)


def main():

    # Load configuration
    config = load_config()

    # Create the model
    model = get_model(config['model'])

    # Load model state
    # model_path = config['model_path']
    model_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.pardir,os.pardir,"TMS_Params/last_checkpoint.pytorch"))
    logger.info(f'Loading model from {model_path}...')
    utils.load_checkpoint(model_path, model)

    if torch.cuda.device_count() == 0:
        device = "cpu"
    else:
        device = "cuda"

    # use DataParallel if more than 1 GPU available
    if torch.cuda.device_count() > 1 and not device == 'cpu':
        model = nn.DataParallel(model)
        logger.info(f'Using {torch.cuda.device_count()} GPUs for prediction')

    logger.info(f"Sending the model to '{device}'")
    model = model.to(device)

    output_dir = config['loaders'].get('output_dir', None)
    if output_dir is not None:
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f'Saving predictions to: {output_dir}')

    # create predictor instance
    predictor = _get_predictor(model, output_dir, config)

    for test_loader in get_test_loaders(config):
        # run the model prediction on the test_loader and save the results in the output_dir
        result=predictor(test_loader)
    return result

if __name__ == '__main__':
    main()
