
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

mutation {
  createArticle(content: "string", creatorId: "1", title: "string") {
    article {
      id
      title
      slug
      content
      creator {
        id
        username
        email
      }
      datetimeCreated
      datetimeUpdated
      comments {
        edges {
          node {
            id
            content
          }
        }
      }
    }
  }
}
```

### Update
```graphql
mutation {
  updateArticle(content: "string11111111111", articleId: 5) {
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
```

### Delete
```graphql
mutation {
  deleteArticle(articleId: 4) {
    success
  }
}

```