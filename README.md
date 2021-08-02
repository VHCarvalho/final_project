# Inspirational Wall
#### Description:
The Inspirational Wall is a project to get the positivity back on our lifes.

The main goal here is to inspire people around the world to post inspirational words to the wall so when you are feeling down or just starting your day you will be able to get the positivity, charge your batteries and spread it through your day.

You can post, upvote and revisit your posts.

The project was made using Flask (Python), Bootstrap (and some tweaks with CSS), Jinja and HTML

Now introducing the main code on this project, `app.py`.

At start, you can see the headers and the `SESSION` configuration. Next, there is the `@login_required` function, with the reference where it was took of.

The first route is the `/``. On this route the app.py will load all posts from the database and render it in the index page.

Next is the `/register`. On this route we will request a username and a password, make the basic checks if there is any name or password and check if the password and the confirmation are the same. If any check come negative, it will render a `apology.html` template with a message telling what's wrong. If all checks come positive, the user and the hash of the password will be saved on the database. At the end, the user will be redirected to `/login`.

On `/login`. On this route we will request the username and password given on the `/register` process. If all checks out, the user will be redirected to the `/post` route.

Now, at the `/post` the user will be able to post a message to the wall. On the background, we will insert the post in our database. When complete, the user will be redirected to `/``.

`/logout` route will simply clear the session and redirect the user to `/login`.

Next is `/history`, where will render all the posts created by the user.

Finnaly we will see the `/upvote`, which an interesting feature. The user is able to upvote the posts that resonates well. On the background we are updating the database so the upvote count on the chosen post is incremeted. At the end the user will be redirected to the same page, refreshing the number of upvotes.

And that's it. Much love from Brasil, 

VH Carvalho.
