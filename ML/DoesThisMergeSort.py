class Solution(object):
    def MergeSort(self, arr, left, right):
        if left < right:
            mid = (left + right - 1) // 2
            self.MergeSort(arr, left, mid)
            self.MergeSort(arr, mid + 1, right)
            return self._merge(arr, left, mid, right)

    def _merge(self, arr, left, mid, right):

        size1 = mid - left + 1
        size2 = right - mid

        tempArr1 = [0] * size1
        tempArr2 = [0] * size2

        for i in range(size1):
            tempArr1[i] = arr[left + i]
        for j in range(size2):
            tempArr2[j] = arr[mid + 1 + j]

        i = j = 0
        k = left
        while i < size1 and j < size2:
            # give arr[k] its val
            if tempArr1[i] <= tempArr2[j]:
                arr[k] = tempArr1[i]
                i += 1
            else:
                arr[k] = tempArr2[j]
                j += 1
            k += 1

        while i < size1:
            arr[k] = tempArr1[i]
            k += 1
            i += 1
        while j < size2:
            arr[k] = tempArr2[j]
            k += 1
            j += 1

        return arr


# Driver function here!
s = Solution()
array = [1, 1, 7, 6, 5, 2, 3, 4]
print(s.MergeSort(array, 0, len(array)-1))
#print(s._merge(array,0,2,4))

quit()