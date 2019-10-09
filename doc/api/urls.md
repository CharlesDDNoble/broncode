# REST api urls

The following is the structure of our apps REST api:

```
/api/
    auth/
        login/
            POST
        register/
            POST
    submissions/
        POST
        {id}/
            GET
    courses/
        GET
        POST
        {id}/
            GET
            POST
            DELETE
            chapters/
                GET
                POST
            users/
                GET
                POST
            owners/
                GET
                POST
    chapters/
        GET
        POST
        {id}/
            GET
            POST
            DELETE
            lessons/
                GET
                POST
    lessons/
        GET
        POST
        {id}/
            GET
            solutions/
                GET
                POST
```

Example usage:

Sending a GET request to `broncode.cs.wmich.edu/api/course/1` might get you some information about course 1, such as its titles, enrolled users, and chapters.