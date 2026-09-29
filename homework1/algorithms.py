import time
import random
import sys

sys.setrecursionlimit(20000)

# 정렬 알고리즘

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    merged = []
    l = r = 0
    while l < len(left) and r < len(right):
        if left[l] < right[r]:
            merged.append(left[l])
            l += 1
        else:
            merged.append(right[r])
            r += 1
    merged.extend(left[l:])
    merged.extend(right[r:])
    return merged

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    #최악의 상황 배제.
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def library_sort(arr):
    if not arr: return []
    gap_array = [None] * (len(arr) * 2)
    gap_array[len(gap_array) // 2] = arr[0]

    for val in arr[1:]:
        pos = len(gap_array) - 1
        for i in range(len(gap_array)):
            if gap_array[i] is not None and gap_array[i] > val:
                pos = i
                break

        if gap_array[pos] is None:
            gap_array[pos] = val
        else:
            inserted = False
            for step in range(1, len(gap_array)):
                if pos - step >= 0 and gap_array[pos - step] is None:
                    gap_array[pos - step:pos] = gap_array[pos - step + 1:pos + 1]
                    gap_array[pos] = val
                    inserted = True
                    break
                elif pos + step < len(gap_array) and gap_array[pos + step] is None:
                    gap_array[pos + 1:pos + step + 1] = gap_array[pos:pos + step]
                    gap_array[pos] = val
                    inserted = True
                    break
            if not inserted:
                gap_array.append(val)
    return [x for x in gap_array if x is not None]

class SortPerformanceSimulator:
    def __init__(self):
        self.sizes = [500, 1000, 2000, 4000]
        self.orders = ['random', 'sorted', 'reversed', 'nearly_sorted']
        self.algorithms = {
            'Merge Sort': merge_sort,
            'Quick Sort': quick_sort,
            'Library Sort': library_sort
        }

    #순서대로 완전 랜덤, 이미 정렬 완료, 역정렬, 일부 정렬
    def _generate_data(self, size, order):
        if order == 'random':
            return [random.randint(1, 10000) for _ in range(size)]
        elif order == 'sorted':
            return list(range(1, size + 1))
        elif order == 'reversed':
            return list(range(size, 0, -1))
        elif order == 'nearly_sorted':
            arr = list(range(1, size + 1))
            swaps = max(1, size // 20)
            for _ in range(swaps):
                idx1, idx2 = random.sample(range(size), 2)
                arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
            return arr

    def run_simulation(self):
        print(f"{'Algorithm':<15} | {'Size':<6} | {'Order':<15} | {'Time (ms)':<10}")
        print("-" * 55)

        for algo_name, sort_func in self.algorithms.items():
            for size in self.sizes:
                for order in self.orders:
                    test_data = self._generate_data(size, order)

                    start_time = time.perf_counter()
                    sort_func(test_data.copy())
                    end_time = time.perf_counter()

                    elapsed_ms = (end_time - start_time) * 1000
                    print(f"{algo_name:<15} | {size:<6} | {order:<15} | {elapsed_ms:>8.2f} ms")

if __name__ == '__main__':
    simulator = SortPerformanceSimulator()
    simulator.run_simulation()
