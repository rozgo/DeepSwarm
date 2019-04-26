# Copyright (c) 2019 Edvinas Byla
# Licensed under MIT License

import argparse
import os
import operator
import sys
from yaml import load, Loader
from pathlib import Path
from shutil import copyfile

# Create argument parser which allows users to pass a custom script name
# If user didn't pass a custom script name then use sys.argv[0]
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--script_name', default=os.path.basename(sys.argv[0]),
    help='Name which should be used to load the settings file, default value is the name of invoked script')
args = parser.parse_args()

# Retrieve name without the extension
script_name = args.script_name
filename = os.path.splitext(script_name)[0]

# If mnist yaml doesn't exist it means package was installed via pip in which
# case we should use current working directory as the base path
base_path = Path(os.path.dirname(os.path.dirname(__file__)))
if not (base_path / 'settings' / 'mnist.yaml').exists():
    module_path = base_path
    # Change the base path to current working directory
    base_path = Path(os.getcwd())
    settings_directory = (base_path / 'settings')
    # Create settings directory if it doesn't exist
    if not settings_directory.exists():
        settings_directory.mkdir()
    # If default settings file doesn't exist, copy one from the module directory
    module_default_config = module_path / 'settings/default.yaml'
    settings_default_config = settings_directory / 'default.yaml'
    if not settings_default_config.exists() and module_default_config.exists():
        copyfile(module_default_config, settings_default_config)

# As the base path is now configured we try to load configuration file
# associated  with the filename
settings_directory = base_path / 'settings'
settings_file_path = Path(settings_directory, filename).with_suffix('.yaml')

# If file doesn't exist fallback to default settings file
if not settings_file_path.exists():
    settings_file_path = Path(settings_directory, 'default').with_suffix('.yaml')

# Read settings file
with open(settings_file_path, 'r') as settings_file:
    settings = load(settings_file, Loader=Loader)

# Add script name to settings, so it's added to the log
settings['script_name'] = script_name

# Create convenient variables
cfg = settings["DeepSwarm"]
nodes = settings["Nodes"]
left_cost_is_better = operator.le if cfg['metrics'] == 'loss' else operator.ge
