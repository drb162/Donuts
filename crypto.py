import requests
import pandas as pd
import matplotlib.pyplot as plt


class CryptoCurrencies:

    """This class contains functions to track and analyze the value of cryptocurrencies
     across various markets. It uses the Alpha Vantage API and requires an API key that
     can be retrieved here: https://www.alphavantage.co/support/#api-key.
     """

    _API_URL = "https://www.alphavantage.co/query?"

    def __init__(self, api_key):

        """ Initialize the class

            Keyword Arguments:
                api_key:  Alpha Vantage api key
        """

        self._api_key = api_key

    def get_timeseries_daily(self, symbol, market, days=None):

        """Return a Pandas object with the daily timeseries of
        the cryptocurrency and market specified.

            Keyword Arguments:
                symbol: symbol of CryptoCurrency to be tracked.
                market: symbol of exchange market to be tracked.
                days (optional): number of days requested. Limit
                and Default is 1000.
        """

        function = 'DIGITAL_CURRENCY_DAILY'

        url = '{}function={}&symbol={}&market={}&apikey={}' \
            .format(self._API_URL,
                    function,
                    symbol,
                    market,
                    self._api_key)

        cc_json = self._api_call(url)['Time Series (Digital Currency Daily)']
        return pd.DataFrame(cc_json).T

    def get_processed_timeseries_daily(self, symbol, market):

        """Return a Pandas object with daily timeseries of closing value of
        cryptocurrency at specified market, 3 day rolling average and 7 day
        rolling average, both calculated with a centered window.

            Keyword Arguments:
                symbol: symbol of CryptoCurrency to be tracked.
                market: symbol of exchange market to be tracked.
        """
        closing_col_name = '4a. close ({})'.format(market)

        cr_df = self.get_timeseries_daily(symbol, market)[[closing_col_name]]
        cr_df[closing_col_name] = cr_df[closing_col_name].astype(float)
        cr_df['3day RA ({})'.format(market)] = cr_df[closing_col_name]\
            .rolling(window=3, center=True).mean()
        cr_df['7day RA ({})'.format(market)] = cr_df[closing_col_name]\
            .rolling(window=7, center=True).mean()

        cr_df = cr_df.rename(columns={closing_col_name: '{} closing value ({})'
                             .format(symbol, market)})
        return cr_df

    @staticmethod
    def plot_timeseries(df):

        """Plot given dataframe.

            Keyword Arguments:
                df: timeseries dataframe with data to be plotted.
        """
        df = df.sort_index()
        df.plot()
        plt.tight_layout()
        plt.grid()
        plt.show()

    @staticmethod
    def _api_call(url):

        """ Makes the api call and handles the response.
            Raises ValueError on problems.

        Keyword Arguments:
            url:  The url of the service API
        """

        response = requests.get(url)
        json_response = response.json()

        if not json_response:
            raise ValueError('API is non responsive.')
        elif "Error Message" in json_response:
            raise ValueError(json_response["Error Message"])
        elif "Information" in json_response:
            raise ValueError(json_response["Information"])
        elif "Note" in json_response:
            raise ValueError(json_response["Note"])

        return json_response


if __name__ == '__main__':

    cc = CryptoCurrencies('6ML9EF1OECFZHJDG')
    btc_data = cc.get_processed_timeseries_daily('BTC', 'USD')

    print('\n\nBitcoin value in USD (last 10 days): \n\n', btc_data.head(10))
    cc.plot_timeseries(btc_data)
