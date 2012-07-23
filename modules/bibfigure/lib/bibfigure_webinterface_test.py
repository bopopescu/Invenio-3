import unittest
from invenio.testutils import make_test_suite, run_test_suite
from bibfigure_webinterface import WebInterfacePageImages

class WebInterfacePageImagesTest(unittest.TestCase):
    """regression tests about BibRecDocs"""

    def test_getMainPdfData(self):
        p = WebInterfacePageImages()
        p.img_width = 800
        p.recid = 10
        p.page_num = 1
        
        self.assertEqual(len(p._get_main_pdf_data()), 383040, "Loading PDF file data likely failed")
    
    def test_meta_info(self):
        p = WebInterfacePageImages()
        p.img_width = 800
        p.recid = 10
        p.page_num = 1
        print p._meta_info(None, None)
   

TEST_SUITE = make_test_suite(WebInterfacePageImagesTest)
                             

if __name__ == "__main__":
    run_test_suite(TEST_SUITE, warn_user=True)