#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#

import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    print(dict)
    resp = ''
    message = ''

    secret = {
        "COUCH_URL": "https://apikey-v2-dy6dy1r1snm0d409rdo557qav4b01e3qydv62igbw8w:113627a0d924cddd86b4e8403d27c7bb@d6a353ac-fc1c-4797-8233-9e4d3982ea2d-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY":  "y2ruhs9Upb2bxNIvtmDlBuX_o_uAk_rftSLm97P6Lr6d",
        "COUCH_USERNAME": "apikey-v2-dy6dy1r1snm0d409rdo557qav4b01e3qydv62igbw8w"
    }


    authenticator = IAMAuthenticator(secret['IAM_API_KEY'])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(secret['COUCH_URL'])

    try:
        if not 'dealerId' in dict:
            status_code = 404
            message = "missing dealerId parameter"
        else:
            result = service.post_find(
                db='reviews',
                selector={'dealership': {'$eq': int(dict["dealerId"])}},
            ).get_result()

            if len(result['docs']) == 0:
                status_code = 404
                message = "dealerId does not exist"
            else:
                print(result)
                status_code = 200
                resp = result['docs']

    except Exception as err:
        status_code = 500
        message = "Something went wrong on the server:" + str(err)

    finally:
        return {
            'statusCode': status_code,
            'headers':{'Content-Type':'application/json'},
            'body':  resp,
            'message': message
        }


