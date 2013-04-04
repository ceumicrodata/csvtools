
import unittest
import left_join as m

class Test_join_lists(unittest.TestCase):
    def test_header_index_getter(self):
        header = ['foo', 'bar', 'baz', 'qux']
        fields = ['bar', 'qux', 'foo']
        indices = [1, 3, 0]

        self.assertEqual(m.get_indices(header, fields),
                indices)
        

    def test_correct_header_and_values(self):
        list1 = [['foo','bar','baz'],
            [0,0,0],
            [1,1,1]]

        list2 = [['lorem','foo','bar'],
            [1,0,0],
            [2,0,0]]

        output_list_1 = [['baz', 'foo', 'bar', 'lorem'],
                [0,0,0,1],
                [0,0,0,2],
                [1,1,1,None]]
        output_list_2 = [['baz', 'bar_1', 'foo', 'lorem', 'baz_2'],
                [0,0,0,1,0],
                [0,0,0,2,0],
                [1,1,1,None,None]]
        
        testList_1 = [x for x in m.join_lists(list1, list2, ['foo', 'bar'])]
        testList_2 = [x for x in m.join_lists(list1, list2, ['foo'])]

        self.assertEqual(testList_1,
                output_list_1)
        self.assertEqual(testList_2,
                testList_2)

