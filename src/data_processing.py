import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml
import sys
logger = get_logger(__name__)

class DataProcessing:
    def __init__(self, input_file,out_putdir):
        self.input_file = input_file
        self.out_putdir = out_putdir
        os.makedirs(self.out_putdir, exist_ok=True)
        logger.info("DataProcessing class initialized")

        self.rating_df = None
        self.anime_df = None
        self.X_train_array = None
        self.X_test_array = None
        self.y_train = None
        self.y_test = None

        self.user2user_encoded = {}
        self.user2user_decoded = {}
        self.anime2anime_encoded = {}
        self.anime2anime_decoded = {}

    def load_data(self,usecols):
        try:
            self.rating_df = pd.read_csv(self.input_file,low_memory=True,usecols=usecols)
            logger.info(f"Data loaded successfully from {self.input_file}")
        except Exception as e:
            logger.error(f"Error loading data from {self.input_file}: {e}")
            raise CustomException(f"Error loading data from {self.input_file}: {e}", e)
    def filter_users(self,min_rating=400):
        try:
            n_ratings = self.rating_df["user_id"].value_counts()
            self.rating_df = self.rating_df[self.rating_df["user_id"].isin(n_ratings[n_ratings>=400].index)].copy()

            logger.info("Filtered users with less than 400 ratings")
        except Exception as e:
            logger.error(f"Error filtering users: {e}")
            raise CustomException(f"Error filtering users: {e}", e)
    def scale_rating(self):
        try:
            min_rating = min(self.rating_df["rating"])
            max_rating = max(self.rating_df["rating"])
            self.rating_df["rating"] = self.rating_df["rating"].apply(lambda x: (x-min_rating)/(max_rating-min_rating)).values.astype(np.float64)
            logger.info("Scaled ratings to a range of 0 to 1")
        except Exception as e:
            logger.error(f"Error scaling ratings: {e}")
            raise CustomException(f"Error scaling ratings: {e}", e)
    def encode_data(self):
        try:
            # users
            user_ids = self.rating_df["user_id"].unique().tolist()
            self.user2user_encoded = {x : i for i , x in enumerate(user_ids)}
            self.user2user_decoded = {i : x for i , x in enumerate(user_ids)}
            self.rating_df["user"] = self.rating_df["user_id"].map(self.user2user_encoded)

            # anime

            anime_ids = self.rating_df["anime_id"].unique().tolist()
            self.anime2anime_encoded = {x : i for i , x in enumerate(anime_ids)}
            self.anime2anime_decoded = {i : x for i , x in enumerate(anime_ids)}
            self.rating_df["anime"] = self.rating_df["anime_id"].map(self.anime2anime_encoded)

            logger.info("Encoded user and anime IDs")
        except Exception as e:
            logger.error(f"Error encoding data: {e}")
            raise CustomException(f"Error encoding data: {e}", e)
    def split_data(self,test_size=1000,random_state=42):
        try:
            self.rating_df = self.rating_df.sample(frac=1,random_state=43).reset_index(drop=True)

            X = self.rating_df[["user","anime"]].values
            y = self.rating_df["rating"]
            train_indices = self.rating_df.shape[0] - test_size
            X_train , X_test , y_train , y_test = (
                X[:train_indices],
                X[train_indices :],
                y[:train_indices],
                y[train_indices:],
                )
            self.X_train_array = [X_train[: , 0] , X_train[: ,1]]
            self.X_test_array = [X_test[: , 0] , X_test[: ,1]]
            self.y_train = y_train
            self.y_test = y_test

            logger.info("Split data into training and testing sets")
        except Exception as e:
            logger.error(f"Error splitting data: {e}")
            raise CustomException(f"Error splitting data: {e}", e)
    def save_artifacts(self):
        try:
            artifacts = {
                "user2user_encoded": self.user2user_encoded,
                "user2user_decoded": self.user2user_decoded,
                "anime2anime_encoded": self.anime2anime_encoded,
                "anime2anime_decoded": self.anime2anime_decoded,
                
            }
            for name, data in artifacts.items():
                file_path = os.path.join(self.out_putdir, f"{name}.pkl")
                joblib.dump(data, file_path)
                logger.info(f"Saved {name} to {file_path}")
            joblib.dump(self.X_train_array, X_TRAIN_ARRAY)
            joblib.dump(self.X_test_array, X_TEST_ARRAY)
            joblib.dump(self.y_train, Y_TRAIN)
            joblib.dump(self.y_test, Y_TEST)

            self.rating_df.to_csv( RATING_DF,index=False)
            logger.info("Saved training and testing data arrays")
        except Exception as e:
            logger.error(f"Error saving artifacts: {e}")
            raise CustomException(f"Error saving artifacts: {e}", e)
    def process_anime_data(self):
        try:
            df = pd.read_csv(ANIME_CSV)
            cols = ["MAL_ID","Name","Genres","sypnopsis"]
            synopis_df = pd.read_csv(ANIME_SYNOPSIS_CSV,usecols=cols)

            df = df.replace("Unknown", np.nan)
            def getAnimeName(anime_id):
                try:
                    name = df[df.anime_id == anime_id].eng_version.values[0]
                    if name is np.nan:
                        name = df[df.anime_id == anime_id].Name.values[0]
                except:
                    print("Error")
                return name 
            df["anime_id"] = df["MAL_ID"]
            df["eng_version"] = df["English name"]
            df["eng_version"] = df.anime_id.apply(lambda x:getAnimeName(x))

            df.sort_values(by=["Score"],
               inplace=True,
               ascending=False,
               kind="quicksort",
               na_position="last")
            df = df[["anime_id" , "eng_version","Score","Genres","Episodes","Type","Premiered","Members"]]
            df.to_csv(DF, index=False)
            synopis_df.to_csv(SYNOPIS_DF, index=False)
            logger.info("Processed anime data and df, synopis_df saved to CSV files")
        except Exception as e:
            logger.error(f"Error processing anime data: {e}")
            raise CustomException(f"Error processing anime data: {e}", e)
    
    def run(self):
        try:
            logger.info("Starting data processing")
            usecols = ["user_id", "anime_id", "rating"]
            self.load_data(usecols)
            self.filter_users()
            self.scale_rating()
            self.encode_data()
            self.split_data()
            self.save_artifacts()
            self.process_anime_data()
            logger.info("Data processing completed successfully")
        except Exception as e:
            logger.error(f"Error in data processing: {e}")
            raise CustomException(f"Error in data processing: {e}", e)
        finally:
            logger.info("Data processing finished")
if __name__ == "__main__":
    
    
    data_processing = DataProcessing(ANIMELIST_CSV, PROCESSED_DIR)
    data_processing.run()