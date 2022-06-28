/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    console.log(params);
    const secret = {
       "COUCH_URL": "https://apikey-v2-dy6dy1r1snm0d409rdo557qav4b01e3qydv62igbw8w:113627a0d924cddd86b4e8403d27c7bb@d6a353ac-fc1c-4797-8233-9e4d3982ea2d-bluemix.cloudantnosqldb.appdomain.cloud",
       "IAM_API_KEY":  "y2ruhs9Upb2bxNIvtmDlBuX_o_uAk_rftSLm97P6Lr6d",
       "COUCH_USERNAME": "apikey-v2-dy6dy1r1snm0d409rdo557qav4b01e3qydv62igbw8w"
    }
    const authenticator = new IamAuthenticator({ apikey: secret.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
    });
    cloudant.setServiceUrl(secret.COUCH_URL);

    const dbName = 'dealerships';


    try {
        console.log("try")

        if (params.state) {
            console.log("State is " + params.state);

            // https://cloud.ibm.com/apidocs/cloudant?code=node#postfind
            const selector /*: CloudantV1.JsonObject*/ = {
                st: {
                    '$eq': params.state
                }
            };
            let resp = await cloudant.postFind({
                db: dbName,
                selector: selector,
            })

            //console.log(resp.result);
            if (resp.result.docs.length > 0) {
                return {
                    "statusCode": 200,
                    "body": resp.result.docs
                };
            } else {
                return {
                    "statusCode": 404,
                    "body": "The state does not exist"
                };
            }
        } else {
            console.log("No state");
            // https://cloud.ibm.com/apidocs/cloudant?code=node#postalldocs
            let docs = await cloudant.postAllDocs({
                db: dbName,
                includeDocs: true,
            }).then(x => {
                console.log(x.result);
                if (x.result.rows.length > 0) {
                    return x.result.rows.map(x => x.doc);
                }
            });
            if (docs.length > 0) {
                return {
                    "statusCode": 200,
                    "body": docs
                };
            } else {
                return {
                    "statusCode": 404,
                    "body": "The database is empty"
                };
            }
        }
    } catch (error) {
        console.error(error)
        return {
            "statusCode": 500,
            "body": error.toString()
        }
    }
}
/*
const Cloudant = require('@ibm-cloud/cloudant');

async function main(params) {

    console.log(params)
    const secret = {
       "COUCH_URL": "https://apikey-v2-dy6dy1r1snm0d409rdo557qav4b01e3qydv62igbw8w:113627a0d924cddd86b4e8403d27c7bb@d6a353ac-fc1c-4797-8233-9e4d3982ea2d-bluemix.cloudantnosqldb.appdomain.cloud",
       "IAM_API_KEY":  "y2ruhs9Upb2bxNIvtmDlBuX_o_uAk_rftSLm97P6Lr6d",
       "COUCH_USERNAME": "apikey-v2-dy6dy1r1snm0d409rdo557qav4b01e3qydv62igbw8w"
    }

    const cloudant = Cloudant({
        url: secret.COUCH_URL,
        plugins: { iamauth: { iamApiKey: secret.IAM_API_KEY } }
    });


    let status_code = 200;
    let headers = { 'Content-Type': 'application/json' };
    let resp = '';

    if (params.state) {
        try {
            resp = await cloudant.use('dealerships').find({
                "selector": {
                    "st": {
                        "$eq": params.state
                    }
                }
            });

            if (resp.docs.length==0) {
                status_code = 404;
            }

        } catch (error) {
            console.log(error.toString());
            resp = error.description;
            status_code = 500
        }
    }

    else {
        try {
            resp =  await cloudant.use('dealerships').list({ include_docs: true });

            if (resp.rows.length==0) {
                status_code = 404;
            }

        } catch (error) {
            console.log(error.toString());
            resp = error.description;
            status_code = 500
        }
    }

    return {
        statusCode: status_code,
        headers: headers,
        body: resp
    }
}
*/

