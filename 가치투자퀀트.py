import pandas as pd
import numpy as np
import FinanceDataReader as fdr


krx_df = fdr.StockListing(('KRX'))
krx_df.head()