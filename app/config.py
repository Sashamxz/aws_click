import os
from dotenv import load_dotenv


load_dotenv()

REGION_LIST = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
    "ap-south-1",
    "ap-northeast-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-northeast-1",
    "ca-central-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "eu-north-1",
    "me-south-1",
    "sa-east-1"
]


class Config:
    dotenv_path = os.path.join(os.path.dirname(
                               os.path.abspath(__file__)),
                               ".env")


class DevelopmentConfig(Config):
    DEBUG = True
    ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
    SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
    REGION = os.getenv("REGION")


class ProductionConfig(Config):
    ...


class DockerConfig(Config):
    ...


settings_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "docker": DockerConfig,
}
