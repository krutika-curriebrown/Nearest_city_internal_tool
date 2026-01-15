"""
Find Nearest Tracked City - Streamlit App
------------------------------------------
A web application to find the nearest tracked city from a list of cities.
Deployable on Azure App Service.
"""

import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.distance import geodesic
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Find Nearest Tracked City",
    page_icon="📍",
    layout="centered"
)

# Initialize geolocator with caching
@st.cache_resource
def get_geolocator():
    return Nominatim(user_agent="city_nearest_matcher_streamlit")

geolocator = get_geolocator()

# Tracked cities data
TRACKED_CITIES = {
    'AKRON': {'latitude': 41.083064, 'longitude': -81.518485, 'state': 'Ohio'},
    'ALBANY': {'latitude': 42.6511674, 'longitude': -73.754968, 'state': 'New York'},
    'ALBUQUERQUE': {'latitude': 35.0841034, 'longitude': -106.650985, 'state': 'New Mexico'},
    'ALEXANDRIA': {'latitude': 38.8051095, 'longitude': -77.0470229, 'state': 'Virginia'},
    'ANAHEIM': {'latitude': 33.8347516, 'longitude': -117.911732, 'state': 'California'},
    'ANCHORAGE': {'latitude': 61.1758781, 'longitude': -149.1107333, 'state': 'Alaska'},
    'ANN ARBOR': {'latitude': 42.2813722, 'longitude': -83.7484616, 'state': 'Michigan'},
    'ATLANTA': {'latitude': 33.7489924, 'longitude': -84.3902644, 'state': 'Georgia'},
    'AUSTIN': {'latitude': 30.2711286, 'longitude': -97.7436995, 'state': 'Texas'},
    'BALTIMORE': {'latitude': 39.2908816, 'longitude': -76.610759, 'state': 'Maryland'},
    'BATON ROUGE': {'latitude': 30.4494155, 'longitude': -91.1869659, 'state': 'Louisiana'},
    'BILLINGS': {'latitude': 45.7874957, 'longitude': -108.49607, 'state': 'Montana'},
    'BIRMINGHAM': {'latitude': 33.5206824, 'longitude': -86.8024326, 'state': 'Alabama'},
    'BOISE': {'latitude': 43.6166163, 'longitude': -116.200886, 'state': 'Idaho'},
    'BOSTON': {'latitude': 42.3554334, 'longitude': -71.060511, 'state': 'Massachusetts'},
    'BUFFALO': {'latitude': 42.8867166, 'longitude': -78.8783922, 'state': 'New York'},
    'BURLINGTON': {'latitude': 44.4761601, 'longitude': -73.212906, 'state': 'Vermont'},
    'CEDAR RAPIDS': {'latitude': 41.9758872, 'longitude': -91.6704053, 'state': 'Iowa'},
    'CHARLESTON (WV)': {'latitude': 38.3498, 'longitude': -81.6326, 'state': 'West Virginia'},
    'CHARLESTON (SC)': {'latitude': 32.7833, 'longitude': -79.9320, 'state': 'South Carolina'},
    'CHARLOTTE': {'latitude': 35.2272086, 'longitude': -80.8430827, 'state': 'North Carolina'},
    'CHATTANOOGA': {'latitude': 35.0457219, 'longitude': -85.3094883, 'state': 'Tennessee'},
    'CHEYENNE': {'latitude': 41.139981, 'longitude': -104.820246, 'state': 'Wyoming'},
    'CHICAGO': {'latitude': 41.8755616, 'longitude': -87.6244212, 'state': 'Illinois'},
    'CINCINNATI': {'latitude': 39.1014537, 'longitude': -84.5124602, 'state': 'Ohio'},
    'CLEVELAND': {'latitude': 41.4996574, 'longitude': -81.6936772, 'state': 'Ohio'},
    'COLUMBIA': {'latitude': 34.0003117, 'longitude': -81.0331309, 'state': 'South Carolina'},
    'COLUMBUS': {'latitude': 39.9622601, 'longitude': -83.0007065, 'state': 'Ohio'},
    'CORPUS CHRISTI': {'latitude': 27.7635302, 'longitude': -97.4033191, 'state': 'Texas'},
    'DALLAS': {'latitude': 32.7762719, 'longitude': -96.7968559, 'state': 'Texas'},
    'DAVENPORT': {'latitude': 41.5235808, 'longitude': -90.5770967, 'state': 'Iowa'},
    'DAYTON': {'latitude': 39.7589478, 'longitude': -84.1916069, 'state': 'Ohio'},
    'DEARBORN': {'latitude': 42.3222599, 'longitude': -83.1763145, 'state': 'Michigan'},
    'DENVER': {'latitude': 39.7392364, 'longitude': -104.984862, 'state': 'Colorado'},
    'DES MOINES': {'latitude': 41.5868654, 'longitude': -93.6249494, 'state': 'Iowa'},
    'DETROIT': {'latitude': 42.3315509, 'longitude': -83.0466403, 'state': 'Michigan'},
    'DULUTH': {'latitude': 46.7729322, 'longitude': -92.1251218, 'state': 'Minnesota'},
    'EL PASO': {'latitude': 31.7601164, 'longitude': -106.4870404, 'state': 'Texas'},
    'ERIE': {'latitude': 42.1294712, 'longitude': -80.0852695, 'state': 'Pennsylvania'},
    'EVANSVILLE': {'latitude': 37.970495, 'longitude': -87.5715641, 'state': 'Indiana'},
    'FAIRBANKS': {'latitude': 64.82897449999999, 'longitude': -147.66991691593407, 'state': 'Alaska'},
    'FARGO': {'latitude': 46.877229, 'longitude': -96.789821, 'state': 'North Dakota'},
    'FLINT': {'latitude': 43.0161693, 'longitude': -83.6900211, 'state': 'Michigan'},
    'FORT WORTH': {'latitude': 32.753177, 'longitude': -97.3327459, 'state': 'Texas'},
    'FRESNO': {'latitude': 36.7394421, 'longitude': -119.78483, 'state': 'California'},
    'GRAND RAPIDS': {'latitude': 42.9632425, 'longitude': -85.6678639, 'state': 'Michigan'},
    'GREEN BAY': {'latitude': 44.5126379, 'longitude': -88.0125794, 'state': 'Wisconsin'},
    'HARTFORD': {'latitude': 41.764582, 'longitude': -72.6908547, 'state': 'Connecticut'},
    'HONOLULU': {'latitude': 21.304547, 'longitude': -157.855676, 'state': 'Hawaii'},
    'HOUSTON': {'latitude': 29.7589382, 'longitude': -95.3676974, 'state': 'Texas'},
    'HUNTSVILLE': {'latitude': 34.729847, 'longitude': -86.5859011, 'state': 'Alabama'},
    'INDIANAPOLIS': {'latitude': 39.7683331, 'longitude': -86.1583502, 'state': 'Indiana'},
    'JACKSON': {'latitude': 32.2998686, 'longitude': -90.1830408, 'state': 'Mississippi'},
    'JACKSONVILLE': {'latitude': 30.3321838, 'longitude': -81.655651, 'state': 'Florida'},
    'KANSAS CITY': {'latitude': 39.100105, 'longitude': -94.5781416, 'state': 'Missouri'},
    'KNOXVILLE': {'latitude': 35.9603948, 'longitude': -83.9210261, 'state': 'Tennessee'},
    'LANSING': {'latitude': 42.7337712, 'longitude': -84.5553805, 'state': 'Michigan'},
    'LAS VEGAS': {'latitude': 36.1672559, 'longitude': -115.148516, 'state': 'Nevada'},
    'LITTLE ROCK': {'latitude': 34.7465071, 'longitude': -92.2896267, 'state': 'Arkansas'},
    'LOS ANGELES': {'latitude': 34.0536909, 'longitude': -118.242766, 'state': 'California'},
    'LOUISVILLE': {'latitude': 38.2542376, 'longitude': -85.759407, 'state': 'Kentucky'},
    'LUBBOCK': {'latitude': 33.5855677, 'longitude': -101.8470215, 'state': 'Texas'},
    'MADISON': {'latitude': 43.074761, 'longitude': -89.3837613, 'state': 'Wisconsin'},
    'MANCHESTER': {'latitude': 42.9956397, 'longitude': -71.4547891, 'state': 'New Hampshire'},
    'MEMPHIS': {'latitude': 35.1460249, 'longitude': -90.0517638, 'state': 'Tennessee'},
    'MIAMI': {'latitude': 25.7741728, 'longitude': -80.19362, 'state': 'Florida'},
    'MILWAUKEE': {'latitude': 43.0386475, 'longitude': -87.9090751, 'state': 'Wisconsin'},
    'MINNEAPOLIS': {'latitude': 44.9772995, 'longitude': -93.2654692, 'state': 'Minnesota'},
    'MOBILE': {'latitude': 30.6913462, 'longitude': -88.0437509, 'state': 'Alabama'},
    'MONTGOMERY': {'latitude': 32.3669656, 'longitude': -86.3006485, 'state': 'Alabama'},
    'NASHVILLE': {'latitude': 36.1622767, 'longitude': -86.7742984, 'state': 'Tennessee'},
    'NEW BEDFORD': {'latitude': 41.6362152, 'longitude': -70.934205, 'state': 'Massachusetts'},
    'NEW BRUNSWICK': {'latitude': 40.4862174, 'longitude': -74.4518173, 'state': 'New Jersey'},
    'NEW HAVEN': {'latitude': 41.3082138, 'longitude': -72.9250518, 'state': 'Connecticut'},
    'NEW ORLEANS': {'latitude': 29.9759983, 'longitude': -90.0782127, 'state': 'Louisiana'},
    'NEW YORK': {'latitude': 40.7127281, 'longitude': -74.0060152, 'state': 'New York'},
    'NEWARK': {'latitude': 40.735657, 'longitude': -74.1723667, 'state': 'New Jersey'},
    'NORFOLK': {'latitude': 36.8448348, 'longitude': -76.2863999, 'state': 'Virginia'},
    'OKLAHOMA CITY': {'latitude': 35.4729886, 'longitude': -97.5170536, 'state': 'Oklahoma'},
    'OMAHA': {'latitude': 41.2587459, 'longitude': -95.9383758, 'state': 'Nebraska'},
    'ORLANDO': {'latitude': 28.5421109, 'longitude': -81.3790304, 'state': 'Florida'},
    'PENSACOLA': {'latitude': 30.421309, 'longitude': -87.2169149, 'state': 'Florida'},
    'PEORIA': {'latitude': 40.6938609, 'longitude': -89.5891008, 'state': 'Illinois'},
    'PHILADELPHIA': {'latitude': 39.9527237, 'longitude': -75.1635262, 'state': 'Pennsylvania'},
    'PHOENIX': {'latitude': 33.4484367, 'longitude': -112.074141, 'state': 'Arizona'},
    'PITTSBURGH': {'latitude': 40.4416941, 'longitude': -79.9900861, 'state': 'Pennsylvania'},
    'PORTLAND (OR)': {'latitude': 45.5202471, 'longitude': -122.674194, 'state': 'Oregon'},
    'PORTLAND (ME)': {'latitude': 43.661471, 'longitude': -70.255325, 'state': 'Maine'},
    'PROVIDENCE': {'latitude': 41.8239891, 'longitude': -71.4128343, 'state': 'Rhode Island'},
    'RALEIGH': {'latitude': 35.7803977, 'longitude': -78.6390989, 'state': 'North Carolina'},
    'READING': {'latitude': 40.335345, 'longitude': -75.9279495, 'state': 'Pennsylvania'},
    'RENO': {'latitude': 39.5261206, 'longitude': -119.8126581, 'state': 'Nevada'},
    'RICHMOND': {'latitude': 37.5385087, 'longitude': -77.43428, 'state': 'Virginia'},
    'RIVERSIDE': {'latitude': 33.7219991, 'longitude': -116.0372472, 'state': 'California'},
    'ROCHESTER (NY)': {'latitude': 43.157285, 'longitude': -77.615214, 'state': 'New York'},
    'ROCHESTER (MN)': {'latitude': 44.0121, 'longitude': -92.4802, 'state': 'Minnesota'},
    'ROCK ISLAND': {'latitude': 41.4411786, 'longitude': -90.5766144, 'state': 'Illinois'},
    'ROCKFORD': {'latitude': 42.2713945, 'longitude': -89.093966, 'state': 'Illinois'},
    'SACRAMENTO': {'latitude': 38.5810606, 'longitude': -121.493895, 'state': 'California'},
    'SALT LAKE CITY': {'latitude': 40.7596198, 'longitude': -111.886797, 'state': 'Utah'},
    'SAN ANTONIO': {'latitude': 29.4246002, 'longitude': -98.4951405, 'state': 'Texas'},
    'SAN DIEGO': {'latitude': 32.7174202, 'longitude': -117.162772, 'state': 'California'},
    'SAN FRANCISCO': {'latitude': 37.7792588, 'longitude': -122.4193286, 'state': 'California'},
    'SAN JOSE': {'latitude': 37.3361663, 'longitude': -121.890591, 'state': 'California'},
    'SANTA BARBARA': {'latitude': 34.4221319, 'longitude': -119.702667, 'state': 'California'},
    'SANTA FE': {'latitude': 35.6876096, 'longitude': -105.938456, 'state': 'New Mexico'},
    'SAVANNAH': {'latitude': 32.0790074, 'longitude': -81.0921335, 'state': 'Georgia'},
    'SCHENECTADY': {'latitude': 42.8142432, 'longitude': -73.9395687, 'state': 'New York'},
    'SCRANTON': {'latitude': 41.4086874, 'longitude': -75.6621294, 'state': 'Pennsylvania'},
    'SEATTLE': {'latitude': 47.6038321, 'longitude': -122.330062, 'state': 'Washington'},
    'SHREVEPORT': {'latitude': 32.5135356, 'longitude': -93.7477839, 'state': 'Louisiana'},
    'SIOUX FALLS': {'latitude': 43.5476008, 'longitude': -96.7293629, 'state': 'South Dakota'},
    'SOUTH BEND': {'latitude': 41.6833813, 'longitude': -86.2500066, 'state': 'Indiana'},
    'SPARTANBURG': {'latitude': 34.9498007, 'longitude': -81.9320157, 'state': 'South Carolina'},
    'SPOKANE': {'latitude': 47.6571934, 'longitude': -117.42351, 'state': 'Washington'},
    'SPRINGFIELD': {'latitude': 42.101483, 'longitude': -72.589811, 'state': 'Massachusetts'},
    'ST LOUIS': {'latitude': 38.6280278, 'longitude': -90.1910154, 'state': 'Missouri'},
    'ST PAUL': {'latitude': 44.954445, 'longitude': -93.091301, 'state': 'Minnesota'},
    'STAMFORD': {'latitude': 41.0534302, 'longitude': -73.5387341, 'state': 'Connecticut'},
    'SYRACUSE': {'latitude': 43.0481221, 'longitude': -76.1474244, 'state': 'New York'},
    'TACOMA': {'latitude': 47.2455013, 'longitude': -122.438329, 'state': 'Washington'},
    'TALLAHASSEE': {'latitude': 30.4380832, 'longitude': -84.2809332, 'state': 'Florida'},
    'TAMPA': {'latitude': 27.9477595, 'longitude': -82.458444, 'state': 'Florida'},
    'TOLEDO': {'latitude': 41.6529143, 'longitude': -83.5378173, 'state': 'Ohio'},
    'TOPEKA': {'latitude': 39.049011, 'longitude': -95.677556, 'state': 'Kansas'},
    'TRENTON': {'latitude': 40.2203074, 'longitude': -74.7659, 'state': 'New Jersey'},
    'TUCSON': {'latitude': 32.2228765, 'longitude': -110.974847, 'state': 'Arizona'},
    'TULSA': {'latitude': 36.1563122, 'longitude': -95.9927516, 'state': 'Oklahoma'},
    'WASHINGTON DC': {'latitude': 38.8950368, 'longitude': -77.0365427, 'state': 'District of Columbia'},
    'WICHITA': {'latitude': 37.6922361, 'longitude': -97.3375448, 'state': 'Kansas'},
    'WILMINGTON': {'latitude': 39.7459468, 'longitude': -75.546589, 'state': 'Delaware'},
    'WORCESTER': {'latitude': 42.2625621, 'longitude': -71.8018877, 'state': 'Massachusetts'},
    'YORK': {'latitude': 39.962493, 'longitude': -76.7276989, 'state': 'Pennsylvania'},
    'YOUNGSTOWN': {'latitude': 41.1035786, 'longitude': -80.6520161, 'state': 'Ohio'},
}

# List of US states for dropdown
US_STATES = [
    "", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",
    "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
    "Washington", "West Virginia", "Wisconsin", "Wyoming"
]


def get_city_coordinates(city_name, state=None):
    """Get coordinates for a city using geocoding."""
    try:
        if state:
            query = f"{city_name}, {state}, USA"
        else:
            query = f"{city_name}, USA"
        
        location = geolocator.geocode(query, addressdetails=True, timeout=10)
        if location and location.raw.get('address'):
            address = location.raw['address']
            return {
                'latitude': location.latitude,
                'longitude': location.longitude,
                'state': address.get('state')
            }
    except GeocoderTimedOut:
        st.error(f"Geocoding timed out for '{city_name}'. Please try again.")
    except Exception as e:
        st.error(f"Error geocoding '{city_name}': {e}")
    return None


def find_nearest_tracked_city(input_city, input_state=None, same_state_only=True):
    """Find the nearest tracked city to an input city."""
    
    # Get coordinates for input city
    city_coords = get_city_coordinates(input_city, input_state)
    
    if not city_coords:
        return None
    
    input_coords = (city_coords['latitude'], city_coords['longitude'])
    input_city_state = input_state or city_coords.get('state')
    
    # Filter cities based on state preference
    search_expanded = False
    if same_state_only and input_city_state:
        input_state_lower = input_city_state.lower()
        valid_cities = {
            city: coords for city, coords in TRACKED_CITIES.items()
            if coords.get('state') and coords.get('state').lower() == input_state_lower
        }
        if not valid_cities:
            search_expanded = True
            valid_cities = TRACKED_CITIES
    else:
        valid_cities = TRACKED_CITIES
    
    # Calculate distances to all valid cities
    distances = []
    for city, coords in valid_cities.items():
        city_coords_tuple = (coords['latitude'], coords['longitude'])
        distance = geodesic(input_coords, city_coords_tuple).km
        distances.append({
            'city': city,
            'state': coords.get('state'),
            'distance_km': round(distance, 2),
            'distance_miles': round(distance * 0.621371, 2)
        })
    
    # Sort by distance
    distances.sort(key=lambda x: x['distance_km'])
    
    if distances:
        return {
            'input_city': input_city,
            'input_state': input_city_state,
            'input_coords': input_coords,
            'nearest': distances[0],
            'top_5': distances[:5],
            'search_expanded': search_expanded,
            'cities_searched': len(valid_cities)
        }
    
    return None


# App UI
st.title("📍 Find Nearest Tracked City")
st.markdown("Enter a city to find the nearest city from our tracked locations.")

st.divider()

# Input form
col1, col2 = st.columns(2)

with col1:
    city_input = st.text_input(
        "City Name",
        placeholder="e.g., Palo Alto",
        help="Enter the name of the city you want to search from"
    )

with col2:
    state_input = st.selectbox(
        "State (Optional)",
        options=US_STATES,
        help="Selecting a state improves geocoding accuracy"
    )

same_state_only = st.selectbox(
    "Search Same State First",
    options=[True, False],
    format_func=lambda x: "Yes - Prioritize cities in the same state" if x else "No - Search all states",
    help="If True, the search will first look for tracked cities in the same state before expanding to all states"
)

st.divider()

# Search button
if st.button("🔍 Find Nearest City", type="primary", use_container_width=True):
    if not city_input:
        st.warning("Please enter a city name.")
    else:
        with st.spinner("Searching..."):
            state = state_input if state_input else None
            result = find_nearest_tracked_city(city_input, state, same_state_only)
        
        if result:
            # Success message
            st.success("Search completed!")
            
            # Display input info
            st.subheader("📌 Your Input")
            input_col1, input_col2 = st.columns(2)
            with input_col1:
                st.metric("City", result['input_city'])
            with input_col2:
                st.metric("State", result['input_state'] or "Auto-detected")
            
            st.caption(f"Coordinates: ({result['input_coords'][0]:.4f}, {result['input_coords'][1]:.4f})")
            
            # Search info
            if result['search_expanded']:
                st.info(f"No tracked cities found in {result['input_state']}. Expanded search to all {result['cities_searched']} tracked cities.")
            else:
                st.info(f"Searched {result['cities_searched']} tracked cities.")
            
            st.divider()
            
            # Display nearest city result
            st.subheader("🎯 Nearest Tracked City")
            
            nearest = result['nearest']
            
            result_col1, result_col2, result_col3 = st.columns(3)
            with result_col1:
                st.metric("City", nearest['city'])
            with result_col2:
                st.metric("State", nearest['state'])
            with result_col3:
                st.metric("Distance", f"{nearest['distance_miles']:.1f} mi")
            
            st.divider()
            
            # Display top 5 nearest cities
            st.subheader("📊 Top 5 Nearest Tracked Cities")
            
            df = pd.DataFrame(result['top_5'])
            df.index = range(1, len(df) + 1)
            df.columns = ['City', 'State', 'Distance (km)', 'Distance (miles)']
            
            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "Distance (km)": st.column_config.NumberColumn(format="%.2f km"),
                    "Distance (miles)": st.column_config.NumberColumn(format="%.2f mi"),
                }
            )
        else:
            st.error("Could not find coordinates for the specified city. Please check the city name and try again.")

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This tool finds the nearest city from our list of **tracked cities** based on geographic distance.
    
    **How it works:**
    1. Enter a city name (and optionally state)
    2. Choose whether to prioritize same-state matches
    3. Click search to find the nearest tracked city
    
    **Same State First Option:**
    - **Yes**: First looks for tracked cities in the same state. If none found, expands to all states.
    - **No**: Searches all tracked cities regardless of state.
    """)
    
    st.divider()
    
    st.header("📋 Tracked Cities")
    st.markdown(f"We currently track **{len(TRACKED_CITIES)}** cities across the United States.")
    
    with st.expander("View All Tracked Cities"):
        # Create a simple list grouped by state
        cities_by_state = {}
        for city, data in TRACKED_CITIES.items():
            state = data['state']
            if state not in cities_by_state:
                cities_by_state[state] = []
            cities_by_state[state].append(city)
        
        for state in sorted(cities_by_state.keys()):
            st.markdown(f"**{state}**: {', '.join(sorted(cities_by_state[state]))}")