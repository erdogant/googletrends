echo "Cleaning previous builds first.."
rm -rf dist
rm -rf build
rm -rf googletrends.egg-info
rm -rf *.svg

echo "Making new wheel.."
echo ""
python setup.py bdist_wheel
echo ""

echo "Making source build .."
echo ""
python setup.py sdist
echo ""

read -p "Press [Enter] to install the pip package..."
pip install -U dist/googletrends-0.1.0-py3-none-any.whl
echo ""

read -p ">twine upload dist/* TO UPLOAD TO PYPI..."
echo ""

read -p "Press [Enter] key to close window..."
