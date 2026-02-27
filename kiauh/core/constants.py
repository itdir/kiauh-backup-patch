# ======================================================================= #
#  Copyright (C) 2020 - 2026 Dominik Willner <th33xitus@gmail.com>        #
#                                                                         #
#  This file is part of KIAUH - Klipper Installation And Update Helper    #
#  https://github.com/dw-0/kiauh                                          #
#                                                                         #
#  This file may be distributed under the terms of the GNU GPLv3 license  #
# ======================================================================= #

import os
import pwd
from pathlib import Path

# global dependencies
GLOBAL_DEPS = ["git", "wget", "curl", "unzip", "dfu-util", "python3-virtualenv"]

# strings
INVALID_CHOICE = "Invalid choice. Please select a valid value."

# current user
CURRENT_USER = pwd.getpwuid(os.getuid())[0]

# base directory for all component and extension installations
# Defaults to the current user's home directory. Override with the
# KIAUH_BASE_DIR environment variable to support system-wide installs
# (e.g. /opt/kiauh, /srv/kiauh).
_base_dir_env = os.environ.get("KIAUH_BASE_DIR", "").strip()
BASE_DIR = Path(_base_dir_env) if _base_dir_env and Path(_base_dir_env).is_absolute() else Path.home()

# dirs
SYSTEMD = Path("/etc/systemd/system")
NGINX_SITES_AVAILABLE = Path("/etc/nginx/sites-available")
NGINX_SITES_ENABLED = Path("/etc/nginx/sites-enabled")
NGINX_CONFD = Path("/etc/nginx/conf.d")
