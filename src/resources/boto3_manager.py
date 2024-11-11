from typing import Union, List, Generator, Dict
import io
import boto3
import pandas as pd
import json

class PandasBucket:
    """
    A class that allows to perform operations on a unique bucket in AWS S3 or any S3 compatible storage.
    It is possible to insert pandas objects into desired formats (feather, parquet, json, csv).
    """
    def __init__(self, client: boto3.client, name: str = "datasets"):
        self.client = client
        self.name = name
        self.create()
    
    @property
    def exists(self) -> bool:
        """ Return True if bucket exists, else False. """
        try:
            self.client.head_bucket(Bucket=self.name)
            return True
        except self.client.exceptions.NoSuchBucket:
            return False

    def create(self) -> None:
        """ Create the bucket if it does not exist. """
        if not self.exists:
            self.client.create_bucket(Bucket=self.name)
    
    def destroy(self) -> None:
        """ Destroy the bucket as well as all of its content. """
        if self.exists:
            for obj in self.client.list_objects_v2(Bucket=self.name).get('Contents', []):
                self.client.delete_object(Bucket=self.name, Key=obj['Key'])
            self.client.delete_bucket(Bucket=self.name)
    
    def __put__(self, name: str, data: io.BytesIO) -> str:
        """ Put an object into S3 storage. data is the content to upload. """
        self.client.put_object(Bucket=self.name, Key=name, Body=data.getvalue())
        return name

    def __get__(self, name: str) -> io.BytesIO:
        """ Get an object from S3 storage. name is the key of the object. """
        response = self.client.get_object(Bucket=self.name, Key=name)
        data = io.BytesIO(response['Body'].read())
        data.seek(0)
        return data

    def put_feather(self, df: Union[pd.Series, pd.DataFrame], name: str) -> str:
        """ Store a pandas.Series or pandas.Dataframe in feather format into S3 storage """
        data = io.BytesIO()
        df.to_feather(data)
        data.seek(0)
        return self.__put__(name, data=data)

    def put_parquet(self, df: Union[pd.Series, pd.DataFrame], name: str) -> str:
        """ Store a pandas.Series or pandas.Dataframe in parquet format into S3 storage """
        data = io.BytesIO()
        df.to_parquet(data, engine='pyarrow')
        data.seek(0)
        return self.__put__(name, data=data)

    def put_json(self, df: Union[pd.Series, pd.DataFrame], name: str, **kwargs) -> str:
        """ Store a pandas.Series or pandas.Dataframe in json format into S3 storage """
        data = io.BytesIO(df.to_json(**kwargs).encode("utf-8"))
        data.seek(0)
        return self.__put__(name, data=data)

    def put_csv(self, df: Union[pd.Series, pd.DataFrame], name: str, index: bool = False, **kwargs) -> str:
        """ Store a pandas.Series or pandas.Dataframe in csv format into S3 storage """
        data = io.BytesIO(df.to_csv(index=index, **kwargs).encode("utf-8"))
        data.seek(0)
        return self.__put__(name, data=data)

    def put(self, df: Union[pd.Series, pd.DataFrame], name: str, **kwargs) -> str:
        """ Store a pandas.Series or pandas.Dataframe into S3 storage in appropriate format deduced from filename. """
        if name.endswith(".feather"):
            return self.put_feather(df, **kwargs)
        elif name.endswith(".parquet"):
            return self.put_parquet(df, **kwargs)
        elif name.endswith(".json"):
            return self.put_json(df, **kwargs)
        elif name.endswith(".csv"):
            return self.put_csv(df, **kwargs)

    def read_feather(self, name: str) -> Union[pd.Series, pd.DataFrame]:
        """ Read a pandas DataFrame stored as feather file from S3 storage. """
        data = self.__get__(name)
        return pd.read_feather(data)

    def read_parquet(self, name: str) -> Union[pd.Series, pd.DataFrame]:
        """ Read a pandas DataFrame stored as parquet file from S3 storage. """
        data = self.__get__(name)
        return pd.read_parquet(data)

    def read_json(self, name: str, **kwargs) -> Union[pd.Series, pd.DataFrame]:
        """ Read a pandas DataFrame stored as json file from S3 storage. """
        data = self.__get__(name)
        return pd.read_json(data, **kwargs)

    def read_csv(self, name: str, **kwargs) -> Union[pd.Series, pd.DataFrame]:
        """ Read a pandas DataFrame stored as csv file from S3 storage. """
        data = self.__get__(name)
        return pd.read_csv(data, **kwargs)

    def read_json_from_s3(self, name: str) -> List:
        """ Read JSON directly from S3 without pandas conversion """
        data_io = self.__get__(name)
        return json.load(data_io)

    def read(self, name: str, **kwargs) -> Union[pd.Series, pd.DataFrame]:
        """ Read a pandas.Series or pandas.Dataframe from S3 storage in the appropriate format. """
        if name.endswith(".feather"):
            return self.read_feather(name, **kwargs)
        elif name.endswith(".parquet"):
            return self.read_parquet(name, **kwargs)
        elif name.endswith(".json"):
            return self.read_json(name, **kwargs)
        elif name.endswith(".csv"):
            return self.read_csv(name, **kwargs)

    def write_dict_to_json(self, data: Dict, name: str, **kwargs) -> None:
        """ Write dictionary as JSON to S3 storage """
        data_io = io.BytesIO(json.dumps(data, indent=4).encode('utf-8'))
        data_io.seek(0)
        return self.__put__(name, data=data_io)
