import time
import pandas as pd
import numpy as np
import datetime
import pprint


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    name = input("Please enter your name")
    print('Hello {name.title()}! Let\'s explore some US bikeshare data!')
    print('Press r to restart at anytime, Enjoy!!')


    while True:
        break_out_flag_1 = False  # A flag to be used to break out of the loop if specified as True
        continue_flag_1 = False   # A flag to rerun a loop if specified as True
        while True:
            # get user input for city (chicago, new york city, washington)
            city = input("Would you like to view the data for Chicago, New York City, or Washington: ")
            if city.lower() in ['chicago','new york city','washington']:
                user_input = input(f'I see you will like to view the data for {city.title()}, press "y" to proceed or "n" to restart the program: ')
                if user_input.lower() == 'n':
                    continue
                elif user_input.lower() == 'y':
                    city = city.lower()
                    break

            elif city.lower() == 'r':
                continue

            else:
                print(f"{city.title()} is not a valid city name, please enter a valid city: ")
                continue


        while True:
            break_out_flag_2 = False  # A flag to break out of the loop if specified as True
            continue_flag_2 = False   # A flag to rerun the loop if specified as True
            # get user input for month (all, january, february, ... , june)
            filter = input("Would you like to filter by month or day: ")
            if filter.lower() == 'month':
                print("We will make sure we filter by month")
                while True:
                    month = input('Please enter the month(in full) you want to filter by , type "all" if you want to view the data for all the months: ')
                    if month.lower() in ['all','january','february','march','april','may','june']:
                        month = month.lower()
                        day = None
                        break_out_flag_1 = True
                        break_out_flag_2 = True
                        break
                    elif month.lower() == 'r':
                        break_out_flag_2 = True
                        break
                    else:
                        print(f"{month} is not a valid month: ")
                        continue

            # get user input for day of week (all, monday, tuesday, ... sunday)
            elif filter.lower() == 'day':
                print("We will make sure we filter by day")
                while True:
                    day = input('Which day? please type a day monday, tuesday, wednesday, thursday, friday, saturday, sunday: ')
                    if day.lower() in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
                        day = day.lower()
                        month = None
                        break_out_flag_1 = True
                        break_out_flag_2 = True
                        break

                    elif day.lower() == 'r':
                        break_out_flag_2 = True
                        break
                    else:
                        print("please enter a valid day of the week")
                        continue

            # Restart the code if the user entered 'r'
            elif filter.lower() == 'r':
                continue_flag_1 =True
                break

            # Handle unexpected errors
            else:
                print('That is not a valid value')
                continue_flag_2 = True
                continue

            # Break out of the inner while loop if the break out flag is set to True
            if break_out_flag_2:
                break

            # rerun inner while loop if the break out flag is set to True
            if continue_flag_2:
                continue

        # Break out of the outer while loop if the break out flag is set to True
        if break_out_flag_1:
            break

        # rerun the outer while loop if the break out flag is set to True
        if continue_flag_1:
            continue

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
    df = pd.read_csv(CITY_DATA[city]) # read the data of the city specified
    df['month'] = pd.to_datetime(df['Start Time']).dt.month # Create a mew column month to get the month from the start time column
    df['weekday'] = pd.to_datetime(df['Start Time']).dt.day_name() # create a new column to get the day

    if month and not day:  # Check if there is a value for month and none for day
        if month == 'all':
            df = df
        elif month in ['january','february','march','april','may','june']:
            df['month'].replace([1,2,3,4,5,6], ['january','february','march','april','may','june'], inplace =True) # convert the month from numeric form to word form
            df['month'] = df['month'].apply(lambda x:x.title()) # apply the title method to every value in the month columns
            df = df[df['month'] == month.title()] # select only the data points containing the months specified
    elif not month and day: # Check if there is a value for day and none for month
        if day == 'all':
            df = df
        elif day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
            df = df[df['weekday'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    print('Calculating statisic...')
    print('\nWhat is the most popular month for travelling?')
    print(df['month'].mode()[0])
    print('This took %s seconds.'% (time.time() - start_time))

    # display the most common day of week
    print('\nCalculating statisic...')
    print('\nWhat is the most popular day of the week for travelling? ')
    print(df['weekday'].mode()[0])
    print('This took %s seconds.'% (time.time() - start_time))

    # display the most common start hour
    print('\nCalculating statisic...')
    print('\nWhat is the most popular start hour for travelling?')
    df['Start_hour'] = pd.to_datetime(df['Start Time']).dt.hour
    print(df['Start_hour'].mode()[0])
    print('This took %s seconds.'% (time.time() - start_time))


    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Calculating statisic...')
    print('\nWhat is the most popular start station for travelling? ')
    print(df['Start Station'].mode()[0])
    print('This took %s seconds.'% (time.time() - start_time))

    # display most commonly used end station
    print('\nCalculating statisic...')
    print('\nWhat is the most popular end station for travelling?')
    print(df['End Station'].mode()[0])
    print('This took %s seconds.'% (time.time() - start_time))

    # display most frequent combination of start station and end station trip

    print('\nCalculating statisic...')
    print('\nWhat is the most frequent combination of start station and end station for travelling? ')
    print(df.groupby(['Start Station','End Station'])['Start_hour'].count().sort_values(ascending=False).index[0])
    print('This took %s seconds.'% (time.time() - start_time))

    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Calculating statisic...')
    print('\nWhat is the total travel time and what was the average time sepnt on each trip? ')
    sum_travel_time= df['Trip Duration'].sum(axis=0)
    avg_travel_time= df['Trip Duration'].mean(axis=0)
    print(datetime.timedelta(seconds=float(sum_travel_time)), datetime.timedelta(seconds=float(avg_travel_time)))
    print('\nThis took %s seconds.'% (time.time() - start_time))


    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Calculating statisic...')
    print('\nWhat is the breakdwon of users? ')
    print(df['User Type'].value_counts())
    print('This took %s seconds.'% (time.time() - start_time))

    # Display counts of gender
    print('Calculating statisic...')
    print('\nWhat is the breakdwon by gender? \n')
    try:
        gender = df['Gender'].value_counts()
    except KeyError:
        print("No gender to share for this particular city")
    else:
        print(gender)
        print('This took %s seconds.'% (time.time() - start_time))
    # Display earliest, most recent, and most common year of birth
    try:
        earliest, most_recent, most_common = int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(df['Birth Year'].mode()[0])
    except KeyError:
        print('No birth year data to share for this particular city')
    else:
        print('Calculating statisic...')
        print('\nWhat is the oldest, youngest and most popular year of birth respectively? \n')
        print(earliest, most_recent, most_common)
        print('\nThis took %s seconds.'% (time.time() - start_time))

    print('-'*40)

def individual_trip_data(df):
    """Asks user to specify if they want to see individual data points and displays them"""
    initial = 0
    step = 5
    while True:
        user_response = input('Would you like to view individual trip data? "yes" or "no" ')
        if user_response.lower() == 'yes':
            try:
                record_dict = df[initial:initial+step].to_dict(orient='records')
            except KeyError:
                break
            else:
                for record in record_dict:
                    pprint.pprint(record)
                initial = (initial + step)

        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        individual_trip_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
