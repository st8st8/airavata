import os


AIRAVATA_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

## Sites specific files base directory
AIRAVATA_SITES_DIR = os.path.join(AIRAVATA_BASE_DIR, 'sites')

## should dots from domain names be replaced by underscores for
## paths used in templates, staticfiles and urls loaders
AIRAVATA_REPLACE_DOTS_IN_DOMAINS = False
