"""
Replicates EzyParts (ezyparts.burson.com.au) vehicle search -> vehicle details flow,
based on acc.vinsearch.js / acc.regosearch.js / acc.vehiclesearch.js.

Flow:
  1. Search (either):
       - VIN:  GET {baseUrl}/vehicle/t/search?text={vin}
       - Rego: GET {baseUrl}/vehicle/rego/search?state={state}&rego={rego}
     Both return the same shape:
       { "vehicles": [ {id, make, model, year, seriesChassis, engine, lngDsc, ...}, ... ] }
  2. Full detail:  GET {baseUrl}/vehicle/{vehicleId}/details
                   -> rich JSON incl. make, model, subModel, configuration, vin,
                      complianceDate, chassis, series, engine, driveType, fuel, etc.
                      (this is what backs the "Compliance Date / Vin / Make / Model /
                      Sub Model / Configuration" fields you're after)

IMPORTANT — Authentication:
EzyParts is a trade-account-gated portal. Use `EzyPartsClient.login(account, username,
password)` to authenticate (replicates the site's own login form, which joins your
account number + username into one field). Credentials can be supplied via:
  - CLI flags: --account --username --password
  - Environment variables: EZYPARTS_ACCOUNT / EZYPARTS_USERNAME / EZYPARTS_PASSWORD (preferred)
  - A raw --cookie header from an already-logged-in browser session, as a fallback

Prefer env vars (or a .env file loaded with python-dotenv) over hardcoding credentials
directly in this file, especially if it's ever going into version control.

Usage:
    export EZYPARTS_ACCOUNT=12345
    export EZYPARTS_USERNAME=myuser
    export EZYPARTS_PASSWORD=mypassword
    python ezyparts_vin_lookup.py --vin KNAPU81GMT7355506
    python ezyparts_vin_lookup.py --rego 1ABC234 --state VIC
"""

import argparse
import os
import re
import sys
import json
from dataclasses import dataclass, field
from typing import List, Optional

import requests

try:
    from dotenv import load_dotenv  # pip install python-dotenv
    load_dotenv()  # reads a .env file in the current working directory, if present
except ImportError:
    pass  # dotenv is optional — env vars set another way (shell, CI, etc.) still work

BASE_URL = "https://ezyparts.burson.com.au"
# Hybris multi-site context path, confirmed from ACC.config.encodedContextPath in the
# site's own JS (Untitled.html): '/burson/ezyparts/en/AUD'. This was the cause of the
# earlier 404s — every endpoint (login, search, details) needs this prefix.
CONTEXT_PATH = "/burson/ezyparts/en/AUD"

LOGIN_PATH = "/j_spring_security_check"  # confirmed via captured HAR of a real login
VIN_SEARCH_PATH = "/vehicle/t/search"
REGO_SEARCH_PATH = "/vehicle/rego/search"
VEHICLE_DETAILS_PATH = "/vehicle/{vehicle_id}/details"

VALID_STATES = {"ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"}

# --------------------------------------------------------------------------------
# Credentials: prefer environment variables over hardcoding. If you really want to
# hardcode for local/throwaway use, set the constants below directly — but never
# commit real credentials to source control (add this file to .gitignore, or keep
# secrets in a .env file loaded via python-dotenv instead).
# --------------------------------------------------------------------------------
EZYPARTS_ACCOUNT = os.environ.get("EZYPARTS_ACCOUNT", "")
EZYPARTS_USERNAME = os.environ.get("EZYPARTS_USERNAME", "")
EZYPARTS_PASSWORD = os.environ.get("EZYPARTS_PASSWORD", "")


class EzyPartsError(Exception):
    pass


@dataclass
class VehicleSummary:
    """One row from the VIN/rego search results list."""
    id: str
    make: str = ""
    model: str = ""
    year: str = ""
    series_chassis: str = ""
    engine: str = ""
    desc: str = ""
    lng_dsc: str = ""
    # Extra fields present on the same search-result object but not shown in the
    # results list — used to populate the page's separate "Registration Details"
    # section (populateSelectedVehicleBox in acc.vehiclesearch.js). Notably, this
    # `vin` is the FULL vin — the /vehicle/{id}/details endpoint's vin is truncated.
    vin: str = ""
    rego: str = ""
    chassis_no: str = ""
    engine_no: str = ""
    body_style: str = ""
    compliance_date: str = ""
    registration_status_current: str = ""
    registration_status_expiry: str = ""
    raw: dict = field(default_factory=dict)


@dataclass
class VehicleDetails:
    """Full detail object from /vehicle/{id}/details — the fields you asked for."""
    make: str = ""
    model: str = ""
    sub_model: str = ""
    configuration: str = ""
    vin: str = ""
    compliance_date: str = ""
    year: str = ""
    chassis: str = ""
    series: str = ""
    engine: str = ""
    body_type: str = ""
    doors: str = ""
    cc: str = ""
    drive_type: str = ""
    fuel: str = ""
    transmission: str = ""
    cyls: str = ""
    rego: str = ""
    registration_status_current: str = ""
    registration_status_expiry: str = ""
    # Populated from the search-result object (not /details) — see VehicleSummary.
    # This vin is the FULL vin; self.vin above (from /details) is truncated by the site.
    full_vin: str = ""
    reg_chassis_no: str = ""
    reg_engine_no: str = ""
    reg_body_style: str = ""
    reg_compliance_date: str = ""
    reg_year: str = ""
    raw: dict = field(default_factory=dict)

    def summary_line(self) -> str:
        parts = [f"Compliance Date: {self.compliance_date}", f"Vin: {self.vin}"]
        parts.append(f"Make: {self.make}")
        parts.append(f"Model: {self.model}")
        parts.append(f"Sub Model: {self.sub_model}")
        parts.append(f"Configuration: {self.configuration}")
        return "\n".join(parts)

    def full_report(self) -> str:
        """Every known field pulled from /vehicle/{id}/details, labeled."""
        labeled = [
            ("Make", self.make),
            ("Model", self.model),
            ("Sub Model", self.sub_model),
            ("Configuration", self.configuration),
            ("Vin", self.vin),
            ("Compliance Date", self.compliance_date),
            ("Year", self.year),
            ("Chassis", self.chassis),
            ("Series", self.series),
            ("Engine", self.engine),
            ("Body Type", self.body_type),
            ("Doors", self.doors),
            ("CC", self.cc),
            ("Drive Type", self.drive_type),
            ("Fuel", self.fuel),
            ("Transmission", self.transmission),
            ("Cylinders", self.cyls),
        ]
        lines = [f"{label}: {value}" for label, value in labeled if value]

        registration = [
            ("Registration", self.rego),
            ("Year", self.reg_year),
            ("Compliance Date", self.reg_compliance_date),
            ("Vin", self.full_vin or self.vin),
            ("Chassis No", self.reg_chassis_no),
            ("Engine No", self.reg_engine_no),
            ("Body Style", self.reg_body_style),
            ("Status", self.registration_status_current),
            ("Expiry", self.registration_status_expiry),
        ]
        registration_lines = [f"{label}: {value}" for label, value in registration if value]
        if registration_lines:
            lines.append("")
            lines.append("Registration Details:")
            lines.extend(registration_lines)

        # Anything else present in the raw response that isn't already covered above
        # (the endpoint returns more fields than acc.vehiclesearch.js renders in the
        # modal — e.g. engineNo, chassisNo, bodyStyle, kw, cam, camType, valves,
        # aspiration, orgnCntry, etc).
        covered_keys = {
            "make", "model", "subModel", "configuration", "vin", "complianceDate",
            "year", "chassis", "series", "engine", "bodyType", "doors", "cc",
            "driveType", "fuel", "transmission", "cyls", "rego",
            "registrationStatusCurrent", "registrationStatusExpiry",
        }
        extra = {
            k: v for k, v in self.raw.items()
            if k not in covered_keys and v not in (None, "", [], {})
        }
        if extra:
            lines.append("")
            lines.append("Additional fields:")
            for k in sorted(extra):
                lines.append(f"{k}: {extra[k]}")

        return "\n".join(lines)


class EzyPartsClient:
    def __init__(self, cookie_header: Optional[str] = None, timeout: float = 10.0):
        self.session = requests.Session()
        self.timeout = timeout
        self.base = BASE_URL + CONTEXT_PATH
        self.session.headers.update(
            {
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
                ),
                "Referer": self.base + "/workbench",
                "Host": "ezyparts.burson.com.au",
            }
        )
        if cookie_header:
            self.session.headers["Cookie"] = cookie_header

    def login(self, account_no: str, username: str, password: str) -> None:
        """
        Replicates the site's real login form submission (confirmed via a captured
        HAR of an actual login): posts acc_no, username, and the combined
        j_username ("{account_no}_{username}") together, plus j_password and a
        doc360_login flag. On success, EzyParts responds with a 302 redirect to
        the site root (e.g. /burson/ezyparts/en/AUD/); a failed login redirects
        back to the login page instead.

        Hybris storefronts embed a CSRFToken in every page (see ACC.config.CSRFToken /
        the hidden `CSRFToken` form input) and reject state-changing POSTs (including
        login) without a valid one. So we first GET the login page to establish a
        session + pick up a fresh token, then submit it alongside the credentials.
        """
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

        # Success redirects to the site root (e.g. /burson/ezyparts/en/AUD/);
        # a failed login redirects back to /login instead.
        if resp.url.rstrip("/").endswith("/login"):
            raise EzyPartsError("Login failed — check account number, username, and password.")

    def _get_json(self, url: str, params: Optional[dict] = None) -> dict:
        resp = self.session.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            raise EzyPartsError(
                "Non-JSON response — likely not authenticated (redirected to login). "
                f"Response started with: {resp.text[:200]!r}"
            )

    def vin_search(self, vin: str) -> List[VehicleSummary]:
        data = self._get_json(self.base + VIN_SEARCH_PATH, params={"text": vin})
        return self._parse_summaries(data)

    def rego_search(self, rego: str, state: str) -> List[VehicleSummary]:
        state = state.upper()
        if state not in VALID_STATES:
            raise EzyPartsError(f"Invalid state '{state}'. Must be one of {sorted(VALID_STATES)}.")
        data = self._get_json(
            self.base + REGO_SEARCH_PATH, params={"state": state, "rego": rego}
        )
        print("----------------------------------------------- rego_search")
        print(json.dumps(data, indent=4))
        return self._parse_summaries(data)

    @staticmethod
    def _parse_summaries(data: dict) -> List[VehicleSummary]:
        vehicles = data.get("vehicles") or []
        return [
            VehicleSummary(
                id=v.get("id", ""),
                make=(v.get("make") or "").strip(),
                model=(v.get("model") or "").strip(),
                year=(v.get("year") or "").strip(),
                series_chassis=(v.get("seriesChassis") or "").strip(),
                engine=(v.get("engine") or "").strip(),
                desc=(v.get("desc") or "").strip(),
                lng_dsc=(v.get("lngDsc") or "").strip(),
                vin=(v.get("vin") or "").strip(),
                rego=(v.get("rego") or "").strip(),
                chassis_no=(v.get("chassisNo") or "").strip(),
                engine_no=(v.get("engineNo") or "").strip(),
                body_style=(v.get("bodyStyle") or "").strip(),
                compliance_date=(v.get("complianceDate") or "").strip(),
                registration_status_current=(v.get("registrationStatusCurrent") or "").strip(),
                registration_status_expiry=(v.get("registrationStatusExpiry") or "").strip(),
                raw=v,
            )
            for v in vehicles
        ]

    def vehicle_details(self, vehicle_id: str) -> VehicleDetails:
        url = self.base + VEHICLE_DETAILS_PATH.format(vehicle_id=vehicle_id)
        data = self._get_json(url)
        print("----------------------------------------------- vehicle_details")
        print(json.dumps(data, indent=4))
        return VehicleDetails(
            make=data.get("make") or "",
            model=data.get("model") or "",
            sub_model=data.get("subModel") or "",
            configuration=data.get("configuration") or "",
            vin=data.get("vin") or "",
            compliance_date=data.get("complianceDate") or "",
            year=data.get("year") or "",
            chassis=data.get("chassis") or "",
            series=data.get("series") or "",
            engine=data.get("engine") or "",
            body_type=data.get("bodyType") or "",
            doors=data.get("doors") or "",
            cc=data.get("cc") or "",
            drive_type=data.get("driveType") or "",
            fuel=data.get("fuel") or "",
            transmission=data.get("transmission") or "",
            cyls=data.get("cyls") or "",
            rego=data.get("rego") or "",
            registration_status_current=data.get("registrationStatusCurrent") or "",
            registration_status_expiry=data.get("registrationStatusExpiry") or "",
            raw=data,
        )

    def lookup_vin(self, vin: str) -> List[VehicleDetails]:
        """Convenience: VIN search -> fetch full details for every matched vehicle id."""
        summaries = self.vin_search(vin)
        return [self._merged_details(s) for s in summaries if s.id]

    def lookup_rego(self, rego: str, state: str) -> List[VehicleDetails]:
        """Convenience: rego search -> fetch full details for every matched vehicle id."""
        summaries = self.rego_search(rego, state)
        return [self._merged_details(s) for s in summaries if s.id]

    def _merged_details(self, summary: VehicleSummary) -> VehicleDetails:
        """
        Fetches /vehicle/{id}/details and layers the search-result summary's
        registration-related fields on top (full vin, rego, chassis no, compliance
        date, reg status) — these live on the search response, not the details
        endpoint, matching the page's separate "Registration Details" section.
        """
        details = self.vehicle_details(summary.id)
        details.full_vin = summary.vin
        details.reg_chassis_no = summary.chassis_no
        details.reg_engine_no = summary.engine_no
        details.reg_body_style = summary.body_style
        details.reg_compliance_date = summary.compliance_date
        details.reg_year = summary.year
        # Prefer summary-sourced rego/status if the details endpoint didn't have them.
        details.rego = details.rego or summary.rego
        details.registration_status_current = (
            details.registration_status_current or summary.registration_status_current
        )
        details.registration_status_expiry = (
            details.registration_status_expiry or summary.registration_status_expiry
        )
        return details


def main():
    parser = argparse.ArgumentParser(description="EzyParts (Burson) vehicle lookup")
    lookup_group = parser.add_mutually_exclusive_group(required=True)
    lookup_group.add_argument("--vin", help="Vehicle VIN to search")
    lookup_group.add_argument("--rego", help="Vehicle registration number to search")
    parser.add_argument(
        "--state",
        choices=sorted(VALID_STATES),
        help="Australian state the rego is registered in (required with --rego)",
    )
    parser.add_argument(
        "--account",
        default=EZYPARTS_ACCOUNT,
        help="Trade account number (or set EZYPARTS_ACCOUNT env var)",
    )
    parser.add_argument(
        "--username",
        default=EZYPARTS_USERNAME,
        help="Trade username (or set EZYPARTS_USERNAME env var)",
    )
    parser.add_argument(
        "--password",
        default=EZYPARTS_PASSWORD,
        help="Trade password (or set EZYPARTS_PASSWORD env var — preferred over passing on the CLI)",
    )
    parser.add_argument(
        "--cookie",
        default=None,
        help="Alternative to --account/--username/--password: a raw Cookie header "
        "from an already-authenticated browser session",
    )
    args = parser.parse_args()

    if args.rego and not args.state:
        parser.error("--rego requires --state")

    client = EzyPartsClient(cookie_header=args.cookie)

    if not args.cookie:
        if not (args.account and args.username and args.password):
            print(
                "No credentials provided. Pass --account/--username/--password "
                "(or set EZYPARTS_ACCOUNT/EZYPARTS_USERNAME/EZYPARTS_PASSWORD env vars), "
                "or use --cookie with a session cookie instead.",
                file=sys.stderr,
            )
            sys.exit(1)
        try:
            client.login(args.account, args.username, args.password)
        except (requests.RequestException, EzyPartsError) as e:
            print(f"Login failed: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        if args.vin:
            results = client.lookup_vin(args.vin)
        else:
            results = client.lookup_rego(args.rego, args.state)
    except (requests.RequestException, EzyPartsError) as e:
        print(f"Lookup failed: {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print("No vehicles found.")
        return

    # for i, v in enumerate(results, 1):
    #     if len(results) > 1:
    #         print(f"--- Result {i} ---")
    #     print(v.full_report())
    #     print()


if __name__ == "__main__":
    main()




# {
#     'searchStatus': {
#         'results': '1', 'message': ''
#         },
#     'vehicles': [
#         {
#             'id': '327957660',
#             'desc': '13~17 HSV GRANGE 6.2L PETROL',
#             'make': 'HSV',
#             'model': 'GRANGE',
#             'subModel': None,
#             'year': '06/2013 ~ 02/2017',
#             'series': 'WN',
#             'chassis': None,
#             'seriesChassis': 'WN -WN',
#             'engine': '6.2L  PET LS3 V8 16v OHV MPFI {340kW}',
#             'details': '4D Sedan, RWD 6G1NR5EW  [AUSTRALIA], AT',
#             'bodyType': None, 
#             'fuel': None, 
#             'doors': None, 
#             'lngDsc': 'HSV GRANGE  Auto WN 06/2013~02/2017 4 Door Sedan RWD PETROL 6.2 litre, LS3 V8 16v OHV MPFI {340kW} ', 
#             'hasMID': True, 
#             'rego': 'BURKIE', 
#             'regoState': 'ACT', 
#             'vin': '6G1NR5EW7EL921381', 
#             'searchStrategy': None
#         }
#     ],
#     'make': '', 
#     'model': '', 
#     'year': '2013', 
#     'complianceDate': '', 
#     'vin': '6G1NR5EW7EL921381', 
#     'chassisNo': 'GMH 8EH19', 
#     'engineNo': '', 
#     'bodyStyle': '', 
#     'rego': 'BURKIE', 
#     'regoState': 'ACT', 
#     'registrationStatusCurrent': None, 
#     'registrationStatusExpiry': None
# }

# {
#     'id': '327957660', 
#     'make': 'HSV', 
#     'model': 'GRANGE', 
#     'subModel': '', 
#     'chassis': 'WN', 
#     'series': 'WN', 
#     'engine': 'LS3', 
#     'cc': '6162', 
#     'configuration': 'V Configuration  8 Cyl', 
#     'cyls': '8', 
#     'cam': 'OHV', 
#     'aspiration': 'Not Specified', 
#     'doors': '4', 
#     'fuelSystem': 'MPFI', 
#     'fuelDesc': 'Multi Point Fuel Injection', 
#     'driveType': 'RWD', 
#     'bodyType': 'Sedan', 
#     'yearMin': '2013', 
#     'yearMax': '2017', 
#     'startMonth': '06', 
#     'endMonth': '02', 
#     'auto': True, 
#     'man': False, 
#     'cvt': False, 
#     'dct': False, 
#     'fuel': 'PETROL', 
#     'orgnCntry': 'AUSTRALIA', 
#     'desc': '13~17 HSV GRANGE 6.2L', 
#     'hasMID': True, 
#     'valves': '16', 
#     'vin': '6G1NR5EW', 
#     'camType': 'CHAIN', 
#     'engineDetails': 'LS3 V8 16v OHV MPFI {340kW}', 
#     'kw': '340', 
#     'transmission': 'Auto '
# }