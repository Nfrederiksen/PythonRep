class Solution(object):
    def findKthLargest(self, arr, k):
        left = 0
        right = len(arr) - 1
        while left <= right:
            pivotIndex = self._partition(arr, left, right)
            if pivotIndex == len(arr) - k:
                return arr[pivotIndex]
            elif pivotIndex > len(arr) - k:
                right = pivotIndex - 1
            else:
                left = pivotIndex + 1
        return -1


    def _partition(self,arr, low, high):
        #return pivotIndex
        pivot = arr[high]
        index = low
        for j in range(low, high):
            if arr[j] <= pivot:
                arr[index], arr[j] = arr[j], arr[index]
                index += 1
        arr[index], arr[high] = arr[high], arr[index]
        return index

print(Solution().findKthLargest([1,3,8,5], 3))
# 5
'''
# Real World Quicksort. it's important to recurse on the smaller part, then loop (or tail-recurse, but that's another story) on the larger part.
This way the range of each recursive call is at most half the range of the caller, and the maximum depth is O(log n)

QUICKSORT(A, p, r)
    while p < r
        q = partition(A, p, r)
        if (q-p <= r-q)
            QUICKSORT(A, p, q - 1)
            p = q+1
        else
            QUICKSORT(A, q + 1, r)
            r = q-1
 '''
