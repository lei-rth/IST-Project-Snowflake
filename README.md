# IST Project - Data Pipeline 

***Students :***
 - Bouzourène Ryad
 - Barros Fernandes Gabriel
 - Nguyen Thomas
 - Rothenbühler Lei

## What is Snowflake ? 

Snowflake is a fully managed SaaS (software as a service) that provides a single platform for data warehousing, data lakes, data engineering, data science, data application development, and secure sharing and consumption of real-time / shared data. Snowflake features out-of-the-box features like separation of storage and compute, on-the-fly scalable compute, data sharing, data cloning, and third-party tools support in order to handle the demanding needs of growing enterprises. [snowflake.com]

## Why it's interesting ? 

Snowflake has several advantages :

**1. Scalability and performance**

Snowflake allows independent scaling of compute and storage, optimizing costs and performance. Resources adjust dynamically based on workload demand, ensuring efficient query execution without manual intervention. Additionally, Snowflake leverages Massively Parallel Processing (MPP), enabling fast execution of complex queries across large datasets.

**2. Multi-Cloud Flexibility**

Snowflake is multi-cloud compatible, running with no interruptions on AWS, Azure, and Google Cloud. It supports cross-cloud data sharing, allowing businesses to exchange and access data across different cloud providers without migration overhead.

**3. Ease of use and Management**

Snowflake provides a fully managed infrastructure, eliminating the need for manual tuning, maintenance or complex configurations. Engineers can interact with Snowflake using standard SQL, making it easy to adopt. The platform also automates performance optimization, ensuring efficient query execution and storage management without requiring dedicated database administrators.

**4. Cost Efficency**

Snowflake adopted the pay-as-you-go plan, which is mean that you only pay for the compute and storage ressources used, avoiding unecessary costs. Additionally, data compression and deduplication minimize storage expenses, further improving cost efficiency compared to traditional data warehouses.

## How to get started

⚠️ This Makefile doesn't work on Windows ⚠️

1. Clone the repository
```bash
git clone git@github.com:lei-rth/IST-Project-Snowflake.git
cd IST-Project-Snowflake
```

2. Clone the OpenSky API repository for getting the planes data 
```bash
git clone git@github.com:openskynetwork/opensky-api.git
```

3. Setup environment variables
```bash
make dotenv
```

4. Create a python virtual environment
```bash
make venv
source venv/bin/activate
```

5. Install dependencies
```bash
make install
```

6. Try to download data. 
```bash
make download
```

7. Verify data in `data/` folder. The data are contained into a .csv file called "flight_data.csv"

## How to use it with the most important commands/operations