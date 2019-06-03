#-*- encoding: utf-8
'''
Test Purpose: Verify that the server implements the Basic
WFS conformance class.

Test Method: Verify that the server implements the Simple WFS
Conformance class. Verify in the capabilities document that
the server includes the operations GetPropertyValue and GetFeature.
Verify the operation of the GetPropertyValue and GetFeature operation
with the stored query action. Verify That the server implements
at least the Minimum Spatial Filter conformance class for ISO 19143.

Simple WFS Conformance class: Sumit requests to the server and verify the following:
the capabilities document that the server generates includes the operations
GetCapabilities, DescribeFeatureType, ListStoredQueries, DescribeStoredQueries,
and GetFeature with the stored query GetFeatureById;
'''