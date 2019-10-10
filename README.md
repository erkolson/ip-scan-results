# `ip-scan-results`

## Objectives
  1. Build a REST API to import a single nmap scan result.
    1. The API should accept a single nmap scan file.
    1. Detail which you chose and why.
  1. Ingest the nmap result into a sqlite database.
  1. Build a UI that allows a user to view the results of nmap scans by IP address.


## Decisions

How to store the data in sqlite?

In example files, only 5 ports are scanned for each host.

- A schema that enumerates these ports will allow for SQL queries on the
ports and services but would make the entire app dependent on this particular
set of ports.
- Serializing the services and ports for each host and storing as a text string
would make it extensible to arbitrary numbers of ports, but, would make it
impossible to perform SQL queries on port/service data.
