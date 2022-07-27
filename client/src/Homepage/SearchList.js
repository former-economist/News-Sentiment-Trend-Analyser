import SearchItem from "./SearchItem";

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
      }).then((res) => {
        return res.json()
      }).then((data) => {
        const items = data
        console.log(items);
        props.setNewResult(items)
      });
    }, 30000);
      if(props.newResult.result !== 0){
          clearInterval(interval)
          console.log('STOPPED')
        };
  }

  console.log(props.queries);
  return (
    <u>
      {props.queries.map((query) => (
        <SearchItem
          key={query.query_id}
          topic={query.topic}
          sentiment={query.sentiment}
          checkSentiment={fetchResult(query.query_id)}
        />
      ))}
    </u>
  );
};

export default SearchList;
