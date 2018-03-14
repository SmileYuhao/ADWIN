## ADWIN:  ADaptive sliding WINdow algorithm

ADWIN is a change detector and estimator that solves in a well-specified way the problem of tracking the average of a stream of bits or real-valued numbers. 

ADWIN keeps a variable-length window of recently seen items, with the property that the window has the maximal length statistically consistent with the hypothesis “there has been no change in the average value inside the window”. More precisely, an older fragment of the window is dropped if and only if there is enough evidence that its average value differs from that of the rest of the window.

```python
class concept_drift.adwin.Adwin
	(delta=0.002, max_buckets=5, min_clock=32, min_length_window=10, min_length_sub_window=5)
```
| Parameters: | |
| ------------- | ------------- |
| delta: | Confidence value |
| max_buckets: | Max number of buckets which have same number of original date in one row |
| min_clock | Min number of new data for starting to reduce window and detect change |
| min\_length\_window | Min window's length for starting to reduce window and detect change |
| min\_length\_sub\_window | Min sub window's length for starting to reduce window and detect change |

**Methods**

```python
set_input(value)
```
> Set input value to the drift detector - ADWIN.

| Parameters: | |
|-------------|------|
| Value: | Input value |

| Return: | |
|-------------|------|
| Boolean | Whether has drift |

**Example**

```python
from concept_drift.adwin import Adwin

adwin = Adwin()
for i in range(1000):
    if adwin.set_input(i):
	print("Here is a drift")
```

## Page-Hinckley Test
The Page-Hinkley test which is a sequential adaptation of the detection of an abrupt change of the average of a Gaussian signal. It allows efficient detection of changes in the normal behaviour of a process which is established by a model.

```python
 class concept_drift.page_hinkley.PageHinkley
 	(delta_=0.005, lambda_=50, alpha_=1 - 0.0001)
```
| Parameters: | |
| ------------- | ------------- |
| delta_: | Magnitude threshold; the minimal absolute value of the amplitude of the jump to be detected |
| lambda_: | Detection threshold |
| alpha_ | Adaption variable for lambda adjustment |

**Methods**

```python
set_input(value)
```
> Set input value to the drift detector - PageHinkley.

| Parameters: | |
|-------------|------|
| Value: | Input value |

| Return: | |
|-------------|------|
| Boolean | Whether has drift |

## Test
 Used the **elecNormNew** dataset;<br>
 Used **GaussianNB** as based classification;<br>
 Used **accuracy_score** as input date for change detector;<br>
 Used the **prequential** evaluation;

<p align="center">
  <img src="image/comparison.png" width="400"/>
</p>

```
GaussianNB :
Mean acc within the window 1000: 0.7289912189511405

Page-Hinkley :
Drift detection: 8
Mean acc within the window 1000: 0.7342849306584686

ADWIN :
Drift detection: 139
Mean acc within the window 1000: 0.7496421003738032
```
