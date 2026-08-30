"""
EzyParts Vehicle Lookup Utility
Replicates EzyParts (ezyparts.burson.com.au) vehicle search -> vehicle details flow.

Flow:
  1. Search (either):
       - VIN:  GET {baseUrl}/vehicle/t/search?text={vin}
       - Rego: GET {baseUrl}/vehicle/rego/search?state={state}&rego={rego}
     Both return:
       { "vehicles": [ {id, make, model, year, seriesChassis, engine, lngDsc, ...}, ... ] }
  2. Full detail:  GET {baseUrl}/vehicle/{vehicleId}/details
                   -> rich JSON incl. make, model, subModel, configuration, vin,
                      complianceDate, chassis, series, engine, driveType, fuel, etc.

Authentication:
Uses trade-account-gated portal. Credentials via environment variables:
  EZYPARTS_ACCOUNT, EZYPARTS_USERNAME, EZYPARTS_PASSWORD
Session cache stored at ~/.ezyparts_session.json
"""

import json
import os
import re
from pathlib import Path
from typing import Optional, Dict, List, Any

import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_URL = "https://ezyparts.burson.com.au"
CONTEXT_PATH = "/burson/ezyparts/en/AUD"

LOGIN_PATH = "/j_spring_security_check"
VIN_SEARCH_PATH = "/vehicle/t/search"
REGO_SEARCH_PATH = "/vehicle/rego/search"
REGO_SEARCH_MORE_PATH = "/vehicle/rego/search/more"
VEHICLE_DETAILS_PATH = "/vehicle/{vehicle_id}/details"

VALID_STATES = {"ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"}

DEFAULT_SESSION_FILE = os.environ.get(
    "EZYPARTS_SESSION_FILE", str(Path.home() / ".ezyparts_session.json")
)


class EzyPartsError(Exception):
    """Custom exception for EzyParts errors"""
    pass


class EzyPartsClient:
    """Client for EzyParts vehicle lookup API"""
    
    def __init__(
        self,
        cookie_header: Optional[str] = None,
        session_file: Optional[str] = DEFAULT_SESSION_FILE,
        timeout: float = 10.0,
    ):
        self.session = requests.Session()
        self.timeout = timeout
        self.base = BASE_URL + CONTEXT_PATH
        self.session_file = session_file
        self.session.headers.update({
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
            "Referer": self.base + "/workbench",
            "Host": "ezyparts.burson.com.au",
        })
        
        if cookie_header:
            self.session.headers["Cookie"] = cookie_header
        elif session_file:
            self._load_cached_cookies()

    # ----- Session Management -----
    
    def _load_cached_cookies(self) -> bool:
        """Load cached session cookies from file"""
        path = Path(self.session_file)
        if not path.exists():
            return False
        try:
            data = json.loads(path.read_text())
        except (ValueError, OSError):
            return False
        for name, value in data.get("cookies", {}).items():
            self.session.cookies.set(name, value)
        return True

    def _save_cached_cookies(self) -> None:
        """Save session cookies to file for reuse"""
        if not self.session_file:
            return
        path = Path(self.session_file)
        try:
            path.write_text(json.dumps({"cookies": self.session.cookies.get_dict()}))
            path.chmod(0o600)
        except OSError:
            pass

    def is_authenticated(self) -> bool:
        """Check if current session is still valid"""
        if not self.session.cookies:
            return False
        try:
            resp = self.session.get(
                self.base + "/workbench", timeout=self.timeout, allow_redirects=True
            )
        except requests.RequestException:
            return False
        return resp.status_code == 200 and "/login" not in resp.url

    def ensure_authenticated(self, account_no: str, username: str, password: str) -> None:
        """Use cached session if valid, otherwise login fresh"""
        if self.is_authenticated():
            return
        self.login(account_no, username, password)
        self._save_cached_cookies()

    def login(self, account_no: str, username: str, password: str) -> None:
        """Perform login to EzyParts portal"""
        login_page_url = self.base + "/login"
        page_resp = self.session.get(login_page_url, timeout=self.timeout)
        page_resp.raise_for_status()

        csrf_match = re.search(
            r'name=["\']CSRFToken["\']\s+value=["\']([^"\']+)["\']', page_resp.text
        )
        form_data = {
            "acc_no": account_no,
            "username": username,
            "j_username": f"{account_no}_{username}",
            "j_password": password,
            "doc360_login": "false",
        }
        if csrf_match:
            form_data["CSRFToken"] = csrf_match.group(1)

        resp = self.session.post(
            self.base + LOGIN_PATH,
            data=form_data,
            allow_redirects=True,
            timeout=self.timeout,
        )
        resp.raise_for_status()

        if resp.url.rstrip("/").endswith("/login"):
            raise EzyPartsError("Login failed — check account number, username, and password.")

    # ----- API Methods -----
    
    def _get_json(self, url: str, params: Optional[dict] = None) -> dict:
        """Make GET request and parse JSON response"""
        resp = self.session.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            raise EzyPartsError(
                "Non-JSON response — likely not authenticated (redirected to login). "
                f"Response started with: {resp.text[:200]!r}"
            )

    def vin_search(self, vin: str) -> Dict[str, Any]:
        """Search vehicle by VIN"""
        return self._get_json(self.base + VIN_SEARCH_PATH, params={"text": vin})

    def rego_search(self, rego: str, state: str) -> Dict[str, Any]:
        """Search vehicle by registration number"""
        state = state.upper()
        if state not in VALID_STATES:
            raise EzyPartsError(f"Invalid state '{state}'. Must be one of {sorted(VALID_STATES)}.")
        return self._get_json(
            self.base + REGO_SEARCH_PATH, params={"state": state, "rego": rego}
        )

    def rego_search_more(self, rego: str, state: str, ac: int = 3) -> dict:
        """
        Calls the endpoint behind the page's "Registration Details" section
        (ACC.vehiclesearch.vehicleMoreDetailsData / populateModalInfo). Unlike
        vin_search/rego_search, this returns a flat object (rego, make, model,
        year, complianceDate, vin, engineNo, chassisNo, bodyStyle,
        registrationStatusCurrent, registrationStatusExpiry) rather than a
        vehicles[] list — this is the actual, authoritative source for that
        section (more reliable than piecing it together from search results).

        `ac` mirrors the site's own hardcoded query param for this call.
        """
        state = state.upper()
        if state not in VALID_STATES:
            raise EzyPartsError(f"Invalid state '{state}'. Must be one of {sorted(VALID_STATES)}.")
        return self._get_json(
            self.base + REGO_SEARCH_MORE_PATH,
            params={"state": state, "rego": rego, "ac": ac},
        )

    def get_vehicle_details(self, vehicle_id: str) -> Dict[str, Any]:
        """Get full vehicle details by vehicle ID"""
        path = VEHICLE_DETAILS_PATH.format(vehicle_id=vehicle_id)
        return self._get_json(self.base + path)

    def lookup_vin(self, vin: str) -> List[Dict[str, Any]]:
        """Lookup vehicle by VIN and return list of vehicle summaries"""
        data = self.vin_search(vin)
        return data.get("vehicles", [])

    def lookup_rego(self, rego: str, state: str) -> List[Dict[str, Any]]:
        """Lookup vehicle by rego and return list of vehicle summaries"""

        rego_data = self.rego_search(rego, state)
        more_data = self.rego_search_more(rego, state)

        data = dict()
        data["vehicle"] = rego_data
        data["registration"] = more_data
        return data


# ----- Helper Functions -----

def get_client(
    account: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    cookie_header: Optional[str] = None,
    session_file: Optional[str] = DEFAULT_SESSION_FILE,
    force_login: bool = False,
) -> EzyPartsClient:
    """Factory function to create and authenticate an EzyPartsClient"""
    
    account = account or os.environ.get("EZYPARTS_ACCOUNT")
    username = username or os.environ.get("EZYPARTS_USERNAME")
    password = password or os.environ.get("EZYPARTS_PASSWORD")
    
    client = EzyPartsClient(cookie_header=cookie_header, session_file=session_file)
    
    if not cookie_header:
        if not (account and username and password):
            raise EzyPartsError(
                "No credentials provided. Set EZYPARTS_ACCOUNT, EZYPARTS_USERNAME, "
                "EZYPARTS_PASSWORD environment variables, or pass cookie_header."
            )
        
        if force_login:
            client.login(account, username, password)
            client._save_cached_cookies()
        else:
            client.ensure_authenticated(account, username, password)
    
    return client


def lookup_vehicle_by_rego(
    rego: str,
    state: str,
    account: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> Dict[str, Any]:
    """Convenience function for rego lookup"""
    client = get_client(account, username, password)
    vehicles = client.lookup_rego(rego, state)
    
    if not vehicles:
        return {"error": "No vehicles found", "vehicles": []}
    
    return {"vehicles": vehicles, "count": len(vehicles)}


def lookup_vehicle_by_vin(
    vin: str,
    account: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> Dict[str, Any]:
    """Convenience function for VIN lookup"""
    client = get_client(account, username, password)
    vehicles = client.lookup_vin(vin)
    
    if not vehicles:
        return {"error": "No vehicles found", "vehicles": []}
    
    return {"vehicles": vehicles, "count": len(vehicles)}


def get_full_vehicle_details(
    vehicle_id: str,
    account: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> Dict[str, Any]:
    """Convenience function for full vehicle details"""
    client = get_client(account, username, password)
    return client.get_vehicle_details(vehicle_id)