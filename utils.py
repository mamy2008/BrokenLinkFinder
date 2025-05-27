import requests
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode


def fetch_page_content(url: str) -> str | None:
	"""
	Retrieves the HTML content of a web page.
	Returns None on error.
	"""
	try:
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
		}
		response = requests.get(url, headers=headers, timeout=15)
		response.raise_for_status()
		print(f"DEBUG_FETCH: Successfully fetched {url}. Status Code: {response.status_code}")
		return response.text
	except requests.exceptions.HTTPError as e:
		print(f"DEBUG_FETCH: HTTP Error fetching {url}: {e.response.status_code} - {e.response.reason}")
		if e.response.status_code == 403:
			print("DEBUG_FETCH: Access Denied (403 Forbidden). The server might be blocking automated requests.")
		return None
	except requests.exceptions.ConnectionError as e:
		print(f"DEBUG_FETCH: Connection Error fetching {url}: {e}")
		print("DEBUG_FETCH: Check your internet connection or if the URL is accessible.")
		return None
	except requests.exceptions.Timeout as e:
		print(f"DEBUG_FETCH: Timeout Error fetching {url}: {e}")
		print("DEBUG_FETCH: The server took too long to respond.")
		return None
	except requests.exceptions.RequestException as e:
		print(f"DEBUG_FETCH: General Request Error fetching {url}: {e}")
		return None
	except Exception as e:
		print(f"DEBUG_FETCH: An unexpected error occurred while fetching {url}: {e}")
		return None


def check_link_status(url: str) -> int:
	"""
	Checks the HTTP status code of a link.
	"""
	try:
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
		}
		response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
		return response.status_code
	except requests.exceptions.RequestException as e:
		return 0
	except Exception as e:
		return 0


def normalize_url(url: str) -> str:
	"""
	Normalizes a URL to a consistent format for comparison.
	- Converts to HTTPS.
	- Removes www. if present from netloc.
	- Ensures all paths (including root) have a trailing slash.
	- Removes common tracking query parameters.
	- Sorts remaining query parameters.
	- Removes fragment (e.g., #section).
	- Converts domain to lowercase.
	"""
	try:
		parsed_url = urlparse(url)

		# 1. Scheme (HTTP to HTTPS)
		scheme = 'https'

		# 2. Netloc (domain) - convert to lowercase, remove www.
		netloc = parsed_url.netloc.lower()
		if netloc.startswith('www.'):
			netloc = netloc[4:]

		# 3. Path - Ensure all paths have a trailing slash (for consistency)
		path = parsed_url.path
		if not path:  # Empty path (e.g., domain.com) becomes '/'
			path = '/'
		if not path.endswith('/'):  # Always add trailing slash if not present
			path += '/'

		# 4. Query - remove common tracking parameters and sort remaining
		query_params = parse_qs(parsed_url.query, keep_blank_values=True)
		tracking_params = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid',
						   'ref', '_ga']

		filtered_query_params = {}
		for key, value in query_params.items():
			if key not in tracking_params:
				filtered_query_params[key] = value

		sorted_query = urlencode(sorted(filtered_query_params.items(), key=lambda x: x[0]), doseq=True)

		# 5. Fragment - remove (e.g., #section)
		fragment = ''

		# Reconstruct the URL
		normalized_url = urlunparse((scheme, netloc, path, parsed_url.params, sorted_query, fragment))

		return normalized_url
	except Exception as e:
		print(f"DEBUG_NORM_ERROR: Error normalizing URL {url}: {e}")
		return url


def get_base_domain(url: str) -> str | None:
	"""
	Extracts the base domain (e.g., 'example.com' from 'www.example.com' or 'blog.example.com')
	without relying on external libraries.
	This is a simplified approach and might not handle all complex TLDs perfectly (e.g., co.uk).
	"""
	try:
		parsed_url = urlparse(url)
		netloc = parsed_url.netloc

		if ':' in netloc:
			netloc = netloc.split(':')[0]

		parts = netloc.split('.')
		if len(parts) >= 2:
			base_domain = ".".join(parts[-2:])
		else:
			base_domain = netloc

		return base_domain if base_domain else None
	except Exception as e:
		print(f"DEBUG_BASE_DOMAIN_ERROR: Error extracting base domain from {url} (manual method): {e}")
		return None