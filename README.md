# BrokenLinkFinder 🛠️🔗

![BrokenLinkFinder](https://img.shields.io/badge/BrokenLinkFinder-Python-blue?style=flat&logo=python) ![Version](https://img.shields.io/badge/version-1.0.0-brightgreen) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Overview

Welcome to **BrokenLinkFinder**, a powerful command-line interface (CLI) tool designed for technical SEO audits. This tool allows you to efficiently find and fix broken links, manage site-wide crawls with customizable depth and page limits, and generate detailed JSON reports. Whether you are a web developer, SEO specialist, or a site owner, this tool can help you maintain a healthy website.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Generating Reports](#generating-reports)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Find Broken Links**: Quickly identify broken links on your website.
- **Site-Wide Crawls**: Set depth and page limits for efficient crawling.
- **Detailed Reports**: Generate JSON reports for further analysis.
- **User-Friendly**: Simple command-line interface for easy use.
- **Open Source**: Contribute to the project and enhance its features.

## Installation

To get started with **BrokenLinkFinder**, you need to download the latest release. You can find the releases [here](https://github.com/mamy2008/BrokenLinkFinder/releases). Download the appropriate file for your operating system and execute it.

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/mamy2008/BrokenLinkFinder.git
   cd BrokenLinkFinder
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure everything is set up by running:
   ```bash
   python main.py --help
   ```

## Usage

Using **BrokenLinkFinder** is straightforward. Here’s how to run it:

```bash
python main.py --url <your-website-url> --depth <depth-limit> --pages <page-limit>
```

### Example

To crawl a website with a depth of 2 and a limit of 50 pages:

```bash
python main.py --url https://example.com --depth 2 --pages 50
```

This command will start the crawling process and check for broken links.

## Configuration

You can customize the behavior of **BrokenLinkFinder** by modifying the configuration file. The configuration file is located in the root directory of the project and is named `config.json`.

### Configuration Options

- **url**: The website URL to crawl.
- **depth**: The maximum depth to crawl.
- **pages**: The maximum number of pages to visit.
- **report_format**: Format of the report (JSON or CSV).

### Example Configuration

```json
{
  "url": "https://example.com",
  "depth": 2,
  "pages": 50,
  "report_format": "json"
}
```

## Generating Reports

After running the tool, you can generate detailed reports. The reports will provide information on the status of each link, including whether they are broken or functional.

To generate a report, simply run:

```bash
python main.py --report
```

This will create a `report.json` file in the current directory.

## Contributing

We welcome contributions to **BrokenLinkFinder**! If you want to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/YourFeature`).
6. Open a pull request.

Please ensure that your code adheres to the existing coding standards and includes tests where applicable.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or support, please reach out to the maintainer:

- **Name**: Your Name
- **Email**: your.email@example.com

Feel free to visit the [Releases](https://github.com/mamy2008/BrokenLinkFinder/releases) section for the latest updates and downloads.

## Conclusion

**BrokenLinkFinder** is your go-to tool for maintaining a healthy website. With its simple interface and powerful features, you can easily identify and fix broken links, ensuring a better user experience and improved SEO performance. Download the latest version from the [Releases](https://github.com/mamy2008/BrokenLinkFinder/releases) section and start optimizing your website today!

---

### Topics

- **broken-links**
- **cli**
- **link-checker**
- **python**
- **seo**
- **technical-seo**
- **url-checker**
- **web-crawler**
- **web-scraping**
- **website-auditing**

---

![SEO](https://img.shields.io/badge/SEO%20Tools-Optimized-brightgreen) ![Web Crawler](https://img.shields.io/badge/Web%20Crawler-Fast-orange) ![Link Checker](https://img.shields.io/badge/Link%20Checker-Accurate-red) 

Thank you for using **BrokenLinkFinder**! Happy crawling!