import streamlit as st
import secrets
import string
import math
from passlib.context import CryptContext

# Password hashing & security context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to check password strength
def check_password_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    score = sum([has_upper, has_lower, has_digit, has_special])

    if length < 6:
        return "Very Weak", "red", 10
    elif length < 8 or score < 2:
        return "Weak", "orange", 30
    elif length < 12 or score < 3:
        return "Medium", "blue", 60
    else:
        return "Strong", "green", 100

# Function to calculate entropy
def calculate_entropy(password):
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += len(string.punctuation)

    if charset_size == 0:
        return 0
    return round(len(password) * math.log2(charset_size), 2)

# Function to generate a strong password
def generate_strong_password(length=12, use_specials=True):
    characters = string.ascii_letters + string.digits
    if use_specials:
        characters += string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

# Streamlit UI
st.set_page_config(page_title="Password Strength Meter", layout="centered")

st.title("🔐 Password Strength Checker")

password = st.text_input("Enter your password", type="password")

if password:
    strength, color, progress = check_password_strength(password)
    entropy = calculate_entropy(password)

    st.markdown(f"**Password Strength:** <span style='color:{color}; font-weight:bold;'>{strength}</span>", unsafe_allow_html=True)
    st.progress(progress / 100)
    st.markdown(f"🔢 **Entropy Score:** `{entropy} bits`")

    if strength in ["Very Weak", "Weak"]:
        st.warning("❗ Your password is weak. Consider making it longer and adding uppercase, digits, and special characters.")
    elif strength == "Medium":
        st.info("✅ Decent password! Try increasing length for better security.")
    else:
        st.success("🎉 Strong password! Well done!")

# Customizable Password Generator
st.subheader("🔑 Need a Secure Password?")

password_length = st.slider("Select Password Length", min_value=6, max_value=24, value=12, step=1)
use_specials = st.checkbox("Include Special Characters", value=True)

if st.button("Generate Password"):
    new_password = generate_strong_password(password_length, use_specials)
    st.text(f"🔹 {new_password}")

# Password Security Guidelines
st.markdown("---")
st.markdown("### 🛡 Password Security Guidelines")
st.markdown("""
- Use at least **12+ characters**.
- Include **uppercase, lowercase, numbers, and special characters**.
- Avoid using **common words or sequences** (e.g., `password123`).
- Never **reuse old passwords**.
- Consider using a **password manager** to store complex passwords.
""")
