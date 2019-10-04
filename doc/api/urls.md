# REST api urls

The following is the structure of our apps REST api:

```
/api/
    auth/
        login/
            POST
        register/
            POST
    submit/
        POST
        {id}/
            GET
    course/
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
    chapter/
        GET
        POST
        {id}/
            GET
            POST
            DELETE
            lessons/
                GET
                POST
    lesson/
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