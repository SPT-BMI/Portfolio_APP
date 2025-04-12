import streamlit as st
import pandas as pd
import math


st.sidebar.subheader("Contact me here")
st.info("I'm a passionate analyst dedicated to turning data into information and bridging the gap between technical and business teams for solutions that matter. I enjoy cross-functional teamwork to solve tough business problems and improve processes. Learning and self-improvement are cornerstones of both my work and personal life. ")

col1,col2,col3 =st.columns(3)
link = col1.link_button("LinkedIn", "https://www.linkedin.com/in/jermit-gunning-779a81172/")
link1 = col2.link_button("Portfolio", "https://sites.google.com/view/jermitgunning/home")
link3 = col3.link_button("Other Apps", "https://share.streamlit.io/user/spt-bmi")


tab1,tab2,tab3 = st.tabs(["📈Chart Data","🗃 Download Data", "Recomendations"])

   
#st.title("Loan Repayments Calculator")
#st.sidebar.header("test")



with tab1: 
    st.title("Loan Repayments Calculator")
    st.sidebar.header("You can contact me here")
    st.sidebar.columns(3)
#datar = [1,2,3,4]
#st.sidebar.add_rows(datar)

#st.sidebar.image("") #this is in code
#st.sidebar.add_rows("funk")

   
#add_selectbox = st.sidebar.selectbox(
    #"How would you like to be contacted?",
    #("Email", "Home phone", "Mobile phone")
#)

#st.sidebar.inf

#tab_title = ['Repayment Line Chart', 'Downloadable Schedule & Recomendation' ]

#tabs = st.tabs(tab_title)


with tab1:
#tab1, tab2 = st.tabs(['Mortgage App', 'Connect with me'])     
    st.info("Input your loans figures into each box and this app will calculate your monthly repayments and interest paid")
    st.write("### Input Data")
    col1, col2 = st.columns(2)
    home_value = col1.number_input("Purchase Value", min_value=0, value=300000)
    deposit = col1.number_input("Deposit", min_value=0, value=100000)
    interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.0, value=1.0, max_value=10.0)
    loan_term = col2.number_input("Loan Term (in years)", min_value=1, value=30)

# Calculate the repayments.
    loan_amount = home_value - deposit
    monthly_interest_rate = (interest_rate / 100) / 12
    number_of_payments = loan_term * 12
    monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
    )

# Display the repayments.
    total_payments = monthly_payment * number_of_payments
    total_interest = total_payments - loan_amount

    st.write("### Repayments")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")
    col2.metric(label="Total Repayments", value=f"${total_payments:,.0f}")
    col3.metric(label="Total Interest", value=f"${total_interest:,.0f}")




# Create a data-frame with the payment schedule.
    schedule = []
    remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)  # Calculate the year into the loan
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )


with tab1:
    df1 = pd.DataFrame(
        schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
    )

# Display the data-frame as a chart.
    st.write("### Payment Schedule")
    payments_df = df1[["Year", "Remaining Balance"]].groupby("Year").min()
    st.line_chart(payments_df)

with tab2:
#print(df)
    st.info("Detailed Breakdown Below")
    st.dataframe(df1)



with tab3:


    st.header("Generated Recommendations")
    st.info("Based on your inputs above we have generated some insights for you below")

    #interest_rate
def interest_helper(interest_rate):
    if interest_rate >= 8:
        st.write("An interest rate of" f" {interest_rate}% is considered high, consider refinancing or imporving credit for better deals")
    elif interest_rate < 5:
        st.write( f"{interest_rate}% is an exceptional rate in todays loan environment")

with tab3:
    st.subheader("As far as your interest rate is concerned:")
    st.write(interest_helper(interest_rate))



##Percent down 
def DP_helper (deposit): 
        if (deposit/home_value) < .2:
            st.write("Consider putting down a larger deposit if possible, this will lower the amount you pay in interest")
        elif (deposit/home_value) > .2:
            st.write("Good job putting down a hefty downpayment, this will mean less interest over time")

with tab3:
    st.subheader(f"Concerning on your deposit of ${deposit}:")
    st.write(DP_helper(deposit))


with tab3:
    st.subheader("Below are resources to learn more about loans/finance")
    url = "https://www.investopedia.com/terms/l/loan.asp"
    url2 = "https://www.investopedia.com/terms/r/refinance.asp"
    url3 = "https://www.investopedia.com"
    st.write(f"Basic info on loans [here](%s)" % url)
    st.write(f"Basic info on refinancing [here](%s)" % url2)
    st.write(f" Investopedia [here](%s)" % url3)
    
   
#st.header(f"{x}: Now that you have a name lets choose a powertrain")

#y = zerotosixty
#if y <2.5:
    #st.write("Ferrari - You have a thing for speed huh?")
#else:
    #st.write("PT Cruiser - Well maybe you won't get there soon but you'll get there")

#st.write(helper)
#else: 
   # print("Deppreciation Monster")

#st.write('Based off your inputs we')


@st.cache_data
def get_data():
    df = df1
    return df

@st.cache_data
def convert_for_download(df):
    return df.to_csv().encode("utf-8")

df = get_data()
csv = convert_for_download(df)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="Payments.csv",
    mime="text/csv",
    icon=":material/download:",
)
