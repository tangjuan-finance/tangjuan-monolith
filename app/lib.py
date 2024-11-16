import hashlib
import hmac
# def verify_signature(payload_body, secret_token, signature_header):
#     """Verify that the payload was sent from GitHub by validating SHA256.

#     Raise and return 403 if not authorized.

#     Args:
#         payload_body: original request body to verify (request.body())
#         secret_token: GitHub app webhook token (WEBHOOK_SECRET)
#         signature_header: header received from GitHub (x-hub-signature-256)
#     """
#     if not signature_header:
#         raise HTTPException(status_code=403, detail="x-hub-signature-256 header is missing!")
#     hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
#     expected_signature = "sha256=" + hash_object.hexdigest()
#     if not hmac.compare_digest(expected_signature, signature_header):
#         raise HTTPException(status_code=403, detail="Request signatures didn't match!")

def is_valid_signature(x_hub_signature, data, private_key):
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)