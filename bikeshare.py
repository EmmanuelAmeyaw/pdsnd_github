#BIKESHARE PROJECT
#import the necessary modules
import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    global city
    global month
    global day
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! AND Oh, you need to have the json module installed too')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city=input('Choose one of the following cities: chicago, new york city, or washington')
        if city.lower() not in ['chicago','new york city','washington']:
             print("make sure you spelled the cities correctly")
 
        else:
            city=city.lower()
            break

    print('You chose {}'.format(city.title()))

    # get user input for month (all, january, february, ... , june)
    while True:
        months=['jan','feb','mar','apr','may','jun','all']
        month=input("Choose a month you want to view: Jan, Feb, Mar, Apr, May, Jun or \"All\"")
        if month.lower() not in months:
            print("choose one of these as specified here:'jan','feb','mar','apr','may','jun', or \"All\"")
        else:
            month=month.lower()
            break
    
    print('You chose {}'.format(month))    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input("Choose a day from these :'mon','tue','wed','thu','fri','sat','sun' or \"All\"")
        days=['mon','tue','wed','thu','fri','sat','sun','all']
        if day.lower() not in days:
            print("c'mmon choose one of these as specified here:'mon','tue','wed','thu','fri','sat','sun','all', or \"All")
        else:
            day=day.lower()
            break
        print('You chose {}'.format(day))
        
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    import pandas as pd
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.weekday
    df['hour']=df['Start Time'].dt.hour
    months=['all','jan','feb','mar','apr','may','jun']
    days=['mon','tue','wed','thu','fri','sat','sun','all']
    if month!='all':
        month=months.index(month)
        df=df[df['month']==month]
        
    if day !='all':
        day=days.index(day)
        df=df[df['day_of_week']==day]
        

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_month=df['month'].mode()
    print ("The Most Common Month")
    print(most_month)
    # display the most common day of week
    most_day=df['day_of_week'].mode()
    print ('The Most Common Weekday')
    print(most_day)

    # display the most common start hour
    most_start_hour=df['hour'].mode()
    print('The Most Common Hour')
    print(most_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station=df['Start Station'].mode()[0]
    print('Most Popular Start Station: {}'.format(pop_start_station))

    # display most commonly used end station
    pop_end_station=df['End Station'].mode()[0]
    print('Most Popular End Station: {}'.format(pop_end_station))

    # display most frequent combination of start station and end station trip
    dfa=df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    c=dfa[0]
    mm = dfa.index[0]
    a = mm[0]
    b = mm[1]
    print('Most Popular Combination of Start and End Stations are: Start: {} End {}. And the total count is {}'.format(a,b,c))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel_time=df['Trip Duration'].sum()
    print("Total Travel Time is: {}".format(tot_travel_time))
    # display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print('Mean Travel Time is: {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types=df.groupby(['User Type']).sum()
    print('User Types\n',user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts=df['Gender'].value_counts()
        print("Gender Counts")
        print(gender_counts)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        early_year=df['Birth Year'].max()
        late_year=df['Birth Year'].min()
        common_year=df['Birth Year'].mode()
        print('The earliest birth year is: {}'.format(early_year))
        print('The most recent birth year is: {}'.format(late_year))
        print('The most common birth year is: {}'.format(common_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def table_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nDisplaying some descriptive statistics\n')
    
    # counts the number of missing values in the entire dataset
    number_of_missing_values = np.count_nonzero(df.isnull())
    print("1. The number of missing values in the {} dataset : {}".format(city, number_of_missing_values))
    print('.....................................................................')

    # counts the number of missing values in the User Type column
    number_of_nonzero = np.count_nonzero(df['User Type'].isnull())
    print("2. The number of missing values in the \'User Type\' column: {}".format(number_of_missing_values))
    print('.....................................................................')

    # Descriptive stat of the data
    df2 = df[['hour','day_of_week']]
    des = df2.describe()
    print('3. Displaying count, mean, std, min, max, 25th percentile, 50th percentile, 75th percentile for day_of_week and hour')
    print(des)

def display_data(df):
    """Displays raw bikeshare data."""
    row_length = df.shape[0]

    # iterate from 0 to the number of rows in steps of 5
    for i in range(0, row_length, 5):
        
        yes = input('\nWould you like to view individual trip data? Type \'yes\' or \'no\'\n> ')
        if yes.lower() != 'yes':
            break
        
        # retrieve and convert data to json format
        # split each json row data 
        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            # pretty print each user data
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)

def by_the_way():
	print('By the way, why are we not doing this project in a notebook, isn\'t using a notebook a better option? HMMMM, just curious')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        table_stats(df, city)
        display_data(df)
        by_the_way()
	
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


