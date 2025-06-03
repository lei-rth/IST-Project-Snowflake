# IST-Project-Snowflake
Pipeline Snowflake for IST class

# Get Started

1. Clone the repository
```bash
git clone git@github.com:lei-rth/IST-Project-Snowflake.git
cd IST-Project-Snowflake
```

2. Clone the OpenSky API repository
```bash
git clone git@github.com:openskynetwork/opensky-api.git
```

3. Setup environment variables
```bash
make dotenv
```

4. Create a virtual environment
```bash
make venv
source venv/bin/activate
```

5. Install dependencies
```bash
make install
```

6. Try to download data
```bash
make download
```

7. Verify data in `data/` folder