import pandas as pd
import plotly.express as px

from nltk import collections
from plotly.graph_objs import Figure

from app.services.genius import tokenize_words
pd.options.plotting.backend = "plotly"
lyrics = """
[Intro]
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
Caught in a bad romance
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
Caught in a bad romance
Ra-ra-ah-ah-ah
Roma Roma-ma
Gaga, "Ooh la-la"
Want your bad romance
Ra-ra-ah-ah-ah
Roma, Roma-ma
Gaga, "Ooh la-la"
Want your bad romance

[Verse 1]
I want your ugly, I want your disease
I want your everything as long as it’s free
I want your love
Love, love, love, I want your love, oh, ey
I want your drama, the touch of your hand (Hey!)
I want your leather-studded kiss in the sand
I want your love
Love, love, love, I want your love
(Love, love, love, I want your love)

[Pre-Chorus]
You know that I want you
And you know that I need you
I want it bad
Your bad romance

[Chorus]
I want your love, and I want your revenge
You and me could write a bad romance (Oh-oh-oh-oh-oh)
I want your love, and all your lover's revenge
You and me could write a bad romance
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
Caught in a bad romance
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
Caught in a bad romance

[Post-Chorus]
Ra-ra-ah-ah-ah
Roma-roma-ma
Gaga, "Ooh la-la"
Want your bad romance

[Verse 2]
I want your horror, I want your design
‘Cause you’re a criminal as long as you’re mine
I want your love
Love, love, love, I want your love, uh
I want your psycho, your vertigo shtick (Shtick, hey!)
Want you in my rear window, baby, you're sick
I want your love
Love, love, love, I want your love
(Love, love, love, I want your love)

[Pre-Chorus]
You know that I want you
And you know that I need you (
'Cause I'm a free bitch, baby
)
I want it bad
Your bad romance

[Chorus]
I want your love, and I want your revenge
You and me could write a bad romance (Oh-oh-oh-oh-oh)
I want your love, and all your lover's revenge
You and me could write a bad romance
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
Caught in a bad romance
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
Caught in a bad romance

[Post-Chorus]
Ra-ra-ah-ah-ah
Roma-roma-ma
Gaga, "Ooh la-la"
Want your bad romance
Ra-ra-ah-ah-ah
Roma-roma-ma
Gaga, "Ooh la-la"
Want your bad romance

[Bridge 1]
Walk, walk, fashion, baby
Work it, move that bitch crazy
Walk, walk, fashion, baby
Work it, move that bitch crazy
Walk, walk, fashion, baby
Work it, move that bitch crazy
Walk, walk, passion, baby
Work it, I'm a free bitch, baby

[Bridge 2]
I want your love, and I want your revenge
I want your love, I don't wanna be friends
Je veux ton amour et je veux ta revanche
Je veux ton amour, I don't wanna be friends
(Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh)
(I want you back) No, I don't wanna be friends
(Caught in a bad romance) I don't wanna be friends
Want your bad romance
(Caught in a bad romance) Want your bad romance

[Chorus]
I want your love, and I want your revenge
You and me could write a bad romance (Oh-oh-oh-oh-oh)
I want your love, and all your lover's revenge
You and me could write a bad romance
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
(Want your bad romance)
Caught in a bad romance (Want your bad romance)
Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
(Want your bad romance)
Caught in a bad romance

[Post-Chorus]
Ra-ra-ah-ah-ah
Roma, Roma-ma
Gaga, "Ooh la-la"
Want your bad romance
"""


def get_lyrics_frequency_df(raw_lyrics: str, limit: int = 10) -> pd.DataFrame:
    all_words_no_urls = tokenize_words(raw_lyrics)
    counts_no_urls = collections.Counter(all_words_no_urls)
    return pd.DataFrame(counts_no_urls.most_common(limit), columns=['words', 'count'])


def plot_lyrics_frequency(raw_lyrics: str) -> Figure:
    df = get_lyrics_frequency_df(raw_lyrics)
    return px.bar(df, x="words", y="count", title="Word Frequency in lyrics")


if __name__ == '__main__':
    fig = plot_lyrics_frequency(lyrics)
    fig.show()
