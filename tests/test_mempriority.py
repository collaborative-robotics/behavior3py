import b3
import unittest
#from common import *
from tests.common import *

def get_node(status):
    stub = NodeStub();
    stub._execute.return_value = status
    return stub

class TestMemPriority(unittest.TestCase):
    def test_category(self):
        self.assertEqual(b3.MemPriority.category, b3.COMPOSITE)

    def test_initialization(self):
        node = b3.MemPriority()

        self.assertIsNotNone(node.id)
        self.assertEqual(node.name, 'MemPriority')
        self.assertEqual(node.title, 'MemPriority')
        self.assertIsNotNone(node.description)

    def test_success(self):
        node1 = get_node(b3.FAILURE)
        node2 = get_node(b3.SUCCESS)
        node3 = get_node(b3.SUCCESS)

        mempriority = b3.MemPriority(children=[node1, node2, node3])
        tick = TickStub()
        tick.blackboard.get.return_value = 0
        status = mempriority.tick(tick)

        self.assertEqual(status, b3.SUCCESS)
        self.assertEqual(node1._execute.call_count, 1)
        self.assertEqual(node2._execute.call_count, 1)
        self.assertEqual(node3._execute.call_count, 0)

    def test_failure(self):
        node1 = get_node(b3.FAILURE)
        node2 = get_node(b3.FAILURE)
        node3 = get_node(b3.FAILURE)

        mempriority = b3.MemPriority(children=[node1, node2, node3])
        tick = TickStub()
        tick.blackboard.get.return_value = 0
        status = mempriority.tick(tick)

        self.assertEqual(status, b3.FAILURE)
        self.assertEqual(node1._execute.call_count, 1)
        self.assertEqual(node2._execute.call_count, 1)
        self.assertEqual(node3._execute.call_count, 1)

    def test_running(self):
        node1 = get_node(b3.FAILURE)
        node2 = get_node(b3.FAILURE)
        node3 = get_node(b3.RUNNING)
        node4 = get_node(b3.SUCCESS)

        mempriority = b3.MemPriority(children=[node1, node2, node3, node4])
        tick = TickStub()
        tick.blackboard.get.return_value = 0
        status = mempriority.tick(tick)

        self.assertEqual(status, b3.RUNNING)
        self.assertEqual(node1._execute.call_count, 1)
        self.assertEqual(node2._execute.call_count, 1)
        self.assertEqual(node3._execute.call_count, 1)
        self.assertEqual(node4._execute.call_count, 0)

    def test_error(self):
        node1 = get_node(b3.FAILURE)
        node2 = get_node(b3.FAILURE)
        node3 = get_node(b3.ERROR)
        node4 = get_node(b3.SUCCESS)

        mempriority = b3.MemPriority(children=[node1, node2, node3, node4])
        tick = TickStub()
        tick.blackboard.get.return_value = 0
        status = mempriority.tick(tick)

        self.assertEqual(status, b3.ERROR)
        self.assertEqual(node1._execute.call_count, 1)
        self.assertEqual(node2._execute.call_count, 1)
        self.assertEqual(node3._execute.call_count, 1)
        self.assertEqual(node4._execute.call_count, 0)

    def test_memory(self):
        node1 = get_node(b3.FAILURE)
        node2 = get_node(b3.FAILURE)
        node3 = get_node(b3.RUNNING)
        node4 = get_node(b3.SUCCESS)
        node5 = get_node(b3.FAILURE)

        mempriority = b3.MemPriority(children=[node1, node2, node3, node4, node5])
        mempriority.id = 'node1';
        tick = TickStub()
        tick.blackboard.get.return_value = 0
        status = mempriority._execute(tick)

        expected = [
            mock.call('is_open', True, 'tree1', 'node1'),
            mock.call('running_child', 0, 'tree1', 'node1'),
            mock.call('running_child', 2, 'tree1', 'node1')
        ]
        result = tick.blackboard.set.mock_calls
        self.assertListEqual(result, expected)

    def test_memory_continue(self):
        node1 = get_node(b3.FAILURE)
        node2 = get_node(b3.FAILURE)
        node3 = get_node(b3.FAILURE)
        node4 = get_node(b3.SUCCESS)
        node5 = get_node(b3.FAILURE)

        mempriority = b3.MemPriority(children=[node1, node2, node3, node4, node5])
        mempriority.id = 'node1';
        tick = TickStub()
        tick.blackboard.get.return_value = 2
        status = mempriority._execute(tick)

        expected = [
            mock.call('is_open', False, 'tree1', 'node1'),
        ]
        result = tick.blackboard.set.mock_calls
        self.assertListEqual(result, expected)

        self.assertEqual(node1._execute.call_count, 0)
        self.assertEqual(node2._execute.call_count, 0)
        self.assertEqual(node3._execute.call_count, 1)
        self.assertEqual(node4._execute.call_count, 1)
        self.assertEqual(node5._execute.call_count, 0)



if __name__ == '__main__':
    unittest.main()
