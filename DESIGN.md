# Location Normalization Using Geo-Buckets

## 1. Geo-Bucket Strategy
We group properties into logical geo-buckets based on:
- Geographic proximity (radius-based)
- Normalized location name similarity

Each bucket represents a neighborhood-level area (~1km radius).

### Why Radius Buckets?
- Human neighborhoods do not align with strict grids
- Radius-based matching handles GPS noise well
- Efficient using PostGIS `ST_DWithin`

---

## 2. Database Schema

### GeoBucket
- id
- name
- normalized_name (indexed)
- center (PostGIS Point)
- radius_meters

### Property
- id
- title
- location_name
- location (PostGIS Point)
- geo_bucket_id (FK)

Indexes:
- GIST index on location fields
- B-tree index on normalized_name

---

## 3. Location Matching Logic

### String Normalization
- Lowercase
- Remove punctuation
- Remove stop-words (e.g. "lagos", "ajah")

### Matching Steps
1. Normalize search term
2. Find nearby geo-buckets by distance
3. Apply string similarity threshold
4. Return all properties in matched buckets

---

## 4. Search Flow Diagram

User Search
    |
    v
Normalize Location Text
    |
    v
Find Nearby GeoBuckets (PostGIS)
    |
    v
String Similarity Match
    |
    v
Fetch Properties
