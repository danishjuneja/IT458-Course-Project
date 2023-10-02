import os
import shutil
import tarfile
from urllib.parse import urlparse

import ir_datasets
import requests
from requests.auth import HTTPBasicAuth
from components.settings import (
    Settings,
    TRECCovidDatasetSettings,
)
from tqdm.auto import tqdm

UNSET_USERNAME = "<NONE>"


def download_file(
    url: str,
    file_path: str,
    username: str = None,
    password: str = None,
    pbar_desc: str = "",
    response_attr: str = "raw",
) -> None:
    """Download a file from a URL to a file path."""
    if os.path.isdir(file_path):
        file_path = os.path.join(file_path, os.path.basename(urlparse(url).path))

    if not os.path.exists(file_path):
        request_kwargs = {}
        if all([username, password]):
            request_kwargs["auth"] = HTTPBasicAuth(username, password)

        response = requests.get(url, stream=True, **request_kwargs)
        response.raise_for_status()

        if response_attr == "raw":
            total_length = int(response.headers.get("Content-Length", 0))
            with tqdm.wrapattr(
                getattr(response, response_attr),
                "read",
                total=total_length,
                ncols=100,
                desc=pbar_desc,
            ) as pbar:
                with open(file_path, "wb") as file:
                    shutil.copyfileobj(pbar, file)
        elif response_attr == "content":
            with open(file_path, "wb") as file:
                file.write(response.content)
        else:
            raise ValueError(f"Invalid response_attr: {response_attr}")

    else:
        print(f"File already exists: {file_path}")

    return file_path


def untar_gzip(file_path: str, output_dir: str) -> None:
    """Untar a gzip file."""
    with tarfile.open(file_path, "r:gz") as tar:
        for name in tar.getnames():
            if not os.path.exists(os.path.join(output_dir, name)):
                tar.extract(name, path=output_dir)


def download():
    # Setup data dir
    settings = Settings()
    os.makedirs(settings.raw_path, exist_ok=True)

    # Download TREC-COVID
    trec_covid_settings = TRECCovidDatasetSettings()
    os.makedirs(trec_covid_settings.raw_path, exist_ok=True)
    out_file = download_file(
        trec_covid_settings.corpus_url,
        trec_covid_settings.raw_path,
        pbar_desc="trec-covid/corpus",
    )
    untar_gzip(out_file, trec_covid_settings.raw_path)
    download_file(
        trec_covid_settings.topics_url,
        trec_covid_settings.raw_path,
        response_attr="content",
        pbar_desc="trec-covid/topcis",
    )
    download_file(
        trec_covid_settings.qrels_url,
        trec_covid_settings.raw_path,
        response_attr="content",
        pbar_desc="trec-covid/qrels",
    )


if __name__ == "__main__":
    main()
