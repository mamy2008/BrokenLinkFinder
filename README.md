# Broken Link Finder (SEO)

A powerful and simple Python Command-Line Interface (CLI) tool designed to perform essential Technical SEO audits on websites. This tool helps web developers, SEO specialists, and site owners quickly identify common technical issues like broken links that can affect search engine rankings and user experience.

## Features

-   **Single-Page Broken Link Checker:** Quickly identifies internal and external broken links (404 errors) on a single specified URL.
-   **Deep Site Broken Link Crawler:** Conducts a comprehensive crawl of an entire website (up to a defined depth and page limit) to discover broken links across all internal pages.
-   **URL Normalization:** Intelligently normalizes URLs (e.g., handles trailing slashes, `www.` vs. non-`www.`, and tracking parameters) to prevent duplicate crawling and ensure accurate results.
-   **Crawl Control:** Allows setting maximum crawl depth, maximum number of pages to crawl, and an overall timeout for deep scans.
-   **Interruption Handling:** Safely stops the crawl process on user interruption (Ctrl+C) and saves accumulated results.
-   **JSON Output:** Generates detailed JSON reports for easy analysis and integration with other tools.
-   **Colored Console Output:** Provides clear, color-coded messages in the terminal for better readability.

## Installation

To get started with SEO Audit CLI, follow these simple steps:

1.  **Install Python:**
    Ensure you have Python (version 3.x is recommended) installed on your system. You can download it from the official Python website: [python.org](https://www.python.org/).

2.  **Clone the repository:**
    Open your terminal or command prompt and clone the project from GitHub:
    ```bash
    git clone [https://github.com/YourUsername/seo-audit-cli.git](https://github.com/YourUsername/seo-audit-cli.git)
    cd seo_audit_cli
    ```
    (Remember to replace `YourUsername` with your actual GitHub username.)

3.  **Install dependencies:**
    Navigate into the cloned directory and install the required Python libraries using pip. It's recommended to do a fresh install to avoid any old cached versions:
    ```bash
    pip install -r requirements.txt --force-reinstall
    ```
    Ensure your `requirements.txt` file contains exactly these lines:
    ```
    requests
    beautifulsoup4
    colorama
    argparse
    ```

## Usage

SEO Audit CLI offers flexible usage options from your terminal.

To run the tool, navigate to the `seo_audit_cli` directory in your terminal and execute `python main.py`. The tool will then prompt you for input.

```bash
python main.py
```
## Command-Line Arguments

You can also provide arguments directly:

-  **--url <YOUR_URL>**: The starting URL for the audit (e.g., **https://www.example.com/**). If omitted, you will be prompted.
- **--scan-type <TYPE>**: **0** for a single-page audit, **1** for a deep site crawl. If omitted, you will be prompted.
- **--max-pages <NUMBER>**: (For deep crawl) Maximum number of unique pages to crawl. Default: 60.
- **--timeout <SECONDS>**: (For deep crawl) Maximum time in seconds the crawl should run. Default: 60 seconds (1 minute).
- **--output-format <FORMAT>**: **text** for console output, **json** for JSON output (also saved to file). Default: **json**.

## Examples

1.  **Perform a single-page audit (prompted input):**
```bash
python main.py
# (Tool will prompt for URL)
# (Enter 0 for scan type)
```
2.  **Perform a deep site crawl (prompted input):**
```bash
python main.py
# (Tool will prompt for URL)
# (Enter 1 for scan type)
```
3.  **Perform a deep site crawl for a specific URL, crawling up to 100 pages for a maximum of 5 minutes, with JSON output:**
```bash
python main.py --url [https://www.yourwebsite.com/](https://www.yourwebsite.com/) --scan-type 1 --max-pages 100 --timeout 300 --output-format json
```
4. Perform a single-page audit for a specific URL with text output to console:
```bash
python main.py --url [https://www.yourwebsite.com/about-us/](https://www.yourwebsite.com/about-us/) --scan-type 0 --output-format text
```
## Reports

All deep crawl results are saved in a **reports/** directory (created automatically) as JSON files. The filename includes the sanitized URL, scan type, timestamp, and indicates if the crawl was interrupted.

Example filename: 
``` 
example_com_-deep_crawl-2025-05-27-10-30-00.json or example_com_-deep_crawl-2025-05-27-10-35-15-interrupted.json.
```
or
``` 
example_com_-deep_crawl-2025-05-27-10-35-15-interrupted.json
``` 
## Limitations

- Not for very large websites: This tool is designed for small to medium-sized websites. Crawling extremely large websites (millions of pages) requires more robust infrastructure (e.g., distributed crawlers, dedicated proxies, database storage).
- Anti-Bot Mechanisms: Websites with aggressive anti-bot detection systems (like Google.com, Facebook.com) may block requests from this tool. For such sites, more advanced techniques (e.g., rotating proxies, headless browsers with human-like behavior) are needed, which are beyond the scope of this simple CLI tool.
- JavaScript Rendering: The tool primarily fetches static HTML. It does not execute JavaScript to discover dynamically loaded links or content. For websites heavily reliant on Client-Side Rendering (CSR) via JavaScript, some links might be missed.
- Throttling: The default **THROTTLE_TIME** is set to 0.1 seconds between requests to be gentle on servers. For faster crawling, this value can be adjusted directly in **audit.py**

## Contributing
We welcome and appreciate any contributions to improve SEO Audit CLI! If you have ideas for new features, bug fixes, or enhancements, please feel free to:
- Submit a [Pull Request](https://github.com/amrnima/BrokenLinkFinder/pulls) with your changes.
- Open an [Issue](https://github.com/amrnima/BrokenLinkFinder/issues) to report bugs or suggest enhancements.
Your involvement helps make this tool better for everyone.

## License
This project is open-sourced under the [MIT License](https://opensource.org/license/MIT). This means you are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, as long as you include the original copyright and permission notice in all copies or substantial portions of the software.

