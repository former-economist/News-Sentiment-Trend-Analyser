import { useEffect } from "react";
import styles from "./SearchItem.module.css";
import SearchResultList from "./SearchResultList";

import Sentiment from "./Sentiment";

const SearchItem = (props) => {
  const { topic, searchResults, setNewResults, id, setServer} = props;
  console.log(props.topic);
  // console.log(props.sentiment)
  // const {findResults, id, topic} = props;
  // useEffect(()=>{
  //     findResults(id)
  // },[id])

//   function fetchResult(id) {
//     let interval = setInterval(() => {
//       console.log(id);
//       const query_id = id;
//       fetch(`/search/${query_id}`, {
//         method: "GET",
//       })
//         .then((res) => {
//           return res.json();
//         })
//         .then((data) => {
//           const items = data;
//           setNewResult(items);
//         });
//     }, 30000);
//     if (newResult.result.length > 1) {
//       clearInterval(interval);
//       console.log("STOPPED");
//     }
//   }
    console.log(searchResults)
  /**
   * Fetches data every ten Query results from API every ten seconds.
   */
  useEffect(() => {
      let interval = setInterval(() => {
        console.log(id);
        const query_id = id;
        fetch(`/search/${query_id}`, {
          method: "GET",
        })
          .then((res) => {
            return res.json();
          })
          .then((data) => {
            const items = data;
            setNewResults(items);
          })
          .catch((err) => {
            setServer(false)
          })
      }, 10000);
      return () => {
        clearInterval(interval);
       };
  }, [setNewResults, id, setServer]);

  return (
    <>
      <h3 className={styles.searchitem}>Searching for: {topic}</h3>
      {searchResults.result === 'None' && <p>Could not find articles relating to search</p>}
      {searchResults.result === 0 && <div className={styles.loadAnimation}></div>}
      {/* {searchResults.result === 0 && <p className={styles.loading}>Loading</p>} */}
      {searchResults.result.length > 1 && searchResults.result !== 'None' && <Sentiment newSentiment={searchResults} />}
      {searchResults.result.length > 1 && searchResults.result !== 'None' && (
        <SearchResultList SearchResult={searchResults} />
      )}
    </>
  );
};

export default SearchItem;
