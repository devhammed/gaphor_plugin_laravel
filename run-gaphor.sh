#!/usr/bin/env bash

poetry build && python3 -m pip uninstall gaphor_plugin_laravel -y && python3 -m pip install dist/gaphor_plugin_laravel-0.1.0-py3-none-any.whl && gaphor
