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

</table>

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
