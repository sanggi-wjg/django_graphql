
* https://docs.graphene-python.org/projects/django/en/latest/
* https://github.com/0soft/graphene-django-plus
* https://github.com/tfoxy/graphene-django-optimizer

### Select
```graphql

{
  articleAll {
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
    "creatorId": "1"
  }
}
```

### Update
```graphql
mutation UpdateArticle($id: ID!, $input:ArticleInputBase!){
  updateArticle(articleId:$id, input: $input){
    article {
      id
      title
      content
    }
  }
}

{ 
  "id": "3",
  "input": {
    "title": "string2222", 
    "content": "string2222222"
  }
}
```

### Delete
```graphql
mutation DeleteArticle($id:ID!){
  deleteArticle(articleId:$id){
    isSuccess
  }
}

{ 
  "id": "6"
}
```