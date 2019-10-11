# REST api urls

The following is the structure of our apps REST api:

```
/api/
    auth/
        login/
            POST
        register/
            POST
    users/
        POST
        {username}/
            GET
            DELETE
            enrolled/
                GET
                PUT
            owned/
                GET
                PUT
            completed/
                GET
                PUT
    submissions/
        POST
        {id}/
            GET
    courses/
        GET
        POST
        {id}/
            GET
            PUT
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
        POST
        {id}/
            GET
            PUT
            DELETE
            lessons/
                GET
                PUT
    lessons/
        POST
        {id}/
            GET
            solutionsets/
                GET
                POST
            submissions/
                GET
                PUT
                {username}
                    GET
```

Example usage:

Sending a GET request to `broncode.cs.wmich.edu/api/course/1` might get you some information about course 1, such as its titles, enrolled users, and chapters.