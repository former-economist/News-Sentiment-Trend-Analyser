const SearchResult = (props) => {
    console.log(props)
  return (
    <li>
      <p>Headline: {props.headline}</p>
      <p>Publisher: {props.publisher}</p>
      <p>Sentiment: {props.sentiment}</p>
    </li>
  );
};

export default SearchResult;
