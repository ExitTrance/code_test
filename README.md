# Coding Test - Weather API Processing

## How to run
Simply run the main.py file from the root directory and provide appropriate arguments. Use the -h flag for help.

```
## Windows
python .\main.py -i 1 -o output.txt -a LINK_TO_API

## Linux
python main.py -i 1 -o output.txt -a LINK_TO_API
```

## Libraries Required
These need installing:
- requests
- pytest

Should already be installed:
- statistics
- json
- sys
- argparse

## Testing
Run this from the root project folder 

```
## Windows
python -m pytest .\tests\weather_test.py .\tests\api_test.py

## Linux
python -m pytest tests/weather_test.py /tests/api_test.py
```
