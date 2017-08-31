![Graph 1](/2017/06/20/Support-vector-machine/svm.png "Graph 1")

v is the point to be classified.  
w is a vector points to the hyperplane perpendicularly.  
The hyperplane is: `w * v + b`

There are 2 classes which are black and red respectively.

if w _v + b > 0, then the v belongs to black  
if w_ v + b < 0, then the v belongs to red  
if w * v + v = 0, then the v is on the decision boundary which is also the hyperplane.

In order to get the value of w and b, we use the following constraint:  
if v belongs to black, then w _v + b = 1  
if v belongs to red, then x_ v + b = -1

Also, we can transform the label to y1 = 1 and y2 = -1 which goes to the next equation:  
`y * (w * v + b) = 1 ==> y * (w * v + b) - 1 = 0`  
If the target point satisfy the equation above, we say it is right classified.

### [](#Process "Process")Process

The basic ideas to get the best separating hyperplane is to first find the margins for each class.

Let a point in the black class (x1, y1)  
Let a point in the red class (x2, y2)  
`Width = (x1 - x2) * w/|w| = x1 * w/|w| - x2 * w/|w|`  
from `y * (w * v + b) - 1 = 0` we get

1.  `w * x = 1 - b` if x belongs to black class since y = 1
2.  `w * x = b - 1` if x belongs to red class since y = -1  
    **So**, `Width = 2 / |w|`  
    Our goal is to maximize the width in order to get the best separating hyperplane. One thing to notice here, the reason why it is called support vector machine is because each newly added training point will affect the result of the hyperplane. So by maximizing the width of the margins, we get the middle plane in the middle to be the hyperplane which makes sense. Every time we add a new training point, it will affect the result of the hyperplane.

In order to maximize the width, we need to minimize the |w| which also means we need to minimize `1/2 * pow(|w|)`. By doing so, we can transform the optimization target into optimizing a quadratic problem which is more easy to solve.  
According to lagarange, `L(w,b) = 1/2 * pow(|w|) - sum(alpha[i] * (y[i] * (v[i] + b) -1))`

### [](#Convex-optimization "Convex optimization")Convex optimization

For dealing with the optimization problem, python provide some library to achieve that. Including:

1.  `cvxopt`
2.  `libsvm`
3.  `sklearn`