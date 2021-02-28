"""This file defines all module wide default values."""

# Credits
DEF_NAME = "redbox_exporter"
DEF_DESC = "Prometheus exporter that throws stuff to httpd endpoints and evaluates their response."
DEF_VERSION = "0.1.3"
DEF_AUTHOR = "cytopia"
DEF_GITHUB = "https://github.com/cytopia/prometheus-redbox_exporter"

# Web server defaults
DEF_SRV_LISTEN_ADDR = "0.0.0.0"
DEF_SRV_LISTEN_PORT = 8080

DEF_SCRAPE_TIMEOUT = 29

# HTTP check defaults
DEF_REQUEST_METHOD = "get"
DEF_REQUEST_TIMEOUT = 60
DEF_REQUEST_USERAGENT = "RedBox Exporter/" + DEF_VERSION


# https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
STATUS_CODE_DESC = {
    "0": "Timeout",
    "100": "INFO: Continue",
    "101": "INFO: Switching Protocols",
    "102": "INFO: Processing",
    "103": "INFO: Early Hints",
    "200": "SUCCESS: OK",
    "201": "SUCCESS: Created",
    "202": "SUCCESS: Accepted",
    "203": "SUCCESS: Non-Authoritative Information",
    "204": "SUCCESS: No Content",
    "205": "SUCCESS: Reset Content",
    "206": "SUCCESS: Partial Content",
    "207": "SUCCESS: Multi-Status",
    "208": "SUCCESS: Already Reported",
    "226": "SUCCESS: IM Used",
    "300": "REDIRECT: Multiple Choices",
    "301": "REDIRECT: Moved Permanently",
    "302": "REDIRECT: Found",
    "303": "REDIRECT: See Other",
    "304": "REDIRECT: Not Modified",
    "305": "REDIRECT: Use Proxy",
    "306": "REDIRECT: Switch Proxy",
    "307": "REDIRECT: Temporary Redirect",
    "308": "REDIRECT: Permanent Redirect",
    "400": "CLIENT ERROR: Bad Request",
    "401": "CLIENT ERROR: Unauthorized",
    "402": "CLIENT ERROR: Payment Required",
    "403": "CLIENT ERROR: Forbidden",
    "404": "CLIENT ERROR: Not Found",
    "405": "CLIENT ERROR: Method Not Allowed",
    "406": "CLIENT ERROR: Not Acceptable",
    "407": "CLIENT ERROR: Proxy Authentication Required",
    "408": "CLIENT ERROR: Request Timeout",
    "409": "CLIENT ERROR: Conflict",
    "410": "CLIENT ERROR: Gone",
    "411": "CLIENT ERROR: Length Required",
    "412": "CLIENT ERROR: Precondition Failed",
    "413": "CLIENT ERROR: Payload Too Large",
    "414": "CLIENT ERROR: URI Too Long",
    "415": "CLIENT ERROR: Unsupported Media Type",
    "416": "CLIENT ERROR: Range Not Satisfiable",
    "417": "CLIENT ERROR: Expectation Failed",
    "418": "CLIENT ERROR: I'm a teapot",
    "421": "CLIENT ERROR: Misdirected Request",
    "422": "CLIENT ERROR: Unprocessable Entity",
    "423": "CLIENT ERROR: Locked",
    "424": "CLIENT ERROR: Failed Dependency",
    "425": "CLIENT ERROR: Too Early",
    "426": "CLIENT ERROR: Upgrade Required",
    "428": "CLIENT ERROR: Precondition Required",
    "429": "CLIENT ERROR: Too Many Requests",
    "431": "CLIENT ERROR: Request Header Fields Too Large",
    "451": "CLIENT ERROR: Unavailable For Legal Reasons",
    "500": "Internal Server Error",
    "501": "Not Implemented",
    "502": "Bad Gateway",
    "503": "Service Unavailable",
    "504": "Gateway Timeout",
    "505": "HTTP Version Not Supported",
    "506": "Variant Also Negotiates",
    "507": "Insufficient Storage",
    "508": "Loop Detected",
    "510": "Not Extended",
    "511": "Network Authentication Required",
    # "": "",
    # "": "",
    # "": "",
    # "": "",
    # "": "",
}
