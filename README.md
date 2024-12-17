Climate Analysis in Hawaii

To help with planning your vacation to Hawaii I've conducted a climate analysis of the area. This analysis is divided into two parts, analyzing and exploring the data and designing a climate app.

In the first part I performed an analysis and data exploration of the climate database provided using Python, SqlAlchemy, Pandas, Matplotlib, and Flask.
I found the most recent date in the dataset, queried the previous 12 months of precipitation data, loaded the results into a Pandas Dataframe, and then plotted the results. I also performed a statistical summary of the data.
Here's a screenshot of the plot:
![Screenshot 2024-12-17 at 5 58 25 PM](https://github.com/user-attachments/assets/aa96dc57-bb96-4b56-9b1f-4504f183b30f)


I also calculted the total number of stations in the dataset, identified the most active station, and queried the lowest, highest, and average temperatires for this station. I then plotted this data as a histogram.
Here's a screenshot of the plot:
![Screenshot 2024-12-17 at 5 58 39 PM](https://github.com/user-attachments/assets/1977c863-3a8e-406d-b697-d85b3e2540f7)

Next I designed a Flash API based on the analysis in part one. The API provides this data:
- `/` - Homepage that lists all available routes.
- `/api/v1.0/precipitation` - Returns the last 12 months of precipitation data as a JSON dictionary.
- `/api/v1.0/stations` - Returns a JSON list of stations from the dataset.
- `/api/v1.0/tobs` - Returns a JSON list of temperature observations for the most-active station for the previous year.
- `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>` - Returns a JSON list of minimum, average, and maximum temperatures for a specified date range.
