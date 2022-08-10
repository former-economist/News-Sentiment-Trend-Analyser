// import { useHistory } from "react-router-dom";
import { useState } from "react";
import SearchForm from "./SearchForm";
// import SearchList from "./SearchList";
// import SearchResultList from "./SearchResultList";

// import Sentiment from "./Sentiment";

import styles from "./Homepage.module.css";
import SearchItem from "./SearchItem";

/**
 *
 * @param {} props
 * @returns A screen with a search item if a search has been made.
 */
const Homepage = (props) => {
  const [queries, setQueries] = useState([]);
  const [newResult, setNewResult] = useState({
    result: 1,
    sentiment: null,
    topic: null,
  });
  const [intro, setIntro] = useState(true);

  /**
   *
   * @param {Object} newData - Incoming data on Query object from API.
   */
  const addQuery = (newData) => {
    setQueries((prevQueries) => {
      return [...newData];
    });
  };

  /**
   *
   * @param {string} enteredQueryData - Input data from form.
   */
  async function fetchPostQueryHandler(enteredQueryData) {
    const queryData = {
      ...enteredQueryData,
    };
    const response = await fetch("/search/", {
      method: "POST",
      body: JSON.stringify(queryData),
      headers: {
        "Content-Type": "application/json",
        "autherisation-token": "",
      },
    });
    const data = await response.json();
    console.log(data);
    addQuery(data);
    setNewResult({ result: 0 });
    console.log(data);
  }

  console.log(queries[0]);

  return (
    <div >
      <header>
        <h1>Sentiment Trender</h1>
      </header>
      {intro && (
        <div className={`${styles.container}`}>
          <div className={`${styles.child}`}>
            <h2 className={`${styles.header}`}>Welcome to Sentiment Trender</h2>
            <p>
              We're a search engine for news articles that helps you figure out
              how the sentiment of the sentiment of article based on it's
              headline.
            </p>
          </div>
          <div className={`${styles.child}`}>
            <h3>All you have to do is</h3>
            <ul>
              <li>Input a topic you want to read about into the search.</li>
              <li>
                Wait a little bit while we find and analysis your results.
              </li>
              <li>
                Once were finished well show you the results and the weekly
                sentminent average for the topic.
              </li>
            </ul>
          </div>
          <h3>Add blocked word if you want to restrict it from the headlines</h3>
        </div>
      )}

      <section className={styles.SearchForm}>
        <SearchForm
          onSubmitQueryData={fetchPostQueryHandler}
          setNewIntro={setIntro}
        />
      </section>
      <section>
        {queries.length > 0 && (
          <SearchItem
            topic={queries[0].topic}
            searchResults={newResult}
            id={queries[0].query_id}
            setNewResults={setNewResult}
          />
        )}
        {/* <p>Search Result: Query</p>
        <div className={styles.positiveSentiment}></div>
        <ul className={styles.searchlist}>
          <li className={`${styles.article} ${styles.neutral}`}>
            <h2>
              <a
                href="https://www.bbc.co.uk/news/uk-politics-62150409"
                className={styles.Neutral}
                target="_blank"
                rel="noopener noreferrer"
              >
                headline of the news today is that css is annoying
              </a>
            </h2>

            <p>publisher</p>
            <p>date</p>
          </li>
        </ul> */}

        {/* <SearchList
          queries={queries}
          newResult={newResult}
          setNewResult={setNewResult}
        />

        {newResult.result === 0 && <p>Loading</p>}
        {newResult.result.length > 1 && <Sentiment newSentiment={newResult} />}
      </section>
      <section>
        {newResult.result.length > 1 && (
          <SearchResultList SearchResult={newResult} />
        )} */}
        {/* <div className={styles.listItem}>
          <p>Headline: {props.headline}</p>
          <p>Publisher: {props.publisher}</p>
          <p>Sentiment: {props.sentiment}</p>
        </div> */}
      </section>
    </div>
  );
};

export default Homepage;
