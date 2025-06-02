from config.paths_config import *
from utils.common_functions import read_yaml
from src.data_processing import DataProcessing
from src.model_training import ModelTraining
from src.logger import get_logger

if __name__ == "__main__":
    

    data_processing = DataProcessing(ANIMELIST_CSV, PROCESSED_DIR)
    data_processing.run()

    model_trainer = ModelTraining(data_path=PROCESSED_DIR)
    model_trainer.train_model()

    