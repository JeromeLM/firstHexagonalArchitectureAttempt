# first_hexagonal_architecture_attempt

Project I will use to try to implement an hexagonal architecture in backend, in Python, for the first time.

The subject is implementing a social networking application.

Use Case 1 : A user can publish messages to his personal timeline
- Business rules :
  - a) a message cannot be empty
  - b) a message must have a max length of 280 characters
- Examples :
  - business rule a :
    - Bob posts message {id: "message-id", text: ""} => Post refused as message is empty
    - Bob posts message {id: "message-id", text: "    "} => Post refused as message is empty
  - business rule b :
    - Bob posts message with a text containing 281 characters => Post refused as max length is exceeded
    - On June 4th 2022 19:00, Bob posts message {id: "message-id", text: "Hello everyone"} => Message is successfully posted : {id: "message-id", text: "Hello everyone", published_at: "2022-06-04T19:00:00.0000Z"}

Use Case 2 : A user can view all his messages on his personal timeline
- Business rules :
  - a) messages are displayed in reverse chronological order
- Examples :
  - business rule a :
    - Bob's personal timeline contains 1 message "Hello everyone" posted on June 4th 2022 19:00 and 1 message "How are you ?" posted on June 4th 2022 19:30 => Bob can see on his timeline : "How are you ?" then "Hello"

Use Case 3 : A user can edit one of his messages from his personal timeline
- Business rules :
  - same as the ones of Use Case 1

Use Case 4 : A user can subscribe to another user's timeline

Use Case 5 : A user can view on his wall all his messages and the ones of his followees
- Business rules :
  - a) messages are displayed in reverse chronological order