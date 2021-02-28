"""This file defines the configuration file template.

type:      Determines the valid type for this key.
default:   Gives a default value if none was defined.
valid:     List of valid values for this key.
regexp:    Regexp expression for valid values of this key.
required:  Determines if this key is requuired or not.
childs:    Defines child nodes if key is a list or dictionary.
"""
from ..defaults import DEF_SCRAPE_TIMEOUT
from ..defaults import DEF_SRV_LISTEN_ADDR, DEF_SRV_LISTEN_PORT
from ..defaults import DEF_REQUEST_METHOD, DEF_REQUEST_TIMEOUT


CONFIG_TEMPLATE = {
    "scrape_timeout": {
        "type": int,
        "default": DEF_SCRAPE_TIMEOUT,
        "required": False,
        "allowed": "^[0-9]+$",
        "childs": {},
    },
    "listen_addr": {
        "type": str,
        "default": DEF_SRV_LISTEN_ADDR,
        "required": False,
        "childs": {},
    },
    "listen_port": {
        "type": int,
        "default": DEF_SRV_LISTEN_PORT,
        "required": False,
        "allowed": "^[0-9]+$",
        "childs": {},
    },
    "targets": {
        "type": list,
        "required": True,
        "childs": {
            "name": {
                "type": str,
                "required": True,
                "childs": {},
            },
            "groups": {
                "type": dict,
                "required": False,
                "default": {},
                "childs": {},
            },
            "url": {
                "type": str,
                "required": True,
                "childs": {},
            },
            "method": {
                "type": str,
                "required": False,
                "default": DEF_REQUEST_METHOD,
                "allowed": "^(get|options|head|post|put|patch|delete)$",
                "childs": {},
            },
            "params": {
                "type": dict,
                "required": False,
                "default": {},
                "childs": {},
            },
            "headers": {
                "type": dict,
                "required": False,
                "default": {},
                "childs": {},
            },
            "timeout": {
                "type": (int, float),
                "required": False,
                "default": DEF_REQUEST_TIMEOUT,
                "childs": {},
            },
            "redirect": {
                "type": bool,
                "required": False,
                "default": False,
                "childs": {},
            },
            "basic_auth": {
                "type": dict,
                "required": False,
                "default": {},
                "childs": {
                    "username": {
                        "type": str,
                        "required": False,
                        "childs": {},
                    },
                    "password": {
                        "type": str,
                        "required": False,
                        "childs": {},
                    },
                },
            },
            "digest_auth": {
                "type": dict,
                "required": False,
                "default": {},
                "childs": {
                    "username": {
                        "type": str,
                        "required": False,
                        "childs": {},
                    },
                    "password": {
                        "type": str,
                        "required": False,
                        "childs": {},
                    },
                },
            },
            "fail_if": {
                "type": dict,
                "required": False,
                "default": {},
                "childs": {
                    "header_matches_regexp": {
                        "type": list,
                        "required": False,
                        "default": [],
                        "childs": {
                            "header": {
                                "type": str,
                                "required": True,
                                "childs": {},
                            },
                            "allow_missing": {
                                "type": bool,
                                "required": True,
                                "childs": {},
                            },
                            "regexp": {
                                "type": str,
                                "required": True,
                                "childs": {},
                            },
                        },
                    },
                    "header_not_matches_regexp": {
                        "type": list,
                        "required": False,
                        "default": [],
                        "childs": {
                            "header": {
                                "type": str,
                                "required": True,
                                "childs": {},
                            },
                            "allow_missing": {
                                "type": bool,
                                "required": True,
                                "childs": {},
                            },
                            "regexp": {
                                "type": str,
                                "required": True,
                                "childs": {},
                            },
                        },
                    },
                },
            },
            "extract": {
                "type": dict,
                "required": False,
                "default": {},
                "childs": {},
            },
        },
    },
}

# targets:
#     fail_if:
#         regexp_header_matches:
#             - header: Set-Cookie
#               allow_missing: True
#               regexp: '.*'
#         regexp_header_not_matches: []
#         regexp_body_matches: []
#         regexp_body_not_matches: []
#         response_time_lt: 30
#         response_time_gt: 60
#         response_size_lt: 50
#         response_size_gt: 50
#         status_code_in: []
#         status_code_not_int: []
