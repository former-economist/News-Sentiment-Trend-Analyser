// import { useHistory } from "react-router-dom";
import { useState } from "react";
import SearchForm from "./SearchForm";
// import SearchList from "./SearchList";
// import SearchResultList from "./SearchResultList";

// import Sentiment from "./Sentiment";

import styles from "./Homepage.module.css";
import SearchItem from "./SearchItem";

const Homepage = (props) => {
  const [queries, setQueries] = useState([]);
  const [newResult, setNewResult] = useState({
    result: 1,
    sentiment: null,
    topic: null,
  });

  const addQuery = (newData) => {
    setQueries((prevQueries) => {
      return [...newData];
    });
  };
  // const navgation = useHistory
  async function fetchPostQueryHandler(enteredQueryData) {
    const queryData = {
      ...enteredQueryData,
    };
    const response = await fetch("/search/", {
      method: "POST",
      body: JSON.stringify(queryData),
      headers: {
        "Content-Type": "application/json",
        "autherisation-token" : ""
      },
    });
    const data = await response.json();
    console.log(data);
    addQuery(data);
    setNewResult({ result: 0 });
    console.log(data);
    //   navgation.push({pathname='/results',
    // state=})
  }

  console.log(queries[0]);

  return (
    <div className={styles.container}>
      <header>
        <h1>Sentiment Trender</h1>
      </header>
      <section className={styles.SearchForm}>
        <SearchForm onSubmitQueryData={fetchPostQueryHandler} />
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
