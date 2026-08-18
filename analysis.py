# ============================================================
# OLA DATA ANALYTICS PROJECT
# Exploratory Data Analysis using Python & Pandas
# ============================================================


# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 2. LOAD DATASET
# ============================================================

df = pd.read_csv("Bookings.csv")

print("\n" + "=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)

print("Dataset Shape:", df.shape)
print("Number of Rows:", df.shape[0])
print("Number of Columns:", df.shape[1])


# ============================================================
# 3. INITIAL DATA INSPECTION
# ============================================================

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nDuplicate Booking IDs:")
print(df["Booking_ID"].duplicated().sum())


# ============================================================
# 4. DATA CLEANING
# ============================================================

# Remove unnecessary columns
df = df.drop(
    columns=["Vehicle Images", "Unnamed: 20"],
    errors="ignore"
)

# Convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Convert Time to time format
df["Time"] = pd.to_datetime(
    df["Time"],
    format="%H:%M:%S"
).dt.time

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED")
print("=" * 60)

print("New Dataset Shape:", df.shape)

print("\nData Types After Conversion:")
print(df.dtypes)


# ============================================================
# 5. BASIC DATA VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("BASIC DATA VALIDATION")
print("=" * 60)

print("\nBooking Value Statistics:")
print(df["Booking_Value"].describe())

print("\nRide Distance Statistics:")
print(df["Ride_Distance"].describe())

print("\nDriver Rating Range:")
print(
    df["Driver_Ratings"].min(),
    "to",
    df["Driver_Ratings"].max()
)

print("\nCustomer Rating Range:")
print(
    df["Customer_Rating"].min(),
    "to",
    df["Customer_Rating"].max()
)


# ============================================================
# 6. FEATURE ENGINEERING
# ============================================================

# Booking hour
df["Booking_Hour"] = pd.to_datetime(
    df["Time"].astype(str),
    format="%H:%M:%S"
).dt.hour

# Day
df["Booking_Day"] = df["Date"].dt.day

# Day name
df["Booking_Day_Name"] = df["Date"].dt.day_name()

# Month
df["Booking_Month"] = df["Date"].dt.month

# Weekday / Weekend
df["Booking_Day_Type"] = df["Booking_Day_Name"].apply(
    lambda day: "Weekend"
    if day in ["Saturday", "Sunday"]
    else "Weekday"
)

# Successful booking indicator
df["Is_Successful"] = (
    df["Booking_Status"] == "Success"
).astype(int)

# Cancellation type
def get_cancellation_type(status):

    if status == "Canceled by Customer":
        return "Customer Cancellation"

    elif status == "Canceled by Driver":
        return "Driver Cancellation"

    elif status == "Driver Not Found":
        return "Driver Not Found"

    else:
        return "Success"


df["Cancellation_Type"] = df["Booking_Status"].apply(
    get_cancellation_type
)


print("\n" + "=" * 60)
print("FEATURE ENGINEERING COMPLETED")
print("=" * 60)

print(
    df[
        [
            "Date",
            "Time",
            "Booking_Hour",
            "Booking_Day",
            "Booking_Day_Name",
            "Booking_Month",
            "Booking_Day_Type",
            "Is_Successful",
            "Cancellation_Type"
        ]
    ].head()
)


# ============================================================
# 7. OVERALL BOOKING PERFORMANCE
# ============================================================

total_bookings = len(df)

successful_bookings = (
    df["Is_Successful"].sum()
)

unsuccessful_bookings = (
    total_bookings - successful_bookings
)

success_rate = (
    successful_bookings / total_bookings * 100
)

unsuccessful_rate = (
    unsuccessful_bookings / total_bookings * 100
)

print("\n" + "=" * 60)
print("OVERALL BOOKING PERFORMANCE")
print("=" * 60)

print("Total Bookings:", total_bookings)
print("Successful Bookings:", successful_bookings)
print("Unsuccessful Bookings:", unsuccessful_bookings)

print(
    "Success Rate:",
    round(success_rate, 2),
    "%"
)

print(
    "Unsuccessful Rate:",
    round(unsuccessful_rate, 2),
    "%"
)


# ============================================================
# 8. BOOKING STATUS ANALYSIS
# ============================================================

booking_status = df["Booking_Status"].value_counts()

booking_status_percentage = (
    df["Booking_Status"]
    .value_counts(normalize=True)
    * 100
)

print("\n" + "=" * 60)
print("BOOKING STATUS ANALYSIS")
print("=" * 60)

print(booking_status)

print("\nBooking Status Percentage:")
print(booking_status_percentage.round(2))


# ============================================================
# 9. TIME ANALYSIS
# ============================================================

hourly_bookings = (
    df["Booking_Hour"]
    .value_counts()
    .sort_index()
)

print("\n" + "=" * 60)
print("BOOKINGS BY HOUR")
print("=" * 60)

print(hourly_bookings)


# ============================================================
# 10. WEEKDAY VS WEEKEND ANALYSIS
# ============================================================

day_type_bookings = (
    df["Booking_Day_Type"]
    .value_counts()
)

day_type_percentage = (
    df["Booking_Day_Type"]
    .value_counts(normalize=True)
    * 100
)

success_by_day_type = (
    df.groupby("Booking_Day_Type")["Is_Successful"]
    .mean()
    * 100
)

print("\n" + "=" * 60)
print("WEEKDAY VS WEEKEND ANALYSIS")
print("=" * 60)

print(day_type_bookings)

print("\nPercentage:")
print(day_type_percentage.round(2))

print("\nSuccess Rate:")
print(success_by_day_type.round(2))


# ============================================================
# 11. VEHICLE ANALYSIS
# ============================================================

vehicle_bookings = (
    df["Vehicle_Type"]
    .value_counts()
)

revenue_by_vehicle = (
    df.groupby("Vehicle_Type")["Booking_Value"]
    .sum()
    .sort_values(ascending=False)
)

avg_value_by_vehicle = (
    df.groupby("Vehicle_Type")["Booking_Value"]
    .mean()
    .sort_values(ascending=False)
)

success_rate_by_vehicle = (
    df.groupby("Vehicle_Type")["Is_Successful"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

avg_distance_vehicle = (
    df.groupby("Vehicle_Type")["Ride_Distance"]
    .mean()
    .sort_values(ascending=False)
)

print("\n" + "=" * 60)
print("BOOKINGS BY VEHICLE TYPE")
print("=" * 60)

print(vehicle_bookings)

print("\n" + "=" * 60)
print("REVENUE BY VEHICLE TYPE")
print("=" * 60)

print(revenue_by_vehicle)

print("\n" + "=" * 60)
print("AVERAGE BOOKING VALUE BY VEHICLE TYPE")
print("=" * 60)

print(avg_value_by_vehicle.round(2))

print("\n" + "=" * 60)
print("SUCCESS RATE BY VEHICLE TYPE")
print("=" * 60)

print(success_rate_by_vehicle.round(2))

print("\n" + "=" * 60)
print("AVERAGE RIDE DISTANCE BY VEHICLE")
print("=" * 60)

print(avg_distance_vehicle.round(2))


# ============================================================
# 12. CUSTOMER CANCELLATION ANALYSIS
# ============================================================

customer_cancellations = (
    df["Canceled_Rides_by_Customer"]
    .dropna()
    .value_counts()
)

print("\n" + "=" * 60)
print("CUSTOMER CANCELLATION REASONS")
print("=" * 60)

print(customer_cancellations)


# ============================================================
# 13. DRIVER CANCELLATION ANALYSIS
# ============================================================

driver_cancellations = (
    df["Canceled_Rides_by_Driver"]
    .dropna()
    .value_counts()
)

print("\n" + "=" * 60)
print("DRIVER CANCELLATION REASONS")
print("=" * 60)

print(driver_cancellations)


# ============================================================
# 14. INCOMPLETE RIDE ANALYSIS
# ============================================================

incomplete_rides = (
    df["Incomplete_Rides"]
    .value_counts(dropna=False)
)

incomplete_reasons = (
    df["Incomplete_Rides_Reason"]
    .dropna()
    .value_counts()
)

print("\n" + "=" * 60)
print("INCOMPLETE RIDE ANALYSIS")
print("=" * 60)

print(incomplete_rides)

print("\nIncomplete Ride Reasons:")
print(incomplete_reasons)


# ============================================================
# 15. PAYMENT ANALYSIS
# ============================================================

payment_methods = (
    df["Payment_Method"]
    .dropna()
    .value_counts()
)

revenue_by_payment = (
    df.groupby("Payment_Method")["Booking_Value"]
    .sum()
    .sort_values(ascending=False)
)

avg_value_payment = (
    df.groupby("Payment_Method")["Booking_Value"]
    .mean()
    .sort_values(ascending=False)
)

print("\n" + "=" * 60)
print("PAYMENT METHOD ANALYSIS")
print("=" * 60)

print(payment_methods)

print("\nRevenue by Payment Method:")
print(revenue_by_payment)

print("\nAverage Booking Value by Payment Method:")
print(avg_value_payment.round(2))


# ============================================================
# 16. LOCATION ANALYSIS
# ============================================================

top_pickup_locations = (
    df["Pickup_Location"]
    .value_counts()
    .head(10)
)

top_drop_locations = (
    df["Drop_Location"]
    .value_counts()
    .head(10)
)

print("\n" + "=" * 60)
print("TOP 10 PICKUP LOCATIONS")
print("=" * 60)

print(top_pickup_locations)

print("\n" + "=" * 60)
print("TOP 10 DROP LOCATIONS")
print("=" * 60)

print(top_drop_locations)


# ============================================================
# 17. REVENUE & RIDE ANALYSIS
# ============================================================

total_revenue = (
    df["Booking_Value"].sum()
)

average_booking_value = (
    df["Booking_Value"].mean()
)

success_by_hour = (
    df.groupby("Booking_Hour")["Is_Successful"]
    .mean()
    .mul(100)
)

print("\n" + "=" * 60)
print("OVERALL REVENUE ANALYSIS")
print("=" * 60)

print(
    "Total Booking Value:",
    total_revenue
)

print(
    "Average Booking Value:",
    round(average_booking_value, 2)
)

print("\nSuccess Rate by Hour:")
print(success_by_hour.round(2))


# ============================================================
# 18. RATINGS ANALYSIS
# ============================================================

average_driver_rating = (
    df["Driver_Ratings"].mean()
)

average_customer_rating = (
    df["Customer_Rating"].mean()
)

print("\n" + "=" * 60)
print("AVERAGE RATINGS")
print("=" * 60)

print(
    "Average Driver Rating:",
    round(average_driver_rating, 2)
)

print(
    "Average Customer Rating:",
    round(average_customer_rating, 2)
)


# ============================================================
# 19. VISUALIZATIONS
# ============================================================

print("\n" + "=" * 60)
print("GENERATING VISUALIZATIONS")
print("=" * 60)


# ------------------------------------------------------------
# Chart 1: Booking Status
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

booking_status.plot(kind="bar")

plt.title("Booking Status Distribution")
plt.xlabel("Booking Status")
plt.ylabel("Number of Bookings")

plt.xticks(rotation=20)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Chart 2: Bookings by Hour
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

hourly_bookings.plot(
    kind="line",
    marker="o"
)

plt.title("Bookings by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Bookings")

plt.xticks(range(24))
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Chart 3: Weekday vs Weekend
# ------------------------------------------------------------

plt.figure(figsize=(7, 5))

day_type_bookings.plot(kind="bar")

plt.title("Weekday vs Weekend Bookings")
plt.xlabel("Day Type")
plt.ylabel("Number of Bookings")

plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Chart 4: Customer Cancellation Reasons
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

customer_cancellations.sort_values().plot(
    kind="barh"
)

plt.title("Customer Cancellation Reasons")
plt.xlabel("Number of Cancellations")
plt.ylabel("Reason")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Chart 5: Driver Cancellation Reasons
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

driver_cancellations.sort_values().plot(
    kind="barh"
)

plt.title("Driver Cancellation Reasons")
plt.xlabel("Number of Cancellations")
plt.ylabel("Reason")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Chart 6: Success Rate by Vehicle Type
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

success_rate_by_vehicle.sort_values().plot(
    kind="barh"
)

plt.title("Success Rate by Vehicle Type")
plt.xlabel("Success Rate (%)")
plt.ylabel("Vehicle Type")

plt.tight_layout()
plt.show()


# ============================================================
# 20. SAVE CLEANED DATASET
# ============================================================

df.to_csv(
    "Bookings_Cleaned.csv",
    index=False
)

print("\n" + "=" * 60)
print("PROJECT COMPLETED SUCCESSFULLY")
print("=" * 60)

print(
    "Cleaned dataset saved as: Bookings_Cleaned.csv"
)

print(
    "Final Dataset Shape:",
    df.shape
)