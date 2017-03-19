def ChoosePivot(list):
    return list[0]

def Partition(A,left,right):
    p = ChoosePivot(A)
    i = left + 1

    for j in range(left + 1,right + 1): #upto right + 1 because of range()
        if A[j] < p:
                A[j], A[i] = A[i], A[j] #swap
                i = i + 1
    A[left], A[i - 1] = A[i-1], A[left] #swap
    return i - 1

def QuickSort(list,left, right):
    if len(list) == 1: return
    if left < right:
        pivot = Partition(list,left,right)
        QuickSort(list,left, pivot - 1)
        QuickSort(list,pivot + 1, right)
        return list[:pivot] + [list[pivot]] + list[pivot+1:]
