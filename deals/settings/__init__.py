import os
from .base import *

# Collect the environment state
environment = os.getenv("ENVIRONMENT")

# Import values based upon production or development level
if environment == "production":
    from .production import *
elif environment == "development":
    # To add settings of development
    from .development import *
    # To add settings of  local.py
    from .local import *
