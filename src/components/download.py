import os

import ir_datasets
from components.settings import Settings, WebisTouche2020DatasetSettings

UNSET_USERNAME = "<NONE>"

def download():
    # Setup data dir
    settings = Settings()
    os.makedirs(settings.raw_path, exist_ok=True)

    # Download Webis Touche 2020
    webis_touche_2020_settings = WebisTouche2020DatasetSettings()
    ir_datasets.load(webis_touche_2020_settings.ir_datasets_name)
    print("Downloaded Webis Touche 2020 dataset.")


