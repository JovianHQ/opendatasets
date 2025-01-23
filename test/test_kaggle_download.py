import os
import unittest


class MyTestCase(unittest.TestCase):
    
    def test_verify_ssl(self):
        import opendatasets as od
        kaggle_dataset_url = r"https://www.kaggle.com/datasets/akashsharma0105/phone-usage-in-india"
        od.download(kaggle_dataset_url, verify_ssl=False)
        exists = os.path.exists("phone-usage-in-india")
        # test
        self.assertEqual(exists, True)
        # cleanup
        import shutil
        shutil.rmtree("phone-usage-in-india")


if __name__ == '__main__':
    unittest.main()
