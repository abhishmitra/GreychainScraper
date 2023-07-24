import unittest
from worker import *

class TestExtractChildUrls(unittest.TestCase):
    def test_extract_child_urls(self):
        # Define a sample URL and its corresponding HTML content.
        sample_url = "https://example.com"
        sample_content = """
        <html>
        <body>
            <a href="https://example.com/page1">Page 1</a>
            <a href="https://example.com/page2">Page 2</a>
            <a href="https://example.com/page3">Page 3</a>
            <a href="https://example.com/page1">Page 1 (duplicate)</a>
            <a href="https://example.com/page4">Page 4</a>
        </body>
        </html>
        """

        # Call the extract_child_urls function with the sample URL and content.
        child_urls = extract_child_urls(sample_url, sample_content)

        # Define the expected list of child URLs.
        expected_urls = [
            "https://example.com/page1",
            "https://example.com/page2",
            "https://example.com/page3",
            "https://example.com/page4",
        ]

        # Assert that the returned child URLs match the expected URLs.
        print(child_urls)
        print(expected_urls)

        self.assertCountEqual(child_urls, expected_urls)


if __name__ == '__main__':
    unittest.main()