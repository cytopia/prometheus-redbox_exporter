"""Read yaml configuration file and return a parsed dictionary."""

from typing import Dict, List, Any

import argparse
import errno
import os
import re
import yaml

from .types import DsConfig
from .types import DsTarget
from .template import CONFIG_TEMPLATE


def _read_config_file(path: str) -> Dict[Any, Any]:
    """Load configuration file and return yaml dictionary.

    Args:
        path (str): Path to configuration file.

    Returns:
        dict: Configuration in yaml format (Python dict).

    Raises:
        OSError: If file not found or yaml cannot be parsed.
    """
    try:
        file_p = open(path)
    except FileNotFoundError as err_file:
        error = os.strerror(errno.ENOENT)
        raise OSError(f"[ERROR] {error}: {path}") from err_file
    except PermissionError as err_perm:
        error = os.strerror(errno.EACCES)
        raise OSError(f"[ERROR] {error}: {path}") from err_perm
    else:
        try:
            return dict(yaml.safe_load(file_p))
        except yaml.YAMLError as err_yaml:
            error = str(err_yaml)
            raise OSError(f"[ERROR]: {path}\n{error}") from err_yaml
        finally:
            file_p.close()


def _check_duplicate_targets(targets: List[Any]) -> None:
    """Check if "- name" key has duplicate values.

    Args:
        config (dict): Yaml configuration.

    Raises:
        OSError: If configuration file is not valid.
    """
    names = []
    for index, target in enumerate(targets):
        name = target["name"]
        if name in names:
            raise OSError(f"[CONFIG-FAIL] conf[target][{index}[name] has duplicate value '{name}'")
        names.append(name)


def _check_config(section: str, config: Dict[Any, Any], template: Dict[Any, Any]) -> None:
    """Recursively check configuration.

    Args:
        section (str): Name of the current section to validate.
        config (dict): Yaml configuration.
        template (dict): Configuration template.

    Raises:
        OSError: If configuration file is not valid.
    """
    for key in template:
        # print(f"[CONFIG-INFO] checking {section}[{key}]")

        # Check Required
        if template[key]["required"] and key not in config:
            raise OSError(f"[CONFIG-FAIL] {section}[{key}] not defined, but required")

        # Check Type
        if key in config and not isinstance(config[key], template[key]["type"]):
            req_type = template[key]["type"]
            raise OSError(f"[CONFIG-FAIL] {section}[{key}] must be of type: {req_type}")

        # Check Allowed value by Regex
        if key in config and "allowed" in template[key]:
            regex = template[key]["allowed"]
            value = str(config[key])
            regobj = re.compile(regex)
            if regobj.match(value) is None:
                raise OSError(f"[CONFIG-FAIL] {section}[{key}] = '{value}' must match: '{regex}'")

        # Recurse into childs
        if template[key]["childs"]:
            if key in config and isinstance(config[key], dict):
                _check_config(section + f"[{key}]", config[key], template[key]["childs"])
            if key in config and isinstance(config[key], list):
                for index, value in enumerate(config[key]):
                    _check_config(
                        section + f"[{key}][{index}]", config[key][index], template[key]["childs"]
                    )


def _merge_defaults(
    section: str, config: Dict[Any, Any], template: Dict[Any, Any]
) -> Dict[Any, Any]:
    """Recursively merge configuration with defined default values from template.

    Args:
        section (str): Name of the current section to validate.
        config (dict): Yaml configuration.
        defaults (dict): Default values.

    Returns:
        dict: Final configuration file.
    """
    for key in template:
        # print(f"[CONFIG-INFO] checking {section}[{key}]")

        # Recurse into childs
        if template[key]["childs"] and "default" not in template[key]:
            if key in config:
                if template[key]["type"] == list:
                    for index, value in enumerate(config[key]):
                        config[key][index] = _merge_defaults(
                            section + f"[{key}][{index}]",
                            value,
                            template[key]["childs"],
                        )
                else:
                    config[key] = _merge_defaults(
                        section + f"[{key}]", config[key], template[key]["childs"]
                    )
        # Flat default values
        else:
            if key not in config and "default" in template[key]:
                config[key] = template[key]["default"]

    return config


def get_config(args: argparse.Namespace) -> DsConfig:
    """Return configuration file as dictionary.

    Args:
        args (dict): Parsed command line arguments

    Returns:
        dict: Configuration

    Raises:
        OSError: If file not found, invalid yaml or invalid config.
    """
    conf = _read_config_file(args.conf)

    # Validate
    _check_config("conf", conf, CONFIG_TEMPLATE)
    _check_duplicate_targets(conf["targets"])

    # Merge with defaults
    conf = _merge_defaults("conf", conf, CONFIG_TEMPLATE)

    # Override with command line arguments if exist
    if args.listen is not None:
        conf["listen_addr"] = args.listen
    if args.port is not None:
        conf["listen_port"] = args.port

    # Return with correct data type
    return DsConfig(
        conf["scrape_timeout"],
        conf["listen_addr"],
        conf["listen_port"],
        [DsTarget(target) for target in conf["targets"]],
    )
