import SearchItem from "./SearchItem";
import styles from "./SearchList.module.css";

const SearchList = (props) => {
  // async function fetchSentiment(id=query.query_id){
  //     setInterval(() => {
  //         const query_id = encodeURIComponent(props.id)
  //         const response = await fetch(`/search/${query_id}`, {
  //             method: 'GET',
  //             headers: {
  //                 'Content-Type': 'application/json'
  //             }
  //         });
  //         const newSentiment = response.json()
  //         props.setNewSentiment(newSentiment)
  //     }, 600000)
  // }

  function fetchResult(id) {
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
          props.setNewResult(items);
        });
    }, 30000);
    if ((props.newResult.result).length > 1) {
      clearInterval(interval);
      console.log("STOPPED");
    }
  }

  console.log(props.queries);
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
    // <>
    //   <SearchItem
    //     key={props.queries.query_id}
    //     topic={props.queries.topic}
    //     sentiment={props.queries.sentiment}
    //     checkSentiment={fetchResult(props.queries.query_id)}
    //   />
    // </>
  );
};

export default SearchList;
