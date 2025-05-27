from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from colorama import Fore, Style
from utils import fetch_page_content, check_link_status, normalize_url, get_base_domain
import time
import signal


# --- Single-page audit function ---
def check_broken_links(url: str, output_format: str = 'text'):
	"""
	Finds broken (internal and external) links on a specified URL.
	Returns results as a list of dictionaries for JSON output, or prints text output.
	"""
	links = []
	broken_links_results = []

	if output_format == 'text':
		print(f"{Fore.CYAN}Checking for broken links on: {url}{Style.RESET_ALL}")

	content = fetch_page_content(url)
	if not content:
		if output_format == 'text':
			print(f"{Fore.RED}Error: Unable to fetch page content.{Style.RESET_ALL}")
		if output_format == 'json':
			return {
				"audited_url": url,
				"total_links_found": 0,
				"total_broken_links": 0,
				"broken_links": []
			}
		return None

	soup = BeautifulSoup(content, 'html.parser')

	for a_tag in soup.find_all('a', href=True):
		href = a_tag['href']
		if href.startswith('http://') or href.startswith('https://'):
			full_url = href
		else:
			try:
				full_url = urljoin(url, href)
				if not full_url.startswith(('http://', 'https://')):
					continue
			except ValueError:
				continue
		links.append(full_url)

	checked_urls_for_status = set()

	for link in links:
		if link in checked_urls_for_status:
			continue
		checked_urls_for_status.add(link)

		status_code = check_link_status(link)

		if status_code >= 400 or status_code == 0:
			broken_links_results.append({
				"link": link,
				"status_code": status_code,
				"status_message": "Broken" if status_code >= 400 else "Connection Error"
			})
			if output_format == 'text':
				print(f"  {Fore.RED}Broken link found: {link} (Code: {status_code}){Style.RESET_ALL}")
		else:
			if output_format == 'text':
				print(f"  {Fore.GREEN}OK: {link} (Code: {status_code}){Style.RESET_ALL}")

	if output_format == 'text':
		if broken_links_results:
			print(f"\n{Fore.YELLOW}Summary: {len(broken_links_results)} broken links found:{Style.RESET_ALL}")
			for bl in broken_links_results:
				print(f"- {bl['link']} (Code: {bl['status_code']})")
		else:
			print(f"\n{Fore.GREEN}No broken links found. Excellent!{Style.RESET_ALL}")
		return None

	elif output_format == 'json':
		return {
			"audited_url": url,
			"scan_type": "single_page",
			"total_links_found": len(links),
			"total_broken_links": len(broken_links_results),
			"broken_links": broken_links_results
		}


# --- Global variable for soft stop control ---
STOP_CRAWL = False


def signal_handler(sig, frame):
	global STOP_CRAWL
	print(f"\n{Fore.YELLOW}Stop signal received. Crawl will stop soon. Please wait...{Style.RESET_ALL}")
	STOP_CRAWL = True


# Register the signal handler once for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)


# --- Deep site crawl function ---
def crawl_site_for_broken_links(start_url: str, max_depth: int, max_pages: int, timeout: int,
								output_format: str = 'json'):
	global STOP_CRAWL
	STOP_CRAWL = False  # Reset stop flag for each new crawl run

	# Normalize the starting URL and its domain
	normalized_start_url = normalize_url(start_url)
	print(f"DEBUG_NORM_START: Original: {start_url} -> Normalized Start: {normalized_start_url}")
	base_domain_of_start_url = get_base_domain(normalized_start_url)
	print(
		f"DEBUG_DOMAIN_START: Normalized Start URL: {normalized_start_url} -> Base Domain: {base_domain_of_start_url}")

	if not base_domain_of_start_url:
		print(
			f"{Fore.RED}Error: Invalid starting URL or base domain could not be extracted: {start_url}{Style.RESET_ALL}")
		return {
			"audited_url": start_url,
			"scan_type": "deep_crawl",
			"error": "Invalid starting URL or base domain could not be extracted.",
			"total_pages_crawled": 0,
			"total_unique_links_checked": 0,
			"total_broken_links_across_site": 0,
			"crawled_pages_summary": [],
			"all_broken_links_detailed": []
		}

	# Data structures for crawling
	queue = [(normalized_start_url, 0)]
	visited_urls = {normalized_start_url}  # Initialize with normalized start_url as visited

	all_broken_links_detailed = []
	crawled_pages_summary = []
	total_unique_links_checked = 0

	THROTTLE_TIME = 0.1  # Reduced throttle time for faster crawling

	start_time = time.time()

	print(f"{Fore.MAGENTA}Starting deep crawl...{Style.RESET_ALL}")

	while queue and len(crawled_pages_summary) < max_pages:
		# --- Overall timeout check (re-enabled) ---
		if time.time() - start_time > timeout:
			print(f"{Fore.RED}Crawl stopped due to timeout ({timeout} seconds).{Style.RESET_ALL}")
			break
		# --- End of timeout check ---

		# Check for user-initiated stop
		if STOP_CRAWL:
			print(f"{Fore.RED}Crawl stopped by user.{Style.RESET_ALL}")
			break

		current_normalized_url, current_depth = queue.pop(0)

		# DEBUG_REPROCESS_ERROR: Check if the URL being processed has already been recorded in summary.
		# This indicates a failure in visited_urls or normalize_url if it occurs.
		if any(s['url'] == current_normalized_url for s in crawled_pages_summary):
			print(
				f"DEBUG_REPROCESS_ERROR: {current_normalized_url} is being re-processed. This indicates an issue and should be investigated.")  # DEBUG
			# If this error occurs, we should skip processing this URL to prevent infinite loops.
			continue

		if current_depth > max_depth:
			print(
				f"DEBUG_DEPTH_SKIP: Skipping {current_normalized_url} due to depth {current_depth} > max_depth {max_depth}")
			continue

		print(
			f"{Fore.BLUE}Crawling (Depth {current_depth}, Page {len(crawled_pages_summary) + 1} of {max_pages}): {current_normalized_url}{Style.RESET_ALL}")

		time.sleep(THROTTLE_TIME)  # Apply throttle

		content = fetch_page_content(current_normalized_url)
		if not content:
			crawled_pages_summary.append({
				"url": current_normalized_url,
				"depth": current_depth,
				"status_code": 0,
				"links_found_on_page": 0,
				"broken_links_on_page": [],
				"note": "Failed to fetch content or connection error."
			})
			continue

		soup = BeautifulSoup(content, 'html.parser')
		links_on_current_page = []
		broken_links_on_current_page = []

		unique_normalized_links_on_this_page = set()

		for a_tag in soup.find_all('a', href=True):
			href = a_tag['href']

			full_link_raw = None
			if href.startswith('http://') or href.startswith('https://'):
				full_link_raw = href
			else:
				try:
					full_link_raw = urljoin(current_normalized_url, href)
					if not full_link_raw.startswith(('http://', 'https://')):
						continue
				except ValueError:
					continue

			if full_link_raw:
				links_on_current_page.append(full_link_raw)

				normalized_current_link = normalize_url(full_link_raw)
				print(f"DEBUG_NORM_LINK: Original: {full_link_raw} -> Normalized: {normalized_current_link}")

				if normalized_current_link in unique_normalized_links_on_this_page:
					print(f"DEBUG_DUPE_ON_PAGE: {normalized_current_link} is duplicate on current page.")
					continue
				unique_normalized_links_on_this_page.add(normalized_current_link)

				link_base_domain = get_base_domain(normalized_current_link)
				is_internal_link = (link_base_domain == base_domain_of_start_url)
				print(
					f"DEBUG_LINK_TYPE: {normalized_current_link} (Domain: {link_base_domain}) is Internal: {is_internal_link}")

				if is_internal_link and normalized_current_link not in visited_urls and current_depth + 1 <= max_depth:
					if len(crawled_pages_summary) + len(queue) + 1 <= max_pages:
						queue.append((normalized_current_link, current_depth + 1))
						visited_urls.add(normalized_current_link)
						print(
							f"DEBUG_QUEUE_ADD: Added {normalized_current_link} (depth {current_depth + 1}) to queue. Visited size: {len(visited_urls)}, Queue size: {len(queue)}")
					else:
						print(
							f"{Fore.YELLOW}Skipping {normalized_current_link} (as new page) due to max pages limit ({max_pages}).{Style.RESET_ALL}")
				else:
					if not is_internal_link:
						print(f"DEBUG_QUEUE_SKIP: Skipping {normalized_current_link} (external).")
					elif normalized_current_link in visited_urls:
						print(f"DEBUG_QUEUE_SKIP: Skipping {normalized_current_link} (already visited/queued).")
					elif current_depth + 1 > max_depth:
						print(f"DEBUG_QUEUE_SKIP: Skipping {normalized_current_link} (exceeds max depth).")

				status_code = check_link_status(full_link_raw)
				total_unique_links_checked += 1

				if status_code >= 400 or status_code == 0:
					broken_link_info = {
						"link": full_link_raw,
						"status_code": status_code,
						"status_message": "Broken" if status_code >= 400 else "Connection Error"
					}
					broken_links_on_current_page.append(broken_link_info)

					is_already_recorded_broken = False
					for entry in all_broken_links_detailed:
						if normalize_url(entry["link"]) == normalized_current_link and entry[
							"status_code"] == status_code:
							is_already_recorded_broken = True
							break

					if not is_already_recorded_broken:
						all_broken_links_detailed.append({
							"link": full_link_raw,
							"status_code": status_code,
							"status_message": broken_link_info["status_message"],
							"source_page": current_normalized_url,
							"depth_found": current_depth
						})
						print(
							f"  {Fore.RED}Broken link found: {full_link_raw} (Code: {status_code}) from {current_normalized_url}{Style.RESET_ALL}")
				else:
					print(
						f"  {Fore.GREEN}OK: {full_link_raw} (Code: {status_code}) from {current_normalized_url}{Style.RESET_ALL}")

		crawled_pages_summary.append({
			"url": current_normalized_url,
			"depth": current_depth,
			"links_found_on_page": len(links_on_current_page),
			"broken_links_on_page": broken_links_on_current_page
		})

	crawl_status_message = "Crawl completed."
	if time.time() - start_time > timeout:
		crawl_status_message = f"Crawl stopped due to timeout ({timeout} seconds)."
	elif STOP_CRAWL:
		crawl_status_message = "Crawl stopped by user."

	print(
		f"{Fore.MAGENTA}{crawl_status_message} Pages crawled: {len(crawled_pages_summary)}, Broken links found: {len(all_broken_links_detailed)}{Style.RESET_ALL}")

	return {
		"audited_url": start_url,
		"scan_type": "deep_crawl",
		"total_pages_crawled": len(crawled_pages_summary),
		"total_unique_links_checked": total_unique_links_checked,
		"total_broken_links_across_site": len(all_broken_links_detailed),
		"crawled_pages_summary": crawled_pages_summary,
		"all_broken_links_detailed": all_broken_links_detailed,
		"crawl_completion_status": crawl_status_message
	}