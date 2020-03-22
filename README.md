# googletrends

[![Python](https://img.shields.io/pypi/pyversions/googletrends)](https://img.shields.io/pypi/pyversions/googletrends)
[![PyPI Version](https://img.shields.io/pypi/v/googletrends)](https://pypi.org/project/googletrends/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/googletrends/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/googletrends/week)](https://pepy.tech/project/googletrends/week)
[![Donate](https://img.shields.io/badge/donate-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)

* googletrends is Python package

### Contents
- [Installation](#-installation)
- [Requirements](#-Requirements)
- [Quick Start](#-quick-start)
- [Contribute](#-contribute)
- [Citation](#-citation)
- [Maintainers](#-maintainers)
- [License](#-copyright)

### Installation
* Install googletrends from PyPI (recommended). googletrends is compatible with Python 3.6+ and runs on Linux, MacOS X and Windows. 
* It is distributed under the MIT license.

### Requirements
* It is advisable to create a new environment. 
```python
conda create -n env_googletrends python=3.6
conda activate env_googletrends
pip install -r requirements
```

#### Quick Start
```
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

#### Example:
```python
df = pd.read_csv('https://github.com/erdogant/hnet/blob/master/googletrends/data/example_data.csv')
model = googletrends.fit(df)
G = googletrends.plot(model)
```
<p align="center">
  <img src="https://github.com/erdogant/googletrends/blob/master/docs/figs/fig1.png" width="600" />
  
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

#### Donation
* This work is created and maintained in my free time. Contributions of any kind are very appreciated. <a href="https://erdogant.github.io/donate/?currency=USD&amount=5">Sponsering</a> is also possible.

