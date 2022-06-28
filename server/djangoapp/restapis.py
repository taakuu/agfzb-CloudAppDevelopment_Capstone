#import requests
#import json
## import related models here
#from requests.auth import HTTPBasicAuth
#

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



import requests
import json
# import related models here
from .models import CarDealer, DealerReview
# from requests.auth import HTTPBasicAuth

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions

base_url = "https://4da3c77e.eu-gb.apigw.appdomain.cloud/api/dealership"

# from dataclasses import asdict

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    # api_key = kwargs.get('api_key')
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters

        # if api_key:
        #     params = dict()
        #     params["text"] = kwargs["text"]
        #     params["version"] = kwargs["version"]
        #     params["features"] = kwargs["features"]
        #     params["language"] = kwargs["language"]
        #     params["return_analyzed_text"] = kwargs["return_analyzed_text"]
        #     response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
        #                                         auth=HTTPBasicAuth('apikey', api_key))
        # else:
        # no authentication GET
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except Exception as err:
        # If any error occurs
        print(f"Network exception occurred: {err}")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        resp = requests.post(url, params=kwargs, json=json_payload)
    except Exception as err:
        # If any error occurs
        print(f"Network exception occurred: {err}")

    status_code = resp.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(resp.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(dealer_id=None):
    url = "https://4da3c77e.eu-gb.apigw.appdomain.cloud/api/dealership"
    results = []
    # Call get_request with a URL parameter
    if dealer_id:
        json_result = get_request(url, did=dealer_id)
        return json_result["body"]["docs"][0]
    else:
        json_result = get_request(url)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]["rows"]

        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            
            
            results.append(dealer_obj)

    return results

# def get_dealers_by_state(url, **kwargs):
#     results = []
#     # Call get_request with a URL parameter
#     json_result = get_request(url, state)
#     if json_result:
#         # Get the row list in JSON as dealers
#         dealers = json_result["body"]["rows"]
#         # For each dealer object
#         for dealer in dealers:
#             # Get its content in `doc` object
#             dealer_doc = dealer["doc"]
#             # Create a CarDealer object with values in `doc` object
#             dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
#                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
#                                    short_name=dealer_doc["short_name"],
#                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
#             results.append(dealer_obj)

#     return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(dealer_id):
    url = "https://4da3c77e.eu-gb.apigw.appdomain.cloud/api/review"
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        # print(json_result)
        reviews = json_result["body"]["docs"]
        for review in reviews:
            print(review)
            # print
            review_obj = DealerReview(**review)
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
            # print(review_obj.sentiment)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(text):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/a2a97c28-23cf-43f9-956c-8d36336c8c3a"

    api_key = "WLp5K0Xffid5Alc870t8o2VN-MvzeBwq9M57lMfktfbM"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text, language='en',features=Features(sentiment=SentimentOptions(targets=[text]))).get_result()
    label = json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    

    # resp = get_request(url=url, api_key=api_key, text=text, language='en',
    #                 return_analyzed_text=False, version='2021-08-01',
    #                 features=Features(sentiment=SentimentOptions(targets=[text]))
    # )
    
    # print(resp)

    # label = json.dumps(resp, indent=2)
    # label = resp['sentiment']['document']['label']

    return (label)

