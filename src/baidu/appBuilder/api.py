class API:
    Host = 'https://qianfan.baidubce.com/v2'

    DescribeKnowledgeBases = Host + '/knowledgeBase?Action=DescribeKnowledgeBases'
    CreateKnowledgeBase = Host + '/knowledgeBase?Action=CreateKnowledgeBase'
    DescribeDocuments = Host + '/knowledgeBase?Action=DescribeDocuments'
    UploadDocuments = Host + '/knowledgeBase?Action=UploadDocuments'
    DeleteDocument = Host + '/knowledgeBase?Action=DeleteDocument'
