import numpy as np


class AdwinListItem:
    def __init__(self, max_buckets=5, next=None, previous=None):
        self.max_buckets = max_buckets
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
        """Insert a new bucket
        """
        self.bucket_total[self.bucket_size_row] = value
        self.bucket_variance[self.bucket_size_row] = variance
        self.bucket_size_row += 1

    def compress_buckets_row(self, number_deleted):
        """Remove the bucket
        """
        self.bucket_total[:self.max_buckets - number_deleted + 1] = self.bucket_total[number_deleted:]
        self.bucket_total[self.max_buckets - number_deleted + 1:] = np.zeros(number_deleted)

        self.bucket_variance[:self.max_buckets - number_deleted + 1] = self.bucket_variance[number_deleted:]
        self.bucket_variance[self.max_buckets - number_deleted + 1:] = np.zeros(number_deleted)

        self.bucket_size_row -= number_deleted
