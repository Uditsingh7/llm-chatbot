"""
This script defines styles and message templates for a chat-like interface.

It includes:

- CSS styles: Define the visual appearance of chat messages for both user and bot.
- bot_template: A formatted HTML string representing a message from the bot.
- user_template: A formatted HTML string representing a message from the user.

You can use these templates within your Streamlit or other web framework application
to create a visually appealing and informative chat interface.
"""

css = """
<style>
  /* --- Gothic, Spacy, Musky Style --- */

  /* General message container for an ethereal feel */
  .chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center; /* Vertically align avatar and message */
    border: 1px solid rgba(200, 180, 255, 0.1); /* Faint nebula-like border */
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); /* Deeper shadow for a floating effect */
  }

  /* Styling for user messages - "Deep Space" */
  .chat-message.user {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); /* Dark space gradient */
    color: #c9d1d9; /* Off-white, like distant stars */
  }

  /* Styling for bot messages - "Cosmic Nebula" */
  .chat-message.bot {
    background: linear-gradient(135deg, #1a0a2e 0%, #2a0845 100%); /* Purple nebula gradient */
    color: #e0d1ff; /* Luminous lavender text */
  }

  /* Styling for avatar images */
  .chat-message .avatar {
    width: 15%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #584966; /* Muted purple border, like a planetary ring */
    box-shadow: 0 0 10px rgba(178, 138, 255, 0.3); /* Soft outer glow */
  }

  /* Styling for the message text itself */
  .chat-message .message {
    width: 85%;
    padding: 0 1.5rem;
    color: #e1e1e1; /* Ensuring high readability */
    font-family: 'Georgia', serif; /* A more classic, gothic-style font */
  }
</style>
"""

bot_template = """
<div class="chat-message bot">
  <div class="avatar">
    <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png">
  </div>
  <div class="message">{{MSG}}</div>
</div>
"""

user_template = """
<div class="chat-message user">
  <div class="avatar">
    <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
  </div>
  <div class="message">{{MSG}}</div>
</div>
"""

# UI Improvements (consider implementing these in your application):
# - Allow users to customize avatar images (through file upload or selection)
# - Implement a message input field for user interaction
# - Integrate the templates with your chosen framework to display chat messages