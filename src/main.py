from components.download import download
from components.elasticsearch import start as start_elasticsearch
if __name__ == "__main__":
    download()
    start_elasticsearch()
