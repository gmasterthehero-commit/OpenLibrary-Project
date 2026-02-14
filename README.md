# OpenLibrary Book Fetcher

A lightweight Python script that retrieves fiction books from the OpenLibrary Search API, filters books published after a specified year (default: 2000), and exports the results to CSV files with summary statistics.

---

## Overview

This script:

* Fetches books from OpenLibrary
* Filters by minimum publication year
* Extracts authors and key metadata
* Generates basic statistics
* Exports structured CSV files

---

## Installation

```bash
git clone https://github.com/yourusername/openlibrary-book-fetcher.git
cd openlibrary-book-fetcher
pip install requests
```

---

## Usage

```bash
python your_script_name.py
```

The script will automatically fetch, filter, export data, and display summary statistics.

---

## Output Files

**filtered_books.csv**
Full dataset including:

* Title
* Authors
* Publish Year
* Edition Count
* Cover ID
* OpenLibrary Work ID

**sample_books.csv**
Smaller subset containing:

* Title
* Authors
* Publish Year

---

## Configuration

Modify parameters directly in the script:

```python
get_books_from_api(limit=100)
filter_books_by_year(all_books, min_year=2000)
```

To change the search query:

```python
"q": "fiction"
```

---

## API

OpenLibrary Search API
[https://openlibrary.org/search.json](https://openlibrary.org/search.json)

Documentation
[https://openlibrary.org/developers/api](https://openlibrary.org/developers/api)
