import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import squarify

# Sample data (sizes of rectangles)
sizes = [500, 300, 200, 100]

# Labels for the rectangles (optional)
labels = ["A", "B", "C", "D"]

plt.figure(figsize=(15,7))
# Plotting the treemap
plt.subplot(1,3,1)
squarify.plot(sizes=sizes, label=labels, alpha=0.8, color=["red", "green", "blue", "grey"])
plt.title("LLM Representation Space")
plt.axis('off')  # Turn off axis
plt.subplot(1,3,2)
plt.plot([], [])
plt.xlim(0,10)
plt.ylim(0,10)
plt.axis("off")

# Draw an arrow from point (2, 1) to point (4, 3)
plt.annotate('', xy=(10, 5), xytext=(0, 5),
             arrowprops=dict(facecolor='black', shrink=0.05),ha="center", va="top")
plt.subplot(1,3,3)
sizes = [200, 600, 100, 400]

# Labels for the rectangles (optional)
labels = ["A", "B", "C", "D"]

# Plotting the treemap
squarify.plot(sizes=sizes, label=labels, alpha=0.8, color=["red", "green", "blue", "grey"])
plt.title("LLM Representation Space After a Prompt")
plt.axis('off')  # Turn off axis
plt.show()