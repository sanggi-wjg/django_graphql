
* https://docs.graphene-python.org/projects/django/en/latest/
* https://github.com/0soft/graphene-django-plus
* https://github.com/tfoxy/graphene-django-optimizer

### Select
```graphql
{
  articleAll(
    title:"11111"
  ) {
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
    edges {
      node {
        id
        title
        slug
        content
      	datetimeCreated
        datetimeUpdated
        creator{
          id
          username
          email
        }
        comments {
          edges {
            node {
              id
              content
              datetimeCreated
              datetimeUpdated
              creator {
                id
                username
                email
              }
              replied {
                edges{
                  node {
                    id
                    content
                  }
                }
              }
            }
          }
          
        }
      }
      cursor
    }
  }
}
```


### Create
```graphql
mutation CreateArticle($input:CreateArticleInput!){
  createArticle(input: $input){
    article {
      id
      title
      content
    }
  }
}

{ 
  "input": {
    "title": "string2222", 
    "content": "string2222222",  
    "creatorId": 1
  }
}
```

### Update
```graphql
mutation UpdateArticle($articleId:ID!, $input:ArticleInputBase!){
  updateArticle(articleId:$articleId, input:$input) {
    article {
      id
      title
      slug
      content
      datetimeCreated
      datetimeUpdated
    }
  }
}


{ 
  "articleId": 1210,
  "input": {
    "title": "123123222222222",
    "content": "12312321323212112321331"
  }
}
```

### Delete
```graphql
mutation DeleteArticle($articleId:ID!){
  deleteArticle(articleId:$articleId) {
    isSuccess
  }
}


{ 
  "articleId": 1209
}
```