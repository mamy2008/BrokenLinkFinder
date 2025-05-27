
import argparse
import sys
import json
import os
from datetime import datetime
from colorama import init, Fore, Style
from audit import check_broken_links, crawl_site_for_broken_links

# Initialize colorama for colored terminal output (especially for Windows)
init()

# Define the directory name for reports
REPORT_DIR = "reports"  # Changed from 'report' to 'reports' for better naming


def main():
	parser = argparse.ArgumentParser(
		description="A simple Python Command-Line Interface (CLI) tool for Technical SEO audits."
	)

	parser.add_argument(
		'--url',
		type=str,
		help='The URL of the website to audit (e.g., https://www.example.com/). If not provided, the tool will prompt for it.'
	)

	parser.add_argument(
		'--scan-type',
		type=int,
		choices=[0, 1],  # 0 for single page, 1 for deep crawl
		help='Specify the scan type: 0 for single-page audit, 1 for deep site crawl. (If not provided, the tool will prompt for it.)'
	)

	parser.add_argument(
		'--max-pages',
		type=int,
		default=60,  # Default limit for deep crawl pages
		help='Maximum number of pages to crawl during a deep site audit. (Default: 60)'
	)

	parser.add_argument(
		'--timeout',
		type=int,
		default=60,  # Default timeout in seconds (1 minute)
		help='Maximum time in seconds for the deep site crawl to run. (Default: 60 seconds / 1 minute)'
	)

	parser.add_argument(
		'--check-broken-links',
		action='store_true',
		help='(Default for single-page scan) Checks for broken (404) links on the specified URL.'
	)

	parser.add_argument(
		'--output-format',
		type=str,
		choices=['text', 'json'],
		default='json',
		help='Specify the output format: "text" for terminal display or "json" for JSON output. (Default: json)'
	)

	args = parser.parse_args()

	# --- 1. Get Target URL ---
	target_url = args.url
	if not target_url:
		target_url = input(
			f"{Fore.CYAN}Please enter the website URL to audit (e.g., https://www.example.com/): {Style.RESET_ALL}")
		if not target_url:
			print(f"{Fore.RED}Error: URL not provided. Exiting program.{Style.RESET_ALL}")
			sys.exit(1)

	# --- 2. Get Scan Type ---
	scan_type = args.scan_type
	if scan_type is None:  # If --scan-type was not provided in command line
		while True:
			try:
				user_input = input(
					f"{Fore.CYAN}Select scan type (0: Single-page audit, 1: Deep site crawl): {Style.RESET_ALL}")
				scan_type = int(user_input)
				if scan_type in [0, 1]:
					break
				else:
					print(f"{Fore.YELLOW}Invalid input. Please enter 0 or 1.{Style.RESET_ALL}")
			except ValueError:
				print(f"{Fore.YELLOW}Invalid input. Please enter a number.{Style.RESET_ALL}")

	results = None

	# --- Try-Except block for KeyboardInterrupt ---
	try:
		# --- 3. Execute Scan Based on Type ---
		if scan_type == 0:  # Single-page audit
			print(f"{Fore.CYAN}Performing single-page broken link check for: {target_url}{Style.RESET_ALL}")
			results = check_broken_links(target_url, output_format=args.output_format)

		elif scan_type == 1:  # Deep site crawl
			MAX_DEPTH = 5  # Fixed maximum crawl depth
			print(
				f"{Fore.CYAN}Performing deep site crawl for: {target_url} (Max Depth: {MAX_DEPTH}, Max Pages: {args.max_pages}, Max Time: {args.timeout} seconds){Style.RESET_ALL}")

			results = crawl_site_for_broken_links(
				start_url=target_url,
				max_depth=MAX_DEPTH,
				max_pages=args.max_pages,
				timeout=args.timeout,
				output_format='json'  # Deep crawl always returns JSON output
			)

	except KeyboardInterrupt:
		print(
			f"\n{Fore.YELLOW}----- Crawl interrupted by user (Ctrl+C). Saving temporary results... -----{Style.RESET_ALL}")
		# If results are None, create a basic structure to ensure a valid JSON file is saved.
		if results is None:
			print(f"{Fore.RED}Error: No temporary results available to save.{Style.RESET_ALL}")
			sys.exit(1)

	# --- 4. Handle Results (Display and Save) ---
	if results:
		# Create reports directory if it doesn't exist
		if not os.path.exists(REPORT_DIR):
			os.makedirs(REPORT_DIR)
			print(f"{Fore.GREEN}Directory '{REPORT_DIR}' created.{Style.RESET_ALL}")

		# Sanitize URL for filename and add timestamp
		# Removes scheme, replaces special chars with underscores, removes trailing underscore
		sanitized_url = target_url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":",
																											"_").replace(
			".", "_").strip('_')
		current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

		# Add scan type to filename for clarity
		scan_type_name = "single_page" if scan_type == 0 else "deep_crawl"

		# Append '-interrupted' to filename if crawl was interrupted
		interrupted_suffix = "-interrupted" if "interrupted" in results.get("crawl_completion_status",
																			"").lower() else ""

		report_filename = f"{sanitized_url}-{scan_type_name}-{current_time}{interrupted_suffix}.json"
		report_filepath = os.path.join(REPORT_DIR, report_filename)

		try:
			with open(report_filepath, 'w', encoding='utf-8') as f:
				json.dump(results, f, indent=4, ensure_ascii=False)
			print(f"{Fore.GREEN}Report successfully saved to '{report_filepath}'.{Style.RESET_ALL}")
		except Exception as e:
			print(f"{Fore.RED}Error saving report: {e}{Style.RESET_ALL}")

		# Display JSON output in terminal if requested
		if args.output_format == 'json':
			print(f"\n{Fore.YELLOW}Full JSON Output (also saved to file):{Style.RESET_ALL}")
			print(json.dumps(results, indent=4, ensure_ascii=False))
		elif scan_type == 1:  # For deep crawl text output, just confirm it's in the file
			print(f"{Fore.YELLOW}Deep scan completed. Full details saved to JSON file.{Style.RESET_ALL}")

	else:  # This block handles cases where no results could be generated (e.g., failed to fetch starting page)
		if scan_type == 0 and args.output_format == 'text':
			print(
				f"{Fore.YELLOW}Single-page scan completed. Text report displayed in console (if issues found).{Style.RESET_ALL}")
		elif scan_type == 1:
			print(f"{Fore.RED}Error: Deep crawl could not generate any results.{Style.RESET_ALL}")


if __name__ == '__main__':
	main()