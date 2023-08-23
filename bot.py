from utils import *
import time

api = ChainEdgeAPI()


def pull_data():

    # pull last 24h
    df = api.get_many_pages(10)

    while True:
        # argument = 1 indicates get the latest page
        new_page = api.get_single_page(1)

        # unique rows get us rows that were pulled but not in existing dataframe
        unique_rows = new_page[~new_page['id'].isin(df['id'])]

        # Prepend the unique rows to the front of the main DataFrame
        df = pd.concat([unique_rows, df], ignore_index=True)

        # delete rows at the end to keep fixed size
        df = df.iloc[:len(df)-len(unique_rows)]

        now = datetime.datetime.now()
        time_5mins_ago = now - datetime.timedelta(minutes=5)
        time_1h_ago = now - datetime.timedelta(minutes=60)
        time_6h_ago = now - datetime.timedelta(minutes=6*60)
        time_24h_ago = now - datetime.timedelta(minutes=24*60)

        # Filter for 5 minutes back
        df['tn_time'] = pd.to_datetime(df['tn_time'])
        df_5m = df[(df['tn_time']) >= time_5mins_ago]
        df_1h = df[(df['tn_time']) >= time_1h_ago]
        df_6h = df[(df['tn_time']) >= time_6h_ago]
        df_24h = df[(df['tn_time']) >= time_24h_ago]

        # Get the most common occurrences for each time window
        common_5m_value = df_5m['values'].value_counts().idxmax()
        common_5m_count = df_5m['values'].value_counts().idxmax()

        common_1h_value = df_1h['values'].value_counts().idxmax()
        common_1h_count = df_1h['values'].value_counts().idxmax()

        common_6h_value = df_6h['values'].value_counts().idxmax()
        common_6h_count = df_6h['values'].value_counts().idxmax()

        common_24h_value = df_24h['values'].value_counts().idxmax()
        common_24h_count = df_24h['values'].value_counts().idxmax()

        print(
            f'most aped coin (past 5mins): ${common_5m_value}, times aped: {common_5m_count}')
        print(
            f'most aped coin (past 1hours): ${common_1h_value}, times aped: {common_1h_count}')
        print(
            f'most aped coin (past 6hours): ${common_6h_value}, times aped: {common_6h_count}')
        print(
            f'most aped coin (past 24hours): ${common_24h_value}, times aped: {common_24h_count}')

        time.sleep(10)


# tomorrow todos:
# change 'values' key to buy_token
# remove WETH from buy_tokens
# remove everything after the first space+number e.g. Wrapped Ether 0.01, ' 0' would be detected and remove everything after

pull_data()
