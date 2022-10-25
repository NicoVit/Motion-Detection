 -*- coding: utf-8 -*-
Motion Detection
#Some imports and functions provided by UCSC
"""---"""

import numpy as np

s = [1., 2., 3., 3., 2., 4., 3.]
print("avg:", np.average(s))
print("std:", np.std(s))

import random # We use random to simulate a stream.

def read_stream():
    """Reads and returns one number from the stream."""
    return random.random()

def use(x):
    """Code to do something with x"""
    pass

# Here we accummulate the sequence, so we can average it.
seq = []

while True:
    x = read_stream()

    # We add x to the average
    seq.append(x)
    print("avg:", np.average(seq))
    use(x)

    # This is an example, and I don't what the code to run forever.
    if len(seq) == 10:
        break

class FullAveragerator(object):

    def __init__(self):
        self.seq = []

    def add(self, x):
        self.seq.append(x)

    @property
    def avg(self):
        return np.average(self.seq)

    @property
    def std(self):
        return np.std(self.seq)

averagerator = FullAveragerator()

for _ in range(10):
    x = read_stream()

    # We add x to the average
    averagerator.add(x)
    print("avg:", averagerator.avg)
    use(x)

import matplotlib.pyplot as plt

averagerator = FullAveragerator()

xs = []
smooth_xs = []
for _ in range(200):
    x = read_stream()
    xs.append(x)
    averagerator.add(x)
    smooth_xs.append(averagerator.avg)
plt.plot(xs, label="xs")
plt.plot(smooth_xs, label="smooth xs")
plt.legend()
plt.show()

class EfficientFullAveragerator(object):

    def __init__(self):
        self.sum_x = 0.
        self.n = 0

    def add(self, x):
        self.sum_x += x
        self.n += 1

    @property
    def avg(self):
        return self.sum_x / self.n

class EfficientFullAveragerator(object):

    def __init__(self):
        self.sum_x = 0.
        self.sum_x_sq = 0.
        self.n = 0

    def add(self, x):
        # We compute the sum of the x, to compute their average.
        self.sum_x += x
        # Sum of the x^2, so we can later compute the average of the x^2.
        self.sum_x_sq += x * x
        self.n += 1

    @property
    def avg(self):
        return self.sum_x / self.n

    @property
    def std(self):
        mu = self.avg # To avoid calling self.avg twice.
        return np.sqrt(self.sum_x_sq / self.n - mu * mu)

averagerator = EfficientFullAveragerator()

xs = []
smooth_xs = []
stdevs = []
for _ in range(200):
    x = read_stream()
    xs.append(x)
    averagerator.add(x)
    smooth_xs.append(averagerator.avg)
    stdevs.append(averagerator.std)
plt.plot(xs, label="xs")
plt.plot(smooth_xs, label="smooth xs")
plt.plot(stdevs, label="std")
plt.legend()
plt.show()

def noisy_temp(noise=1., d=0.05):
    t = -d # time
    while True:
        t += d # We increment time.
        yield 15. + 10. * np.sin(t) + noise * 2.  * (random.random() - 0.5)

# Let's show how this looks.
xs = []
for x in noisy_temp():
    xs.append(x)
    if len(xs) == 400:
        break
plt.plot(xs)
plt.show()

def noisy_temp_with_outliers(noise=1., d=0.05, outlier_prob=0.02, outlier_size=10.):
    t = -d # time
    while True:
        t += d # We increment time.
        x = 15. + 10. * np.sin(t) + noise * 2.  * (random.random() - 0.5)
        # Adds the outlier, with a certain probability.
        if random.random() < outlier_prob:
            x += outlier_size * 2. * (random.random() - 0.5)
        yield x

# Let's show how this looks.
xs = []
for x in noisy_temp_with_outliers():
    xs.append(x)
    if len(xs) == 400:
        break
plt.plot(xs)
plt.show()

xs = []
avgs = []
stds = []
a = EfficientFullAveragerator()
for x in noisy_temp_with_outliers():
    xs.append(x)
    a.add(x)
    avgs.append(a.avg)
    stds.append(a.std)
    if len(xs) == 400:
        break
plt.plot(xs, label='x')
plt.plot(avgs, label='average')
# Let's move to numpy to compute average plus and minus standard deviation.
a_avg = np.array(avgs)
a_std = np.array(stds)
plt.plot(a_avg + a_std, label='avg + std', color='g')
plt.plot(a_avg - a_std, label='avg - std', color='g')
plt.legend()
plt.show()

### Question 1: Implement a `SlidingWindowAveragerator`

class SlidingWindowAveragerator(object):

    # YOUR CODE HERE
  def __init__(self, window_size):
    self.size = window_size
    self.hold = []

  def add(self, x):
    if len(self.hold) >= self.size:
      self.hold = self.hold[1:]
      self.hold.append(x)
    else:
      self.hold.append(x)


  @property
  def avg(self):
    num = 0
    for x in self.hold:
      num += x
    return num / len(self.hold)
  
  @property
  def std(self):
    sum = 0
    for x in self.hold:
      sum += abs(x - self.avg) ** 2
    return np.sqrt(sum / len(self.hold))

### 5 points: Tests for `SlidingWindowAveragerator`

# First some simple cases.
sa = SlidingWindowAveragerator(20)
for _ in range(10):
    sa.add(10)
    assert sa.avg == 10
    assert sa.std == 0

sa = SlidingWindowAveragerator(10)
for _ in range(10):
    sa.add(4)
assert sa.avg == 4
for _ in range(10):
    sa.add(8)
assert sa.avg == 8
assert sa.std == 0

# 10 points. Then, for more complex cases.

sa = SlidingWindowAveragerator(10)
for _ in range(10):
    sa.add(1)
    assert sa.avg == 1
    assert sa.std == 0

sa = SlidingWindowAveragerator(4)
for _ in range(4):
    sa.add(3)
assert sa.avg == 3
for _ in range(4):
    sa.add(2)
assert sa.avg == 2
assert sa.std == 0
for _ in range(4):
    sa.add(1)
assert sa.avg == 1
assert sa.std == 0

sa = SlidingWindowAveragerator(4)
for x in range(10):
    sa.add(x)
    if x < 4:
        assert sa.avg == x / 2
    else:
        assert sa.avg == (2 * x - 3) / 2

sa = SlidingWindowAveragerator(5)
for x in range(10):
    sa.add(x)
    if x < 5:
        assert sa.avg == x / 2
    else:
        assert sa.avg == (2 * x - 4) / 2
        assert abs(sa.std - np.sqrt(2)) < 0.001

### 10 points: Now for even more complex tests.

sa = SlidingWindowAveragerator(10)
for i in range(10):
    sa.add(i)
assert sa.avg == 4.5
assert abs(sa.std - 2.87) < 0.1
for i in range(10):
    sa.add(i)
assert sa.avg == 4.5
assert abs(sa.std - 2.87) < 0.1
for _ in range(10):
    sa.add(1)
assert sa.avg == 1
assert sa.std == 0

class DiscountedAveragerator:

    def __init__(self, alpha):
        """Creates an averagerator with a specified discounting factor alpha."""
        self.alpha = alpha
        self.w = 0.
        self.sum_x = 0.
        self.sum_x_sq = 0.

    def add(self, x):
        self.w = self.alpha * self.w + 1.
        self.sum_x = self.alpha * self.sum_x + x
        self.sum_x_sq = self.alpha * self.sum_x_sq + x * x

    @property
    def avg(self):
        return self.sum_x / self.w

    @property
    def std(self):
        mu = self.avg
        # The np.maximum is purely for safety.
        return np.sqrt(np.maximum(0., self.sum_x_sq / self.w - mu * mu))

def noisy_sin(noise=1.):
    d = 0.05 # Time increment.
    t = -d # time
    while True:
        t += d # We increment time.
        yield np.sin(t) + noise * (random.random() - 0.5)


# Let's display it.
xs = []
for x in noisy_sin():
    xs.append(x)
    if len(xs) == 200:
        break
import matplotlib.pyplot as plt
plt.plot(xs)
plt.show()

xs = []
smooth_xs = []
a = DiscountedAveragerator(0.9)
for x in noisy_sin():
    xs.append(x)
    a.add(x)
    smooth_xs.append(a.avg)
    if len(xs) == 200:
        break
import matplotlib.pyplot as plt
plt.plot(xs)
plt.plot(smooth_xs)
plt.show()

xs = []
smooth_xs = []
a = DiscountedAveragerator(0.9)
for x in noisy_sin(noise=0.):
    xs.append(x)
    a.add(x)
    smooth_xs.append(a.avg)
    if len(xs) == 200:
        break
import matplotlib.pyplot as plt
plt.plot(xs)
plt.plot(smooth_xs)
plt.show()

a = DiscountedAveragerator(0.9)

xs = []
avgs = []
stds = []
for x in noisy_temp_with_outliers(d=0.02):
    xs.append(x)
    a.add(x)
    avgs.append(a.avg)
    stds.append(a.std)
    if len(xs) == 400:
        break
plt.plot(xs, label='x')
plt.plot(avgs, label='average')
# Let's move to numpy to compute average plus and minus standard deviation.
a_avg = np.array(avgs)
a_std = np.array(stds)
plt.plot(a_avg + 2. * a_std, label='avg + 2 std', color='g')
plt.plot(a_avg - 2. * a_std, label='avg - 2 std', color='g')
plt.legend()
plt.show()

### Question 2: Implement the `CleanData` class

class CleanData(object):

    def __init__(self, discount_factor):
        """
        @param discount_factor: discount factor for the averagerator.
        """
        # YOUR CODE HERE
        self.hold = DiscountedAveragerator(discount_factor)

    def filter(self, x, num_stdevs=2.):
        """Returns a filtered value for x.
        @param x: the value to be filtered.
        @param num_stdevs: number of standard deviations from the average
           beyond which data is rejected.
        It can be done in 5 lines of code.
        """
        # YOUR CODE HERE
        self.hold.add(x)
        if abs(self.hold.avg - x) > num_stdevs * self.hold.std:
          return self.hold.avg
        return x

a = DiscountedAveragerator(0.9)
xs = []
clean_xs = []
avgs = []
stds = []
cleaner = CleanData(0.9)
for x in noisy_temp_with_outliers(d=0.02):
    xs.append(x)
    a.add(x)
    avgs.append(a.avg)
    stds.append(a.std)
    clean_xs.append(cleaner.filter(x, num_stdevs=2))
    if len(xs) == 400:
        break
plt.plot(xs, label='noisy x')
plt.plot(clean_xs, label='clean x')
# Let's move to numpy to compute average plus and minus standard deviation.
a_avg = np.array(avgs)
a_std = np.array(stds)
plt.plot(a_avg + 2. * a_std, label='avg + 2 std', color='g')
plt.plot(a_avg - 2. * a_std, label='avg - 2 std', color='g')
plt.legend()
plt.show()

### 10 points: Tests for `CleanData`
import numpy as np

a = np.zeros(10)
a[3] = 1
a[8] = 10
c = CleanData(0.9)
aa = [c.filter(x) for x in a]
assert max(aa) < 2.

a = np.zeros(100)
a[13] = 10
a[14] = 10
a[18] = 10
a[50] = 10
c = CleanData(0.95)
aa = [c.filter(x, num_stdevs=2) for x in a]
assert aa[13] < 10
assert 1 < aa[14] < 2
assert aa[18] == 10
assert aa[50] < 10

a = DiscountedAveragerator(0.9)

xs = []
avgs = []
stds = []
for x in noisy_temp_with_outliers(d=0.02):
    xs.append(x)
    if len(xs) >= 20:
        # We need enough data to be able to rely on the statistics.
        a_avg, a_std = a.avg, a.std
        x_min, x_max = a_avg - 2 * a_std, a_avg + 2. * a_std
        if x_min < x < x_max:
            # The data is good.
            a.add(x)
    else:
        # We add all data until we have reliable statistics.
        a.add(x)
    avgs.append(a.avg)
    stds.append(a.std)
    if len(xs) == 400:
        break

plt.plot(xs, label='x')
plt.plot(avgs, label='average')
# Let's move to numpy to compute average plus and minus standard deviation.
a_avg = np.array(avgs)
a_std = np.array(stds)
plt.plot(a_avg + 2. * a_std, label='avg + 2 std', color='g')
plt.plot(a_avg - 2. * a_std, label='avg - 2 std', color='g')
plt.legend()
plt.show()

from PIL import Image
import requests
from zipfile import ZipFile
from io import BytesIO

# Gets the zip file.
ZIP_URL = "https://storage.googleapis.com/lucadealfaro-share/GardenSequence.zip"
r = requests.get(ZIP_URL)
# List of images, represented as numpy arrays.
images_as_arrays = []
# Makes a file object of the result.
with ZipFile(BytesIO(r.content)) as myzip:
    for fn in myzip.namelist():
        with myzip.open(fn) as my_image_file:
            img = Image.open(my_image_file)
            # Converts the image to a numpy matrix, and adds it to the list.
            images_as_arrays.append(np.array(img).astype(np.float32))

print(images_as_arrays[0].shape)

print(images_as_arrays[0][10, 20, 2])

a = np.random.random((4, 5, 3))
b = np.random.random((4, 5, 3))
print("a:", a)
print("b:", b)
print("a > b:", a > b)

a = np.random.random((4, 5)) > 0.7
b = np.random.random((4, 5)) > 0.7
np.logical_or(a, b)

a = np.random.random((4, 5, 3))
aa = a > 0.8
print("aa shape:", aa.shape)
b = np.max(aa, axis=2)
print("b shape:", b.shape)
print("b:", b)

### Question 3: Implement the `MotionDetection` class

class MotionDetection(object):

    def __init__(self, num_sigmas=4., discount=0.96):
        """Motion detection implemented via averagerator.
        @param num_sigmas: by how many standard deviations should a pixel
            differ from the average for motion to be detected.  This is
            the \kappa of the above explanation.
        @param discount: discount factor for the averagerator.
        """
        # YOUR CODE HERE
        self.avg = DiscountedAveragerator(discount)
        self.limit = num_sigmas

    def detect_motion(self, img):
        """Detects motion.
        @param img: an h x w x 3 image.
        @returns: an h x w boolean matrix, indicating where motion occurred.
        A pixel is considered a motion pixel if one of its color bands deviates
        by more than num_sigmas standard deviations from the average."""
        # YOUR CODE HERE
        self.avg.add(img)
        change = np.logical_or((img > (self.avg.avg + self.limit * self.avg.std)), (img < (self.avg.avg - self.limit * self.avg.std)))
        return np.max(change, axis = 2)

def detect_motion(image_list, num_sigmas=4., discount=0.96):
    """Takes as input:
    @param image_list: a list of images, all of the same size.
    @param num_sigmas: a parameter specifying how many standard deviations a
        pixel should be to count as detected motion.
    @param discount: the discount factor for the averagerator.
    """
    detector = MotionDetection(num_sigmas=num_sigmas, discount=discount)
    detected_motion = []
    for i, img in enumerate(image_list):
        motion = detector.detect_motion(img)
        if np.sum(motion) > 500:
            detected_motion.append((i, motion))
    return detected_motion

# Compute the motion detections.
motions = detect_motion(images_as_arrays[:60])

import matplotlib.pyplot as plt
for i, m in motions:
    # We only print images where there are at least 500 pixels of motion.
    if np.sum(m) > 500:
        print("Motion at image", i, ":", np.sum(m), "------------------------------------")
        # We first show the image, for reference.
        plt.imshow(images_as_arrays[i] / 255)
        plt.show()
        # And then the motion detection.
        plt.imshow(m)
        plt.show()

### 20 points: Tests for motion detection

motions = detect_motion(images_as_arrays[:60])
motion_idxs = [i for i, _ in motions]
assert motion_idxs == [1, 10, 47, 48, 49, 57, 58, 59]
assert np.sum(motions[6][1]) == 1199

# 10 points: some more tests.

motions = detect_motion(images_as_arrays)
motion_idxs = [i for i, _ in motions]
assert motion_idxs[:12] == [1, 10, 47, 48, 49, 57, 58, 59, 66, 67, 68, 85]
