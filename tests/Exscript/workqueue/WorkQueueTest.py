import sys, unittest, re, os.path, threading, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from Exscript.workqueue import WorkQueue, Action, Sequence
from ActionTest         import TestAction

class WorkQueueTest(unittest.TestCase):
    CORRELATE = WorkQueue

    def setUp(self):
        self.wq = WorkQueue()

    def testConstructor(self):
        self.assertEqual(1, self.wq.get_max_threads())
        self.assertEqual(0, self.wq.debug)

    def testSetDebug(self):
        self.assertEqual(0, self.wq.debug)
        self.wq.set_debug(2)
        self.assertEqual(2, self.wq.debug)

    def testGetMaxThreads(self):
        self.assertEqual(1, self.wq.get_max_threads())
        self.wq.set_max_threads(9)
        self.assertEqual(9, self.wq.get_max_threads())

    def testSetMaxThreads(self):
        self.testGetMaxThreads()

    def testEnqueue(self):
        self.assertEqual(0, self.wq.get_length())
        self.wq.enqueue(Action())
        self.assertEqual(1, self.wq.get_length())
        self.wq.enqueue(Action())
        self.assertEqual(2, self.wq.get_length())
        self.wq.shutdown()
        self.assertEqual(0, self.wq.get_length())

        # Enqueue 111 * 3 = 333 actions.
        lock = threading.Lock()
        data = {}
        for i in range(111):
            actions  = [TestAction(lock, data),
                        TestAction(lock, data),
                        TestAction(lock, data)]
            sequence = Sequence(actions = actions)
            self.wq.enqueue(sequence)
        self.assertEqual(111, self.wq.get_length())

        # Run them, using 50 threads in parallel.
        self.wq.set_max_threads(50)
        self.wq.unpause()
        self.wq.wait_until_done()
        self.wq.pause()

        # Check whether each has run successfully.
        self.assertEqual(0,   self.wq.get_length())
        self.assertEqual(333, data['sum'])
        self.wq.shutdown()
        self.assertEqual(0, self.wq.get_length())

    def testPriorityEnqueue(self):
        # Well, this test sucks.
        self.assertEqual(0, self.wq.get_length())
        self.wq.priority_enqueue(Action())
        self.assertEqual(1, self.wq.get_length())
        self.wq.priority_enqueue(Action())
        self.assertEqual(2, self.wq.get_length())

    def testPause(self):
        pass # See testEnqueue()

    def testUnpause(self):
        pass # See testEnqueue()

    def testWaitUntilDone(self):
        pass # See testEnqueue()

    def testShutdown(self):
        pass # See testEnqueue()

    def testIsPaused(self):
        self.assert_(self.wq.is_paused())
        self.wq.pause()
        self.assert_(self.wq.is_paused())
        self.wq.unpause()
        self.failIf(self.wq.is_paused())
        self.wq.pause()
        self.assert_(self.wq.is_paused())

    def testInQueue(self):
        action1 = Action()
        action2 = Action()
        self.failIf(self.wq.in_queue(action1))
        self.failIf(self.wq.in_queue(action2))

        self.wq.enqueue(action1)
        self.assert_(self.wq.in_queue(action1))
        self.failIf(self.wq.in_queue(action2))

        self.wq.enqueue(action2)
        self.assert_(self.wq.in_queue(action1))
        self.assert_(self.wq.in_queue(action2))

        self.wq.shutdown()
        self.failIf(self.wq.in_queue(action1))
        self.failIf(self.wq.in_queue(action2))

    def testGetLength(self):
        pass # See testEnqueue()

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(WorkQueueTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity = 2).run(suite())
