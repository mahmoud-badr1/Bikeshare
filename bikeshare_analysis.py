import time
import pandas as pd
import numpy as np

chicago_file = 'https://drive.google.com/file/d/1x3VGbv48yS8z6qbRV7FpZ7wwKWBIRIeS/view?usp=sharing'
chicago_file = 'https://drive.google.com/uc?id=' + chicago_file.split('/')[-2]

new_york_file = 'https://drive.google.com/file/d/1teSgHxQNsSG62U9bzUCZECm-bhUk6LL2/view?usp=sharing'
new_york_file = 'https://drive.google.com/uc?id=' + new_york_file.split('/')[-2]

washington_file = 'https://drive.google.com/file/d/1M8uuuOGYNyymcVl3Xbk0WctauMhsFWG5/view?usp=sharing'
washington_file = 'https://drive.google.com/uc?id=' + washington_file.split('/')[-2]

CITY_DATA = { 'Chicago': chicago_file,
              'New York': new_york_file,
              'Washington': washington_file }

def get_filters():
    """
    Function asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # gets user input for city (chicago, new york city, washington).
    while True:
        try:
            city = input('Please select a city from the following: Chicago, New York, Washington: ').title().strip()
            if city == 'Chicago' or city == 'New York' or city == 'Washington':
                print('You have selected: ',city)
                break
            else: 
                print ('Invalid input!')
        except Exception:
            print('Unexpected error! please try again: ')
            
    # gets user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Please select a month from the following: January, February, March, April, May, June\n(OR) type "All" for a general insight: ').title().strip()
            months_list = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
            if month in months_list:
                print('You have selected: ',month)
                break
            else: 
                print ('Invalid input!')
        except Exception:
            print('Unexpected error! please try again: ')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Please select a a day of the week from Monday to Sunday\n(OR) type "All" for a general insight: ').title().strip()
            days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']
            if day in days_list:
                print('You have selected: ',day)
                break
            else: 
                print ('Invalid input!')
        except Exception:
            print('Unexpected error! please try again: ')
    print('\nCalculating stats based on the data you selected: \nCity: {} \nMonth: {} \nDay: {} '.format(city, month, day))
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
        df - Pandas DataFrame containing city data filtered by inputs from get_filters function
    """
    
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'All':
        months_list = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months_list.index(month) + 1
        df = df[df['month'] == month]

    if day != 'All':
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    df['hour'] = df['Start Time'].dt.hour
    months_list = ['January', 'February', 'March', 'April', 'May', 'June']

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_com_month = int(df['month'].mode()[0])
    most_com_month = months_list[most_com_month - 1]
    print('Most common month is: {}'.format(most_com_month))

    # display the most common day of week
    most_com_day = df['day_of_week'].mode()[0]
    print('Most common day is: {}'.format(most_com_day))

    # display the most common start hour
    most_com_hour = df['hour'].mode()[0]
    print('Most common hour month is: {}:00. Time displayed is in 24 Hours format'.format(most_com_hour))
    
    print("\nThis took %s seconds." % round(time.time() - start_time, 4))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_com_station_st = df['Start Station'].value_counts().idxmax()
    print('The most common start station is: {} station'.format(most_com_station_st))

    # display most commonly used end station
    most_com_station_end = df['End Station'].value_counts().idxmax()
    print('The most common end station is: {} station'.format(most_com_station_end))
    
    # display most frequent combination of start station and end station trip
    most_com_station_combination = df['Start Station'] + " to " + df['End Station']
    df['most_com_station_combination'] = most_com_station_combination
    print('The most frequent combination of stations is: {} stations, which were repeated {} times.'.format(df['most_com_station_combination'].mode()[0], df['most_com_station_combination'].value_counts().max()))
    
    print("\nThis took %s seconds." % round(time.time() - start_time, 3))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_time = df['Trip Duration'].sum()
    print('The total travel time is: {} mins and {} seconds. That makes a total of {} seconds.'.format(int(total_trip_time // 60), round(total_trip_time % 60, 2), total_trip_time))

    # display mean travel time
    mean_trip_time = df['Trip Duration'].mean()
    print('The mean travel time is: {} mins and {} seconds. That makes a total of {} seconds.'.format(int(mean_trip_time // 60) , round(mean_trip_time % 60,2), round(mean_trip_time, 3)))
    
    print("\nThis took %s seconds." % round(time.time() - start_time, 3))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].unique()
    print('The user types available are either {} or {}'.format(user_types[0], user_types[1]))
    
    user_types_count = df['User Type'].value_counts()
    print('There are {} Subscribers and {} Customers.'.format(user_types_count[0], user_types_count[1]))
    
    # Display counts of gender
    try:
        if 'Gender' in df:
            gender_counts = df['Gender'].value_counts()
            print('The numbers of Male users are {} and the number of Female users are {}.'.format(gender_counts['Male'], gender_counts['Female']))
    except Exception:
        print('Sorry! No gender specific stats available for this city.')

    # Display earliest, most recent, and most common year of birth
    try: 
        if 'Birth Year' in df:
            most_common_birth_year = df['Birth Year'].mode()[0]
            print('The most common year of birth is {}'.format(int(most_common_birth_year)))
            
            earliest_birth_year = df['Birth Year'].min()
            print('The earliest year of birth is {}'.format(int(earliest_birth_year)))
            
            mostrecent_birth_year = df['Birth Year'].max()
            print('The most recent year of birth is {}'.format(int(mostrecent_birth_year)))
    except:
        print('Sorry! No birth year related stats available for this city.')


    print("\nThis took %s seconds." % round(time.time() - start_time, 3))
    print('-'*40)

def raw_data(city):

    """This functions ask user if he or she wants to check and display raw data sample
    and continue iterating through it displaying the next 5 lines of raw data at each iteration."""
    user_response = input('\n Would like to check some raw data? Please select "Y" or "N":').title().strip()
    while user_response == 'Y':
        try:
            for raw_rows in pd.read_csv(CITY_DATA[city], chunksize= 5):
                print(raw_rows)
                user_response = input('\nWould like to check some raw data? Please select "Y" or "N":\n').title().strip()
                if user_response != 'Y' and user_response != 'N':
                    print('\nInvalid input!\n')
                
                elif user_response == 'N' :
                    print('\nSkipping raw data display\n')
                    break
            break
        except Exception:
            print('An unexcpected error has occured!')


def random_df_data(df):
    """This functions ask user if he or she wants to check and display some random df data sample"""
    
    while True:

        # User keeps getting asked if wants to view more data every time Y is selected
        while True:

            # check gathers input from user and returns data if Y or breaks if N     
            check = input('\nWould you like to check a random Data Frame data sample? Please select "Y" or "N":\n').title().strip()
            
            if check in ('Y', 'N'):
                break
            print('\nInvalid input\n')
        
        # Displays a random sample of 5 rows of data
        if check == 'Y':
            random_df_data_rows = df.sample(n=5)
            print(random_df_data_rows)
            
        else:
            print('\nSkipping raw data display.\n')
            break   

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(city)
        random_df_data(df)

        # Asks user if he or she wants to rerun program or exit
        # Takes Yes or No as an input and shows Invalid if any other input was given
        while True:
            restart = input('\nPlease Enter "Yes" if you would like to restart or "No" if you would like to exit program.\n').strip()
            if restart.lower() in ('yes', 'no') :
                break
            print('\nInvalid input\n')
        if restart.lower() =='yes':
            continue
        else:
            print ('\nEnd of data exploration.\nThank you!')
            break

if __name__ == "__main__":
	main()