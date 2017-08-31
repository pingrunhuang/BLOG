HBase is an open source distributed database built on top of hadoop eco-system. It is becoming a popular choice for application who need fast and random access to large amount of data. In this post, I want to explain my summary on reading the paper written by Amandeep khurana on explaining the design of HBase architecture. In hadoop, HBASE has components called Master and regionserver.

* * *

### [](#HBase-data-model "HBase data model")HBase data model

* * *

1.  _Table_ : data are stored into tables whose names are strings and composed with characters that are safe for use in a file system path.
2.  _Row_ : each row is a data entry identified with row keys (like the primary key in relational database). Row keys have no data type and are treated as a byte[] (byte array).
3.  _Column Family_ : data within a row are grouped by column family. It should be defined up front since this will impact the physical arrangement of how data are stored in HBase.  
    `Question: why do you think it is necessary to have column family? I think`
4.  _Column qualifier_ : Data within a column family is addressed via its column quali er, or simply, column. Need not defined up front since it is `dynamic`. Like Row keys, they are treated as byte[].
5.  _Cell_ : where data are actually stored. It is treated as byte[] too.
6.  _Time stamp_ : each cell are versioned with timestamp which is the time when the value is inserted by default.

![How the concepts above are actually mapped to the real table](/2017/04/01/Design-of-Hbase-architecture/1.jpg "How the concepts above are actually mapped to the real table")

##### [](#From-the-view-of-key-value "From the view of key-value:")From the view of key-value:

<figure class="highlight">

<table>

<tbody>

<tr>

<td class="gutter">

<pre>

<div class="line">1</div>

<div class="line">2</div>

<div class="line">3</div>

<div class="line">4</div>

<div class="line">5</div>

<div class="line">6</div>

<div class="line">7</div>

<div class="line">8</div>

<div class="line">9</div>

<div class="line">10</div>

<div class="line">11</div>

<div class="line">12</div>

<div class="line">13</div>

<div class="line">14</div>

</pre>

</td>

<td class="code">

<pre>

<div class="line">{</div>

<div class="line">  001:</div>

<div class="line">  {</div>

<div class="line">    personal:</div>

<div class="line">    {</div>

<div class="line">      Name:</div>

<div class="line">      {</div>

<div class="line">        Timestamp1:tom,</div>

<div class="line">        Timestage2:allen</div>

<div class="line">      }</div>

<div class="line">    }</div>

<div class="line">    ...</div>

<div class="line">  }</div>

<div class="line">}</div>

</pre>

</td>

</tr>

</tbody>

</table>

</figure>

Actually, the key of an entry in the table is formed by [row key, column family, column qualifier, timestamp] and key is the content of the cell. So to get the value of the name in the cell, you will go through the following process:  
`001 -> Personal -> Name -> Timestamp1 : tom`  
If you left out the timestamp1, the return value will be a dictionary with 2 version of name:  
`001 -> Personal -> Name : {Timestamp1 : tom,Timestamp1 : allen`  
Following the same rule, the returned value will be possibly the following one:  
`001 : {Personal : {Name : {Timestamp1 : tom,Timestamp1 : allen } }` .etc

* * *

### [](#HBase-table-design "HBase table design")HBase table design

* * *

Several questions have been asked to design an HBase table. To do so, one have to consider the following questions:

1.  What should the row key structure be and what should it contain?
2.  How many column families should the table have?
3.  What data goes into what column family?
4.  How many columns are in each column family?
5.  What should the column names be? Although column names don’t need to be de ned on table creation, you need to know them when you write or read data
6.  What information should go into the cells?
7.  How many versions should be stored for each cell?

To answer the questions above, the following features of HBase should be noticed:

1.  Indexing is only done based on the Key.
2.  Tables are stored sorted based on the row key. Each region in the table is responsible for a part of the row key space and is identified by the start and end row key. The region contains a sorted list of rows from the start key to the end key.
3.  Everything in HBase tables is stored as a byte[]. There are no types.
4.  Atomicity is guaranteed only at a row level. There is no atomicity guarantee across rows, which means that _there are no multi-row transactions_.
5.  Column families have to be defined up front at table creation time.(Not changeable)
6.  _Column qualifiers are dynamic and can be defined at write time_. They are stored  
    as byte[] so you can even put data in them.

* * *

### [](#Paper-Summary "Paper Summary")Paper Summary

* * *

Inside the paper, the author also provided an example of how to design a Follows-following relationship using HBase to demonstrate how to combine the knowledge that we talk about above. I will leave a link below just in case you are interested on it.

* * *

# [](#In-reality "In reality")In reality

This section will talk about HBase key concept in production.

* * *

### [](#Column-family "Column family")Column family

* * *

ColumnFamily is the storing unit of a Region. One region contains multiple ColumnFamilies which are stored in different directory. This is the reason that we need the Column family in order to decentralize the data.

* * *

### [](#relationship-between-region-and-RegionServer "relationship between region and RegionServer")relationship between region and RegionServer

* * *

RegionServer is a node in the cluster. Each RegionServer can contains one or more Regions. The relationship between different concept of hbase can be shown below.  
|-> Table  
|—-> Region (regions for table)  
|——–> Store (store per column_family for each region for the table)  
|————> Memstore (memstore for each store for each region for the table)  
|—————-> StoreFile (StoreFiles for each store for each region for the table)  
|——————–> Block

* * *

### [](#Manipulating-Hbase "Manipulating Hbase")Manipulating Hbase

* * *

Actually, we can treat the HBase as a book management system. `HClient` is the readers who want to borrow books. `RegionServer` is different libraries on different states. `Region` is different floor inside a library which contains different categories of different books. `Zookeeper` is the library manager (providing the lock services).  
In order to prevent the loss of data when writing data into `Memstore`, data will also be written into `HLog` files which are stored on HDFS.

#### [](#Hbase-command "Hbase command")Hbase command

`describe 'table_name'`: this will return a result containing different column family structure for each row.

`disable 'table'`: first disable the table.

`drop 'table'`: before deleting a table, you will have to `disable 'table'` first.

`grant <user>,<permissions>,<table>,<column family>,<column qualifier>`: the <permissions>option can be a combination of “RWXCA”(read, write, exec, create, admin)</permissions>

`revoke <user>,<table>`: revoke all the rights including read, write, exec, create and admin for a user.

‘user_permission ‘: check the list of rights on a table.

<table></table>

`put 'table', 'rowkey', 'column_family:column_qualifier', 'value'`: insert a record

`create 'namespace:table_qualifier', { NAME=>'column_family1' ,VERSIONS => 1, ... } ...`: the name space is optional. Leaving it means using ‘default’ namespace. Or `create 'table', 'column_family'...`.  
`create_namespace 'space name'`: `namespace` is actually the directory name on hdfs that is going to store the HFile. By default you are storing it in the _default_ namespace.

<figure class="highlight plain">

<table>

<tbody>

<tr>

<td class="gutter">

<pre>

<div class="line">1</div>

<div class="line">2</div>

<div class="line">3</div>

<div class="line">4</div>

<div class="line">5</div>

</pre>

</td>

<td class="code">

<pre>

<div class="line"># create table</div>

<div class="line">T = create 'emp',  {NAME => 'family', VERSIONS => 5}</div>

<div class="line">T.put '001', 'family:qualifier', 'Tom Too'</div>

<div class="line">T.get '001'</div>

<div class="line">T.get '001', {COLUMN => 'family:qualifier', TIMERANGE => [0, 1438165671345]}</div>

</pre>

</td>

</tr>

</tbody>

</table>

</figure>

* * *

### [](#HBase-spliting "HBase spliting")HBase spliting

Apache hbase region splitting and merging

### [](#Reference "Reference")Reference

* * *

[Introduction to HBase schema design](http://0b4af6cdc2f0c5998459-c0245c5c937c5dedcca3f1764ecc9b2f.r43.cf2.rackcdn.com/9353-login1210_khurana.pdf)