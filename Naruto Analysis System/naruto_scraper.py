import scrapy
from bs4 import BeautifulSoup

class WorkingNarutoSpider(scrapy.Spider):
    name = 'workingnaruto'
    
    def start_requests(self):
        # Use the cookies from your cURL command
        cookies = {
            'sessionId': '995b21a6-1e46-4054-801d-a6184bba41b8',
            'fandom_session': 'MTc1OTUxMTI0MXxqMWxpbGFiM1p5MDF3S19zaTVtVWE2X3lTQWlMZ2tCaE84X3hlQ0JIdFgwWHY5TDlUWjQtUGxvTVMxNkdSdnFFcFJVVEdldXVHQjR6V05reWN3d3M2YUNqYjJSMWZ4ZDRXSDlnTk9LY2tLMkZrWFRsY3VfTk53dUNEeVFtanJSRjlhOW0xNkkzVnd2cHhDaVo3YmVYSGIwSXI3ZlFSLTN4Q0RhMmQtdFNreWN3ZmVad1ZmcVZiMFJnSjFoeGtCWm9yeEE1ZmlIQmpuRnhRYjh5VFBkZDFibU9YdFU0bXlhdUJuT0xTd3puRnNMVnBTZUc2U2g2dlJDOXFXb192Zm1GTmtrODBiRGRUVWtYWllrMlNOYTl8unJLwNJ6nKKRYX15K43R1Adscuj-26yz8P4WGXNkK2o=',
            'wikia_session_id': 'BFdqLXz4zm',
            'fandom_global_id': 'b618d336-3258-4398-a203-c33d15edcb79',
        }
        
        self.logger.info("Using session cookies for authentication")
        
        yield scrapy.Request(
            'https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu',
            cookies=cookies,
            callback=self.parse_jutsu_list,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
            }
        )

    def parse_jutsu_list(self, response):
        self.logger.info(f"Status: {response.status}")
        self.logger.info(f"Title: {response.css('title::text').get()}")
        
        # Check if we have access
        if response.css('.smw-columnlist-container'):
            self.logger.info("✓ SUCCESS: Can access protected content with session cookies!")
            
            jutsu_links = response.css('.smw-columnlist-container')[0].css("a::attr(href)").extract()
            self.logger.info(f"Found {len(jutsu_links)} jutsu links")
            
            # Process first 3 jutsu to test
            for i, href in enumerate(jutsu_links):
                self.logger.info(f"Processing jutsu {i+1}: {href}")
                yield scrapy.Request(
                    "https://naruto.fandom.com" + href,
                    callback=self.parse_jutsu,
                    cookies=self.get_cookies()  # Pass cookies to subsequent requests
                )
            
            # Handle pagination
            next_page = response.css('a.mw-nextlink::attr(href)').get()
            if next_page:
                self.logger.info(f"Found next page: {next_page}")
                yield response.follow(
                    next_page, 
                    self.parse_jutsu_list,
                    cookies=self.get_cookies()
                )
        else:
            self.logger.error("✗ FAILED: Cannot access content")
            # Save the response for debugging
            with open('debug_response.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            self.logger.info("Saved response to 'debug_response.html' for analysis")

    def get_cookies(self):
        """Helper method to get cookies for subsequent requests"""
        return {
            'sessionId': '995b21a6-1e46-4054-801d-a6184bba41b8',
            'fandom_session': 'MTc1OTUxMTI0MXxqMWxpbGFiM1p5MDF3S19zaTVtVWE2X3lTQWlMZ2tCaE84X3hlQ0JIdFgwWHY5TDlUWjQtUGxvTVMxNkdSdnFFcFJVVEdldXVHQjR6V05reWN3d3M2YUNqYjJSMWZ4ZDRXSDlnTk9LY2tLMkZrWFRsY3VfTk53dUNEeVFtanJSRjlhOW0xNkkzVnd2cHhDaVo3YmVYSGIwSXI3ZlFSLTN4Q0RhMmQtdFNreWN3ZmVad1ZmcVZiMFJnSjFoeGtCWm9yeEE1ZmlIQmpuRnhRYjh5VFBkZDFibU9YdFU0bXlhdUJuT0xTd3puRnNMVnBTZUc2U2g2dlJDOXFXb192Zm1GTmtrODBiRGRUVWtYWllrMlNOYTl8unJLwNJ6nKKRYX15K43R1Adscuj-26yz8P4WGXNkK2o=',
            'wikia_session_id': 'BFdqLXz4zm',
        }

    def parse_jutsu(self, response):
        self.logger.info(f"Processing jutsu page: {response.url}")
        
        try:
            jutsu_name = response.css("span.mw-page-title-main::text").get()
            if jutsu_name:
                jutsu_name = jutsu_name.strip()
            else:
                jutsu_name = "Unknown"
                self.logger.warning("Could not find jutsu name")

            div_selector = response.css("div.mw-parser-output")
            if not div_selector:
                self.logger.warning("Could not find content div")
                return
                
            div_html = div_selector[0].extract()
            soup = BeautifulSoup(div_html, 'html.parser').find('div')

            jutsu_type = ""
            if soup and soup.find('aside'):
                aside = soup.find('aside')
                for cell in aside.find_all('div', {'class': 'pi-data'}):
                    if cell.find('h3'):
                        cell_name = cell.find('h3').text.strip()
                        if cell_name == "Classification":
                            jutsu_type = cell.find('div').text.strip()

            # Remove aside if it exists
            if soup and soup.find('aside'):
                soup.find('aside').decompose()

            jutsu_description = soup.text.strip() if soup else "No description available"
            jutsu_description = jutsu_description.split('Trivia')[0].strip()

            yield {
                'jutsu_name': jutsu_name,
                'jutsu_type': jutsu_type,
                'jutsu_description': jutsu_description,
                'url': response.url
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing jutsu: {e}")