'''
Created on Feb 10, 2011

@author: vgapeyev
'''

from obsparser.churner import churn

if __name__ == '__main__':
    src_dir = "zprod_data/inputs"
    dest_dir = "zprod_data/outputs"
    work_dir = "zprod_data/work"
    print ("In PRODUCTION")
    churn(src_dir, dest_dir, work_dir)
