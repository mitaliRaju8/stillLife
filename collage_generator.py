import streamlit as st
import openai
import requests
from PIL import Image
import io
import base64
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Still Life Collage Generator",
    page_icon="✂️",
    layout="wide"
)

def main():
    st.title("✂️ Still Life Collage Generator")
    st.markdown("Create vibrant collages with cut-out objects arranged in artistic still life compositions! Mix and match objects in a creative collage style.")
    
    # Sidebar for API key
    with st.sidebar:
        st.header("🔑 Configuration")
        api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
        
        st.markdown("---")
        st.header("📝 Instructions")
        st.markdown("""
        1. Enter your OpenAI API key
        2. List objects separated by commas
        3. Choose your collage style
        4. Click Generate to create your collage
        5. Download the result!
        """)
        
        st.markdown("---")
        st.markdown("**Example objects:**")
        st.markdown("apple, vintage camera, sunflowers, coffee cup, books")
        
        st.markdown("---")
        st.info("💡 **Collage Style**: Objects will appear as cut-out pieces arranged together, not as a painted scene!")

    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("✂️ Design Your Collage")
        
        # Object input
        objects_input = st.text_area(
            "Objects for your collage (comma-separated)",
            placeholder="Enter objects like: apple, vintage camera, sunflowers, coffee cup, old books, vinyl record...",
            height=100
        )
        
        # Collage-specific style options
        st.subheader("🎨 Collage Style Options")
        
        collage_style = st.selectbox(
            "Collage Technique",
            [
                "Paper cut-out collage style",
                "Magazine cut-out collage",
                "Mixed media collage",
                "Digital photo collage",
                "Vintage scrapbook collage",
                "Modern geometric collage",
                "Layered paper collage"
            ]
        )
        
        arrangement_style = st.selectbox(
            "Object Arrangement",
            [
                "Overlapping scattered arrangement",
                "Organized grid-like layout",
                "Circular radiating pattern",
                "Asymmetrical artistic scatter",
                "Layered depth arrangement",
                "Flowing organic composition",
                "Balanced symmetrical layout"
            ]
        )
        
        color_treatment = st.selectbox(
            "Color Treatment",
            [
                "Vibrant full-color objects",
                "Retro color-filtered objects",
                "High contrast pop art colors",
                "Pastel tinted objects",
                "Mixed color and black-white",
                "Neon accent colors",
                "Vintage sepia and color mix"
            ]
        )
        
        # Background and texture options
        with st.expander("🖼️ Background & Texture Options"):
            background_style = st.selectbox(
                "Background Style",
                [
                    "Clean white background",
                    "Textured paper background",
                    "Cork board background",
                    "Fabric texture background",
                    "Wooden surface background",
                    "Abstract gradient background",
                    "Collage paper scraps background"
                ]
            )
            
            edge_style = st.selectbox(
                "Object Edges",
                [
                    "Clean cut edges",
                    "Torn paper edges",
                    "Rough scissor cuts",
                    "Soft feathered edges",
                    "Sharp geometric cuts",
                    "Hand-torn organic edges"
                ]
            )
            
            shadow_effect = st.selectbox(
                "Shadow/Depth Effect",
                [
                    "Drop shadows for depth",
                    "No shadows (flat style)",
                    "Soft ambient shadows",
                    "Strong directional shadows",
                    "Layered shadow effects"
                ]
            )
        
        # Technical options
        with st.expander("⚙️ Technical Settings"):
            image_size = st.selectbox(
                "Image Size",
                ["1024x1024", "1792x1024", "1024x1792"],
                help="Square, landscape, or portrait format"
            )
            
            object_density = st.selectbox(
                "Object Density",
                [
                    "Spacious layout with breathing room",
                    "Moderately packed arrangement",
                    "Dense collage with lots of overlap",
                    "Minimal sparse composition"
                ]
            )
        
        # Generate button
        generate_button = st.button("✂️ Create Collage", type="primary", use_container_width=True)
    
    with col2:
        st.header("🖼️ Your Collage")
        
        # Image display area
        image_placeholder = st.empty()
        
        # Show placeholder initially
        with image_placeholder.container():
            st.info("👈 Configure your collage settings and click Create Collage to see your artwork here!")
            st.markdown("**Expected result:** Cut-out style objects arranged as a collage, not a painted still life scene.")
    
    # Generation logic
    if generate_button:
        if not api_key:
            st.error("❌ Please enter your OpenAI API key in the sidebar.")
            return
        
        if not objects_input.strip():
            st.error("❌ Please enter some objects for your collage.")
            return
        
        # Parse objects
        objects_list = [obj.strip() for obj in objects_input.split(',') if obj.strip()]
        
        if len(objects_list) == 0:
            st.error("❌ Please enter valid objects separated by commas.")
            return
        
        # Create the collage-specific prompt
        objects_text = ", ".join(objects_list)
        
        prompt = f"""Create a vibrant COLLAGE (not a painting) featuring these cut-out objects: {objects_text}. 

IMPORTANT: This should be a COLLAGE style composition where each object appears as if it was cut out from different sources and arranged together, NOT a painted still life scene.

Collage specifications:
- Style: {collage_style}
- Arrangement: {arrangement_style}
- Colors: {color_treatment}
- Background: {background_style}
- Edge treatment: {edge_style}
- Shadows: {shadow_effect}
- Density: {object_density}

Each object should look like it was individually cut out (from magazines, photos, or paper) and then arranged/pasted together on the background. Objects should have distinct edges and appear as separate layered elements, not blended into a cohesive painted scene. Make it colorful, creative, and clearly recognizable as a collage artwork where individual cut-out pieces are visible and arranged artistically. All specified objects must be included as distinct collage elements."""

        # Show generation status
        with st.spinner("✂️ Creating your collage... Cutting and arranging objects!"):
            try:
                # Initialize OpenAI client
                client = openai.OpenAI(api_key=api_key)
                
                # Generate image
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size=image_size,
                    quality="standard",
                    n=1,
                )
                
                # Get the image URL
                image_url = response.data[0].url
                
                # Download the image
                img_response = requests.get(image_url)
                img_response.raise_for_status()
                
                # Convert to PIL Image
                image = Image.open(io.BytesIO(img_response.content))
                
                # Display the image
                with image_placeholder.container():
                    st.image(image, caption=f"Collage featuring: {objects_text}", use_container_width=True)
                    
                    # Download button
                    img_buffer = io.BytesIO()
                    image.save(img_buffer, format='PNG')
                    img_buffer.seek(0)
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"still_life_collage_{timestamp}.png"
                    
                    st.download_button(
                        label="💾 Download Your Collage",
                        data=img_buffer.getvalue(),
                        file_name=filename,
                        mime="image/png",
                        type="primary",
                        use_container_width=True
                    )
                    
                    # Show generation details
                    with st.expander("📋 Collage Details"):
                        st.write(f"**Objects included:** {objects_text}")
                        st.write(f"**Collage technique:** {collage_style}")
                        st.write(f"**Arrangement:** {arrangement_style}")
                        st.write(f"**Color treatment:** {color_treatment}")
                        st.write(f"**Background:** {background_style}")
                        st.write(f"**Edge style:** {edge_style}")
                        st.write(f"**Shadow effect:** {shadow_effect}")
                        st.write(f"**Object density:** {object_density}")
                        st.write(f"**Image size:** {image_size}")
                        st.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                st.success("✅ Your collage has been created successfully!")
                
                # Tips for better results
                with st.expander("💡 Tips for Better Collages"):
                    st.markdown("""
                    **For more collage-like results:**
                    - Try objects that are commonly found in magazines or photos
                    - Mix different types of objects (natural, manufactured, vintage, modern)
                    - Use "Paper cut-out" or "Magazine cut-out" styles
                    - Choose "Torn paper edges" for more authentic collage feel
                    - If result looks too much like a painting, try regenerating with different style options
                    """)
                
            except openai.AuthenticationError:
                st.error("❌ Invalid API key. Please check your OpenAI API key.")
            except openai.RateLimitError:
                st.error("❌ Rate limit exceeded. Please try again later.")
            except openai.BadRequestError as e:
                st.error(f"❌ Request error: {str(e)}")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

    # Footer with examples
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🎨 Collage Ideas:**")
        st.markdown("• Vintage objects  \n• Travel items  \n• Kitchen utensils  \n• Art supplies")
    
    with col2:
        st.markdown("**✂️ Best Techniques:**")
        st.markdown("• Paper cut-out style  \n• Magazine collage  \n• Mixed media  \n• Torn edges")
    
    with col3:
        st.markdown("**🌈 Color Tips:**")
        st.markdown("• Mix vibrant colors  \n• Try retro filters  \n• Use high contrast  \n• Add neon accents")
    
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit and DALL-E 3 | ✂️ Collage Style Generator")

if __name__ == "__main__":
    main()