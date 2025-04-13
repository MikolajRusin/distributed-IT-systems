# Laboratory Tasks 💻

---

## Laboratory 1 – UDP Mini-Chat Application 💬

### 1.1 Goal of the Task 🎯  
The objective of this laboratory was to design and implement a simple distributed application in Python using the **UDP protocol**. The application simulates a minimalistic chat system consisting of two main modules:
- **Server**
- **Client**
  
--

### 1.2 Message Format 🧾  
Each message is a string divided into fields separated by the `|` character. The format consists of:
1. **Operation Code**: One of the following characters: `+`, `-`, `?`, or `!`.
2. **Username**: A string without spaces or special characters.
3. **Optional Parameters**: Depending on the operation, different additional fields are used.

### 1.3 Server Functionality 🖥️  
The server handles client communication using the following logic:
- **Registration**: Upon receiving `+ | username |`, the user is registered.
- **Unregistration**: On receiving `- | username |`, the user is removed from the list.
- **User List Query**: `? | pattern |` triggers a list of registered users matching the regex `pattern`.
- **Message Forwarding**: `! | receiver | sender | message |` forwards a message to the specified recipient, including sender name and optional timestamp.

### 1.4 Client Functionality 👤  
The client module is responsible for:
- **Registration**  
  Format: `+ | username |`  
  Expected response: `+ | username | OK |`

- **Unregistration**  
  Format: `- | username |`  
  Expected response: `- | username | OK |`

- **User List Retrieval**  
  Format: `? | pattern |`  
  Expected response: `? | pattern | user1 user2 ... userN |`

- **Sending a Chat Message**  
  Format: `! | receiver | sender | message |`  
  Expected response: `! | receiver | sender | OK |`

> 🧠 **Note**: To enable simultaneous sending and receiving, the client spawns a separate thread immediately after registration to continuously listen for incoming messages.

---
