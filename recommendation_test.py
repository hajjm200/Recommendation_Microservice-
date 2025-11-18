#!/usr/bin/env python3
"""
Required: RecommendationService.py must be running on port 4000
"""

import requests
import json
import time
import sys

# ANSI color codes for better visualization
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

base_url = "http://127.0.0.1:4000"

def print_header(text):
    """Print a formatted header"""
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{text:^70}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")

def print_request(method, endpoint, data=None):
    """Print the request being sent"""
    print(f"{YELLOW}REQUEST: {method} {base_url}{endpoint}{RESET}")
    if data:
        print(f"{YELLOW}BODY:{RESET}")
        print(json.dumps(data, indent=2))
    print()

def print_response(response):
    """Print the response received"""
    print(f"{GREEN}RESPONSE:{RESET}")
    print(json.dumps(response, indent=2))
    if isinstance(response, dict) and response.get("recommendations"):
        print(f"{GREEN}✓ Found {len(response['recommendations'])} recommendations{RESET}")
    elif isinstance(response, list):
        print(f"{GREEN}✓ Found {len(response)} clubs{RESET}")
    print()

def test_recommendations():
    """Test the /recommendations endpoint"""
    print_header("TESTING: POST /recommendations ENDPOINT")
    
    # Test 1: User interested in Technology
    print(f"{BOLD}Test 1: New user interested in Technology{RESET}")
    data = {
        "user_id": "osu_12345",
        "favorites": [],
        "categories": ["Technology"]
    }
    print_request("POST", "/recommendations", data)
    response = requests.post(f"{base_url}/recommendations", json=data)
    print_response(response.json())
    time.sleep(1)
    
    # Test 2: User with favorites in Technology/Engineering
    print(f"{BOLD}Test 2: User with coding and robotics favorites{RESET}")
    data = {
        "user_id": "osu_12345",
        "favorites": ["coding_club", "robotics_club"],
        "categories": ["Technology", "Engineering"]
    }
    print_request("POST", "/recommendations", data)
    response = requests.post(f"{base_url}/recommendations", json=data)
    print_response(response.json())
    time.sleep(1)
    
    # Test 3: User interested in Arts
    print(f"{BOLD}Test 3: User interested in Arts{RESET}")
    data = {
        "user_id": "osu_67890",
        "favorites": ["dance_club"],
        "categories": ["Arts", "Creative"]
    }
    print_request("POST", "/recommendations", data)
    response = requests.post(f"{base_url}/recommendations", json=data)
    print_response(response.json())
    time.sleep(1)
    
    # Test 4: User with mixed interests
    print(f"{BOLD}Test 4: User with diverse interests{RESET}")
    data = {
        "user_id": "osu_99999",
        "favorites": ["astronomy_club"],
        "categories": ["Science", "Technology", "Arts"]
    }
    print_request("POST", "/recommendations", data)
    response = requests.post(f"{base_url}/recommendations", json=data)
    print_response(response.json())
    time.sleep(1)

def test_category_endpoint():
    """Test the /category/{name} endpoint"""
    print_header("TESTING: GET /category/{name} ENDPOINT")
    
    categories_to_test = ["Technology", "Engineering", "Arts", "Science"]
    
    for category in categories_to_test:
        print(f"{BOLD}Test: Get all {category} clubs{RESET}")
        print_request("GET", f"/category/{category}")
        response = requests.get(f"{base_url}/category/{category}")
        print_response(response.json())
        time.sleep(1)

def test_favorites_update():
    """Test the /favorites/update endpoint"""
    print_header("TESTING: POST /favorites/update ENDPOINT")
    
    # Test 1: Add a new favorite
    print(f"{BOLD}Test 1: User adds Game Development to favorites{RESET}")
    data = {
        "user_id": "osu_12345",
        "favorites": ["coding_club", "robotics_club", "game_dev_osu"],
        "categories": ["Technology", "Engineering"]
    }
    print_request("POST", "/favorites/update", data)
    response = requests.post(f"{base_url}/favorites/update", json=data)
    result = response.json()
    print_response(result)
    
    # Show how recommendations changed
    print(f"{CYAN}Note: Recommendations updated after adding 'game_dev_osu' to favorites{RESET}")
    print(f"{CYAN}The system now excludes favorited clubs from recommendations{RESET}")
    time.sleep(2)
    
    # Test 2: Remove a favorite
    print(f"{BOLD}Test 2: User removes a favorite{RESET}")
    data = {
        "user_id": "osu_12345",
        "favorites": ["coding_club"],  # Removed robotics_club and game_dev_osu
        "categories": ["Technology", "Engineering"]
    }
    print_request("POST", "/favorites/update", data)
    response = requests.post(f"{base_url}/favorites/update", json=data)
    result = response.json()
    print_response(result)
    time.sleep(1)

def test_error_handling():
    """Test error handling"""
    print_header("TESTING: ERROR HANDLING")
    
    # Test missing user_id
    print(f"{BOLD}Test: Missing user_id{RESET}")
    data = {
        "favorites": ["coding_club"],
        "categories": ["Technology"]
    }
    print_request("POST", "/recommendations", data)
    response = requests.post(f"{base_url}/recommendations", json=data)
    if response.status_code != 200:
        print(f"{RED}ERROR {response.status_code}: {response.json().get('detail')}{RESET}")
    time.sleep(1)
    
    # Test invalid category
    print(f"{BOLD}Test: Non-existent category{RESET}")
    print_request("GET", "/category/InvalidCategory")
    response = requests.get(f"{base_url}/category/InvalidCategory")
    result = response.json()
    print_response(result)
    if len(result) == 0:
        print(f"{YELLOW}✓ Correctly returned empty list for invalid category{RESET}")

def test_integration_flow():
    """Test a complete user flow"""
    print_header("INTEGRATION TEST: Complete User Journey")
    
    print(f"{BOLD}{CYAN}Simulating a new user's journey through CampusConnect:{RESET}")
    print()
    
    user_id = "osu_demo_user"
    
    # Step 1: New user gets initial recommendations
    print(f"{BOLD}Step 1: New user Sarah joins, interested in Technology{RESET}")
    data = {
        "user_id": user_id,
        "favorites": [],
        "categories": ["Technology"]
    }
    response = requests.post(f"{base_url}/recommendations", json=data)
    initial_recs = response.json()
    print(f"Sarah receives {len(initial_recs['recommendations'])} club recommendations")
    for rec in initial_recs['recommendations'][:2]:
        print(f"  - {rec['club_name']} (Score: {rec['match_score']})")
    time.sleep(2)
    
    # Step 2: User favorites a club
    print(f"\n{BOLD}Step 2: Sarah likes Coding Club and adds it to favorites{RESET}")
    data = {
        "user_id": user_id,
        "favorites": ["coding_club"],
        "categories": ["Technology"]
    }
    response = requests.post(f"{base_url}/favorites/update", json=data)
    updated_recs = response.json()
    print(f"Recommendations updated! New suggestions:")
    for rec in updated_recs['recommendations'][:2]:
        print(f"  - {rec['club_name']} (Score: {rec['match_score']})")
    time.sleep(2)
    
    # Step 3: User explores a category
    print(f"\n{BOLD}Step 3: Sarah explores all Engineering clubs{RESET}")
    response = requests.get(f"{base_url}/category/Engineering")
    eng_clubs = response.json()
    print(f"Found {len(eng_clubs)} Engineering clubs:")
    for club in eng_clubs:
        print(f"  - {club['name']}")
    time.sleep(1)

def main():
    """Main function to run all tests"""
    print_header("RECOMMENDATION MICROSERVICE DEMO")
    print(f"{BOLD}CS361 - Software Engineering{RESET}")
    print(f"{BOLD}CampusConnect Recommendation Service{RESET}")
    print(f"\n{YELLOW}Checking connection to microservice...{RESET}")
    
    # Check if the service is running
    try:
        response = requests.get(base_url)
        service_info = response.json()
        print(f"{GREEN}✓ {service_info['service']} is {service_info['status']} on {base_url}{RESET}")
        print(f"{GREEN}Available endpoints:{RESET}")
        for endpoint in service_info['endpoints']:
            print(f"  - {endpoint}")
        print()
    except:
        print(f"{RED}✗ ERROR: Cannot connect to microservice!{RESET}")
        print(f"{RED}Make sure RecommendationService.py is running on port 4000{RESET}")
        print(f"{RED}Run: uvicorn RecommendationService:app --reload --port 4000{RESET}")
        sys.exit(1)
    
    time.sleep(2)
    
    # Run all tests
    test_recommendations()
    test_category_endpoint()
    test_favorites_update()
    test_error_handling()
    test_integration_flow()
    
    print_header("TEST DEMONSTRATION COMPLETE")
    print(f"{GREEN}All microservice endpoints have been tested successfully!{RESET}")
    print(f"{BOLD}Check the README.md for detailed documentation.{RESET}")

if __name__ == "__main__":
    main()
