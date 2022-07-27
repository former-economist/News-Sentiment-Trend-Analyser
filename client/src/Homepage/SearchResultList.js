import SearchResult from "./SearchResult";

const SearchResultList = (props) => {
  console.log(props.SearchResult);
  return (
    <u>
      {props.SearchResult.result.map((finding) => (
        <SearchResult
          key={finding.id}
          headline={finding.headline}
          publisher={finding.publisher}
          date={finding.publish_date}
          url={finding.url}
          sentiment={finding.sentiment}
        />
      ))}
    </u>
  );
};

export default SearchResultList;
