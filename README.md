# Geo Bucket System – Location-Based Property Management API

A Django REST Framework API that intelligently groups nearby properties into geo-buckets using spatial clustering and fuzzy location matching.

---

## 🚀 Features

- **Intelligent Geo-Bucketing**  
  Automatically groups nearby properties into logical geographic areas.

- **Fuzzy Location Matching**  
  Handles typos, case variations, and common suffix variations.

- **Spatial Search**  
  Radius-based property search powered by PostGIS.

- **Efficient Queries**  
  Pre-computed buckets enable fast location-based lookups.

- **Comprehensive Stats**  
  Real-time analytics on bucket efficiency and distribution.

- **RESTful API**  
  Fully documented OpenAPI / Swagger interface.

---

## 📋 Prerequisites

- Docker & Docker Compose
- Git
- 4GB+ RAM recommended

---

## 🛠️ Quick Start



```bash
# Clone the repository
git clone <repository-url>
cd expertlisting

# Create environment file
cp .env.sample .env
# Edit .env if needed (update SECRET_KEY for production)


### 2. Start the Application
# Build and start all services
docker compose up --build -d
```

 Access the Application

API: http://localhost:8000

Swagger UI: http://localhost:8000/api/v1/doc/

ReDoc: http://localhost:8000/api/v1/redoc/

### API Endpoints
Property Management
POST /api/properties/ - Create property with auto-bucket assignment

GET /api/properties/ - List all properties

GET /api/properties/{id}/ - Retrieve specific property

GET /api/properties/search/?location=query - Search by location

GET /api/properties/nearby/?lat=X&lng=Y&radius=Z - Radius search

Geo-Bucket Management
GET /api/geo-buckets/ - List all buckets

GET /api/geo-buckets/{id}/ - Retrieve bucket details

GET /api/geo-buckets/stats/ - Get bucket statistics

GET /api/geo-buckets/{id}/properties/ - Get properties in bucket

GET /api/geo-buckets/{id}/similar/ - Find similar buckets

You can also run the command below to seed data for testing:
Save as seed.py in your project root
````
python manage.py shell < seed.py

# Or run in Docker
docker compose exec web python manage.py shell < seed.py