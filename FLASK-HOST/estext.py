from elasticsearch import Elasticsearch#引入es
es=Elasticsearch(["10.10.21.148"],timeout=360)#连接服务器

data = {
    "mappings":{
        "properties":{
            "title":{
                "type":"text",
                "index":True
            },
            "keywords":{
                "type":"text",
                "index":True
            },
            "link":{
                "type": "string",
                "index": True
            },
            "content":{
                "type": "text",
                "index": True
            }

        }
    }
}
es.indices.create(index="pythontest",body=data)#插入索引