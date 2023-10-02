from components.download import download
from components.elasticsearch import start as start_elasticsearch
from components.first_stage import first_stage
if __name__ == "__main__":
    # download() #run once to download the data then comment it out, not required for touche database
    # start_elasticsearch() # run if using docker otherwise don't
    dataset_name = "touche"
    first_stage(dataset_name)