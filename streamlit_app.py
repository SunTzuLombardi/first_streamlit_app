import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Parents Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


#imprt pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#add a picklist
fruits_selected = streamlit.multiselect("Pick some Fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)


#create function
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

#NEW SECTIOn to display fruityapi response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like info about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit.")
  else:
    back_from_funtion = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_funtion)
    
    
except URLError as e:
  streamlit.error()



#dont do below until we troubleshoot
streamlit.stop()

#import snowflake connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The Fruit load list contains:")
streamlit.dataframe(my_data_rows)

#NEW SECTIOn to display fruityapi response
fruit_choice2 = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for entering',fruit_choice2)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")





