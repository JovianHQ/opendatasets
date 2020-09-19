# opendatasets

A curated collection of datasets for data analysis &amp; machine learning, downloadable with a single Python command.

Try it out online: https://jovian.ml/aakashns/opendatasets-demo

## Installation & Usage

Install the library using `pip`:

```
pip install opendatasets --upgrade
```

To use the library, just import it and use the `download` function.

```
import opendatasets as od
od.download('stackoverflow-developer-survey-2020')
```

See the next section for a list of available dataset IDs.

## Datasets

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

### Adding Datasets

TODO - more details will be added here later

This package is developed and mainted by the [Jovian.ml](https://www.jovian.ml) team.
