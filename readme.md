# Project Name

## Project Structure

```
project-root/
│
├── app/
│
├── assets/
│
├── db/
│
├── scripts/
│
├── .env
│
├── docker-compose.yml
│
├── readme.md
│
└── start_services.sh
```

- **app**: Contains the api code.

- **assets**: Directory for all CSVs, including `airports_w_wiki.csv`

- **db**: Database-related files.

- **scripts**: Utility and setup scripts.
  - `eval.py`: Provided file for testing.
  - `filterAirportsWithWk.py`: Filtering the airports with wiki links on file `assets/airports.csv`.
  - `getUsers.py`: Getting users from 42Hacks api and generate the file `assets/user_locations.csv`.
  - `transformCSVToSQL.py`: Read the files `./assets/user_closest_airports.csv` and `./assets/airports_w_wiki.csv` to generate the file `init.sql` that will be responsible for populate the database.
  - `userClosestAirport.py`: Read the files `/assets/user_locations.csv` and `/assets/airports_w_wiki.csv` to generate the file `/assets/user_closest_airports.csv` that constains the closest file to each user.

- **.env**: Environment variables for configuration. Should be not versionated but it is for convinence.

- **docker-compose.yml**: Docker Compose file for setting up services.

- **start_services.sh**: Script to start services.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

For convinence all the files that need to be generated or downloaded are already included in this repo, so it is possible to just run the service. But I leave here a guide for how generate each one of them.

1. Clone the repository: TODO

    ```bash
    git clone https://github.com/mfenerich/42Hacks.git
    cd 42Hacks
    ```

2. Give permission to scripts:

    ```bash
    chmod +x start_services.sh
    chmod +x db/init_db.sh
    ```

3. Get all the users and its locations: (It my take a while)

    ```bash
    docker-compose run --rm script_runner_get_users
    ```

4. Filter out all airports with no wikipedia link:

    ```bash
    docker-compose run --rm script_runner_filter_airports_with_wk
    ```

5. Find all closest airport to each user:

    ```bash
    docker-compose run --rm script_runner_find_user_closest_airport
    ```

6. Once everything is generated, start the api:

    ```bash
    ./start_services.sh
    ```

    Once you run this command, if you have a database it will be deleted a new file `init.sql` will be generated to populate the database with required data.

6. Now you can test the accuracy of the project by running:

    ```bash
    docker-compose run --rm script_runner_eval
    ```


## API Documentation

### Endpoints

| HTTP Method | Endpoint | Description | Request Parameters | Response | Status Codes |
|-------------|----------|-------------|--------------------|----------|--------------|
| GET         | `/nearest_airports/<user_id>` | Retrieve the nearest airport ID for a given user. | `user_id`: integer (path parameter), The unique ID of the user. | `{ 'airport_id': integer }` | `200: OK - Success`<br>`404: Not Found - User not found or has no closest airport` |
| GET         | `/nearest_airports_wikipedia/<user_id>` | Retrieve the Wikipedia link for the nearest airport to a given user. | `user_id`: integer (path parameter), The unique ID of the user. | `{ 'wikipedia_link': string }` | `200: OK - Success`<br>`404: Not Found - User not found or airport not found` |
