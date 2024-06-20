import time

from backend.scraper.scraper_manager import ScraperManager

if __name__ == "__main__":
    # Record start time
    start_time = time.time()
    manager = ScraperManager(config_path='configs/ime_requests_config.json')
    manager.run_specific_scraper("CategoryGroups")
    # Record end time
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
