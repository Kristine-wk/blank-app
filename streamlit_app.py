from openai import OpenAI
import streamlit as st

# Initialiser OpenAI
api-key = st.secrets["openai"]["api_key]
client = OpenAI(api_key="api-key")

def generate_activity(ages, num_children, time, location, materials):
    ages_str = ", ".join([f"{age} år" for age in ages])
    prompt = f"""
    Find på tre kreative, sjove og pædagogiske aktiviteter for {num_children} børn i alderen {ages_str}. 
    Aktiviteterne skal tage cirka {time}, foregå {location}, og kunne laves med følgende materialer: {materials}. 

    Skriv på dansk. For hver aktivitet:
    1. Giv en fængende titel.
    2. Giv en kort, tydelig beskrivelse (max 100 ord), skrevet så forældre nemt forstår hvad de skal gøre.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Du er en hjælpsom AI, der finder på aktiviteter for børn."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def main():
    st.set_page_config(page_title="Aktiviteter for børn", layout="centered")  # ⬅️ vigtig for mobilvisning

    st.title("🎨 Aktivitetsidéer til Familier")
    st.markdown("Få skræddersyede idéer til kreative og sjove aktiviteter med børn. 👨‍👩‍👧‍👦")

    with st.sidebar:
        st.header("🎛️ Dine valg")
        num_children = st.selectbox("Antal børn", [1, 2, 3, 4, 5])
        time = st.selectbox("Tid til rådighed", ["15 minutter", "30 minutter", "1 time", "2 timer", "5 timer"])
        location = st.radio("Sted", ["Indenfor", "Udenfor"])
        ages = st.multiselect("Børnenes alder", [f"{age} år" for age in range(1, 13)], default=["5 år"])
        materials = st.text_input("Materialer", placeholder="Fx papir, tusser, tape")
        st.caption("Brug komma til at adskille materialer")

    if st.button("✨ Giv mig idéer"):
        with st.spinner("Finder på noget sjovt..."):
            if not ages:
                st.warning("Vælg mindst én alder.")
            else:
                ideas = generate_activity([int(age.split()[0]) for age in ages], num_children, time, location, materials)
                st.success(f"Her er tre idéer til {num_children} børn:")
                for idea in ideas.split("\n\n"):
                    st.markdown("---")
                    st.markdown(idea)

if __name__ == "__main__":
    main()
