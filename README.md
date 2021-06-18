# opendatasets

`opendatasets` is a Python library for downloading datasets from online sources like [Kaggle](https://www.kaggle.com/datasets) and Google Drive using a simple Python command. 


### Installation

Install the library using `pip`:

```
pip install opendatasets --upgrade
```

### Usage - Downloading a dataset

Datasets can be downloaded within a Jupyter notebook or Python script using the `opendatasets.download` helper function. Here's some sample code for downloading the [US Elections Dataset](https://www.kaggle.com/tunguz/us-elections-dataset):

```
import opendatasets as od
dataset_url = 'https://www.kaggle.com/tunguz/us-elections-dataset'
od.download('https://www.kaggle.com/tunguz/us-elections-dataset')
```

`dataset_url` can also point to a public Google Drive link or a raw file URL.

### Kaggle Credentials

`opendatasets` uses the [Kaggle Official API](https://github.com/Kaggle/kaggle-api) for donwloading dataset from Kaggle.  Follow these steps to find your API credentials:

1. Sign in to  [https://kaggle.com/](https://kaggle.com),  then click on your profile picture on the top right and select "My Account" from the menu.

2. Scroll down to the "API" section and click "Create New API Token". This will download a file `kaggle.json` with the following contents:

```
{"username":"YOUR_KAGGLE_USERNAME","key":"YOUR_KAGGLE_KEY"}
```

3. When you run `opendatsets.download`, you will be asked to enter your username & Kaggle API, which you can get from the file downloaded in step 2.

Note that you need to download the `kaggle.json` file only once. You can also place the `kaggle.json` file in the same directory as the Jupyter notebook, and the credentials will be read automatically.

### Some interesting datasets

You can find interesting datasets on Kaggle: https://www.kaggle.com/datasets

*You can also create a new dataset on Kaggle by uploading a CSV file here: https://www.kaggle.com/datasets?new=true (make sure to keep your dataset public, otherwise it will not be downloadable)*

- Video Games sales: https://www.kaggle.com/gregorut/videogamesales
- World University Rankings: https://www.kaggle.com/mylesoneill/world-university-rankings
- Netflix Tv shows and Movies: https://www.kaggle.com/shivamb/netflix-shows/notebooks
- StackOverflow Developer Survey: https://www.kaggle.com/stackoverflow/stack-overflow-2018-developer-survey
- Google Play Store Android Apps Data: https://www.kaggle.com/lava18/google-play-store-apps
- Indian Stock Market Data: https://www.kaggle.com/rohanrao/nifty50-stock-market-data
- Indian Air Quality: https://www.kaggle.com/rohanrao/air-quality-data-in-india
- Worldwide Covid-19 Cases: https://www.kaggle.com/imdevskp/corona-virus-report
- USA Covid-19 Cases: https://www.kaggle.com/sudalairajkumar/covid19-in-usa
- US Election Results (2012): https://www.kaggle.com/tunguz/us-elections-dataset
- US Stock Market: https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs/
- Crop production in India: https://www.kaggle.com/srinivas1/agricuture-crops-production-in-india
- Agricultural raw material prices: https://www.kaggle.com/kianwee/agricultural-raw-material-prices-19902020
- Agricultural land values: https://www.kaggle.com/jmullan/agricultural-land-values-19972017
- Digital payments in India: https://www.kaggle.com/lazycipher/upi-usage-statistics-aug16-to-feb20
- US Unemployment Rate Data: https://www.kaggle.com/jayrav13/unemployment-by-county-us
- India Road accident Data: https://community.data.gov.in/statistics-of-road-accidents-in-india/
- Data Science Jobs Data:
    - https://www.kaggle.com/sl6149/data-scientist-job-market-in-the-us
    - https://www.kaggle.com/jonatancr/data-science-jobs-around-the-world
    - https://www.kaggle.com/rkb0023/glassdoor-data-science-jobs
- Youtube Trending Videos: https://www.kaggle.com/datasnaek/youtube-new
- Asteroid Dataset: https://www.kaggle.com/sakhawat18/asteroid-dataset
- Solar flares Data: https://www.kaggle.com/khsamaha/solar-flares-rhessi
- F-1 Race Data: https://www.kaggle.com/cjgdev/formula-1-race-data-19502017
- Automobile Insurance: https://www.kaggle.com/aashishjhamtani/automobile-insurance
- PUBG video game matches: https://www.kaggle.com/skihikingkevin/pubg-match-deaths
- CounterStrike GO (video game)
    - https://www.kaggle.com/mateusdmachado/csgo-professional-matches
    - https://www.kaggle.com/skihikingkevin/csgo-matchmaking-damage
- Dota 2 (video game): https://www.kaggle.com/devinanzelmo/dota-2-matches
- Cricket One-Day Internationals Data: https://www.kaggle.com/jaykay12/odi-cricket-matches-19712017
- Cricket Indian Premier League Data: https://www.kaggle.com/nowke9/ipldata
- Basketball (NCAA): https://www.kaggle.com/ncaa/ncaa-basketball
- Basketball NBA Players Stats: https://www.kaggle.com/ncaa/ncaa-basketball
- Football datasets: 
    - https://www.kaggle.com/martj42/international-football-results-from-1872-to-2017
    - https://www.kaggle.com/abecklas/fifa-world-cup
    - https://www.kaggle.com/egadharmawan/uefa-champion-league-final-all-season-19552019
- Hotel Booking Demand: https://www.kaggle.com/jessemostipak/hotel-booking-demand
- New York Airbnb listings: https://www.kaggle.com/dgomonov/new-york-city-airbnb-open-data


Other sources to look for datasets: 
- [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/index.php)
- [awesome-public-datasets](https://github.com/awesomedata/awesome-public-datasets)
- [Google Dataset Search](https://datasetsearch.research.google.com)

*If you use an external source other than Kaggle, you'll create a new dataset on Kaggle by uploading a CSV file here: https://www.kaggle.com/datasets?new=true (make sure to keep your dataset public, otherwise it will not be downloadable using `opendatasets`)*



## Curated Datasets

`opendatasets` also provides some curated datsets that you can download by passing the Dataset ID to `opendatasets.download`. Here's an example:

```
import opendatasets
opendatasets.download('stackoverflow-developer-survey-2020')
```

The following datasets are available for download.

<table>
    <tr>
        <th>Dataset ID</th>
        <th>Description</th>
        <th>Source</th>
    </tr>
    <tr>
        <td><code>stackoverflow-developer-survey-2020</code></td>
        <td>Stack Overflow Developer Survey 2020</td>
        <td>
            <a href="https://insights.stackoverflow.com/survey/">Stack Overflow</a>
        </td>
    </tr>
    <tr>
        <td><code>owid-covid-19-latest</code></td>
        <td>Covid-19 Stats by Our World in Data</td>
        <td>
            <a href="https://github.com/owid/covid-19-data/tree/master/public/data">Our World in Data</a>
        </td>
    </tr>
    <tr>
        <td><code>state-of-javascript-2016</code></td>
        <td>State of Javascript Annual Survey 2016</td>
        <td>
            <a href="https://www.kaggle.com/sachag/state-of-js-2019">StateOfJS</a>
        </td>
    </tr>
    <tr>
        <td><code>state-of-javascript-2017</code></td>
        <td>State of Javascript Annual Survey 2017</td>
        <td>
            <a href="https://www.kaggle.com/sachag/state-of-js-2019">StateOfJS</a>
        </td>
    </tr>
    <tr>
        <td><code>state-of-javascript-2018</code></td>
        <td>State of Javascript Annual Survey 2018</td>
        <td>
            <a href="https://www.kaggle.com/sachag/state-of-js-2019">StateOfJS</a>
        </td>
    </tr>
    <tr>
        <td><code>state-of-javascript-2019</code></td>
        <td>State of Javascript Annual Survey 2019</td>
        <td>
            <a href="https://www.kaggle.com/sachag/state-of-js-2019">StateOfJS</a>
        </td>
    </tr>
    <tr>
        <td><code>countries-languages-spoken</code></td>
        <td>Languages Spoken in Different Countries</td>
        <td>
            <a href="https://www.infoplease.com/world/countries/languages-spoken-in-each-country-of-the-world">Infoplease</a>
        </td>
    </tr>
</table>

More datasets will be added soon..

## Contributing

This is an open source project and we welcome contributions.

### Local Development Setup

1. Clone the repository:

```
git clone https://github.com/JovianML/opendatasets.git
```

2. Setup the Python environment for development

```
conda create -n opendatasets python=3.5
conda activate opendatasets
pip install -r requirements.txt
```

3. Open up the project in VS code and make your changes. Make sure to install the Python Extension for VS Code and select the `opendatasets` conda environment.

This package is developed and maintained by the [Jovian](https://www.jovian.ai) team.
