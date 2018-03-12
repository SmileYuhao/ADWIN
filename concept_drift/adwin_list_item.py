import numpy as np


class AdwinListItem:
    """
    A list item contains a list (array) of buckets limited to a maximum of buckets as set in '__init__'. As the new
    buckets are added at the end of the internal array, when old entries need to be removed, they are taken from the
    head of this array. Each item has a connection to a previous and next list item.
    """

    def __init__(self, max_buckets=5, next=None, previous=None):
        self.max_buckets = max_buckets
        # current number of buckets in this list item
        self.bucket_size_row = 0

        self.next = next
        # add the 'previous' connection of the following list item to this item
        if next is not None:
            next.previous = self

        self.previous = previous
        # add the 'next' connection of the previous list item to this item
        if previous is not None:
            previous.next = self

        self.bucket_total = np.zeros(self.max_buckets + 1)
        self.bucket_variance = np.zeros(self.max_buckets + 1)

    def insert_bucket(self, value, variance):
        """
        Insert a new bucket at the end of the array.
        """
        self.bucket_total[self.bucket_size_row] = value
        self.bucket_variance[self.bucket_size_row] = variance
        self.bucket_size_row += 1

    def compress_buckets_row(self, number_deleted):
        """
        Remove the 'number_deleted' buckets as they are the oldest ones.
        """
        delete_index = self.max_buckets - number_deleted + 1
        self.bucket_total[:delete_index] = self.bucket_total[number_deleted:]
        self.bucket_total[delete_index:] = np.zeros(number_deleted)

        self.bucket_variance[:delete_index] = self.bucket_variance[number_deleted:]
        self.bucket_variance[delete_index:] = np.zeros(number_deleted)

        self.bucket_size_row -= number_deleted
