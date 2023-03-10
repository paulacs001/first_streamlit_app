import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')
  
streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg') 
streamlit.text('🥑🍞Avo Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
sel = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
to_show = my_fruit_list.loc[sel]

# Display the table on the page.
streamlit.dataframe(to_show)


def get_fruityvice_data(choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
     streamlit.error('Select a fruit')
  else:
    res = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(res)
    
except URLError as e:
  streamlit.error()

 ####################
streamlit.header("View and add in our fruit list!")
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

def get_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return  my_cur.fetchall()
  
if streamlit.button('Load'):
  my_data_row = get_list()
  my_cnx.close()
  streamlit.dataframe(my_data_row)

  
def insert_row(fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('"+ fruit +"')")
    return "Thank for adding " + fruit
 


add_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add fruit'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  res = insert_row(add_fruit)
  streamlit.text(res)
  
  
  
streamlit.stop()  





