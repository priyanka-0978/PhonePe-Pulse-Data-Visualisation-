import streamlit as st
import pandas as pd
import PIL 
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px
import mysql.connector 

# Setting up page configuration
icon = Image.open(r"C:\Users\Priyanka\Downloads\phone_pe.png")
st.set_page_config(page_title= "PhonePe Pulse Data Visualization and Exploration",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About':"This dashboard app is created by Priyanka Pal!"}
                   )

#-----------------------------------------------Creating dashboard-----------------#

st.sidebar.header(":violet[Hey! Welcome to the dashboard]")



with st.sidebar:
    selected = option_menu("Menu", ["Home","Basic Insights","Top Charts","Explore Data","About"], 
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})

#--------------------------------Connecting to Mysql--------------#

mydb = mysql.connector.connect(host="localhost",
                   user="root",
                   password="Priya1234",
                   database= "phone_pe",
                   port = "3306"
                  )
mycursor = mydb.cursor(buffered=True)

#--------------------------------------------------------------------------#
img=Image.open(r"C:\Users\Priyanka\Downloads\phone.png")


if selected == "Home":
    st.subheader(":violet[PhonePe Pulse Data Visualization and Exploration]")

    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.markdown(":green[PhonePe has become one of the most popular digital payment platforms in India, with millions of users relying on it for their day-to-day transactions. The app is known for its simplicity, user-friendly interface, and fast and secure payment processing. It has also won several awards and accolades for its innovative features and contributions to the digital payments industry.]")
        st.markdown(":blue[India's top fintech platform, announced the debut of PhonePe Pulse, India's first interactive website providing statistics, insights, and trends on digital payments in the country, on September 3, 2021. The PhonePe Pulse website displays over 2000 crores in customer transactions on an interactive map of India. PhonePe's data, with over 45% market share, is typical of the country's digital payment habits.]")

        st.markdown(":red[This web app is built to analyse the Phonepe transaction and users depending on various Years, Quarters, States, and Types of transaction and give a Geo visualization output based on given requirements.]")
    with col2:
         st.image(img)

#-------------------------------------------------Get some informtion from mysql data ---------------------------------------#
        

if selected == "Basic Insights":
    st.subheader(":red[BASIC INSIGHTS]")
    st.subheader(":green[Let's know some basic insights about the data]")
    options = ["--select--",
               "Top 10 States or Union Territory  based on transaction year and amount of transaction",
               "Top 10 Registered-users based on States or Union Territory and District",
               "Top 10 Districts based on States or Union Territory and Count of transaction",
               "Top 5 Transaction_Type based on Transaction_Amount",
               "List of 10 States or Union Territory based on District and Count of transaction",
               "List of 10 Transaction_Count based on Districts and States or Union Territory",
               "List of 10 States or Union Territory based on Transaction Type and Amount of transaction"]

    select = st.selectbox("Select the option",options)
    if select=="Top 10 States or Union Territory  based on transaction year and amount of transaction":
        mycursor.execute("SELECT DISTINCT States_OR_Union_Territory, Transaction_Year, SUM(Transaction_Amount) AS Total_Transaction_Amount FROM top_transaction GROUP BY States_OR_Union_Territory, Transaction_Year ORDER BY Total_Transaction_Amount DESC LIMIT 10");
        df=pd.DataFrame(mycursor.fetchall(), columns=['States_OR_Union_Territory','Transaction_Year', 'Transaction_Amount'])
        st.write(df)
    elif select=="Top 10 Registered-users based on States or Union Territory and District":
        mycursor.execute("SELECT DISTINCT States_OR_Union_Territory,District,SUM(RegisteredUsers) AS Registered_users FROM top_users GROUP BY States_OR_Union_Territory,District ORDER BY Registered_users DESC LIMIT 10");
        df=pd.DataFrame(mycursor.fetchall(), columns=['States_OR_Union_Territory','District','RegisteredUsers'])
        st.write(df)

    elif select=="Top 10 Districts based on States or Union Territory and Count of transaction":
        mycursor.execute("SELECT DISTINCT District,States_OR_Union_Territory,SUM(Transaction_Count) AS Transaction_Counts FROM top_transaction GROUP BY District,States_OR_Union_Territory ORDER BY Transaction_Counts DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['District','States_OR_Union_Territory','Transaction_Count'])

        st.write(df)

    elif select=="Top 5 Transaction_Type based on Transaction_Amount":
        mycursor.execute("SELECT DISTINCT Transaction_Type, SUM(Transaction_Amount) AS Transaction_amount FROM top_transaction GROUP BY Transaction_Type ORDER BY Transaction_amount  DESC LIMIT 5");
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_Type', 'Transaction_Amount'])
        st.write(df)

    elif select=="List of 10 States or Union Territory based on District and Count of transaction":
        mycursor.execute("SELECT DISTINCT States_OR_Union_Territory,District,SUM(Transaction_Count) AS Counts FROM map_transaction GROUP BY States_OR_Union_Territory,District ORDER BY Counts DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(), columns=['States_OR_Union_Territory','District','Transaction_Count'])
        st.write(df)

    elif select=="List of 10 Transaction_Count based on Districts and States or Union Territory":
        mycursor.execute("SELECT DISTINCT States_OR_Union_Territory , District, SUM(Transaction_Count) AS Counts FROM map_transaction GROUP BY States_OR_Union_Territory,District ORDER BY Counts ASC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['States_OR_Union_Territory ','District','Transaction_Count'])
        st.write(df)
    elif select=="List of 10 States or Union Territory based on Transaction Type and Amount of transaction":
        mycursor.execute("SELECT DISTINCT States_OR_Union_Territory,Transaction_Type, SUM(Transaction_Count) as Transaction_count FROM aggregated_transaction GROUP BY States_OR_Union_Territory,Transaction_Type ORDER BY Transaction_count DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['States_OR_Union_Territory ','Transaction_Type','Transaction_Count'])
        st.write(df)    
#-----------------------------------------------Top charts based on transaction and users data--------------------------------------------------------------#
if selected=="Top Charts":
    st.subheader(":green[Top Charts]")
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
   
    Year = st.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.slider("Quarter", min_value=1, max_value=4)
    

    if Type == "Transactions":
      with st.sidebar:
          a=st.checkbox("Top 10 State or Union_Territory based on Total number of transaction and Total amount spent on phonepe.")
          b=st.checkbox('Top 10 Transaction_Count based on Districts and States or Union Territory')
          c=st.checkbox('Top 10 Districts based on States or Union Territory and Count of transaction')
      if a:
        mycursor.execute(f"select States_OR_Union_Territory, sum(Transaction_Count) as Total_Transactions_Count, sum(Transaction_Amount) as Total from aggregated_transaction where Transaction_Year = {Year} and Quarters = {Quarter} group by States_OR_Union_Territory order by Total DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(), columns=['States_OR_Union_Territory', 'Transactions_Count','Transaction_Amount'])
        fig = px.pie(df, values='Transaction_Amount',
                     names='States_OR_Union_Territory',
                     color_discrete_sequence=px.colors.sequential.Agsunset)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
      if b:
        mycursor.execute(f'SELECT States_OR_Union_Territory,District,SUM(Transaction_Count) AS Counts FROM map_transaction where Transaction_Year = {Year} and Quarters = {Quarter} GROUP BY States_OR_Union_Territory,District ORDER BY Counts DESC LIMIT 10');
        df = pd.DataFrame(mycursor.fetchall(), columns=['States_OR_Union_Territory','District','Transaction_Count'])
        fig = px.pie(df, values='Transaction_Count',
                     names='States_OR_Union_Territory',
                     color_discrete_sequence=px.colors.sequential.Agsunset)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
      if c:
        mycursor.execute(f'SELECT DISTINCT District,States_OR_Union_Territory,SUM(Transaction_Count) AS Transaction_Counts FROM top_transaction where Transaction_Year = {Year} and Quarters = {Quarter}  GROUP BY District,States_OR_Union_Territory ORDER BY Transaction_Counts DESC LIMIT 10');
        df = pd.DataFrame(mycursor.fetchall(),columns=['District','States_OR_Union_Territory','Transaction_Count'])
        fig=px.bar(df,x="District",y="Transaction_Count",color = 'Transaction_Count', color_continuous_scale  = 'viridis')
        fig.update_traces(textposition='inside')
        st.plotly_chart(fig,use_container_width=True)

    if Type=='Users':
      with st.sidebar:
          a=st.checkbox("Top 10 Registered-users based on States or Union Territory.")
          b=st.checkbox('Top 10 District based on Registered _Users')
          c=st.checkbox('Top 10 states or Union Territory based on Phone-pe Appopens by users.')
      if a:
        mycursor.execute(f"SELECT States_OR_Union_Territory,District,SUM(RegisteredUsers) AS Registered_users FROM top_users where Transaction_Year = {Year} and Quarters = {Quarter} GROUP BY States_OR_Union_Territory,District ORDER BY Registered_users DESC LIMIT 10");
        df=pd.DataFrame(mycursor.fetchall(), columns=['States_OR_Union_Territory','District','RegisteredUsers'])
        fig = px.pie(df, values='RegisteredUsers',
                     names='States_OR_Union_Territory',
                     color_discrete_sequence=px.colors.sequential.Agsunset)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
      if b:
        mycursor.execute(f"SELECT distinct District,RegisteredUsers AS Registered_users FROM map_users where Transaction_Year = {Year} and Quarter = {Quarter} ORDER BY RegisteredUsers DESC LIMIT 10");
        df=pd.DataFrame(mycursor.fetchall(), columns=['District','RegisteredUsers'])
        fig = px.pie(df, values='RegisteredUsers',
                     names='District',
                     color_discrete_sequence=px.colors.sequential.Agsunset)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
      if c:
        if Year == 2018 and Quarter==1:
                 st.markdown(":green[Sorry No Data to Display for the year-2018 and quarter-1]")
                 st.markdown(":green[You can move the slider range & quarter range to view charts ]")
        else:
          mycursor.execute(f"SELECT States_OR_Union_Territory,sum(AppOpens) as App_users FROM aggregated_users where Transaction_Year = {Year} and Quarters = {Quarter} GROUP BY States_OR_Union_Territory ORDER BY App_users DESC LIMIT 10");
          df=pd.DataFrame(mycursor.fetchall(), columns=['States_OR_Union_Territory','AppOpens'])
          fig = px.bar(df,x='States_OR_Union_Territory',y='AppOpens',color = 'States_OR_Union_Territory',color_continuous_scale  = 'viridis')

          fig.update_traces(textposition='inside')
          st.plotly_chart(fig,use_container_width=True)


#---------------------------------creating chart to explore data statewise for various years and quarters based on transactions and users---------------#
if selected =="Explore Data":
    st.subheader(":blue[Explore Data]")
    with st.sidebar:
        Type = st.selectbox("**Type**", ("Transaction", "Users"))
   
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    st.markdown(" :red[Select any State to explore more]")
    selected_state = st.selectbox("",
                           ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                            'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                            'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                            'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                            'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                            'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
     
    if Type == "Transaction":
       st.write(":green[Explore overall state data based on transactions from various years and quarters.]")
       mycursor.execute(f"select States_OR_Union_Territory,Transaction_Year,Quarters,District,sum(Transaction_Count) as Total_Count, sum(Transaction_Amount) as Total_amount  from top_transaction where Transaction_Year  = {Year} and Quarters = {Quarter} and States_OR_Union_Territory = '{selected_state}' group by States_OR_Union_Territory  ,District,Transaction_Year,Quarters order by States_OR_Union_Territory ,District")
       df = pd.DataFrame(mycursor.fetchall(), columns=['States_OR_Union_Territory ','Transaction_Year', 'Quarters', 'District','Transaction_Count','Transaction_Amount'])
       fig = px.bar(df,
               title=selected_state,
               x="District",
               y="Transaction_Count",
               orientation='v',
               color='Transaction_Count',
               color_continuous_scale=px.colors.sequential.Agsunset)
       st.plotly_chart(fig,use_container_width=True)

    if Type == "Users":
      st.write(":green[Explore overall state data based on users from various years and quarters.]")


      mycursor.execute(f"select States_OR_Union_Territory,Transaction_Year,Quarter,District,sum(RegisteredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from map_users where Transaction_Year  = {Year} and Quarter = {Quarter} and States_OR_Union_Territory = '{selected_state}' group by States_OR_Union_Territory  , District,Transaction_Year,Quarter order by States_OR_Union_Territory ,District")

      df = pd.DataFrame(mycursor.fetchall(), columns=['States_OR_Union_Territory ','Transaction_Year', 'Quarter', 'District', 'RegisteredUsers','AppOpens'])

      fig = px.bar(df,
                   title=selected_state,
                   x="District",
                   y="RegisteredUsers",
                   orientation='v',
                   color='RegisteredUsers',
                  color_continuous_scale=px.colors.sequential.Agsunset)
      st.plotly_chart(fig,use_container_width=True)
#-----------------------------------------------------------------------------------------------#

if selected == "About":
    st.subheader(":red[About PhonePe]")
    st.markdown("India's top financial platform, PhonePe, has more than 300 million registered customers. Users of PhonePe can send and receive money, recharge mobile phones and DTH, pay for goods and services at merchant locations, purchase gold, and make investments.")
    
    st.subheader(":green[About Project:]")
    st.write("The website's insights and the report's findings were derived from two important sources: the whole transaction data of PhonePe and merchant and customer interviews. The report is freely downloadable from GitHub and the PhonePe Pulse website.")
    st.write("The outcome of this project is a complete and user-friendly solution for extracting, processing, and visualising data from the Phonepe pulse Github repository.")

    st.write(":violet[Gratitude for visiting and exploring this website!!!]")
    
   


    


        

     
 
       



























     


       

         
            




























             



     


    



















          

          












