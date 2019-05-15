# WFS(Web Feature Service) BayesBA实现

## 1. 概要

参考标准：OGC 09-025r1 and ISO/DIS 19142

目前仅实现标准中的Basic WFS即：

```
The server shall implement the Simple WFS conformance class and shall additionally implement the GetFeature operation with the Query action and the GetPropertyValue Operation.

Simple WFS: The server shall implement the follow operations: GetCapabilities, DescribeFeatureType, ListStoredQueries, DescribeStoredQueries, GetFeature operations with only the StoredQuery action ...

```

需要实现：

    GetCapabilities
    DescribeFeatureType
    ListStoredQueries
    DescribeStoredQueries
    GetFeature (With stored query and query action.)
    GetPropertyValue

在返回需要实现Response Paging：The server shall implement the ability to page through the set of response features or values.

后续考虑实现有权限的 Manage Stored Query.

且仅支持HTTP GET, HTTP POST。SOA支持没有在当前计划中。

## 2. WHY

市面上已经有WFS的实现了，如[FeatureServer](http://featureserver.org/)、[GEOServer](http://geoserver.org/)等，为什么我们还要自己实现一个？

    1. 必须足够轻量，能够集成到我们自己的系统中，不用独立部署；
    2. 和中台的结合，能够和中台数据自然结合起来；
    3. 维护成本，后续不需要因为添加数据类型再去修改代码或添加配置等。


## 3. 测试

所有的兼容性测试在bayes.wfs.test包下，测试文件名为标准《OGC 09-025r1 and ISO/DIS 19142》中附录A章节编码。

## 4. GetCapabilities

GetCapabilities返回服务描述信息，目前近支持KVP-encoding。

URL示例

    http://hostname:port/path?SERVICE=WCS&REQUEST=GetCapabilities&ACCEPTVER SIONS=1.0.0,0.8.3&SECTIONS=Contents&UPDATESEQUENCE=XYZ123& ACCEPTFORMATS=text/xml


名称和例子| 用途 | 定义
-----------------|---------------------|-----------------------
service=WFS | | Service Type and Identifier。当前实现里面，仅包含WFS，将来可能添加为WCS
request=GetCapabilities | | 操作名
AcceptVersions=2.0.0,3.0.0 | 可选 | 逗号分割的版本序列，客户端支持的协议版本，目前2.0.0
Sections=Contents | 可选 | 逗号分割的metadata章节。应该支持：ServiceIdentification, ServiceProvider, OperationsMetaData, Contents, All
updateSequence | 0，可选 | 当前暂不支持
acceptFormats | | 客户端支持的格式，当前服务器仅支持json。

返回对象描述：

### 4.1 ServiceIdentification
名称和例子  |   定义
----------|--------
title     | String，BayesBa Map Server DEV，协议中title是LanguageString，本实现中简化为String，缺失了多语言的支持。
abstract  | String. description
keywords  | String-Array, Keywords of Server
serviceType | fixed, OGC:WFS
serviceTypeVersion | String-Array, Supported version
Fees | None
AcccessConstraints | fixed, since we need jwt.

#### 4.1.1 LanguageString
Name | Define
-----|-------
lang | zh-CN, en-US
value | string

详细定义可参考[ServiceIdentification XML schema document](https://www.mediamaps.ch/ogc/schemas-xsdoc/sld/1.1.0/owsServiceIdentification_xsd.html)

### 4.2 ServiceProvider

服务提供商，运维WFS的组织。

名称和例子  |  定义 
----------|------------
providerName | 提供商代码，Character String
serviceContact| ResponsibleParty负责人，可选，最多一个
providerSite | OnlineResource网站，可选，最多一个

#### 4.2.1 ResponsibleParty

名称和例子   |    定义
-----------|--------
individualName | CharacterString
positionName | CharacterString
contactInfo | 角色

#### 4.2.2 Role

名称和例子    |     定义
------------|----------
hoursOfService | CharacterString
contactInstructions | CharacterString
address | 地址
phone | 联系方式

#### 4.2.3 Address

名称和例子    |     定义
-------------|------------
deliveryPoint | CharacterString
city | CharacterString
administrativeArea | CharacterString
postalCode | CharacterString
country | CharacterString
electronicMailAddress | Character

#### 4.2.4 Telephone

名称和例子 | 定义
----------|------------
voice | CharacterString
facsimile | CharacterString

#### 4.2.5 OnlineResource

名称和例子 | 定义
--------|--------------
linkage | URL

### 4.3 OperationsMetaData

服务中所实现的操作文档，包含操作地址。

### 4.4 Contents

Metadata about the data served by this server.

#### 4.4.1 OWSContents

This abstract Contents class shall be subclassed by each specific OWS that includes a Contents section in its service metadata document.

名称和例子|定义
-----------|-----------
datasetSummary | DatasetSummary

##### 4.4.2 DatasetSummary

名称和例子 | 定义
---------|---------
title  | CharacterString
abstract | CharacterString
keywords | String-Array 关键字
identifier | Code
boundingBox | BoundingBox
metadata | MetaData


##### 4.4.3 Code
 
名称和例子 | 定义
---------|---------
code  | CharacterString
codeSpace | URI

##### 4.4.4 BoundingBox

名称和例子 | 定义
---------|---------
lowerCorner  | Number-Array
upperCorner | Number-Array
crs | 4326
dimensions | 2

###### 4.4.5 Metadata

名称和例子 | 定义
---------|---------
metadata  | any
link | URL
about | URI