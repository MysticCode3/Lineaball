import random
import time

def random_list(length):
    l = [random.randint(-50, 9999) for i in range(length)]
    return l

def selection_sort(target_list):
    for start_i in range(len(target_list)):
        lowest_i = start_i

        # Finds smallest value that occurs after start_i
        for check_i in range(start_i + 1, len(target_list)):
            if target_list[check_i] < target_list[lowest_i]:
                lowest_i = check_i

        # Swap the lowest and start value
        target_list[start_i], target_list[lowest_i] = target_list[lowest_i], target_list[start_i]

    return target_list

def selection_sort_fast(target_list):
    for start_i in range(len(target_list)):
        check_list = target_list[start_i:]
        lowest_i = check_list.index(min(check_list)) + start_i
        target_list[start_i], target_list[lowest_i] = target_list[lowest_i], target_list[start_i]
    return target_list

start_time = time.time()
l = random_list(1000000)
print(l)
#print(selection_sort(l))
print(selection_sort_fast(l))
#l.sort()
#print(l)
print("--- %s seconds ---" % round(time.time() - start_time, 5))