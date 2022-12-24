from operator import itemgetter
import numpy
arr = {
    ("a1",5,6),
    ("a2",1,5),
    ("a3",1,2),
    ("a4",3,5),
    ("a5",6,7),
    ("a6",5,9)  
}
arr = sorted(arr, key=itemgetter(2))
arr = a = numpy.array(arr)
   

def ActivitySelection(start, finish, n):
    j = 0
    print(arr[0])
    for i in range(n):
        if start[i] >= finish[j]:
            print(arr[i])
            j = i

start = arr[:,1]
finish = arr[:,2]
ActivitySelection(start, finish, len(start))

   
