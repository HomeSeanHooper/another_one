How to run:

`python.37 twistd_app.py`

or 

```
docker build -t test .
docker run -p 8080:8080 test
```

Hit these endpoints:
```
GET localhost:8080/data/<id>`
GET localhost:8080/data/cheapest/<number>
```

What I could have improved with more time:

* Ingestion is not super-efficient. There were some sneaky data issues.
* Should have chosen a mock mongo DB
* More tests to deal with data formats
* A down period after the first request due to lazy data ingestion - this should be finished beforehand. And
for some reason, `@app.before_first_request` will not run :( 

Hope it looks decent enough!


