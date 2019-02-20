# This file contains different error condition code when request url

bad_code = {400, 401, 403, 403, 404, 405, 406, 407, 409, 410, 411, 412, 414, 415, 416, 417, 418, 422, 425, 426, 428, 431, 451, 502, 504, 505, 511}
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429
retry_code = {408, 413, 429, 503}


# Internal server error 500: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500
# Precondition 428: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/428
