'''
Test Purpose: To verify that the order and case of parameters in KVP-encoded
requests does not affect the response.

Test Method: Pick a selection of KVP-encoded requests and invoke them with the
parameters specified in different order each time and with the mixed-case parameter
names. Verify that the server's response is unaffected in each case.
'''