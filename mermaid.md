```mermaid

---
title: DynamoDBテーブル
---
erDiagram
    USERS {
      integer userId "PK（プロフィール取得）"
      varchar username
      varchar profile
      varchar picture
    }

    RECIPES {
      integer recipeId "PK（レシピ一件取得）"
      varchar type "GSI1 PK（レシピ全件取得）"
      integer userId "GSI2 PK（ユーザーを指定してレシピ全件取得）"
      varchar name
      text recipe
      varchar username
      varchar imageUrl
      timestamp created_at "GSI1,2 SK"
      integer likesCount
    }

    LIKE {
      integer recipeId "PK"
      integer userId
      varchar createdAt "SK"
    }

    COMMENT {
      integer commentId "PK"
      integer recipeId "GSI1 PK"
      integer userId
      varchar username
      text content
      varchar createdAt "GSI1 SK"
    }

    USERS ||--o{ RECIPES : "many-to-one"
    RECIPES ||--o{ LIKE : "one-to-many"
    RECIPES ||--o{ COMMENT : "one-to-many"

```
