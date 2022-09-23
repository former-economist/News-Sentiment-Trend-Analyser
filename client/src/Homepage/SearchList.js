import SearchItem from "./SearchItem";
import styles from "./SearchList.module.css";

const SearchList = (props) => {
  /**
   * Fetch results data for search topic.
   * @param {int} id Id of search topic.
   */
  function fetchResult(id) {
    let interval = setInterval(() => {
      const query_id = id;
      fetch(`/search/${query_id}`, {
        method: "GET",
      })
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          const items = data;
          props.setNewResult(items);
        });
    }, 30000);
    if (props.newResult.result.length > 1) {
      clearInterval(interval);
    }
  }

  return (
    <u className={styles.searchlist}>
      {props.queries.map((query) => (
        <SearchItem
          key={query.query_id}
          topic={query.topic}
          sentiment={query.sentiment}
          id={query.query_id}
          findResults={fetchResult}
        />
      ))}
    </u>
  );
};

export default SearchList;
