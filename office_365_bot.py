import openai
import streamlit as st

def assistant(prompt, context):
    messages = context + [
        {
            'role':'system', 
            'content': ''' You are an expert of Microsoft Office 365 version. 
                            Answer the questions of the user efficiently without making things up by yourself. Summarize your answer into minimum possible words. If the user asks anything other than your expertise, politely refuse him and tell about your area of expertise. Do not say offensive or harmful things. Stay humble, calm, professional and polite. Be clear and concise. '''
        },
        {
            'role':'user', 'content': f"{prompt}"   # dont write in {} until its f-string!!!
        }
    ]

    response = openai.ChatCompletion.create(
        messages = messages,
        model = 'gpt-3.5-turbo',
        max_tokens = 150,
        temperature = 0.3,
    )

    system = response['choices'][0]['message']['content']
    return system
    
st.title("Office 365 Bot")

with st.sidebar:
    api_key = st.text_input('Enter your OpenAI API key here', type = 'password')
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

if "context" not in st.session_state:
    st.session_state.context = []

for msg in st.session_state.context:   # Displays all the messages in loop
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# user = st.chat_input(placeholder = "Your message", max_chars=50)

if query:= st.chat_input("Your message: ", max_chars= 50):   # := Walrus operator
    st.chat_message("user").markdown(query)
    st.session_state.context.append({"role": "user", "content": query})

    system_response = assistant(query, st.session_state.context)
    st.chat_message("system").markdown(system_response)
    st.session_state.context.append({"role":"system", "content":system_response})
    

if not api_key:
    st.warning("Please enter your OpenAI API key in the sidebar.")
else:
    openai.api_key = api_key
    
