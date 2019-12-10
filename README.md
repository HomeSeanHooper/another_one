How to run:

`python.37 src/products_service.py`

What I could have improved with more time:

* Ingestion is not super-efficient. There were some sneaky data issues.
* Should have chosen a mock mongo DB
* More tests to deal with data formats
* a Docker file
* Run in Twistd rather than development Flask
* A down period after the first request due to lazy data ingestion - this should be finished beforehand.

Hope it looks decent enough!


