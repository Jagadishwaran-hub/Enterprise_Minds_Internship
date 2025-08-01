from langgraph.graph import StateGraph, END
from typing import TypedDict
from typing import Optional, Dict, Any
from src.services.weather_service import get_weather_real
from src.memory import memory

# --- GROQ LLM Integration ---
from groq import Groq

groq_api_key = ""  # <-- Replace with your actual API key
llm = Groq(api_key=groq_api_key)

# Define state schema
class WeatherState(TypedDict):
    user_input: Optional[str]
    message: Optional[str]
    next: Optional[str]

def ask_city_node(state: WeatherState) -> WeatherState:
    return {
        "user_input": state.get("user_input"),
        "message": "Enter a city name (e.g., Chennai, Delhi, Bangalore, Mumbai):",
        "next": "validate_city"
    }

def validate_city_node(state: WeatherState) -> WeatherState:
    city = state.get("user_input", "").strip()
    if not city:
        return {
            "user_input": state.get("user_input"),
            "message": "City name cannot be empty.",
            "next": "retry"
        }
    weather = get_weather_real(city)
    if not weather:
        return {
            "user_input": state.get("user_input"),
            "message": f"Sorry, '{city}' not found or weather unavailable.",
            "next": "retry"
        }
    memory.set("last_location", city.title())
    memory.set("last_weather", weather)
    return {
        "user_input": state.get("user_input"),
        "message": city,
        "next": "respond"
    }

def retry_node(state: WeatherState) -> WeatherState:
    return {
        "user_input": state.get("user_input"),
        "message": "Please enter a valid city (e.g., Chennai, Delhi, Bangalore, Mumbai):",
        "next": "validate_city"
    }

def respond_node(state: WeatherState) -> WeatherState:
    last_city = memory.get("last_location", "Unknown")
    last_weather = memory.get("last_weather", "No data")
    # Use Groq LLM to rephrase the weather response in a friendly way
    prompt = f"Rephrase this weather report in a friendly, conversational way for the user: Current weather in {last_city}: {last_weather} (Last successful city: {last_city})"
    try:
        llm_response = llm.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        friendly_message = llm_response.choices[0].message.content
    except Exception as e:
        friendly_message = f"Current weather in {last_city}: {last_weather}\n(Last successful city: {last_city})\n[LLM error: {e}]"
    return {
        "user_input": state.get("user_input"),
        "message": friendly_message,
        "next": END
    }

# Build the graph
workflow = StateGraph(WeatherState)

# Add nodes
workflow.add_node("ask_city", ask_city_node)
workflow.add_node("validate_city", validate_city_node)
workflow.add_node("retry", retry_node)
workflow.add_node("respond", respond_node)

# Set entry point
workflow.set_entry_point("ask_city")

# Compile the graph
graph = workflow.compile()

# Helper functions for Streamlit
def validate_city_and_get_weather(city: str) -> tuple[bool, str]:
    """
    Validate city and get weather. Returns (is_valid, message)
    """
    if not city.strip():
        return False, "City name cannot be empty."
    
    weather = get_weather_real(city)
    if not weather:
        return False, f"Sorry, '{city}' not found or weather unavailable."
    
    memory.set("last_location", city.title())
    memory.set("last_weather", weather)
    return True, weather

def get_friendly_weather_response(city: str, weather: str) -> str:
    """
    Use Groq LLM to rephrase the weather response in a friendly way
    """
    prompt = f"Rephrase this weather report in a friendly, conversational way for the user: Current weather in {city}: {weather} (Last successful city: {city})"
    try:
        llm_response = llm.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        return llm_response.choices[0].message.content
    except Exception as e:
        return f"Current weather in {city}: {weather}\n(Last successful city: {city})\n[LLM error: {e}]"