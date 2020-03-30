# googletrends

[![Python](https://img.shields.io/pypi/pyversions/googletrends)](https://img.shields.io/pypi/pyversions/googletrends)
[![PyPI Version](https://img.shields.io/pypi/v/googletrends)](https://pypi.org/project/googletrends/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/googletrends/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/googletrends/week)](https://pepy.tech/project/googletrends/week)
[![Donate](https://img.shields.io/badge/donate-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)

* googletrends is Python package to examine trending, spatio and temporal google searching for input queries.
* Distributed under the MIT license.

### Contentsa 
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Contribute](#-contribute)
- [Citation](#-citation)
- [Maintainers](#-maintainers)
- [License](#-copyright)

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

#### Examine google searches over time.

In this example multiple searchwords are examined for multiple countries over time.
Countries can be in the form of their abbrevation or country name.
The until date is not given and automatically set on today.

```python
# Gather temporal searches
results = googletrends.temporal(['corona','covid-19','virus'], geo=['NL','DE','italy','BE'], date_start='01-01-2020')

# Make plot
googletrends.plot(results)
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
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/fig_spatio_1.png" width="600" />
</p>

```python
# Make worldmap plot
googletrends.plot_worldmap(results)
```
<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/fig_spatio_2.png" width="600" />
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
<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/fig_trending.png" width="600" />
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

#### References
* 
   
#### Maintainers
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)

#### Contribute
* Contributions are welcome.

#### Licence
See [LICENSE](LICENSE) for details.

#### Coffee
* This work is created and maintained in my free time. If you wish to buy me a <a href="https://erdogant.github.io/donate/?currency=USD&amount=5">Coffee</a> for this work, it is very appreciated.

