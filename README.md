# MUICT2023 ITCS414 Project 2 Section 3

This application is a full text food search engine using `Elasticsearch` and `Flask` application.

Source code for ITCS414 search engine project at Faculty of ICT, Mahidol University.

## Members

- 6488004 Kittipich Aiumbhornsin
- 6488089 Pattaravit Suksri
- 6688092 Thanaphat Sumrith

## Instructions

- Make sure your system has Python3 and Elastic installed.
- Navigate to the application directory and open it on the terminal.
- Run the local Elastic server on port `9200`.
- Edit the file named `elasticsearch_loader.py` as following instructed:
  - Comment out `line 7`.
  - Assign your __Elasticsearch password__ to the variable at `line 7`.
- On the terminal, run `python elasticsearch_loader.py --filename <.json> --index <index_name>`
  - Please note that you might repeat this step multiple times as the amount of the `.json` index files in the directory.
- Create the virtual environment and activate it or install the dependencies directly.
- To install the dependencies, run the following command on the terminal: `pip install -r requirements.txt`
- Edit the file named `__init__.py` as by __assign your Elasticsearch password__ at `line 7`.
- On the terminal, run `python main.py`
  - Please note that by default the application will attempt to run using production setting and the application might ran just a second, to disable this (change to development setting), edit the file named `main.py` as instructed below:
    - __Uncomment__ `line 12`
    - __Comment__ out `line 13`
- Open your browser, paste the following url and click go (enter): `127.0.0.1:5500`
- Explore the amazing application!
