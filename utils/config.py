
# Importing configparser properly
import configparser

# Creating a ConfigParser object
config = configparser.ConfigParser()

# Reading the property file (assuming it's named 'config.re')
config.read('config/config.ini')