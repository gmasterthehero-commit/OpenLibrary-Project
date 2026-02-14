import requests
import csv
import time


def get_books_from_api(limit=50):
    url = "https://openlibrary.org/search.json"
    collected = []
    page = 1

    print(f"Collecting {limit} books published after 2000...")

    while len(collected) < limit:
        params = {"q": "fiction", "page": page, "limit": 100}

        response = requests.get(url, params=params, timeout=15)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()
        books = data.get("docs", [])

        if not books:
            break

        for book in books:
            year = book.get("first_publish_year")
            if isinstance(year, int) and year > 2000:
                collected.append(book)

                if len(collected) >= limit:
                    break

        page += 1

    print(f"Collected {len(collected)} books after 2000")
    return collected


def extract_publish_year(book):
    """
    Get the publish year from Search API response

    Args:
        book (dict): Book information dictionary from search.json

    Returns:
        int or None: Year if found, None otherwise
    """

    year = book.get("first_publish_year")

    if year and isinstance(year, int):
        if 1800 <= year <= 2025:
            return year

    return None


def filter_books_by_year(books, min_year=2000):
    """
    Filter books published after year 2000

    Args:
        books (list): List of book dictionaries
        min_year (int): Minimum year to filter by

    Returns:
        list: Filtered list of books
    """
    filtered_books = []
    books_without_year = 0

    for book in books:
        year = extract_publish_year(book)

        if year is None:
            books_without_year += 1
            continue

        if year > min_year:
            book["extracted_year"] = year
            filtered_books.append(book)

    if books_without_year > 0:
        print(f"Note: Could not find publish year for {books_without_year} books")

    return filtered_books


def get_book_authors(book):
    """
    Extract author names

    Args:
        book (dict): Book information

    Returns:
        str: Comma-separated author names or "Unknown"
    """
    authors = book.get("author_name", [])

    if not authors:
        return "Unknown Author"

    return ", ".join(authors) if authors else "Unknown Author"


def save_books_to_csv(books, filename="books_filtered.csv"):
    """
    Save book data to CSV file

    Args:
        books (list): List of book dictionaries
        filename (str): Name of CSV file to create
    """
    if not books:
        print("No books to save!")
        return False

    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "title",
                "authors",
                "publish_year",
                "editions",
                "cover_id",
                "openlibrary_id",
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for book in books:
                row = {
                    "title": book.get("title", "No Title"),
                    "authors": get_book_authors(book),
                    "publish_year": book.get("extracted_year", "Unknown"),
                    "editions": book.get("edition_count", 0),
                    "cover_id": book.get("cover_i", ""),
                    "openlibrary_id": book.get("key", "").replace("/works/", ""),
                }

                writer.writerow(row)

        print(f"Successfully saved {len(books)} books to '{filename}'")
        return True

    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False


def create_sample_file(books, sample_size=10, filename="sample_books.csv"):
    """
    Create a smaller sample file for GitHub

    Args:
        books (list): List of book dictionaries
        sample_size (int): Number of books for sample
        filename (str): Name for sample file
    """
    if not books:
        return False

    sample_books = books[: min(sample_size, len(books))]

    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["title", "authors", "publish_year"]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for book in sample_books:
                row = {
                    "title": book.get("title", "No Title"),
                    "authors": get_book_authors(book),
                    "publish_year": book.get("extracted_year", "Unknown"),
                }

                writer.writerow(row)

        print(f"Created sample file '{filename}' with {len(sample_books)} books")
        return True

    except Exception as e:
        print(f"Error creating sample: {e}")
        return False


def main():
    """Main function to run the script"""
    print("=" * 50)
    print("OpenLibrary Book Fetcher (Search API)")
    print("=" * 50)

    start_time = time.time()

    all_books = get_books_from_api(limit=50)

    if not all_books:
        print("Failed to get books from API. Exiting.")
        return

    filtered_books = filter_books_by_year(all_books, min_year=2000)

    print(f"\nFound {len(filtered_books)} books published after 2000")
    print(f"Out of {len(all_books)} total books fetched")

    if filtered_books:
        save_books_to_csv(filtered_books, "filtered_books.csv")
        create_sample_file(filtered_books, sample_size=10, filename="sample_books.csv")
    else:
        print("\nNo books published after 2000 found.")
        print("Try changing the search query or sorting method.")

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\nScript completed in {elapsed_time:.2f} seconds")
    print("\nFiles created:")
    print(" - filtered_books.csv : All books published after 2000")
    print(" - sample_books.csv : Small sample for GitHub")

    if filtered_books:
        years = [b.get("extracted_year", 0) for b in filtered_books]
        if years:
            avg_year = sum(years) / len(years)
            print(f"\nStatistics:")
            print(f" • Average publication year: {avg_year:.1f}")
            print(f" • Newest book: {max(years)}")
            print(f" • Oldest after 2000: {min(years)}")


if __name__ == "__main__":
    main()
