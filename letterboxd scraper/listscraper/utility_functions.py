# Some utility functions are stored here
import requests
import time
import random

def stars2val(stars, not_found):
    """
    Transforms star rating into float value.
    """
    
    conv_dict = {
        "★": 1.0,
        "★★": 2.0,
        "★★★": 3.0,
        "★★★★": 4.0,
        "★★★★★": 5.0,
        "½": 0.5,
        "★½": 1.5,
        "★★½": 2.5,
        "★★★½": 3.5,
        "★★★★½": 4.5 }

    try:
        val = conv_dict[stars]
        return val
    except:
        return not_found
    
def val2stars(val, not_found):
    """
    Transforms float value into star string.
    """
    conv_dict = {
        1.0 : "★",
        2.0 : "★★",
        3.0 : "★★★",
        4.0 : "★★★★",
        5.0 : "★★★★★",
        0.5 : "½",
        1.5 : "★½",
        2.5 : "★★½",
        3.5 : "★★★½",
        4.5 : "★★★★½" }
    try:
        stars = conv_dict[val]
        return stars
    except:
        return not_found

def repeated_request(url):
    """
    Makes a request to a URL with a backoff for 429 errors.

    Parameters:
        url (str): The URL to make a request to.

    Returns:
        requests.Response: The successful response object.

    Raises:
        requests.exceptions.RequestException: If the request fails after all retries.
    """
    retry_seconds = [5,45,120]
    retry_index = 0

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    }

    while retry_index < len(retry_seconds):
        try:
            response = requests.get(url, headers=headers)
            
            # Wait a random amount of seconds, with an average of .75 seconds
            wait_time = random.gauss(mu=0.75, sigma=0.08)
            time.sleep(wait_time)
            
            # Check for a 429 "Too Many Requests" error
            if response.status_code == 429:
                current_delay = retry_seconds[retry_index]
                print(f"Received 429 response. Retrying in {current_delay} seconds...")
                time.sleep(current_delay)
                retry_index += 1
                
                continue  # Skip to the next iteration of the while loop
            
            # If the request is successful, or another error occurs, break the loop
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during request: {e}")
            if retry_index < len(retry_seconds):
                current_delay = retry_seconds[retry_index]
                print(f"Retrying in {current_delay} seconds...")
                time.sleep(current_delay)
                retry_index += 1
            else:
                print("Max retries exceeded. Giving up.")
                raise # Re-raise the last exception

    print(f"Request failed after all retries. Server status code: {response.status_code}")
    raise requests.exceptions.RequestException(f"Request failed after all retries. Server status code: {response.status_code}")