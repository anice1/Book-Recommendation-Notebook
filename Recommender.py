import pandas as pd
from fuzzywuzzy import process



class Recommend:

    # Read data
    books = pd.read_csv('Books.csv', usecols=['ISBN','Book-Title',
                                                    'Book-Author','Year-Of-Publication',
                                                    'Publisher','Image-URL-S'], date_parser='Year-Of-Publication',nrows=50000)
    ratings = pd.read_csv('Ratings.csv', nrows=50000)

    # Create a copy of the dataset
    tmp_books, tmp_ratings = books, ratings
    
    def __init__(self):

        self.edit_df_column(self.tmp_books, self.tmp_ratings)

        # Merge the books dataframe to rating
        self.df = pd.merge(self.tmp_books,self.tmp_ratings, on='isbn')
        self.df.sort_values(by='book_rating', ascending=False, inplace=True)
        self.df.dropna(inplace=True)

        # Create a new df indicating the number of rating for each book
        self.book_ratings = pd.DataFrame(self.df.groupby('book_title')['book_rating'].count()).sort_values(by='book_rating', ascending=False).reset_index()

        # Create a pivot table
        self.book_users = self.df.pivot_table(index='user_id', columns=['book_title'], values='book_rating').fillna(0)


    def edit_df_column(self, *df):
        for i in df:
            i.columns = [x.replace('-','_').lower() for x in i.columns]

    # Create a recommender function that take a book name and return a list of recommendations
    def recommend(self, book_name:str):
        df_query = self.book_users

        # Get the book 
        get_book = df_query[book_name]
        
        # Get Books with similarities to book name
        book_corr = df_query.corrwith(get_book)
        
        # Create a data frame of the book
        similar_books = pd.DataFrame(book_corr, columns=['Correlation'])
        
        # Drop null values from the similar book dataframe
        similar_books.dropna(inplace=True)
        
        # Join the ratings columns to the similar_book df
        similar_books = similar_books.join(self.book_ratings['book_rating']).reset_index()
        
        # Get the books with highest number of ratings
        return similar_books[similar_books['book_rating'] > 20].sort_values('Correlation', ascending=False)