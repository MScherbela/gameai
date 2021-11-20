from connectfour_lib import evaluate
import numpy as np
import timeit

def my_naive_clip(input, a, b):
    result = np.zeros(input.shape[0])
    for i in range(input.shape[0]):
        if input[i] < a:
            result[i] = a
        elif input[i] > b:
            result[i] = b
        else:
            result[i] = input[i]
    return result

np.random.seed(0)
state = np.random.randint(0, 2+1, [6,7], dtype=np.int32)
value = evaluate(state)

t = timeit.timeit("evaluate(state, 3, 2)", globals=globals(), number=100_000)
print(t)




# N = 100
# clip_min, clip_max = 0.2, 0.7
# a = np.random.uniform(0, 1, N)
#
# r1 = my_clipping_func(a, clip_min, clip_max)
# r2 = my_naive_clip(a, clip_min, clip_max)
# r3 = np.clip(a, clip_min, clip_max)
#
# assert np.allclose(r1, r2)
# assert np.allclose(r1, r3)
#
# t_cython = timeit.timeit("my_clipping_func(a, clip_min, clip_max)", globals=globals(), number=10_000)
# t_naive = timeit.timeit("my_naive_clip(a, clip_min, clip_max)", globals=globals(), number=10_000)
# t_numpy = timeit.timeit("np.clip(a, clip_min, clip_max)", globals=globals(), number=10_000)
# print(f"Cython: {t_cython:.3f} sec")
# print(f"Naive: {t_naive:.3f} sec")
# print(f"Numpy: {t_numpy:.3f} sec")






