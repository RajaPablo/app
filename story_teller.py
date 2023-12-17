from openai import OpenAI
import streamlit as st
import os

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

def generateImage(client, image_description):
    prompt = "You are a creative comic book artist. Given the following prompt, construct a colorful and vibrant comic book page with a few panels that should fit into the given image size dimensions (note: only the comic book page panels should be shown): " + image_description

    response = client.images.generate(
        model = "dall-e-3",
        prompt = prompt,
        size = "1024x1792",
        quality = "standard",
        n = 1
    )

    image_url = response.data[0].url

    return image_url

def tellStory(client, image_url):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze the content of this comic book page and write a creative, engaging story that brings the scene to life. Describe the characters, setting, and actions in a way that would captivate a young audience:"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=500,
    )

    return response.choices[0].message.content

def main():
    client = OpenAI()

    st.set_page_config(page_title="Your Fabulous Storyteller!", layout="wide")
    st.title("Your Fabulous Storyteller!")

    with st.sidebar:
        st.header("Prompt")
        image_description = st.text_area("Whether it's a single word or a captivating sentence, share it with us and we'll weave a story just for you. Every contribution adds a unique twist to our creative tale. What's your word or sentence? Let the storytelling adventure begin!", height=100)
        generate_image_btn = st.button("Story Time!")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Art")
        if generate_image_btn and image_description:
            with st.spinner("Hold your horses! It's not every day you get an entire story in a few seconds. Your story is on its way!"):
                image_path = generateImage(client, image_description)
                if image_path:
                    st.image(
                        image_path,
                        caption="Generated Comic Image",
                        use_column_width=True,
                    )
                else:
                    st.error("Failed to generate image.")

    with col2:
        st.header("Story")
        if generate_image_btn and image_description:
            with st.spinner("Sorry about the wait! just a few more seconds!"):
                story = tellStory(client, image_path)
                st.text_area("response", value = story, height = 750)

if __name__ == "__main__":
    main()