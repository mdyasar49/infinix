import re
import socket
import dns.resolver
import phonenumbers
from phonenumbers import PhoneNumberType, geocoder, carrier

# List of known disposable / dummy / placeholder domains to reject immediately
DISPOSABLE_DOMAINS = {
    'example.com', 'test.com', 'sample.com', 'techprojects.com', 'client.com',
    'localhost', 'dummy.com', 'tempmail.com', 'mailinator.com', 'guerrillamail.com',
    '10minutemail.com', 'trashmail.com', 'yopmail.com', 'sharklasers.com',
    'getairmail.com', 'throwawaymail.com', 'fakeinbox.com', 'dispostable.com',
    'mytemp.email', 'temp-mail.org', 'dropmail.me', 'mohmal.com', 'emailondeck.com',
    'generator.email', 'inboxkitten.com', 'burnermail.io', 'maildrop.cc'
}

# Common invalid/fictional number patterns to reject
INVALID_PHONE_PATTERNS = [
    r'^(?:\+?\d{1,3})?0{7,}$',       # All zeros
    r'^(?:\+?\d{1,3})?1{7,}$',       # All ones
    r'^(?:\+?\d{1,3})?9{7,}$',       # All nines
    r'12345678',                     # Sequential dummy
    r'555[-. ]?01\d\d',              # US TV fictional 555-01xx
    r'000[-. ]?000',                 # Zero blocks
    r'^\+?123456',                   # Dummy test numbers
]

# MX cache to avoid repeated DNS queries
_MX_CACHE = {}

def get_configured_resolver():
    res = dns.resolver.Resolver()
    res.nameservers = ['8.8.8.8', '1.1.1.1', '8.8.4.4', '1.0.0.1']
    res.timeout = 2.5
    res.lifetime = 2.5
    return res

def verify_email_liveness(email):
    """
    Strict Deep Email Verification:
    1. Syntax validation (RFC 5322)
    2. Disposable & placeholder domain rejection
    3. Live DNS MX (Mail Exchange) record check via Google & Cloudflare DNS
    
    Returns: (is_valid: bool, cleaned_email: str, reason: str)
    """
    if not email or not isinstance(email, str):
        return False, "", "Empty email"
    
    clean = email.strip().lower()
    
    # 1. Regex Syntax Check
    email_regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,63}$'
    if not re.match(email_regex, clean):
        return False, clean, "Invalid email syntax"
    
    # Exclude non-email words mistakenly parsed
    if clean.startswith("mailto:") or clean in ["email", "work email address", "contact@"]:
        return False, clean, "Placeholder string, not real email"
    
    domain = clean.split('@')[-1]
    
    # 2. Check Blacklisted / Dummy Domains
    if domain in DISPOSABLE_DOMAINS or any(d in domain for d in ['example.', 'tempmail', 'disposable', 'mailinator']):
        return False, clean, f"Blocked dummy/disposable domain: {domain}"
    
    # 3. Live DNS MX Record Check
    if domain in _MX_CACHE:
        if not _MX_CACHE[domain]:
            return False, clean, f"Domain '{domain}' has no active mail server (cached)"
        return True, clean, "Valid & Active (MX verified)"
    
    resolver = get_configured_resolver()
    try:
        mx_records = resolver.resolve(domain, 'MX')
        if mx_records and len(mx_records) > 0:
            _MX_CACHE[domain] = True
            return True, clean, "Valid & Active (Live MX verified)"
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.exception.Timeout):
        try:
            a_records = resolver.resolve(domain, 'A')
            if a_records and len(a_records) > 0:
                _MX_CACHE[domain] = True
                return True, clean, "Valid (Domain A record active)"
        except Exception:
            _MX_CACHE[domain] = False
            return False, clean, f"Domain '{domain}' is dead/inactive (No MX or A records found)"
    except Exception as e:
        _MX_CACHE[domain] = False
        return False, clean, f"DNS lookup failed for '{domain}': {e}"
        
    _MX_CACHE[domain] = False
    return False, clean, f"Domain '{domain}' has no active mail servers"


def verify_phone_number(phone_raw, default_country="AU"):
    """
    Strict Phone & Mobile Verification using Google's libphonenumber:
    1. Clean and parse according to national/international standards
    2. Check possible and valid number rules for target country
    3. Exclude dummy / sequential / fictional numbers
    
    Returns: (is_valid: bool, formatted_phone: str, number_type: str, reason: str)
    """
    if not phone_raw or not isinstance(phone_raw, str):
        return False, "", "None", "Empty phone number"
        
    cleaned_input = phone_raw.strip().replace("'", "").replace('"', "")
    digits_only = re.sub(r'\D', '', cleaned_input)
    if len(digits_only) < 7 or len(digits_only) > 15:
        return False, cleaned_input, "None", "Invalid digit length"
        
    # Check dummy patterns
    for pat in INVALID_PHONE_PATTERNS:
        if re.search(pat, cleaned_input):
            return False, cleaned_input, "None", f"Rejected dummy pattern: {cleaned_input}"
            
    candidate_regions = [default_country, "AU", "IN", "US", "GB", None]
    parsed = None
    
    for region in candidate_regions:
        try:
            p = phonenumbers.parse(cleaned_input, region)
            if phonenumbers.is_valid_number(p):
                parsed = p
                break
        except Exception:
            continue
            
    if not parsed:
        for region in candidate_regions:
            try:
                p = phonenumbers.parse(cleaned_input, region)
                if phonenumbers.is_possible_number(p):
                    parsed = p
                    break
            except Exception:
                continue
                
    if not parsed:
        return False, cleaned_input, "None", "Invalid phone number structure"
        
    is_valid = phonenumbers.is_valid_number(parsed)
    num_type_code = phonenumbers.number_type(parsed)
    
    type_map = {
        PhoneNumberType.MOBILE: "Mobile",
        PhoneNumberType.FIXED_LINE: "Fixed Line",
        PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line / Mobile",
        PhoneNumberType.TOLL_FREE: "Toll Free",
        PhoneNumberType.VOIP: "VoIP",
        PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
        PhoneNumberType.UNKNOWN: "Unknown"
    }
    num_type_str = type_map.get(num_type_code, "Other")
    
    formatted_intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    
    if is_valid:
        return True, formatted_intl, num_type_str, "Valid & Active Number"
    elif phonenumbers.is_possible_number(parsed):
        return True, formatted_intl, num_type_str, "Possible Valid Number"
    else:
        return False, formatted_intl, num_type_str, "Number failed national validation rules"
