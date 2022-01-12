import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class MovieAnalysis(object):
    def __init__(self, filename: str):
        self._dataframe: pd.DataFrame = pd.DataFrame()
        self.load_data(filename)

    def load_data(self, filename: str):
        self._dataframe = pd.read_csv(filename, parse_dates=['Release Date']).infer_objects()

        # data preprocessing
        self._dataframe['US Gross'].replace(to_replace='Unknown', value=0, inplace=True)  # replace 'Unknown' with 0
        self._dataframe['Worldwide Gross'].replace(to_replace='Unknown', value=0, inplace=True)  # replace 'Unknown' with 0
        self._dataframe['US DVD Sales'].fillna(value=0, inplace=True)  # replace missing with 0
        self._dataframe['Production Budget'].fillna(value=0, inplace=True)  # replace missing with 0
        self._dataframe['Running Time (min)'].fillna(round(self._dataframe['Running Time (min)'].mean()), inplace=True)  # replace missing with mean value
        self._dataframe['Rotten Tomatoes Rating'].fillna(value=0, inplace=True)  # replace missing with 0
        self._dataframe['IMDB Rating'].fillna(value=0, inplace=True)  # replace missing with 0
        self._dataframe['IMDB Votes'].fillna(value=0, inplace=True)  # replace missing with 0

        # type conversion to int64
        int64_columns = ['US Gross', 'Worldwide Gross', 'US DVD Sales', 'Production Budget']
        self._dataframe[int64_columns] = self._dataframe[int64_columns].astype(dtype=np.int64)

        # type conversion to int
        int_columns = ['Running Time (min)', 'Rotten Tomatoes Rating', 'IMDB Votes']
        self._dataframe[int_columns] = self._dataframe[int_columns].astype(dtype=np.int)

        # type conversion to float
        float_columns = ['IMDB Rating']
        self._dataframe[float_columns] = self._dataframe[float_columns].astype(dtype=np.float)

        # order by 'Release Date'
        self._dataframe.sort_values(by='Release Date')

        # print data
        # print(self._dataframe)

    def get_top_directors_based_on_worldwide_gross_revenue(self):
        """
        Top movie directors – based on worldwide gross revenue
        """
        df2 = self._dataframe[['Director', 'Worldwide Gross']].copy()
        df2 = df2.groupby(['Director']).sum().sort_values('Worldwide Gross', ascending=False)
        print(df2[:10])

        x_values = list(df2['Worldwide Gross'].to_dict().keys())[:10]
        y_values = list(df2['Worldwide Gross'].to_dict().values())[:10]

        plt.figure(figsize=(17, 5))
        plt.bar(x_values, y_values, color='maroon', width=0.4)
        plt.xlabel("Directors who gave highest grossing movies")
        plt.ylabel("Worldwide Gross (in billions)")
        plt.title("Top movie directors – based on worldwide gross revenue")
        plt.show()

    def get_popular_movie_based_on_gross_earning(self):
        """
        Popular movies – based on gross earning
        """
        df2 = self._dataframe[['Title', 'Worldwide Gross']].copy()
        df2 = df2.sort_values('Worldwide Gross', ascending=False)
        print(df2[:10])

    def get_popular_movie_based_on_user_earning(self):
        """
        Popular movies – based on gross earning
        """
        df2 = self._dataframe[['Title', 'IMDB Rating']].copy()
        df2 = df2.sort_values('IMDB Rating', ascending=False)
        print(df2[:10])


if __name__ == '__main__':
    movie_analysis = MovieAnalysis('movies.csv')
    movie_analysis.get_top_directors_based_on_worldwide_gross_revenue()
    movie_analysis.get_popular_movie_based_on_gross_earning()
    movie_analysis.get_popular_movie_based_on_user_earning()
