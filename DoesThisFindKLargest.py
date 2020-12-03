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