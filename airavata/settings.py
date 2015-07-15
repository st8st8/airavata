import os


POLLA_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

## Sites specific files base directory
POLLA_SITES_DIR = os.path.join(POLLA_BASE_DIR, 'sites')

## should dots from domain names be replaced by underscores for
## paths used in templates, staticfiles and urls loaders
POLLA_REPLACE_DOTS_IN_DOMAINS = False
