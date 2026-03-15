# Modular Test – Async Network‑Coverage Backend

A Flask 2+ application that receives a JSON payload of addresses and returns,
for each address, the nearest mobile‑network coverage (2G/3G/4G) for every French operator.

## Features

* **Async** endpoint (`POST /coverage`) – non‑blocking calls to
  `https://api-adresse.data.gouv.fr` via `httpx`.
* Reads the CSV file
  `2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93_ver2.csv`
  (Lambert‑93 coordinates → GPS conversion with **pyproj**).
* Returns JSON data.
* **Server‑side logging** (INFO + ERROR) to monitor request volume and error rates.

## Project layout

modular_test/
│   app.py
│   utils.py
│   coverage_service.py
│   requirements.txt
│   README.md
    2018-01-sites-mobiles-2g-3g-4g-france-metropolitaine-l93-ver2-1-.csv (missing)


## Prerequisites

* Python 3.9+
* The CSV file **must be placed in the project root** (same folder as `app.py`).

## Installation


## Clone / copy the repository
git clone https://github.com/rohclemosiv-wq/modular_test
cd modular_test

# Optional: virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# Install dependencies
 pip install -r requirements.txt
 requirements.txt contains:

    Flask[async]>=2.0
    httpx>=0.24
    pyproj>=3.6

# Running the server (development)

First of all, put the "2018-01-sites-mobiles-2g-3g-4g-france-metropolitaine-l93-ver2-1-.csv" file on the root of the source directory as indicated on the project layout. Then,

  python app.py

The console will show INFO logs such as

  INFO:root:Flask async coverage service starting
  INFO:root:Received /coverage request with 2 entries
  ERROR:root:Error processing id7: <exception message>
  These logs give you a quick view of error rates per request.

## Production tip

The development server (app.run) is not suitable for production.
Deploy the async Flask app with an ASGI/WSGI server that supports async, e.g.:


### Using hypercorn (install via `pip install hypercorn`)
    hypercorn app:app --bind 0.0.0.0:5000

Example request

    bash
    curl -X POST http://localhost:5000/coverage \
         -H "Content-Type: application/json" \
         -d '{
               "id1": "157 boulevard Mac Donald 75019 Paris",
               "id4": "5 avenue Anatole France 75007 Paris"
             }'
Expected response (pretty‑printed)

    {
      "id1": {
        "Orange": {"2G": true, "3G": true, "4G": false},
        "SFR": {"2G": true, "3G": true, "4G": true},
        "Bouygues": {"2G": true, "3G": true, "4G": false}
    },
      "id4": {
        "Orange": {"2G": true, "3G": true, "4G": false},
        "Bouygues": {"2G": true, "3G": false, "4G": false},
        "SFR": {"2G": true, "3G": true, "4G": false}
        }
    }

## Monitoring error rates
All malformed requests and per‑ID processing failures are logged at ERROR level:


    logging.error(f"Error processing {identifier}: {e}")

You can redirect the logs to a file by adjusting the basicConfig call in app.py, e.g.:

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        filename="coverage_service.log",
        filemode="a"
    )

# License

MIT – feel free to fork, adapt and improve.

GitHub repository (placeholder)

https://github.com/rohclemosiv-wq/modular_test


