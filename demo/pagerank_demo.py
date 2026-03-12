from pyspark.sql import SparkSession
import re
import sys
import time

def compute_contribs(urls, rank):
    """Calculates URL contributions to the rank of other URLs."""
    num_urls = len(urls)
    for url in urls:
        yield (url, rank / num_urls)

def parse_neighbors(urls):
    """Parses a line of neighbors into (node, neighbor) pairs."""
    parts = re.split(r'\s+', urls)
    return parts[0], parts[1]

if __name__ == "__main__":
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("PySparkPageRank") \
        .getOrCreate()

    # Path to the data file
    file_path = "/opt/bitnami/spark/work/data/web-Google.txt"

    # Load data
    lines = spark.read.text(file_path).rdd.map(lambda r: r[0])
    links = lines.filter(lambda line: not line.startswith('#')) \
                 .map(parse_neighbors) \
                 .distinct() \
                 .groupByKey() \
                 .cache()

    # Initialize Ranks
    ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))

    # Number of iterations
    iterations = 10

    print(f"Starting PageRank calculation for {iterations} iterations...")

    for i in range(iterations):
        contribs = links.join(ranks).flatMap(
            lambda url_urls_rank: compute_contribs(url_urls_rank[1][0], url_urls_rank[1][1])
        )
        ranks = contribs.reduceByKey(lambda x, y: x + y).mapValues(lambda rank: rank * 0.85 + 0.15)
        print(f"Completed iteration {i + 1}")

    # Output top 100 ranked pages to a file
    output_path = "/opt/bitnami/spark/work/data/pagerank_results.txt"
    top_100 = ranks.sortBy(lambda x: x[1], ascending=False).take(100)
    
    print(f"\nWriting Top 100 Ranked Pages to {output_path}...")
    with open(output_path, "w") as f:
        f.write("Top 100 Ranked Pages:\n")
        for (link, rank) in top_100:
            f.write(f"Page ID: {link} - Rank: {rank:.4f}\n")
    
    print("\nTop 10 Ranked Pages (Preview):")
    for (link, rank) in top_100[:10]:
        print(f"Page ID: {link} - Rank: {rank:.4f}")

    try:
        time.sleep(120)
    except KeyboardInterrupt:
        print("\nĐã ngắt lệnh chờ.")

    spark.stop()
