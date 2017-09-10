HBase is an open source distributed database built on top of hadoop eco-system. It is becoming a popular choice for application who need fast and random access to large amount of data. In this post, I want to explain my summary on reading the paper written by ![Amandeep khurana](http://0b4af6cdc2f0c5998459-c0245c5c937c5dedcca3f1764ecc9b2f.r43.cf2.rackcdn.com/9353-login1210_khurana.pdf) on explaining the design of HBase architecture. This post is not meant to be read at one time since it is too long. I am just writing it as a note when learning the architecture and usage of hbase.
***

### HBase data model

1.  _Table_ : data are stored into tables whose names are strings and composed with characters that are safe for use in a file system path.
2.  _Row_ : each row is a data entry identified with row keys (like the primary key in relational database). Row keys have no data type and are treated as a byte[] (byte array).
3.  _Column Family_ : data within a row are grouped by column family. It should be defined up front since this will impact the physical arrangement of how data are stored in HBase.  
> Question: why do you think it is necessary to have column family?
My thought:

4.  _Column qualifier_ : Data within a column family is addressed via its column quali er, or simply, column. Need not defined up front since it is `dynamic`. Like Row keys, they are treated as byte[].
5.  _Cell_ : where data are actually stored. It is treated as byte[] too.
6.  _Time stamp_ : each cell are versioned with timestamp which is the time when the value is inserted by default.

![How the concepts above are actually mapped to the real table](/static/images/HBase_design/HBase_table_design.jpg)

##### From the view of key-value:

```
{
  001:{
    personal:{
      Name:{
        Timestamp1:tom,
        Timestage2:allen
      }
    }
        ...
  }
}
```

Actually, the key of an entry in the table is formed by *[row key, column family, column qualifier, timestamp]* and key is the content of the cell. So to get the value of the name in the cell, you will go through the following process:  
`001 -> Personal -> Name -> Timestamp1 : tom` in order to get the value that you want. This process is called the coordinate.
If you left out the timestamp1, the return value will be a dictionary with 2 version of name:  
`001 -> Personal -> Name : {Timestamp1 : tom,Timestamp1 : allen`  
Following the same rule, the returned value will be possibly the following one:  
`001 : {Personal : {Name : {Timestamp1 : tom,Timestamp1 : allen } }` .etc

***
### HBase table design

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

***

### Paper Summary

Inside the paper, the author also provided an example of how to design a Follows-following relationship using HBase to demonstrate how to combine the knowledge that we talk about above. I will leave a link below just in case you are interested on it.

***
# In reality

> This section will talk about HBase key concept in production.

### Column family

ColumnFamily is the storing unit of a Region. One region contains multiple ColumnFamilies which are stored in different directory. This is the reason that we need the Column family in order to decentralize the data.

### relationship between region and RegionServer

RegionServer is a node in the cluster. Each RegionServer can contains one or more Regions. The relationship between different concept of hbase can be shown below.  
|-> Table  
|—-> Region (regions for table)  
|——–> Store (store per column_family for each region for the table)  
|————> Memstore (memstore for each store for each region for the table)  
|—————-> StoreFile (StoreFiles for each store for each region for the table)  
|——————–> Block

### Manipulating Hbase

Actually, we can treat the HBase as a book management system. `HClient` is the readers who want to borrow books. `RegionServer` is different libraries on different states. `Region` is different floor inside a library which contains different categories of different books. `Zookeeper` is the library manager (providing the lock services).  
In order to prevent the loss of data when writing data into `Memstore`, data will also be written into `HLog` files which are stored on HDFS.

#### Hbase command

`describe 'table_name'`: this will return a result containing different column family structure for each row.

`disable 'table'`: first disable the table.

`drop 'table'`: before deleting a table, you will have to `disable 'table'` first.

`grant <user>,<permissions>,<table>,<column family>,<column qualifier>`: the <permissions>option can be a combination of “RWXCA”(read, write, exec, create, admin)</permissions>

`revoke <user>,<table>`: revoke all the rights including read, write, exec, create and admin for a user.

‘user_permission ‘: check the list of rights on a table.

`put 'table', 'rowkey', 'column_family:column_qualifier', 'value'`: insert a record

`create 'namespace:table_qualifier', { NAME=>'column_family1' ,VERSIONS => 1, ... } ...`: the name space is optional. Leaving it means using ‘default’ namespace. Or `create 'table', 'column_family'...`.  
`create_namespace 'space name'`: `namespace` is actually the directory name on hdfs that is going to store the HFile. By default you are storing it in the _default_ namespace.

```
# create table
T = create 'emp',  {NAME => 'family', VERSIONS => 5}
T.put '001', 'family:qualifier', 'Tom Too'
T.get '001'
T.get '001', {COLUMN => 'family:qualifier', TIMERANGE => [0, 1438165671345]}
```

### HBase spliting

Apache hbase region splitting and merging


### HBase architecture and benefits of this design
Hbase contains the following type of servers:
* Hbase region server: which is used for storing Regions. HBase Tables are divided by row key(marked as start key and end key) into regions. A region server can contains 1000 regions.
```
Region server  <- regions
```
* Master server:
  * Hbase master process: which control region servers.
    * If client wants to create delete tables, one should communicate with HBase Master.
    * Assigning regions on startup or re-assigning regions.
    * monitoring based on zookeeper.
  * Zookeeper: maintain the live cluster state.
    * check if region server is available to guarantee the consensus of data.
  * NameNode: maintains meta info

### How zookeeper work in hbase?

### how to read?
* first time read
  1. get meta table location (which region server host this meta table according to the coordinate the client supply) from HMaster.
  2. with meta table, client knows which regionserver will have the data specified by the rowkey. the client caches this info along with the meta table location.
  3. get the row from the regionserver.

* future read
  uses the caches info to get what you want unless there is a miss which will perform update on the cache based on the previous process.

### Hbase meta table
![](/static/images/HBase_design/hbase_meta_table.png)
I want to demonstrate this part by quoting the schema from ![This post](https://mapr.com/blog/in-depth-look-hbase-architecture/)
where the author has well demonstrate how the .META table is designed.

### Regionserver component


### Reference

![Introduction to HBase schema design](http://0b4af6cdc2f0c5998459-c0245c5c937c5dedcca3f1764ecc9b2f.r43.cf2.rackcdn.com/9353-login1210_khurana.pdf)

![An in depth look at the hbase architecture](https://mapr.com/blog/in-depth-look-hbase-architecture/)
