# `ip-scan-results`

A *local* web app for investigating results of [nmap](https://nmap.org) scans.  The
standard nmap xml ouptut file format is supported for uploading.  All previous records
are purged when a new file is uploaded.

## Run app

1.  Copy `dotenv` to `.env`, and enter a random string for the `XSS_KEY`
1.  Install dependencies
    ```
    make setup
    ```
1.  Run the app:
    ```
    source venv/bin/activate
    make run
    ```
1.  The app will be available on your browser at [http://127.0.0.1:8080](http://127.0.0.1:8080)

## Objectives

1.  Build a REST API to import a single nmap scan result.
    1.  The API should accept a single nmap scan file.
    1.   Detail which you chose and why.
1.  Ingest the nmap result into a sqlite database.
1.  Build a UI that allows a user to view the results of nmap scans by IP address.


## Decisions

### File format

The xml file is easiest to work with as it is intended to be a machine readable
format.  In addition, python has a `libnmap` package that readily parses `nmap`
xml outputs.

### How to store data in SQLite

In example files, only 5 ports are scanned for each host.  This leaves to main
options for working with the SQLite datastore:

1.  A schema that enumerates these ports will allow for SQL queries on the
    ports and services but would make the entire app dependent on this particular
    set of ports.
1.  Serializing the services and ports for each host and storing as a text string
    would make it extensible to arbitrary numbers of ports, but, would make it
    impossible to perform SQL queries on port/service data.

The code in this repository follows the first option.

## Return Types

The API will return json at the following endpoints for any `Accept` header except
`text/html`. (If no Accept header is provided, it will also return json)
```
/scan
/scan/open/80
/scan/open/443
/scan/open/5000
/scan/open/8080
/scan/open/8443
```
For the above paths, With the header `Accept: text/html`, html will be returned.

## Next Steps

1. Package in a Dockerfile, non-root user, etc
1. Run with an actual web server
1. Implement logger
1. Add webapp tests
1. Make the UI look nice
