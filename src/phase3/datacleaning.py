import pandas as pd

# Load the data into a Pandas dataframe
def load_data(file):
  return pd.read_csv(file)

N = 4000
# Create a sample from a file
def create_sample(n=N, file='all_games.csv', entire=False):
    df = pd.read_csv(file)
    if entire or n == -1:
        return df
    sample = df.sample(n)
    print("length of sample: ",len(sample))
    return sample

def filter_duplicates(sample):
    # Sort the games by their 'meta_score' column in descending order
    sample = sample.sort_values(by='meta_score', ascending=False)

    # Drop any duplicate games from the sample, keeping only the highest rated
    # version of each game.
    sample = sample.drop_duplicates(subset=['name'], keep='first')
    print("length of sample after removing duplicates: ",len(sample))
    return sample

#remove rows where user_review = 'tbd'
def remove_empty_reviews(sample):
    sample = sample[sample.user_review != 'tbd']
    print("length of sample after removing empty reviews",len(sample))
    return sample

def clean_summaries(sample):
    # remove all whitespace and then just keep ascii chars
    sample['summary'] = sample['summary'].astype(str).apply(lambda x: x.strip().encode("ascii", errors="ignore").decode("ascii"))
    return sample

def normalize_rating(sample, columns):
    for column in columns:
      new_col = column + "_normalized"
      mean = sample.loc[:, column].astype(float).mean()
      std = sample.loc[:, column].astype(float).std()

      # create a new column based on the values of the mean, std
      sample[new_col] = sample[column].astype(float).apply(lambda x: (x-mean)/std)

    return sample

def format_date(sample):
    # turn input to datatime object
    sample['release_date'] = pd.to_datetime(sample['release_date'], format='%B %d, %Y')
    return sample

def year_and_month(sample):
    # extrapolate features into own columns
    sample['year'] = sample['release_date'].dt.year
    sample['month'] = sample['release_date'].dt.strftime('%B')
    return sample

# takes a sample and column name to drop
def drop_column(sample, col="index"):
    sample = sample.drop(col, axis=1)
    return sample

def add_genres(sample, file):
    names = {}
    # read the other file
    extra = create_sample(-1, file)

    # create a word map of genres and basic names
    for key, i in enumerate(extra["name"]):
        second = extra.at[key, "Genre"]
        names["".join([l.lower() for l in i if l.isalnum()])] = second

    # check for names from the dictionary and supplement genres
    for key, i in enumerate(sample["name"]):
        cleaned = "".join([l.lower() for l in i if l.isalnum()])
        sample.at[key, "genre"] = None
        if cleaned in names:
            sample.at[key, "genre"] = names[cleaned]

    print(len(sample[['genre']]))
    return sample

def remove_award_text(sample):
    # match prefix w regex
    sample['summary'] = sample['summary'].str.replace(r'\[.*\] ', '', regex=True)
    return sample

def clean_data(sample):
  # call all the defined functions from the data cleaning section in the correct order
  sample = add_genres(sample, "games.csv")
  sample = filter_duplicates(sample)
  sample = remove_empty_reviews(sample)
  sample = normalize_rating(sample, ["user_review", "meta_score"])
  sample = format_date(sample)
  sample = year_and_month(sample)
  sample = drop_column(sample, "index")
  sample = remove_award_text(sample)
  sample = clean_summaries(sample)
  return sample