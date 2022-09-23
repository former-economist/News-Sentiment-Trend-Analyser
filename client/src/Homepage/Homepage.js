import { useState } from "react";
import SearchForm from "./SearchForm";

import styles from "./Homepage.module.css";
import SearchItem from "./SearchItem";


const Homepage = (props) => {
  const [queries, setQueries] = useState([]);
  const [newResult, setNewResult] = useState({
    result: 1,
    sentiment: null,
    topic: null,
  });
  const [intro, setIntro] = useState(true);
  const [serverRunning, setServerRunning] = useState(true);

  /**
   * Add query to state.
   * @param {Object} newData - Incoming data on Query object from API.
   */
  const addQuery = (newData) => {
    setQueries((prevQueries) => {
      return [...newData];
    });
  };

  /**
   * Fetch query data from API.
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

    addQuery(data);
    setNewResult({ result: 0 });
  }

  return (
    <div>
      <header>
        <h1>Sentiment Trender</h1>
      </header>
      {intro && (
        <div className={`${styles.container}`}>
          <div className={`${styles.child}`}>
            <h2 className={`${styles.header}`}>Welcome to Sentiment Trender</h2>
            <p className={`${styles.paragraphs}`}>
              We're a search engine for news articles that helps you figure out
              how the sentiment of the sentiment of article based on it's
              headline.
            </p>
          </div>
          <div className={`${styles.child}`}>
            <h3 className={`${styles.header3}`}>All you have to do is</h3>
            <ul>
              <li className={`${styles.liItem}`}>
                Input a topic you want to read about into the search.
              </li>
              <li className={`${styles.liItem}`}>
                Wait a little bit while we find and analysis your results.
              </li>
              <li className={`${styles.liItem}`}>
                Results and the weekly sentminent average for the topic will
                show below.
              </li>
            </ul>
          </div>
          <h3 className={`${styles.header3}`}>
            Add blocked word if you want to restrict it from the headlines
          </h3>
        </div>
      )}

      <section className={styles.SearchForm}>
        <SearchForm
          onSubmitQueryData={fetchPostQueryHandler}
          setNewIntro={setIntro}
          setServer={setServerRunning}
        />
      </section>
      <section>
        <div className={`${styles.container}`}>
          {!serverRunning && (
            <p className={`${styles.paragraphs}`}>
              Oh no we've lost connection to the server
            </p>
          )}
        </div>

        {queries.length > 0 && serverRunning && (
          <SearchItem
            topic={queries[0].topic}
            searchResults={newResult}
            id={queries[0].query_id}
            setNewResults={setNewResult}
            setServer={setServerRunning}
          />
        )}
      </section>
    </div>
  );
};

export default Homepage;
