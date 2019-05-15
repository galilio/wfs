import unittest
from bayes.wfs.assets import XSD

class TestAssets(unittest.TestCase):
    def test_camel_to_snake(self):
        from bayes.wfs.assets import camel_to_snake

        self.assertEqual(camel_to_snake('OGC_Web_Feature_Service_WFS'), 'ogc_web_feature_service_wfs')
        self.assertEqual(camel_to_snake('expre'), 'expre')
        self.assertEqual(camel_to_snake('filterAll'), 'filter_all')
        self.assertEqual(camel_to_snake('filterCapabilities'), 'filter_capabilities')
        self.assertEqual(camel_to_snake('ReadMeFilter203'), 'read_me_filter203')
        self.assertEqual(camel_to_snake('ResponseHTTPCodeError404'), 'response_http_code_error404')

    def test_assets(self):
        self.assertIn('expr', XSD)
        self.assertIn('filter', XSD)
        self.assertIn('filter_all', XSD)
        self.assertIn('filter_capabilities', XSD)
        self.assertIn('query', XSD)
        self.assertIn('sort', XSD)

    def test_valid_test_filter(self):
        test_filter = '''
        <fes:Filter
            xmlns:fes="http://www.opengis.net/fes/2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/fes/2.0 filterAll.xsd">
            <fes:And>
                <fes:Or>
                    <fes:PropertyIsEqualTo>
                        <fes:ValueReference>FIELD1</fes:ValueReference>
                        <fes:Literal>10</fes:Literal>
                    </fes:PropertyIsEqualTo>
                    <fes:PropertyIsEqualTo>
                        <fes:ValueReference>FIELD1</fes:ValueReference>
                        <fes:Literal>20</fes:Literal>
                    </fes:PropertyIsEqualTo>
                </fes:Or>
                <fes:PropertyIsEqualTo>
                    <fes:ValueReference>STATUS</fes:ValueReference>
                    <fes:Literal>VALID</fes:Literal>
                </fes:PropertyIsEqualTo>
            </fes:And>
        </fes:Filter>
        '''
        XSD['filter_all'].validate(test_filter)
        f = XSD['filter_all'].to_dict(test_filter)
        self.assertEqual(f['fes:And']['fes:Or'][0]['fes:PropertyIsEqualTo'][0]['fes:ValueReference'], 'FIELD1')

if __name__ == '__main__':
    unittest.main()