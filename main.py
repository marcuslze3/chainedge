import requests
import re
import time
import pandas as pd
from utils import *

api = ChainEdgeAPI()
df = api.get_pages_data(2000)

df.to_csv('data.csv')
