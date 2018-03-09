"""Add new bucket at head of window (which has smaller number of merged),
remove old bucket from tail of window (which has bigger number of merged)
"""
from concept_drift.adwin_list_item import AdwinListItem


class AdwinList:
    def __init__(self, max_buckets=5):
        """
        :param max_buckets:max number of element in each bucket
        """
        self.count = 0
        self.max_buckets = max_buckets
        self.head = None
        self.tail = None
        self.add_to_head()

    def add_to_head(self):
        """Add the object at the beginning of the window
        """
        # TODO: this code is only called once in init. Should it be removed and hence also shortened as we do not need to check for self.tail is None (it is always the case!)?
        self.head = AdwinListItem(self.max_buckets, next=self.head)
        if self.tail is None:
            self.tail = self.head
        self.count += 1

    def add_to_tail(self):
        """Add the object at the end of the window
        """
        self.tail = AdwinListItem(self.max_buckets, previous=self.tail)
        if self.head is None:
            self.head = self.tail
        self.count += 1

    def remove_from_tail(self):
        """Remove the last object in the window
        """
        self.tail = self.tail.previous
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
        self.count -= 1
