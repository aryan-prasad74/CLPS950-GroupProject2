

# Mood Badge (Pie Chart)
# Define mood categories
positive = sum(1 for score in compound_scores if score > 0.05)
neutral = sum(1 for score in compound_scores if -0.05 <= score <= 0.05)
negative = sum(1 for score in compound_scores if score < -0.05)

# Data for pie chart
labels = ['Positive', 'Neutral', 'Negative']
sizes = [positive, neutral, negative]
colors = ['green', 'grey', 'red']

# Create pie chart
sns.set(style = "whitegrid") 
fig, axs = plt.subplots(2, 1, figsize = (12, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Mood Distribution in Final Playlist')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


# Plotting mood over time (Using data from CSV File)
df = pd.read_csv('playlist_history.csv', names=['Timestamp', 'Average_Score'])
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.sort_values('Timestamp', inplace=True)

plt.plot(df['Timestamp'], df['Average_Score'], marker='o', linestyle='-')
plt.title('Average Sentiment Score Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Average Sentiment Score')
plt.grid(True)

plt.tight_layout()
plt.show()