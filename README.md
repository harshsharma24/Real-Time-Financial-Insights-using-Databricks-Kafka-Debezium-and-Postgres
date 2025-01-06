# Financial Insights ETL Pipeline

## Overview
This project implements a robust ETL (Extract, Transform, Load) pipeline for financial data analytics. Using a layered architecture (Bronze, Silver, Gold), it captures real-time transactional data, processes it, and generates business-ready insights. The pipeline leverages tools such as Docker, Postgres, Kafka, Debezium, Databricks, and Delta Lake to handle large volumes of data while ensuring accuracy and scalability.

---

## Key Features
- **Real-Time Data Capture**:
  - Streams Change Data Capture (CDC) events from Postgres using Debezium.
- **Layered Architecture**:
  - **Bronze Layer**: Stores raw Kafka messages for audit and reprocessing.
  - **Silver Layer**: Cleans and deduplicates data for structured storage.
  - **Gold Layer**: Aggregates metrics for business intelligence.
- **Insights Delivered**:
  - Transaction summaries (totals, averages, debits, credits).
  - Customer balances over time.
  - Popular product analysis.
  - Scheduled payments summary.

---

## Architecture
The pipeline consists of:
1. **Postgres**:
   - Source database with tables for transactional and account data.
2. **Debezium**:
   - Captures changes (inserts, updates, deletes) from Postgres.
3. **Kafka**:
   - Streams CDC data to downstream consumers.
4. **Databricks**:
   - Processes and transforms data using PySpark.
5. **Delta Lake**:
   - Provides ACID transactions and schema enforcement.

---

## Prerequisites
- **Docker** installed on your system.
- A **Databricks workspace** with Delta Lake support.
- **Kafka** and **Debezium** containers configured using Docker Compose.

---

## Setup and Execution

### 1. Deploy Docker Containers
- Use the provided `docker-compose.yml` to deploy Postgres, Kafka, and Debezium.
```bash
docker-compose up -d
```

### 2. Configure Postgres
- Create the required tables in Postgres:
```sql
CREATE TABLE purchase_trends (
    id SERIAL PRIMARY KEY,
    product VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE checking_account (
    account_id SERIAL PRIMARY KEY,
    account_holder_name VARCHAR(100) NOT NULL,
    account_balance NUMERIC(10, 2) NOT NULL,
    last_transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE public.purchase_trends REPLICA IDENTITY FULL;
ALTER TABLE public.checking_account REPLICA IDENTITY FULL;
```

### 3. Deploy Debezium Connector
- Configure and deploy the Debezium Postgres connector:
```bash
curl -i -X POST -H "Accept: application/json" -H "Content-Type: application/json" \
--data @debezium.json http://127.0.0.1:8083/connectors/
```

### 4. Process Data in Databricks
- Upload the PySpark scripts to Databricks notebooks and execute them in the following order:
  1. **Bronze Layer**: Ingest raw Kafka messages into Delta Lake.
  2. **Silver Layer**: Clean and deduplicate data for structured storage.
  3. **Gold Layer**: Generate business insights (e.g., transaction summaries, customer balances).

---

## Output Examples

### Transaction Summary (Gold Layer)
| customer_id | total_transactions | average_transaction | total_debits | total_credits |
|-------------|--------------------|---------------------|--------------|---------------|
| 101         | 300.0             | 150.0              | 100.0        | 200.0         |

### Customer Balance (Gold Layer)
| customer_id | updt_ts               | latest_balance |
|-------------|-----------------------|----------------|
| 101         | 2023-08-15T12:00:00Z | 1500.00        |

### Popular Products (Gold Layer)
| product     | total_quantity_sold |
|-------------|---------------------|
| Laptop      | 300                 |
| Smartphone  | 250                 |

---

## Key Insights Delivered
1. **Real-Time Transaction Monitoring**:
   - Understand customer transaction patterns (e.g., totals, averages).
2. **Customer Profiling**:
   - Track balances and scheduled payments for personalized services.
3. **Product Trends**:
   - Identify top-performing products for inventory management.

---

## Future Enhancements
1. **Real-Time Streaming**:
   - Use Spark Structured Streaming for live processing.
2. **Predictive Analytics**:
   - Add machine learning models for churn prediction and credit risk assessment.
3. **Visualization**:
   - Integrate with BI tools like Tableau or Power BI for interactive dashboards.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Author
**Your Name**
Feel free to connect at [harshsharma2413@gmail.com] for questions or collaborations.

