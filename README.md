# Recommendation Microservice – CampusConnect  
Created by **Mia Hajj**  
CS361 – Small Pool Implementation (Milestone #2)

This microservice provides **personalized club recommendations** for the CampusConnect project.  
It receives a user’s favorites and preferred categories, computes match scores, and returns tailored suggestions.  
It also supports category lookups and favorite updates.

---

# 1. How to REQUEST Data From This Microservice

###  Endpoint  
`POST http://127.0.0.1:4000/recommendations`

###  Required JSON Body
```json
{
  "user_id": "osu_12345",
  "favorites": ["coding_club"],
  "categories": ["Technology", "Engineering"]
}
```

###  What This Does  
- Sends the user’s ID  
- Sends their favorite clubs  
- Sends their interest categories  
- Microservice returns a **ranked list** of recommended clubs  

---

# 2. How to RECEIVE Data From This Microservice

###  Example Response JSON
```json
{
  "user_id": "osu_12345",
  "recommendations": [
    {
      "club_name": "Game Development Club",
      "category": "Technology",
      "match_score": 1.0,
      "description": "Create video games and learn about game programming and design.",
      "id": "game_dev_osu"
    },
    {
      "club_name": "Robotics Club",
      "category": "Engineering",
      "match_score": 0.8,
      "description": "Build robots for competitions and education.",
      "id": "robotics_club"
    }
  ]
}
```

---

# 3. Additional Supported Endpoints

###  A. GET /category/{category_name}  
Returns all clubs belonging to a category.

Example:  
`GET http://127.0.0.1:4000/category/Technology`

**Response format:**
```json
[
  {
    "id": "coding_club",
    "name": "Coding Club",
    "category": "Technology",
    "description": "Learn programming, web development, and software design."
  }
]
```

---

###  B. POST /favorites/update  
Updates user favorites and returns updated recommendations.

**Example Request:**
```json
{
  "user_id": "osu_12345",
  "favorites": ["coding_club", "game_dev_osu"],
  "categories": ["Technology"]
}
```

---

# 4. Example Test Program (Required for Assignment)

The included file `recommendation_test.py` demonstrates ALL endpoints.

It tests:
- Recommendations  
- Favorites update  
- Category lookup  
- Error handling  
- Full integration journey  

### Run it with:
```bash
python3 recommendation_test.py
```

Your output should show all tests passing successfully.

---

# 5. UML Sequence Diagram (Required for Assignment)

<img width="688" height="261" alt="Screenshot 2025-11-17 at 8 48 23 PM" src="https://github.com/user-attachments/assets/63150e3d-dcca-48b6-858a-e58d3873a693" />


This diagram shows the communication flow between the **Test Program** and the **Microservice**.

---

# 6. How to Run This Microservice

###  Step 1 — Install required dependencies:
```bash
pip install fastapi uvicorn
```

###  Step 2 — Start the microservice:
```bash
uvicorn RecommendationService:app --reload --port 4000
```

You should see:
```
Uvicorn running on http://127.0.0.1:4000
Application startup complete.
```

###  Step 3 — Run the test program in a new terminal tab:
```bash
python3 recommendation_test.py
```

---

# 7. Microservice Communication Contract (Do Not Change)

### Endpoints:
- `POST /recommendations`
- `GET /category/{category_name}`
- `POST /favorites/update`

### Request Format:
```json
{
  "user_id": "string",
  "favorites": ["club_id_1", "club_id_2"],
  "categories": ["Technology", "Science"]
}
```

### Response Format:
```json
{
  "user_id": "string",
  "recommendations": [...]
}
```

---

# 8. Notes for Teammates  
- Built with **FastAPI**  
- Returns recommendations ranked by match score  
- Always returns clean JSON  
- Clubs already in favorites are excluded from suggestions  
- CORS enabled  
- No authentication required  
- Response time under 200ms (small dataset)

---

This README includes all required components for Assignment 8 and fully matches the implemented microservice.

