"""Adaptive Sliding Window"""

# Author: Yuhao ZHAO
from concept_drift.adwin_list import AdwinList
from math import log, sqrt, fabs


class Adwin:
    def __init__(self, delta=0.002, max_buckets=5, min_clock=32, min_length_window=10, min_length_sub_window=5):
        """
        :param delta: confidence value
        :param max_buckets: max number of buckets which have same number of original date in one row
        :param min_clock: min number of new data for starting to reduce window and detect change
        :param min_length_window: min window's length for starting to reduce window and detect change
        :param min_length_sub_window: min sub window's length for starting to reduce window and detect change
        """
        self.delta = delta
        self.max_buckets = max_buckets
        self.min_clock = min_clock
        self.min_length_window = min_length_window
        self.min_length_sub_window = min_length_sub_window
        # time is used for comparison with min_clock parameter
        self.time = 0
        # width of the window
        self.width = 0
        # sum of all values in the window
        self.total = 0.0
        # incremental variance of all values in the window
        self.variance = 0.0
        # number of buckets that held the values
        # this value has the upper limit set by max_buckets
        self.bucket_number = 0
        # last_bucket_row: defines the max number of merged
        self.last_bucket_row = 0
        self.list_row_buckets = AdwinList(self.max_buckets)

    def set_input(self, value):
        """
        Main method for adding a new data value and automatically detect a possible concept drift.
        :param value: new data value
        :return: true if there is a concept drift, otherwise false
        """
        self.time += 1
        # Insert the new element
        self.__insert_element(value)
        # Reduce window
        return self.__reduce_window()

    def __insert_element(self, value):
        """
        Insert a new element by creating a new bucket for the head element of the list. The overall variance and
        total value are updated incrementally. At the end, buckets maybe compressed (merged) if the maximum number of
        buckets has been reached.
        :param value: new data value from the stream
        """
        self.width += 1
        # Insert the new bucket
        self.list_row_buckets.head.insert_bucket(value, 0)
        self.bucket_number += 1
        # Calculate the incremental variance
        incremental_variance = 0
        if self.width > 1:
            incremental_variance = (self.width - 1) * pow(2, (value - self.total / (self.width - 1))) / self.width
        self.variance += incremental_variance
        self.total += value
        # compress (merge) buckets if necessary
        self.__compress_buckets()

    def __compress_buckets(self):
        """Merging two buckets corresponds to creating a new bucket whose size is equal to the sum of the sizes of
        those two buckets. The size of a bucket means how many original data is contained inside it.
        """
        cursor = self.list_row_buckets.head
        i = 0
        while cursor is not None:
            # Find the number of buckets in a row
            k = cursor.bucket_size_row

            # Merge buckets if row is full
            if k == self.max_buckets + 1:
                next_node = cursor.next
                if next_node is None:
                    self.list_row_buckets.add_to_tail()
                    # new list item was added to the list
                    # hence, next pointer has been reset now to this new tail
                    next_node = cursor.next
                    self.last_bucket_row += 1

                n1 = pow(2, i)
                n2 = pow(2, i)

                # consider values from buckets 0 and 1 as these are the heading bucket elements inside a list item
                u1 = cursor.bucket_total[0] / n1
                u2 = cursor.bucket_total[1] / n2

                external_variance = n1 * n2 * (u1 - u2) * (u1 - u2) / (n1 + n2)

                # create and insert a new bucket into the next list item
                new_bucket_total = cursor.bucket_total[0] + cursor.bucket_total[1]
                new_bucket_variance = cursor.bucket_variance[0] + cursor.bucket_variance[1] + external_variance
                next_node.insert_bucket(new_bucket_total, new_bucket_variance)
                self.bucket_number += 1

                # remove 2 buckets from the current list item
                cursor.compress_buckets_row(2)

                # stop if the the max number of buckets does not exceed for the next item list  
                if next_node.bucket_size_row <= self.max_buckets:
                    break
            else:
                break
            cursor = cursor.next
            i += 1

    def __reduce_window(self):
        """
        Detect a change in the distribution and reduce the window if there is a concept drift.
        :return: boolean: whether has changed
        """
        is_changed = False
        if self.time % self.min_clock == 0 and self.width > self.min_length_window:
            is_reduced_width = True
            while is_reduced_width:
                is_reduced_width = False
                is_exit = False
                n0, n1 = 0, self.width
                u0, u1 = 0, self.total

                # start building sub windows from the tail (old entries)
                cursor = self.list_row_buckets.tail
                i = self.last_bucket_row
                while (not is_exit) and (cursor is not None):
                    for k in range(cursor.bucket_size_row):
                        # In case of n1 equals 0
                        if i == 0 and k == cursor.bucket_size_row - 1:
                            is_exit = True
                            break

                        # sub window 0 is growing while sub window 1 is getting smaller
                        n0 += pow(2, i)
                        n1 -= pow(2, i)
                        u0 += cursor.bucket_total[k]
                        u1 -= cursor.bucket_total[k]
                        diff_value = (u0 / n0) - (u1 / n1)

                        # remove old entries iff there is a concept drift and the minimum sub window length is matching
                        if n0 > self.min_length_sub_window + 1 and n1 > self.min_length_sub_window + 1 and \
                                self.__reduce_expression(n0, n1, diff_value):
                            is_reduced_width, is_changed = True, True
                            if self.width > 0:
                                n0 -= self.__delete_element()
                                is_exit = True
                                break
                    cursor = cursor.previous
                    i -= 1
        return is_changed

    def __reduce_expression(self, n0, n1, diff_value):
        """
        Calculate epsilon_cut value and check if difference between the mean values of two sub windows is greater than
        it.
        :param n0: number of elements in sub window 0
        :param n1: number of elements in sub window 1
        :param diff_value: difference of mean values of both sub windows
        :return: true if difference of mean values is higher than epsilon_cut
        """
        # harmonic mean of n0 and n1 (originally: 1 / (1/n0 + 1/n1))
        m = 1 / (n0 - self.min_length_sub_window + 1) + 1 / (n1 - self.min_length_sub_window + 1)
        d = log(2 * log(self.width) / self.delta)
        variance = self.variance / self.width
        epsilon = sqrt(2 * m * variance * d) + 2 / 3 * m * d
        return fabs(diff_value) > epsilon

    def __delete_element(self):
        """
        Remove a bucket from tail of window
        :return: Number of elements to be deleted
        """
        # last list item (the oldest bucket) with the oldest entry at first internal array position
        node = self.list_row_buckets.tail
        deleted_number = pow(2, self.last_bucket_row)
        self.width -= deleted_number
        self.total -= node.bucket_total[0]
        deleted_element_mean = node.bucket_total[0] / deleted_number

        incremental_variance = node.bucket_variance[0] + deleted_number * self.width * \
                                                         pow(2, (deleted_element_mean - self.total / self.width)) / \
                                                         (deleted_number + self.width)
        self.variance -= incremental_variance
        # Delete bucket
        node.compress_buckets_row(1)
        self.bucket_number -= 1
        # if after removing an entry, the bucket becomes empty, remove it from the tail
        if node.bucket_size_row == 0:
            self.list_row_buckets.remove_from_tail()
            self.last_bucket_row -= 1
        return deleted_number
