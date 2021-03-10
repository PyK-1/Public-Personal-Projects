import csv
import statistics
import matplotlib.pyplot as plt
import streamlit as st
import os
import pandas as pd
import datetime
import numpy as np


def main():
    # Disable warning that shows up
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Dictionaries, lists, and variables initialized
    analysisDictionary = {"name": 1, "host_id": 2, "host_name": 3, "neighbourhood": 5, "room_type": 8, "price": 9, "minimum_nights": 10, "number_of_reviews": 11}
    mainOptionsDictionary = {"Neighbourhood Listings & Reviews Data": 1, "Pricing Data": 2}
    neighborhoodNames = ('West Cambridge', 'North Cambridge', 'The Port', 'Neighborhood Nine', 'Riverside', 'Mid-Cambridge', 'Agassiz', 'Cambridgeport', 'East Cambridge', 'Strawberry Hill', 'Wellington-Harrington', 'Area 2/MIT')

    mainListingData = "airbnb_cambridge_listings_20201123.csv"
    extraListingData = "airbnb_cambridge_20201123.csv"

    filesDict = {'Main Listing Info': mainListingData, 'Listing History & Additional Info': extraListingData}

    # Selecting file sidebar with title and header
    st.sidebar.title('AirBnB Cambridge Listing Data')
    st.sidebar.subheader('Created by Peter Kassabov')
    fileSelection = st.sidebar.selectbox("Select a file option: ", list(filesDict.keys()))


    if fileSelection == 'Main Listing Info':
        # Interface file selection details
        st.sidebar.header('Options')
        st.write("File Name: ", mainListingData)
        listingDataSelection = st.sidebar.radio("Select an option: ", list(mainOptionsDictionary.keys()))

        # Main listing information dataframe created
        airbnbMainDF = pd.read_csv( os.path.join("airbnb_cambridge_listings_20201123.csv"),
                            usecols = ['id', 'name', 'neighbourhood', 'room_type', 'price', 'number_of_reviews'])
        st.write("Dataframe chosen: ", airbnbMainDF)

        # Pivot tables and graphs made for neighbourhood data when selected
        if listingDataSelection == 'Neighbourhood Listings & Reviews Data':
            neighborhoodSelection = st.sidebar.radio("Select which neighbourhood to view listings from: ", list(neighborhoodNames))
            table1 = pd.pivot_table(data=airbnbMainDF, index=['neighbourhood'], aggfunc={'neighbourhood':np.count_nonzero})
            table3 = pd.pivot_table(data=airbnbMainDF, index=['neighbourhood'], aggfunc={'number_of_reviews':np.sum})
            st.write("Total listings in each neighbourhood:")
            st.write(table1)
            st.write("Below is the total listings available for each neighbourhood shown in a bar chart:")
            table1bargraph = table1.plot(kind='bar', ylabel='Number of Listings', xlabel='Neighbourhood', title='Total Listings In Each Neighbourhood', color='green')
            st.pyplot()

            st.write("Total reviews for each neighbourhood:")
            st.write(table3)
            st.write("Below is the total reviews for each neighborhood shown in a bar chart:")
            table3bargraph = table3.plot(kind='bar', ylabel='Number of Reviews', xlabel='Neighbourhood', title='Total Reviews For Each Neighbourhood', color='c')
            st.pyplot()

        # Pivot table and graph made for pricing data
        if listingDataSelection == 'Pricing Data':
            table2 = pd.pivot_table(data=airbnbMainDF, index=['neighbourhood'], aggfunc={'price':np.mean})
            table2 = table2.sort_values(by=('price'), ascending=True)
            st.write("Average price per night in each neighbourhood, from least expensive to most:")
            st.write(table2)
            st.write("Below is the average price per night for each neighborhood displayed in a line chart:")
            table2linegraph = table2.plot(kind='line', ylabel='Price in $', xlabel='Neighbourhood', title='Average Price/Night For Each Neighbourhood', fontsize=6, color='indigo')
            st.pyplot()
    else:
        # Additional AirBnB listing CSV file loaded into dataframe and shown to user
        st.write("File Name: ", extraListingData)
        airbnbDatesDF = pd.read_csv( os.path.join("airbnb_cambridge_20201123.csv"),
                            usecols = ['listing_id', 'date'])
        st.write("Dataframe chosen: ", airbnbDatesDF)

        # Creating a pivot table to show the number of bookings for each unique ID
        table4 = pd.pivot_table(data=airbnbDatesDF, index=['listing_id'], aggfunc={'date':np.count_nonzero})
        st.write("Number of bookings to date per ID:")
        st.write(table4)


main()


