Manipulating big data like 1 billion _(1 billion == 1,000,000,000 == “十亿”, 1 million == 1,000,000 == “百万” which I always forget how to transform back and forth)_ , is quite memory consuming if we just use an array for storing it. We can either divide the file into smaller file and process them accordingly _(ideas like map reduce, will talk about it later in another post)_ or use ‘bitmap’ and ‘hashmap’. In this post, I will focus on the bitmap.

## What is bitmap?

Bitmap is some sort of Array where each element is represented by a bit. Given a value, we use an transform function in order to get the unique index inside the bitmap. Each element inside the bitmap is actually a integer(which is 4 bytes, 32 bits on java compiler). Therefore an integer can represent 32 numbers. In a nutshell, bitmap is some sort of bucket like data structure.

## Why bitmap?

The bitmap is used for sorting and check if a given value is in the given big data collection. It has the following advantage:

* High efficiency: The worst query time complexity is 2N. If the maximum value of the given collection is known, we can have an optimized time complexity with N. (N is the maximum value)
* Less memory consumption: Say the N = 10,000,000, we will only need 10,000,000 / 8(bits) = 1,250,000 bytes which is almost 1.2m of memory to store the value. But if we use an array of integer, we will need 10,000,000 * 4 = 40,000,000 bytes which is almost 40m of memory.

However, to implement the bitmap, we will need to the data collection to contain _unique_ data entry.

## How bitmap work?

As I mentioned before, the bitmap is actually like an array of bucket. Each bucket is actually an integer, a specific data is marked as 1 or 0 on the specific bit of the integer.  
![how bitmap index a specific value](/2017/05/22/Use-bitmap-for-storing-big-data/bitmap.jpg)  
As shown above, the `32` is how many bits an Integer has which is actually depend on the compiler and the platform. I am using Java to implement it, so an Integer actually contains 32 bits.  
Check out my implementation of bitmap sorting [here](https://github.com/pingrunhuang/CodeChallenge/blob/master/src/main/java/DataStructure/BitMap.java)

### [Reference](https://alaindefrance.wordpress.com/2014/09/28/linear-sorting-algorithm-bitmap-sort/)
