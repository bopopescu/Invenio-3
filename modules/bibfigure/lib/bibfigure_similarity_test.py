import unittest
from invenio.testutils import make_test_suite, run_test_suite
from bibfigure_similarity import FigureSimilarity

class BoxSimilarityTest(unittest.TestCase):
    """regression tests about BibRecDocs"""

    def test_norm2(self):
        bs = FigureSimilarity()
        self.assertEquals(0, bs.norm2min([(1,1), (2,2)], [(2,2), (1,1)]), "norm2 similarity meassure didnt work")
   

TEST_SUITE = make_test_suite(BoxSimilarityTest)
                             

if __name__ == "__main__":
    run_test_suite(TEST_SUITE, warn_user=True)
