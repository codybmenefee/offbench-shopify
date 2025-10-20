"""Direct test of Convex API."""
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("CONVEX_DEPLOYMENT_URL")
print(f"Testing Convex at: {url}")

# Test mutation
mutation_data = {
    "path": "mutations/projects:upsertProject",
    "args": {
        "scenarioId": "test-direct-123",
        "name": "Direct Test Project",
        "confidence": 75.5,
        "gapsCount": 0,
        "conflictsCount": 0,
        "ambiguitiesCount": 0,
        "documentsCount": 0,
        "status": "active"
    }
}

try:
    client = httpx.Client(timeout=30.0)
    response = client.post(
        f"{url}/api/mutation",
        json=mutation_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.text}")
    print(f"JSON: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

