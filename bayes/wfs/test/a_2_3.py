'''
Test Purpose: To verify that a request, other than a GetCapabilities request with the
version number set to one that the server does not claim to support in its
capabilities docuement fails.

Test Method: Review the response to the GetCapabilities request and detemine whhich
request version(s) the server claims to support. Execute one or more WFS requests
with a version that is not in the list of supported version and verify that the server
generates and InvalidParameterValue exception.
'''