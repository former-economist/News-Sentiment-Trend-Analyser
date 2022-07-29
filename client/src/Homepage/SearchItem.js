import { useEffect } from "react";
import styles from "./SearchItem.module.css";
import SearchResultList from "./SearchResultList";

import Sentiment from "./Sentiment";

const SearchItem = (props) => {
  const { topic, searchResults, setNewResults, id } = props;
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
        });
    }, 20000);
    return () => {
      clearInterval(interval);
     };
  }, [setNewResults, id]);

  return (
    <>
      <h3 className={styles.searchitem}>{topic}</h3>
      {searchResults.result === 0 && <p className={styles.loading}>Loading</p>}
      {searchResults.result.length > 1 && <Sentiment newSentiment={searchResults} />}
      {searchResults.result.length > 1 && (
        <SearchResultList SearchResult={searchResults} />
      )}
    </>
  );
};

export default SearchItem;
