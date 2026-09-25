import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_name = "/Users/saschachodry/Desktop/tess_rocky_planets.xlsx"

df = pd.read_excel(
    file_name,
    sheet_name="Rocky TESS Planets"
)


def make_graph(column, earth_value, title, y_label):

    planets = df["Planet"]
    values = df[column]

    plt.figure(figsize=(14, 7))

    # Positions for every planet
    x = np.arange(len(planets))

    # Plot bars.
    # Missing values are temporarily changed to 0 so the planet
    # still has a position on the graph.
    graph_values = values.fillna(0)

    bars = plt.bar(x, graph_values)

    # Mark planets whose NASA data is missing
    for i in range(len(values)):
        if pd.isna(values.iloc[i]):
            plt.text(
                i,
                0,
                "No data",
                rotation=90,
                ha="center",
                va="bottom"
            )

    # Earth comparison line
    plt.axhline(
        y=earth_value,
        linestyle="--",
        label="Earth"
    )

    plt.title(title)
    plt.xlabel("Planet")
    plt.ylabel(y_label)

    plt.xticks(
        x,
        planets,
        rotation=45,
        ha="right"
    )

    plt.legend()

    plt.tight_layout()
    plt.show()


# Radius
make_graph(
    "Radius (Earth=1)",
    1,
    "Planet Radius Compared to Earth",
    "Radius (Earth Radii)"
)


# Mass
make_graph(
    "Mass (Earth=1)",
    1,
    "Planet Mass Compared to Earth",
    "Mass (Earth Masses)"
)


# Density
make_graph(
    "Density (g/cm³)",
    5.51,
    "Planet Density Compared to Earth",
    "Density (g/cm³)"
)


# Temperature
make_graph(
    "Equilibrium Temp (K)",
    255,
    "Planet Equilibrium Temperature Compared to Earth",
    "Equilibrium Temperature (K)"
)


# Insolation
make_graph(
    "Insolation (Earth=1)",
    1,
    "Planet Insolation Compared to Earth",
    "Insolation (Earth = 1)"
)


# Orbital Period
make_graph(
    "Orbital Period (days)",
    365.25,
    "Planet Orbital Period Compared to Earth",
    "Orbital Period (Days)"
)



def similarity(value, earth_value):
    difference = abs(value - earth_value)

    score = 100 * (1 - difference / earth_value)

    if score < 0:
        score = 0

    return score


def make_percentage_graph(column, earth_value, title):

    planets = df["Planet"]
    values = df[column]

    similarity_scores = []

    for value in values:
        if pd.isna(value):
            similarity_scores.append(np.nan)
        else:
            similarity_scores.append(similarity(value, earth_value))

    plt.figure(figsize=(14, 7))

    x = np.arange(len(planets))

    # Use 0 only for graph placement.
    # Missing values are still labeled as "No data".
    graph_values = [
        0 if pd.isna(score) else score
        for score in similarity_scores
    ]

    plt.bar(x, graph_values)

    for i in range(len(similarity_scores)):
        if pd.isna(similarity_scores[i]):
            plt.text(
                i,
                2,
                "Not calculable",
                rotation=90,
                ha="center",
                va="bottom"
            )

        # Similarity was calculated, but equals 0%
        elif similarity_scores[i] == 0:
            plt.text(
                i, 2,
                "0%",
                ha="center",
                va="bottom"
            )

    # Earth is always 100% similar to itself
    plt.axhline(
        y=100,
        linestyle="--",
        label="Earth"
    )

    plt.title(title)
    plt.xlabel("Planet")
    plt.ylabel("Similarity to Earth (%)")

    plt.ylim(0, 105)

    plt.xticks(
        x,
        planets,
        rotation=45,
        ha="right"
    )

    plt.legend()

    plt.tight_layout()
    plt.show()


# Radius similarity
make_percentage_graph(
    "Radius (Earth=1)",
    1,
    "Radius Similarity to Earth"
)


# Mass similarity
make_percentage_graph(
    "Mass (Earth=1)",
    1,
    "Mass Similarity to Earth"
)


# Density similarity
make_percentage_graph(
    "Density (g/cm³)",
    5.51,
    "Density Similarity to Earth"
)


# Equilibrium temperature similarity
make_percentage_graph(
    "Equilibrium Temp (K)",
    255,
    "Equilibrium Temperature Similarity to Earth"
)


# Insolation similarity
make_percentage_graph(
    "Insolation (Earth=1)",
    1,
    "Insolation Similarity to Earth"
)


# Orbital period similarity
make_percentage_graph(
    "Orbital Period (days)",
    365.25,
    "Orbital Period Similarity to Earth"
)


def total_similarity(row):

    scores = []

    # Radius similarity
    if not pd.isna(row["Radius (Earth=1)"]):
        scores.append(
            similarity(row["Radius (Earth=1)"], 1)
        )

    # Density similarity
    if not pd.isna(row["Density (g/cm³)"]):
        scores.append(
            similarity(row["Density (g/cm³)"], 5.51)
        )

    # Equilibrium temperature similarity
    if not pd.isna(row["Equilibrium Temp (K)"]):
        scores.append(
            similarity(row["Equilibrium Temp (K)"], 255)
        )

    # Insolation similarity
    if not pd.isna(row["Insolation (Earth=1)"]):
        scores.append(
            similarity(row["Insolation (Earth=1)"], 1)
        )

    # Average only the criteria that have data
    if len(scores) > 0:
        return sum(scores) / len(scores)

    return np.nan


df["Total Similarity (%)"] = df.apply(
    total_similarity,
    axis=1
)


def make_total_similarity_graph():

    planets = df["Planet"]
    scores = df["Total Similarity (%)"]

    x = np.arange(len(planets))

    plt.figure(figsize=(14, 7))

    plt.bar(x, scores)

    # Earth reference
    plt.axhline(
        y=100,
        linestyle="--",
        label="Earth"
    )

    # Percentage above each bar
    for i in range(len(scores)):

        if not pd.isna(scores.iloc[i]):

            plt.text(
                i,
                scores.iloc[i] + 1,
                str(round(scores.iloc[i], 1)) + "%",
                ha="center"
            )

    plt.title(
        "Overall Earth Similarity of Rocky TESS Exoplanets"
    )

    plt.xlabel("Planet")
    plt.ylabel("Average Similarity to Earth (%)")

    plt.ylim(0, 110)

    plt.xticks(
        x,
        planets,
        rotation=45,
        ha="right"
    )

    plt.legend()

    plt.tight_layout()
    plt.show()


make_total_similarity_graph()


def environmental_similarity(row):

    values = [
        similarity(row["Radius (Earth=1)"], 1),
        similarity(row["Density (g/cm³)"], 5.51),
        similarity(row["Equilibrium Temp (K)"], 255),
        similarity(row["Insolation (Earth=1)"], 1)
    ]

    weights = [
        0.15,   # Radius
        0.15,   # Density
        0.35,   # Temperature
        0.35    # Insolation
    ]

    total = 0
    available_weight = 0
    available_count = 0

    for value, weight in zip(values, weights):

        if not pd.isna(value):
            total += value * weight
            available_weight += weight
            available_count += 1

    # Need at least 3 of the 4 measurements
    if available_count < 3:
        return np.nan

    # Renormalize based on available measurements
    return total / available_weight


df["Environmental Similarity (%)"] = df.apply(
    environmental_similarity,
    axis=1
)



def physical_similarity(row):

    values = [
        similarity(row["Radius (Earth=1)"], 1),
        similarity(row["Density (g/cm³)"], 5.51),
        similarity(row["Equilibrium Temp (K)"], 255),
        similarity(row["Insolation (Earth=1)"], 1)
    ]

    weights = [
        0.35,   # Radius
        0.35,   # Density
        0.15,   # Temperature
        0.15    # Insolation
    ]

    total = 0
    available_weight = 0
    available_count = 0

    for value, weight in zip(values, weights):

        if not pd.isna(value):
            total += value * weight
            available_weight += weight
            available_count += 1

    # Need at least 3 of the 4 measurements
    if available_count < 3:
        return np.nan

    # Renormalize based on available measurements
    return total / available_weight


df["Physical Similarity (%)"] = df.apply(
    physical_similarity,
    axis=1
)



def make_model_graph(column, title):

    planets = df["Planet"]
    scores = df[column]

    x = np.arange(len(planets))

    plt.figure(figsize=(14, 7))

    # Replace NaN with 0 only for graph display
    graph_values = [
        0 if pd.isna(score) else score
        for score in scores
    ]

    plt.bar(x, graph_values)

    plt.axhline(
        y=100,
        linestyle="--",
        label="Earth"
    )

    # Display scores or "Not calculable"
    for i in range(len(scores)):

        if pd.isna(scores.iloc[i]):

            plt.text(
                i,
                2,
                "Not calculable",
                rotation=90,
                ha="center",
                va="bottom"
            )

        else:

            plt.text(
                i,
                scores.iloc[i] + 1,
                str(round(scores.iloc[i], 1)) + "%",
                ha="center"
            )

    plt.title(title)
    plt.xlabel("Planet")
    plt.ylabel("Similarity to Earth (%)")

    plt.ylim(0, 110)

    plt.xticks(
        x,
        planets,
        rotation=45,
        ha="right"
    )

    plt.legend()

    plt.tight_layout()
    plt.show()



make_model_graph(
    "Environmental Similarity (%)",
    "Earth Similarity — Environmental Emphasis"
)


make_model_graph(
    "Physical Similarity (%)",
    "Earth Similarity — Physical Emphasis"
)