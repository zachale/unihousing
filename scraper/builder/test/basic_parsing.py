"""Quick smoke tests for the `handler` function using local HTML fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scraper.builder.main import handler  # noqa: E402


FIXTURES_DIR = Path(__file__).resolve().parent / "html"


EXPECTED_LISTINGS: dict[str, dict[str, Any]] = {
    "101772": {
        "headline": "117 Janefield Ave, Guelph",
        "address": "117 Janefield Avenue, Guelph, ON, Canada",
        "price": "$634.13",
        "description": (
            "We’re 6 girls looking for 1 subletter to join our cozy home from January to August (8 months)! "
            "The room is fully furnished, and the house is super clean and well taken care of. ✨ Details: 1 furnished "
            "bedrooms available 12 min bus (bus stop close by!) 30 min walk to U of G campus . Parking spot available "
            "Shared kitchen, living room & laundry Friendly, tidy housemates Perfect for students looking for a comfortable "
            "and convenient spot. Message for pics or to come check it out! 💛"
        ),
        "category": "House",
        "date_available": "1/Jan/2026",
        "date_posted": "8/Nov/2025",
        "shared": "Yes",
        "sublet": "Yes",
        "beds": "1",
        "parking": True,
        "no_smoking": True,
        "laundry_facilities": True,
        "cooking_facilities": True,
        "photos": [
            "https://thecannon.ca/wp-content/uploads/2025/11/user_19574_6933eb11-3e18-46c0-8f86-bd22a60481d4_20251106214035.jpeg",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_19574_7600a3dd-be6c-4f38-89cb-e4c1402a0596_20251106214253.jpeg",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_19574_bcfec83f-75c7-4495-b14b-ad8e382f2eeb_20251106214313.jpeg",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_19574_722866c4-395e-4e94-99c8-03003bdf5ecc_20251106214330.jpeg",
        ],
        "listing_id": "101772",
    },
    "101922": {
        "headline": "11 Smart St, Guelph",
        "address": "11 Smart Street, Guelph, ON, Canada",
        "price": "$1100",
        "description": (
            "Looking for a sublet January-August 2026. Single bedroom in a 2 people girls basement apartment. "
            "Will be fully furnished. 5 min drive from the University of Guelph Campus. 2 min walk from the bus stop. "
            "3 min drive from Stone Road mall."
        ),
        "category": "Apartment or Condo",
        "date_available": "1/Jan/2025",
        "date_posted": "7/Nov/2025",
        "shared": "Yes",
        "sublet": "Yes",
        "beds": "1",
        "parking": True,
        "no_smoking": True,
        "laundry_facilities": True,
        "cooking_facilities": True,
        "photos": [
            "https://thecannon.ca/wp-content/uploads/2025/11/user_19585_img_6359_20251108030647.jpg",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_19585_img_6361_20251108030656.jpg",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_19585_img_6362_20251108030704.jpg",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_19585_img_6364_20251108030713.jpg",
        ],
        "listing_id": "101922",
    },
    "101927": {
        "headline": "1219 Gordon St, Guelph",
        "address": "1219 Gordon Street, Guelph, ON, Canada",
        "price": "$900",
        "description": (
            "Lease takeover/sublet available in a shared all male 4 bedroom apartment in desirable building. "
            "This beautiful room comes with its own *private bathroom, *walk-in closet, *shared kitchen, living room and "
            "*in-unit laundry facilities. Utilities and wifi included. The building has private study rooms, free gym "
            "and lounges. Only a 6 minute bus ride to campus (Routes 99N, 99S, 1, 2, 5, 56U) All other tenants are UofG "
            "students – all friendly and laid back. Please message Rose at 365-228-1327 for showings or questions"
        ),
        "category": "Apartment or Condo",
        "date_available": "1/Jan/2026",
        "date_posted": "7/Nov/2025",
        "shared": "Yes",
        "sublet": "Yes",
        "beds": "1",
        "parking": False,
        "no_smoking": False,
        "laundry_facilities": True,
        "cooking_facilities": True,
        "photos": [
            "https://thecannon.ca/wp-content/uploads/2025/11/user_18059_solstice-bedroom_20251107235218.jpg",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_18059_solstice-bathroom-2_20251107235227.jpg",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_18059_solstice-kitchen_20251107235247.jpg",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_18059_solstice-layout_20251108040756.png",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_18059_solstice-exterior-2_20251108040812.jpg",
        ],
        "listing_id": "101927",
    },
    "101947": {
        "headline": "303 Victoria Rd N, Guelph",
        "address": "303 Victoria Rd. North, Guelph",
        "price": "$2,500 + util. ($835 /rm.)",
        "description": (
            "Spacious bungalow with 3 bedrooms & 2 bathrooms for 3 students to lease. Utilities: you pay for gas and "
            "hydro, I cover water expenses. Up to 3 tenants’ parking is included. There is separate laundry and storage "
            "rooms. The bus stop is at the corner of the house. Close to everything. Please text or call 519 781-7485."
        ),
        "category": "House",
        "date_available": "1/May/2026",
        "date_posted": "8/Nov/2025",
        "shared": "No",
        "sublet": "No",
        "beds": "3",
        "parking": True,
        "no_smoking": True,
        "laundry_facilities": True,
        "cooking_facilities": True,
        "photos": [
            "https://thecannon.ca/wp-content/uploads/2025/11/user_1899_living-room-apr-2024_20251108144523.png",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_1899_bedroom1-apr-2024_20251108144547.png",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_1899_bedroom-2-apr-2024_20251108144602.png",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_1899_vanity-mast-bathroom-apr-2024_20251108144622.png",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_1899_303-kitchen-apr-2024_20251108144636.png",
        ],
        "listing_id": "101947",
    },
    "101953": {
        "headline": "301 Victoria Rd N, Guelph",
        "address": "301a Victoria Road North, Guelph, ON, Canada",
        "price": "$2,400 incl. ($800 rm.)",
        "description": (
            "Furnished basement unit with separate entrance and the Storage room. Great space for 3 Students. Very "
            "clean 3 Bedrooms / 1 bathroom. Bus stop located at the corner of the property. Within 30 min walk to downtown, "
            "Guelph General Hospital, Market Fresh grocery, restaurants, entertainment, Timmy’s, and more. Kitchen with "
            "new appliances, cupboards, backsplash, and dishes, cups, etc. Private, in-suite Laundry. There are blinds or "
            "drapes on all windows. Utilities are included. Up to 3 tenants’ parking spaces are included. Please text or "
            "call 519 781-7485"
        ),
        "category": "Apartment or Condo",
        "date_available": "1/May/2026",
        "date_posted": "8/Nov/2025",
        "shared": "No",
        "sublet": "No",
        "beds": "3",
        "parking": True,
        "no_smoking": True,
        "laundry_facilities": True,
        "cooking_facilities": True,
        "photos": [
            "https://thecannon.ca/wp-content/uploads/2025/11/user_1899_301-a-living-room-apr-2023-png_20251108145440.png",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_1899_301-a-master-bedroom-apr-2023-png_20251108145453.png",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_1899_301-a-bedroom-2-apr-2023-png_20251108145519.png",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_1899_301-a-bathroom-apr-2023-png_20251108145539.png",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_1899_301-a-kitchen-apr-2023-png_20251108145611.png",
        ],
        "listing_id": "101953",
    },
    "101975": {
        "headline": "1280 Gordon St, Guelph",
        "address": "1280 Gordon Street, Guelph, ON, Canada",
        "price": "$1200 pp/inc",
        "description": (
            "The perfect location for UoG students, only a 5 minute bus ride to and from campus. Located within minutes "
            "to Pergola commons, restaurants, groceries and entertainment, this location is unbeatable. Gordon/Edinburgh. "
            "Bus stop directly outside. 3 Bedroom, top floor (4th) unit available at Liberty Square Condo as of May 01 2026. "
            "Unit windows and balcony overlook the conservation area directly across (no parking lot views or noise). No "
            "construction around. 10 foot ceilings, creating a spacious feeling and no upstairs neighbours. Very safe condo "
            "with security. Open kitchen with stainless steel appliances and centre island. Full vinyl plank flooring "
            "throughout unit, no carpet. Air conditioning. On demand water heater (no running out of hot water) Each bedroom "
            "has a large closet. All rooms professionally painted 2025. Brand new laundry unit installed 2025. Stainless "
            "steel appliances. Huge extra storage locker on same floor. One inside garage parking spot available."
        ),
        "category": "Apartment or Condo",
        "date_available": "1/May/2026",
        "date_posted": "8/Nov/2025",
        "shared": "No",
        "sublet": "No",
        "beds": "3",
        "parking": True,
        "no_smoking": True,
        "laundry_facilities": True,
        "cooking_facilities": True,
        "photos": [
            "https://thecannon.ca/wp-content/uploads/2025/11/user_19487_img_5005-1_20251108185823-rotated.jpeg",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_19487_img_5002-1_20251108185830-rotated.jpeg",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_19487_img_5006_20251108185840.jpeg",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_19487_img_5007_20251108185846.jpeg",
            "https://thecannon.ca/wp-content/uploads/2025/11/user_19487_img_5008_20251108185853-rotated.jpeg",
        ],
        "listing_id": "101975",
    },
}


def load_fixture(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_fixture(path: Path) -> None:
    html = load_fixture(path)
    listing_id = path.stem
    expected = EXPECTED_LISTINGS[listing_id]

    event = {"html_content": html, "listing_id": listing_id}
    response = handler(event, context=None)

    assert response["statusCode"] == 200, f"Handler failed for {path}: {response}"

    body = json.loads(response["body"])
    assert isinstance(body, dict), f"Expected dict body for single listing, got {type(body)}"
    assert body == expected, f"Parsed output mismatch for {listing_id}\nexpected: {expected}\nactual: {body}"


def main() -> int:
    html_files = sorted(FIXTURES_DIR.glob("*.txt"))
    if not html_files:
        print(f"No fixtures found in {FIXTURES_DIR}", file=sys.stderr)
        return 1

    for fixture in html_files:
        test_fixture(fixture)
        print(f"✓ Parsed {fixture.name}")

    print("All fixtures parsed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
