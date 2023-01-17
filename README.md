# Solarized

A simulation program to track solar power production and consumption in a neighbourhood and generate related finances.

## Dependencies

* python3
  * PyQt5
  * matplotlib
  * mysql-connector-python
* MySQL

## Installation

1. Clone this repository into a directory.
2. Edit the file *bridge.py*. Set the variables user, passwd and database as the username of the mysql user, password and the database name respectively.

```python
#========== GLOBALS ==========#

host = "localhost"
user = "<username>"
passwd = "<password>"
database = "<database>"
```

3. Create the above mentioned user with password and database in mysql.

## Usage

In order to run the program, execute *gui.py* present in the base directory. The program comes with various shortcut keys which are listed below.

### Shortcuts

|Key|Action|
|---|---|
|a|Add house|
|v|Remove house|
|/|Search house|
|space|Run one cycle|
|f|Fast forward a number of cycles|
|g|Get the profit generated|
|r|Update the table from the database|
|n|Load the default table|
|c|Clear the current table|
|x|Clear the graph|
|o|Import table from csv|
|s|Export table to csv|
|q|Quit the program|

## Screenshots

![image](https://user-images.githubusercontent.com/122805944/212985839-e55f9120-6406-4e1b-bd2e-c23e6a657d3e.png)

## File descriptions
  
|File|Description|
|---|---|
|bridge.py|Contains the functions for manipulating the mysql database|
|grid.py|Generates the production and consumption matrix|
|gui.py|Display the simulation|
|port.py|Provides import/export functionalities|
|default.csv|Stores the default data values|
|settings.dat|Stores saved settings|

