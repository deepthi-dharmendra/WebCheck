

\# WebCheck — Website Availability \& HTTP Diagnostics



A Python-based website monitoring tool that checks HTTP responses, measures response times, identifies unsuccessful requests, and exports diagnostic results to CSV.



\## Features



\- Checks website availability using HTTP requests

\- Measures HTTP response time in milliseconds

\- Reports HTTP status codes, including errors such as 404

\- Distinguishes server reachability from page availability

\- Supports repeated checks (1–20 attempts)

\- Calculates average response time for checks that receive HTTP responses

\- Handles connection errors and request timeouts

\- Exports timestamped diagnostic results to CSV

\- Includes automated unit tests using Python's `unittest` and mocking



\## Requirements



\- Python 3

\- Internet connection for live website checks



No third-party Python packages are required.



\## Run the Application



From the project directory, run:



```bash

python webcheck.py

```



Enter a website URL and choose the number of checks when prompted.



\## Run Automated Tests



```bash

python -m unittest -v test\_webcheck.py

```



The tests use mocked HTTP responses to verify key behaviours without depending on live websites.



\## Output



The monitoring report is saved as `webcheck\_report.csv` in the current working directory.



The CSV file records timestamps, URLs, HTTP status codes, response times, reachability, availability, and error details.



\## Project Structure



```text

WebCheck/

├── webcheck.py

├── test\_webcheck.py

├── README.md

├── .gitignore

└── screenshots/

&#x20;   ├── website-check.png

&#x20;   └── tests-passed.png

```



\## Screenshots



\### Website Monitoring



!\[WebCheck monitoring results](screenshots/website-check.png)



\### Automated Tests



!\[WebCheck automated tests](screenshots/tests-passed.png)



\## Limitations



\- Results reflect the checks performed during a run and do not guarantee continuous uptime.

\- HTTP availability is defined as receiving a status code from 200 through 399.

\- The project does not currently perform dedicated TLS certificate expiry checks.



\## Technologies



Python, HTTP, URL handling, CSV reporting, unit testing, mocking, and basic network diagnostics.



