import pandas as pd
from dirs import ROOT_DIR


def sample_run():
    df = pd.read_csv(ROOT_DIR / 'tests/data/youtube/api/youtube_videos_most_pop_us.csv')
    print(df)


if __name__ == '__main__':
    sample_run()
