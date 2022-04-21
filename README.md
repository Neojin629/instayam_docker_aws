# Instayam with Docker and AWS


## Description

An Instagram Clone called Instayam.  


| Endpoint                    	| Method 	| JSON Parameters                                            	| Output                                                     	| Description                          	|
|-----------------------------	|--------	|------------------------------------------------------------	|------------------------------------------------------------	|--------------------------------------	|
| posts/''                    	| index  	| content: str, created_at: timestamp, id: int, user_id: int 	| content: str, created_at: timestamp, id: int, user_id: int 	| Shows all posts                      	|
| posts/<int:id>              	| show   	| post_id: int                                               	| content: str, created_at: timestamp, id: int, user_id: int 	| Shows post connected to post_id      	|
| posts/''                    	| create 	| user_id: int, content: str                                 	| content: str, created_at: timestamp, id: int, user_id: int 	| Creates a new post                   	|
| posts/<int:id>              	| delete 	| post_id: int                                               	| Deleted: True, Not Deleted: False                          	| Deletes a post by ID.                	|
| posts/<int:id>/liking_users 	| likes  	| post_id: int                                               	| user_id: int, username: str                                	| Shows list of users that liked post. 	|
| users/''                    	| index  	| id: int, username: str                                     	| id: int, username: str                                     	| Shows all users                      	|
| users/<int:id>              	| show   	| user_id: int                                               	| id: int, username: str                                     	| Shows username connected to ID.      	|
| users/''                    	| create 	| username: str, password: str (scrambled)                   	| id: int, username: str                                     	| Creates a new user, hides password.  	|
| users/<int:id>              	| delete 	| user_id: int                                               	| Deleted: True, Not Deleted: False                          	| Deletes a user by ID.                	|
| users/<int:id>              	| update 	| username: str, password: str (scrambled)                   	| id: int, username: str                                     	| Updates username or password.        	|
| users/<int:id>/liked_posts  	| likes  	| id: int                                                    	| content: str. created_at: timestamp, id: int, user_id: int 	| Shows list of liked posts by user_id 	|

## Retrospective 

1. The project design changed drastically from ERD to the final product.  I noticed that at first my ERD was more complicated than it should've been.  Way too many connections and too much duplicate information in different tables.  As first built, they definitely weren't normalized.  Thanks to the feedback provided by the instructor, I was able to go back and simplify the design.  Since this was an Instagram clone, it was very similar to the Twitter exercise we worked on.  This also helped clarify some setbacks of my original design.  

2. I decided to go with ORM over raw SQL since I already use SQL at work.  I felt that ORM would give me more exposure to using Python and understanding how it all works together.  I still have much to learn but definitely ready for it.  

3. I added indexes to the users, tags and posts tables as I feel these would need the speed bump when querying.  I added the queries for the Index below:

CREATE INDEX users_index ON users USING HASH (username);
CREATE INDEX posts_index ON posts (user_id);
CREATE INDEX tags_index ON tags (post_id);

Originally on Flask, now this is a Django version with the hope of uploading it to AWS by end of Project.  
