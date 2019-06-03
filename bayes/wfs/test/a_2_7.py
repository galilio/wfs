'''
Test Purpose: to verify that the server ignores and unrecognized parameters in a
KVP-encoded request.

Test Method: Generate a selection of valid KVP-encoded requests and add one or more
parameters to the request that are not defined in this international Standard.
Ensure that these additinal parameters are not vendor-specified parameters declared in the serve's
capabilities document. Verify that the server reponds to the request thus ignoring the
additional unrecognized parameters.
'''
