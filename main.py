from dataframes.dataframe_generator import DataFrame
from multiprocessing import Process


def main(q, after, before, sources):
    df = DataFrame(q, after, before, sources)
    print(df.dataframe)
    df.save_to_csv()


if __name__ == "__main__":
    stocks = ["AMC"]
    start = "01-12-2022"
    end = "07-12-2022"
    sources = ["reddit", "stocktwits", "twitter"]

    # create a process for each stock in the list
    threads = [Process(target=main, args=(stock, start, end, sources)) for stock in stocks]
    for thread in threads:
        thread.start()   # start them simultaneously
    for thread in threads:
        thread.join()   # wait for every process to be done before the program finishes
    print("Done.")
