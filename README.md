# googletrends

[![Python](https://img.shields.io/pypi/pyversions/googletrends)](https://img.shields.io/pypi/pyversions/googletrends)
[![PyPI Version](https://img.shields.io/pypi/v/googletrends)](https://pypi.org/project/googletrends/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/googletrends/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/googletrends)](https://pepy.tech/project/googletrends)
[![Coffee](https://img.shields.io/badge/coffee-black-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)

* googletrends is Python package to examine trending, spatio and temporal google searching for input queries.

Data is al arround us. Some data is easy to get, others are not. Especially when it comes to what people are "thinking" related to an issue/brand/company can be though. However, the "thinking" process can supported by googling about the subject. So if we know what people are searching for, it can give insights in the "common" thoughts. To make it a bit less creepy, lets not do this on an individual basis. I developed the python package googletrends that allows to easily examine the search results per country/region and/or per time-frame and with(out) a specific keyword.

To demonstrate this, lets examine the google searches for the keywords "Corona" and "Virus", "covid-19" in the Netherlands, Italy, Belgium and Germany starting from December 2019 up to today. If you want to examine other keywords/countries/time frames, simply pip install the library.

<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/summary.png" width="1000" />
</p>


### Content
- [Installation](#-installation)
- [Examples](#-installation)
- [Contribute](#-contribute)
- [Citation](#-citation)
- [Maintainers](#-maintainers)

### Installation
* Install googletrends from PyPI (recommended). googletrends is compatible with Python 3.6+ and runs on Linux, MacOS X and Windows. 
* A new environment can be created as following: 
```python
conda create -n env_googletrends python=3.6
conda activate env_googletrends
```

Pip install:
```python
pip install googletrends
```

* Alternatively, install googletrends from the GitHub source:
```bash
git clone https://github.com/erdogant/googletrends.git
cd googletrends
python setup.py install
```  

#### Import googletrends package
```python
import googletrends as googletrends
```

#### Get country names and abbrevations.

```python
geo_names = googletrends.get_geo_names()
print(geo_names)

#     code               country
# 0     AD               andorra
# 1     AE  united arab emirates
# 2     AF           afghanistan
# 3     AR             argentina
# 4     AO                angola
# ..   ...                   ...
# 251   YE                 yemen
# 252   YT               mayotte
# 253   ZA          south africa
# 254   ZM                zambia
# 255   ZW              zimbabwe

```


#### Examine google searches over time.

In this example multiple searchwords are examined for multiple countries over time.
Countries can be in the form of their abbrevation or country name.
The until date is not given and automatically set on today.

```python
# Gather temporal searches
results = googletrends.temporal(['corona','covid-19','virus'], geo=['NL','DE','italy','BE'], date_start='01-01-2020')

# Make plot using default settings
googletrends.plot(results)
```

Progress looks like this:

```python
# [googletrends] Collecting trends over time for geographically: ['NL', 'DE', 'italy', 'BE']
# [googletrends] 01 January 2020 - 30 March 2020
# [worldmap] Downloading resources..
# [worldmap.extract] Warning: Directory with maps does not exist: .\worldmap\worldmap\data\SVG_MAPS
# [EXTRACT FILES] Directory already exists and will be used: .\worldmap\worldmap\data
# [EXTRACT FILES] Extracting SVG_MAPS.zip..
# 100%|██████████| 1/1 [00:00<00:00,  9.12it/s]
# [EXTRACT FILES] Done!
# [googletrends] [NL] Working on corona..

# [googletrends] [NL] Working on covid-19..
# [googletrends] [DE] Working on corona..
# [googletrends] [DE] Working on covid-19..
# [googletrends] [IT] Working on corona..
# [googletrends] [IT] Working on covid-19..
# [googletrends] [BE] Working on corona..
# [googletrends] [BE] Working on covid-19..
```

#### Color and make different subgroups for the results.

```python
googletrends.plot(results, color_by_searchword=False, group_by_searchword=False)
```
<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/fig1.png" width="600" />
</p>

```python
googletrends.plot(results, color_by_searchword=True, group_by_searchword=False)
```
<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/fig2.png" width="600" />
</p>

```python
googletrends.plot(results, color_by_searchword=False, group_by_searchword=True)
```
<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/fig3.png" width="600" />
</p>


```python
googletrends.plot(results, color_by_searchword=True, group_by_searchword=True)
```
<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/fig4.png" width="600" />
</p>


#### Examine google searches over geographical locations.

In this example multiple searchwords are examined for multiple geographical locations.
All frequencies are summarized into one value between the start-stop date.
Countries can be in the form of their abbrevation or country name.

```python
# Gather searches over geographical locations
results = googletrends.spatio(['corona','covid-19','virus'], geo=['NL','DE','italy','BE'], date_start='01-01-2020')

# Make plot
googletrends.plot(results)
```
<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/spatio_NL.png" width="400" />
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/spatio_DE.png" width="400" />
</p>
<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/spatio_IT.png" width="400" />
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/spatio_BE.png" width="400" />
</p>

<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/Netherlands_total.png" width="250"/>
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/Germany_total.png" width="250"/>
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/Italy_total.png" width="250"/>
</p>

```python
# Make worldmap plot
googletrends.plot_worldmap(results)
```
<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/total_worldmap.png" width="600" />
</p>

#### Examine trending searches.

In this example multiple searchwords at multiple geographical locations are examined for trending searches.
All frequencies are summarized into one value between the start-stop date.

```python
# Gather searches over geographical locations
results = googletrends.trending(['corona','covid-19','virus'], geo=['NL','DE','italy','BE'], date_start='01-01-2020')

# Make plot
googletrends.plot(results)
```

Trending searchwords in the Netherlands

<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/trending_NL.png" width="500" />
</p>

Trending searchwords in Germany

<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/trending_DE.png" width="500" />
</p>

Trending searchwords in Italy

<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/trending_IT.png" width="500" />
</p>

Trending searchwords in Belgium

<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/trending_BE.png" width="500" />
</p>


#### Citation
Please cite googletrends in your publications if this is useful for your research. Here is an example BibTeX entry:
```BibTeX
@misc{erdogant2020googletrends,
  title={googletrends},
  author={Erdogan Taskesen},
  year={2019},
  howpublished={\url{https://github.com/erdogant/googletrends}},
}
```

* References: http://www.w3.org/Consortium/Legal/copyright-software

### Maintainer
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)
* Contributions are welcome.
* If you wish to buy me a <a href="https://erdogant.github.io/donate/?currency=USD&amount=5">Coffee</a> for this work, it is very appreciated :)
