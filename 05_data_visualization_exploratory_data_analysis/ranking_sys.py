import pandas as pd


class Ranking:
    def __init__(self, data_views, data_likes, data_posts):
        self.data_views = data_views
        self.data_likes = data_likes
        self.data_posts = data_posts

    def get_mean(self):
        mean_value = pd.Series(self.data_views).mean()
        return mean_value

    def second_example(self):
        return 'Second Success'

    def third_example(self):
        return self.data_views
