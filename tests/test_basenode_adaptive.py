import unittest
import mock

#from common import *
from tests.common import *

import b3

#def get_node(status):
    #stub = NodeStub();
    #stub._execute.return_value = status
    #return stub

epsilon = 1.0E-10   # floating point accuracy spec

class Tnode_suc(b3.BaseNode):
    def tick(self,tick):
        return b3.SUCCESS
    
    
class Tnode_alt(b3.BaseNode):
    def __init__(self):
        super(Tnode_alt,self).__init__()
        self.N=0        
    def tick(self,tick):
        self.N+=1
        if self.N%2==0:
           return b3.SUCCESS
        else:
           return b3.FAILURE
        
class TestBaseNodeAdaptive(unittest.TestCase):
    
    def test_initialization(self):
        #print(' test basenode init')
        node = b3.BaseNode()

    def test_Psucc(self):
        #global epsilon
        #node = b3.BaseNode()
        #node = b3.Succeeder()
        node = Tnode_suc()
        
        node.BHdebug = 0

        nticks = 5
        for i in range(nticks):
            #print ('try tick!')
            r=node._tick(TickStub())          
            #print ('return:', r)
            
        #node.report_stats()

        assert node.N_ticks == len(range(nticks)) , "incorrect tick count"
        
        node = Tnode_alt()
        nticks = 6
        for i in range(nticks):
            #print ('try tick!')
            r=node._tick(TickStub())          
            #print ('return:', r)
            
        #node.report_stats()

        assert node.N_ticks == len(range(nticks)) , "incorrect tick count"
        assert node.N_success == 0.5*len(range(nticks)) , "incorrect success count"
        assert abs(node.prob() - 0.5) < epsilon, "incorrect frequentist probability"
        
        node.p_reset()  # clear the counters
        assert node.N_ticks == 0, "Error clearing data"
        assert node.N_ticks == 0, "Error clearing data"
        assert node.N_success == 0, "Error clearing data"
        assert node.Ps == 0, "Error clearing data"
        assert node.N_tik2 == [0.0,0.0,0.0,0.0], "Error clearing data"
        assert node.N_suc2 == [0.0,0.0,0.0,0.0], "Error clearing data"
 

if __name__ == '__main__':
    unittest.main()

        
        
        
        
